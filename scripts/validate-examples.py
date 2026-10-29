#!/usr/bin/env python3
"""Extract and validate inline Typst code blocks from skill documentation.

Extracts ```typst fenced code blocks from .md files using a CommonMark parser,
wraps snippets with a standard preamble to supply common undefined variables,
and attempts to compile each block with `typst compile`.

Each block ends up in one of four states, and only `fail` is a problem:

* ``pass``     — compiles on its own.
* ``skip``     — not a program by shape: API signature listings (`) -> content`),
                 `...` placeholders, blocks that load an external file, shell
                 transcripts, and so on. See SKIP_RULES.
* ``fragment`` — real code that needs a surrounding document: it uses a name the
                 same markdown file binds elsewhere, or it is a Touying deck
                 snippet that relies on the theme. See fragment_reason().
* ``fail``     — compiles, was expected to, and did not.

Requires: markdown-it-py (pip install markdown-it-py)

Usage:
    python3 scripts/validate-examples.py                    # skill's own docs
    python3 scripts/validate-examples.py basics.md types.md # specific files
    python3 scripts/validate-examples.py --all               # + upstream mirrors
    python3 scripts/validate-examples.py --json             # JSON output
    python3 scripts/validate-examples.py --keep             # keep temp files for debugging
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ImportError:
    print(
        "ERROR: markdown-it-py is required. Install with: pip install markdown-it-py",
        file=sys.stderr,
    )
    sys.exit(2)

# Standard preamble injected before each snippet to define common variables
# used across documentation examples.
PREAMBLE = r"""
// === Validation preamble (auto-injected) ===
#let items = ("alpha", "beta", "gamma")
#let condition = true
#let x = 5
#let config = (color: blue, size: 12pt, name: "test")
#let dict = (name: "Alice", age: 30, city: "NYC")
#let key = "name"
#let default = "N/A"
#let body = [Sample body content]
#let prefix = [Pre]
#let suffix = [Suf]
#let prefix-str = "Pre"
#let body-str = "Body"
#let suffix-str = "Suf"
#let transform(x) = x
// === End preamble ===
"""

# Blocks that are not standalone programs. Each entry is (regex, reason): the
# reason is what gets printed and stored in the JSON, so a skip is auditable
# instead of just "matched some pattern".
SKIP_RULES = [
    (r"^\s*//\s*\.\.\.", "placeholder comment"),
    (r"\.\.\.", "ellipsis placeholder"),
    # API signature listing, e.g. `#block(\n  width: auto | relative,\n) -> content`.
    # `->` has no meaning in Typst code, and upstream uses this shape for every
    # function reference page (~435 blocks in the mirror). The arrow line is
    # always the block's last non-empty line and no such block contains a real
    # command, so matching the arrow is safe.
    (r"(?m)^\s*\)\s*->", "API signature listing"),
    # `#let name(args)` with no body: the signature of a user-defined function.
    # `[^=\n]*` rather than `[^)]*` because the parameter list can nest parens
    # (`enum-args: (:)`), and a real definition always has `=` on the line.
    (r"(?m)^\s*#let\s+[\w-]+\s*\([^=\n]*\)\s*$", "function signature without body"),
    (r"\{\s*\.\.\s*\}", "`{ .. }` body placeholder"),
    (r"=>\s*\.\.", "`=> ..` body placeholder"),
    # A block whose first line is a bare `name(`: the argument list of a call
    # whose head was elided (upstream does this for theme config snippets, e.g.
    # `config-common(handout: true)`). Real Typst code starts with `#`, `//`, `$`
    # or markup, so a lowercase identifier followed directly by `(` is never code.
    (r"(?m)\A\s*[a-z][\w-]*\(", "argument list without `#`"),
    # Upstream marks anti-patterns with a leading comment saying so.
    (
        r"(?m)^\s*//\s*(?:This|That)\s+(?:doesn'?t|does not|won'?t)\s+work",
        "documented anti-pattern",
    ),
    # A typst block containing a fence marker means the markdown source itself is
    # malformed (upstream `raw.md` demonstrates inline ``` in prose). The extracted
    # "code" is then half prose, so there is nothing meaningful to compile.
    # ```xml is matched first so its more specific reason wins.
    (r"```xml", "embedded raw XML block"),
    (r"```", "malformed markdown: fence inside block"),
    # Shell transcript mislabelled as a typst block (`$ typst query ...`).
    # Matched by command name on purpose: a bare `^\s*\$ ` also hits display math
    # (`$ E = m c^2 $`), which is valid Typst and must still be compiled.
    (
        r"(?m)^\s*\$ (?:typst|pdftotext|pdftoppm|git|npm|npx|python3?|curl|magick|convert|ls|cd|cat)\b",
        "shell transcript",
    ),
    (r"#panic\(", "example that is meant to fail"),
    (r'#import\s+"[^@]', "relative import (file not present)"),
    (r'#import\s+"@local/', "local package (not installed)"),
    (r'#import\s+"@preview/', "preview package (needs network/cache)"),
    (r'#import\s+"@preview/package-name', "placeholder package name"),
    (r'#include\s+"', "include (file not present)"),
    (r"image\(", "image file reference"),
    (r"#bibliography\(", "bibliography file reference"),
    (r"#cite\(", "citation needs a bibliography"),
    # File loaders read from disk, so they fail wherever the data file is absent.
    # Matched without requiring `#`: upstream writes them inside `#let x = csv(..)`.
    (r"\bread\(", "read() file reference"),
    (r"\bcsv\(", "csv() file reference"),
    (r"\bjson\(", "json() file reference"),
    (r"\byaml\(", "yaml() file reference"),
    (r"\btoml\(", "toml() file reference"),
    # xml() accepts inline XML (`xml("<a/>")`), so only flag a path argument.
    (r'\bxml\(\s*"[^<]', "xml() file reference"),
    (r"\bplugin\(", "wasm plugin file reference"),
    (r"#pdf\.attach\(", "pdf.attach() file reference"),
    (r'#raw\("', "raw() with string (often partial)"),
    (r"item\.key", "assumes dict-shaped items"),
    (r"@\w+\d{4}", "citation reference (needs .bib file)"),
]
SKIP_PATTERNS = [r for r, _ in SKIP_RULES]  # kept for callers that only need regexes

# Errors that mean "this needs an in-development feature flag", not "this is wrong".
FEATURE_GATED = re.compile(
    r"unknown variable: (html|bundle)\b|module `pdf` does not contain"
)
ALL_FEATURES = "html,bundle,a11y-extras"

# `unknown variable: X` — the identifier the block wanted but could not see.
UNKNOWN_VAR = re.compile(r"unknown variable: ([\w-]+)")
# Names a markdown file defines or imports somewhere in its own prose.
LET_DEF = re.compile(r"(?m)^\s*#let\s+([A-Za-z_][\w-]*)")
LET_TUPLE_DEF = re.compile(r"(?m)^\s*#let\s*\(([^)]*)\)\s*=")
IMPORT_TAIL = re.compile(r"(?m)^\s*#import\s+[^\n]*?:\s*([^\n]+)")


def extract_blocks(md_path: Path) -> list[dict]:
    """Extract ```typst code blocks with line numbers using CommonMark parsing."""
    text = md_path.read_text(encoding="utf-8")
    md = MarkdownIt()
    tokens = md.parse(text)
    blocks = []

    for token in tokens:
        if token.type == "fence" and token.info.strip() == "typst":
            # token.map is [start_line, end_line] (0-indexed)
            # Content starts on the line after the opening fence
            line = token.map[0] + 2  # +1 for 0-index, +1 for fence line
            blocks.append(
                {
                    "file": str(md_path),
                    "line": line,
                    "code": token.content,
                }
            )

    return blocks


def should_skip(code: str) -> str | None:
    """Return a human-readable reason if this block should be skipped, else None."""
    for pattern, reason in SKIP_RULES:
        if re.search(pattern, code):
            return reason
    return None


def file_definitions(md_path: Path) -> tuple[set[str], bool]:
    """Names a markdown file binds somewhere in its own text, plus wildcard flag.

    Used to recognise *fragments*: upstream docs split one program across several
    blocks, so a later block can legitimately use a name an earlier block defined
    (`#let frame(stroke) = ...` in guides/tables.md, for instance). Compiling such
    a block in isolation must fail, and that is a property of the docs, not a bug.
    """
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return set(), False

    names = set(LET_DEF.findall(text))
    for group in LET_TUPLE_DEF.findall(text):
        for part in group.split(","):
            name = part.strip().split(":")[0].strip()
            if re.fullmatch(r"[A-Za-z_][\w-]*", name):
                names.add(name)

    wildcard = False
    for tail in IMPORT_TAIL.findall(text):
        if tail.strip() == "*":
            wildcard = True
            continue
        for part in tail.split(","):
            name = part.strip().split(" as ")[-1].strip()
            if re.fullmatch(r"[A-Za-z_][\w-]*", name):
                names.add(name)
    return names, wildcard


def fragment_reason(
    code: str, stderr: str, md_path: Path, defs: tuple[set[str], bool]
) -> str | None:
    """Explain a failure as "this block is a fragment", or return None.

    Only two explanations are accepted, both checkable:

    * the missing name is bound elsewhere in the same markdown file, so the block
      was written to follow that definition;
    * the block lives in the Touying mirror, whose snippets are all pasted into a
      deck and rely on the theme to provide `slide`, `utils`, `config-colors`, ...
    """
    match = UNKNOWN_VAR.search(stderr)
    if not match:
        return None
    name = match.group(1)
    names, wildcard = defs
    if name in names:
        return f"fragment: uses `{name}`, bound elsewhere in this file"
    if wildcard:
        return f"fragment: uses `{name}` from this file's wildcard import"
    if "touying-author" in md_path.as_posix():
        return f"fragment: uses `{name}` from the surrounding Touying deck"
    return None


def default_md_files(skill_dir: Path, scan_mirrors: bool = False) -> list[Path]:
    """Pick the markdown files to validate.

    Only the skill's own prose is validated by default. references/typst-author/
    and references/touying-author/ are verbatim mirrors of upstream docs (~1100
    code blocks between them); sweeping them turns a 3-minute run into a
    30-minute one, so they are opt-in via --all.
    """
    if scan_mirrors:
        return sorted(skill_dir.rglob("*.md"))

    files = set(skill_dir.glob("*.md"))
    typst_refs = skill_dir / "references" / "typst"
    if typst_refs.is_dir():
        files.update(typst_refs.rglob("*.md"))
    return sorted(files)


def compile_block(
    code: str, preamble: bool = True, keep: bool = False
) -> tuple[bool, str]:
    """Try to compile a Typst code block. Returns (success, stderr).

    The output must be a real file path: passing a Unix-style sink such as
    /dev/null fails on Windows with "failed to write PDF file (os error 3)".
    Compile inside a scratch directory so nothing is left behind.

    Upstream documents in-development APIs (`html.*`, `pdf.data-cell`) that only
    exist behind a feature flag. When the first attempt fails for that reason the
    block is retried once with every feature enabled, so those blocks are judged
    on their own merits instead of being written off as broken.
    """
    full_code = (PREAMBLE + "\n" + code) if preamble else code

    work_dir = tempfile.mkdtemp(prefix="typst-validate-")
    try:
        src_path = os.path.join(work_dir, "snippet.typ")
        out_path = os.path.join(work_dir, "snippet.pdf")
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(full_code)

        def run(features: str | None) -> subprocess.CompletedProcess:
            cmd = ["typst", "compile", src_path, out_path, "-f", "pdf"]
            if features:
                cmd += ["--features", features]
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )

        try:
            result = run(None)
            if result.returncode != 0 and FEATURE_GATED.search(result.stderr):
                result = run(ALL_FEATURES)
            ok = result.returncode == 0
            if keep:
                print(f"  (kept: {src_path})", file=sys.stderr)
            return ok, result.stderr.strip()
        except FileNotFoundError:
            return False, "typst not found in PATH"
        except subprocess.TimeoutExpired:
            return False, "compilation timed out (10s)"
    finally:
        if not keep:
            shutil.rmtree(work_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(
        description="Validate inline Typst examples from skill .md files",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific .md files to validate (default: all *.md in skill dir)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep temporary .typ files for debugging",
    )
    parser.add_argument(
        "--no-preamble",
        action="store_true",
        help="Skip injecting the standard variable preamble",
    )
    parser.add_argument(
        "--include-skipped",
        action="store_true",
        help="Also attempt to compile blocks that would normally be skipped",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="scan_mirrors",
        help=(
            "Also validate the vendored upstream doc mirrors "
            "(references/typst-author, references/touying-author). "
            "Adds ~1100 blocks and takes tens of minutes."
        ),
    )
    args = parser.parse_args()

    # Resolve skill directory
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent

    if args.files:
        md_files = [skill_dir / f for f in args.files]
    else:
        md_files = default_md_files(skill_dir, args.scan_mirrors)

    results = []
    counts = {"pass": 0, "fail": 0, "skip": 0, "fragment": 0}
    defs_cache: dict[Path, tuple[set[str], bool]] = {}

    for md_file in md_files:
        if not md_file.exists():
            print(f"WARNING: {md_file} not found, skipping", file=sys.stderr)
            continue

        blocks = extract_blocks(md_file)
        for block in blocks:
            skip_reason = should_skip(block["code"])
            rel_path = md_file.relative_to(skill_dir).as_posix()

            if skip_reason and not args.include_skipped:
                counts["skip"] += 1
                results.append(
                    {
                        "file": rel_path,
                        "line": block["line"],
                        "status": "skip",
                        "reason": skip_reason,
                    }
                )
                continue

            ok, stderr = compile_block(
                block["code"],
                preamble=not args.no_preamble,
                keep=args.keep,
            )

            entry = {"file": rel_path, "line": block["line"]}
            if ok:
                counts["pass"] += 1
                entry["status"] = "pass"
            else:
                if md_file not in defs_cache:
                    defs_cache[md_file] = file_definitions(md_file)
                frag = fragment_reason(
                    block["code"], stderr, md_file, defs_cache[md_file]
                )
                if frag:
                    counts["fragment"] += 1
                    entry["status"] = "fragment"
                    entry["reason"] = frag
                else:
                    counts["fail"] += 1
                    entry["status"] = "fail"
                # Show first line of error for context
                first_error = stderr.split("\n")[0] if stderr else "unknown error"
                entry["error"] = first_error
            results.append(entry)

    # Output
    if args.json_output:
        print(json.dumps({"counts": counts, "results": results}, indent=2))
    else:
        icons = {"pass": "OK", "fail": "FAIL", "skip": "SKIP", "fragment": "FRAG"}
        for r in results:
            icon = icons[r["status"]]
            loc = f"{r['file']}:{r['line']}"
            msg = r.get("error", r.get("reason", ""))
            suffix = f"  {msg}" if msg else ""
            print(f"{icon:>4}  {loc:<30}{suffix}")

        print()
        total = sum(counts.values())
        print(
            f"Total: {total}  Pass: {counts['pass']}  Fail: {counts['fail']}  "
            f"Skip: {counts['skip']}  Fragment: {counts['fragment']}"
        )

    # Only real failures are a problem. Skipped blocks are not code by shape;
    # fragments are code that needs a surrounding document to compile.
    sys.exit(1 if counts["fail"] > 0 else 0)


if __name__ == "__main__":
    main()
