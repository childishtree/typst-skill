#!/usr/bin/env python3
"""Rewrite site-absolute links in the vendored upstream doc mirrors to relative paths.

`references/typst-author/` is a verbatim copy of the Typst documentation site, so
every cross-reference inside it is a site-absolute URL such as
`/docs/reference/model/strong/` or `/reference/text/text/#parameters-tracking`.
Those resolve on typst.app but are dead ends in a local checkout — an agent that
follows one gets nothing.

This script rewrites them to relative paths that exist on disk:

    /docs/reference/model/strong/           -> ../model/strong.md
    /docs/reference/math/                   -> ../math/
    /reference/text/text/#parameters-tracking -> text.md#parameters-tracking

Rules
-----
* `<mirror>/<path>.md` wins if it exists (most links).
* Otherwise `<mirror>/<path>/` is used when it is a directory (category pages).
* Anything that resolves to neither is left untouched and reported.
* Links inside a **language-tagged** code fence are example content, not cross
  references, and are left alone. A bare ``` fence is scanned as prose: upstream
  `reference/text/raw.md` has one that never closes properly and buries 19 real
  links in what a naive fence detector calls "code".

Fragments are preserved as-is. Note that the upstream fragments are anchors the
docs *site* generates from its frontmatter (e.g. `#parameters-tracking`); a plain
markdown viewer will not generate the same anchors, so a fragment may not jump.
The file link itself is what matters — the reader can search within the page.

The rewrite is idempotent: links that are already relative are skipped, so it is
safe to run again after re-syncing the mirror from upstream.

Usage:
    python3 scripts/localize-mirror-links.py --check    # report only
    python3 scripts/localize-mirror-links.py            # rewrite in place
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
MIRRORS = [
    SKILL_DIR / "references" / "typst-author",
    SKILL_DIR / "references" / "touying-author",
]

# Markdown inline link / image: ](target) or ](<target>)
LINK_RE = re.compile(r"\]\(\s*(<[^>]*>|[^)\s]+)\s*\)")
# Opening or closing code fence line (CommonMark: up to 3 spaces of indent,
# 3+ backticks or tildes, then an optional info string such as `typst`).
FENCE_LINE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
# Only these prefixes are treated as site-absolute doc paths.
SITE_PREFIXES = ("/docs/", "/reference/", "/tutorial/", "/guides/")


def fence_spans(text: str) -> list[tuple[int, int, bool]]:
    """Character ranges covered by fenced code blocks, with a language flag.

    A line-based state machine rather than a regex: fence markers can appear an
    odd number of times in these mirrors (a stray ``` in prose or inside an
    example), and any greedy pairing then swallows whole paragraphs as "code".
    Toggling per line keeps an unterminated fence open to end of file, which is
    how CommonMark behaves.

    The third tuple element records whether the opening fence carried an info
    string (```typst, ```md). Only those are treated as real code by
    `rewrite_file`. A *bare* ``` that swallows prose is a defect of the upstream
    markdown — `reference/text/raw.md` has one, and it buries 19 genuine
    cross-references — so bare fences are scanned as prose. Measured on the
    current mirror: 2383 links in prose, 19 inside bare fences (all of them the
    raw.md paragraphs), 0 inside language-tagged fences.
    """
    spans: list[tuple[int, int, bool]] = []
    pos = 0
    open_at: int | None = None
    open_marker = ""
    open_lang = False
    for line in text.splitlines(keepends=True):
        m = FENCE_LINE_RE.match(line)
        if m:
            marker, info = m.group(1), m.group(2).strip()
            if open_at is None:
                open_at = pos
                open_marker = marker
                open_lang = bool(info)
            elif marker[0] == open_marker[0] and len(marker) >= len(open_marker):
                spans.append((open_at, pos + len(line), open_lang))
                open_at = None
                open_marker = ""
                open_lang = False
        pos += len(line)
    if open_at is not None:
        spans.append((open_at, len(text), open_lang))
    return spans


def resolve(mirror: Path, url_path: str) -> Path | None:
    """Map a site-absolute path to something that exists under `mirror`."""
    rel = url_path.lstrip("/")
    if rel.startswith("docs/"):
        rel = rel[len("docs/"):]
    rel = rel.strip("/")
    if not rel:
        return None
    as_file = mirror / (rel + ".md")
    if as_file.exists():
        return as_file
    as_dir = mirror / rel
    if as_dir.is_dir():
        return as_dir
    return None


def rewrite_file(
    md: Path, mirror: Path, apply: bool
) -> tuple[int, int, list[str], int]:
    """Returns (rewritten, untouched_site_absolute, unresolved_paths, in_code).

    ``in_code`` counts site-absolute links left alone because they sit inside a
    language-tagged code block — those are example content, not cross
    references, and rewriting them would corrupt the example.
    """
    text = md.read_text(encoding="utf-8")
    # Only language-tagged fences count as code; see fence_spans().
    code_spans = [(a, b) for a, b, has_lang in fence_spans(text) if has_lang]

    def in_code(pos: int) -> bool:
        return any(a <= pos < b for a, b in code_spans)

    out = []
    last = 0
    rewritten = 0
    untouched = 0
    in_code_count = 0
    unresolved: list[str] = []

    for m in LINK_RE.finditer(text):
        target = m.group(1)
        raw = target[1:-1] if target.startswith("<") else target
        if not raw.startswith(SITE_PREFIXES):
            continue
        if in_code(m.start()):
            in_code_count += 1
            continue
        path, sep, frag = raw.partition("#")
        dest = resolve(mirror, path)
        if dest is None:
            untouched += 1
            unresolved.append(raw)
            continue
        rel_str = Path(os.path.relpath(dest, md.parent)).as_posix()
        if dest.is_dir():
            rel_str += "/"
        new = rel_str + (sep + frag if sep else "")
        out.append(text[last:m.start(1)])
        out.append(new)
        last = m.end(1)
        rewritten += 1

    if rewritten and apply:
        out.append(text[last:])
        md.write_text("".join(out), encoding="utf-8")
    return rewritten, untouched, unresolved, in_code_count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report only, do not modify")
    args = ap.parse_args()

    total_rw = total_un = 0
    total_code = 0
    all_unresolved: list[tuple[str, str]] = []

    for mirror in MIRRORS:
        if not mirror.is_dir():
            print(f"skip (missing): {mirror}", file=sys.stderr)
            continue
        files = sorted(mirror.rglob("*.md"))
        rw = un = in_code = 0
        for md in files:
            r, u, unresolved, c = rewrite_file(md, mirror, apply=not args.check)
            rw += r
            un += u
            in_code += c
            for url in unresolved:
                all_unresolved.append((md.relative_to(SKILL_DIR).as_posix(), url))
        verb = "would rewrite" if args.check else "rewrote"
        print(
            f"{mirror.name}: {len(files)} files, {verb} {rw} links, "
            f"{un} unresolved, {in_code} left in code blocks"
        )
        total_rw += rw
        total_un += un
        total_code += in_code

    print(f"\ntotal: {total_rw} rewritten, {total_un} unresolved, {total_code} in code blocks")
    if all_unresolved:
        print(f"\nunresolved ({len(all_unresolved)}), first 20:")
        for where, url in all_unresolved[:20]:
            print(f"  {where}: {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
