---
name: typst-skill
description: 'Typst document creation, editing, debugging, package development, and presentation slides (Touying). Use when: (1) Working with .typ files, (2) User mentions typst, typst.toml, or typst-cli, (3) Creating/editing Typst documents, templates, or packages, (4) Creating presentation slides with Touying, (5) Converting Markdown/LaTeX to Typst, (6) Troubleshooting Typst compilation or syntax issues. 中文触发：排版、Typst 模板、写论文、做幻灯片/PPT、公式排版、表格、编译报错、中文粗体/斜体不生效、.typ 文件。'
---

# Typst Skill

Comprehensive skill for Typst document authoring, package development, and presentation creation. Combines detailed reference guides, a full mirror of official Typst documentation, Touying presentation support, and searchable API/package indexes. Targets Typst 0.15+ by default.

## Quick Start: Compilation

```bash
typst compile document.typ              # compile once -> PDF
typst compile document.typ output.pdf   # explicit output path
typst compile document.typ -f png       # export as PNG image
typst compile src/main.typ --root .     # set project root for /path imports
typst watch document.typ                # recompile on change
```

**Agent verification methods** (see [references/typst/debug.md](references/typst/debug.md) for details):

| Method      | Command                                                                 | Best for                                  |
| ----------- | ----------------------------------------------------------------------- | ----------------------------------------- |
| HTML export | `typst compile doc.typ /dev/stdout -f html --features html 2>/dev/null` | Text content, structure, headings, tables |
| PNG export  | `typst compile doc.typ page-{p}.png -f png`                             | Visual layout, alignment, spacing, fonts  |
| pdftotext   | `typst compile doc.typ && pdftotext doc.pdf -`                          | Fallback for page-specific content        |

## Minimal Document

```typst
#set page(paper: "a4", margin: 2cm)
#set text(size: 11pt, lang: "en")

= Title
== Section

Content goes here. #lorem(50)
```

## Documentation Structure

This skill uses a **three-tier documentation system**:

> Tier 1 的完整索引（含 starter 模板对照表）另见 [`references/typst/SKILL.md`](references/typst/SKILL.md)。

### Tier 1: Task-Oriented Guides (`references/typst/`)
Concise, pattern-first reference docs covering specific tasks. Each doc links to related docs.

| When you need to...                                | Read                                                              |
| -------------------------------------------------- | ----------------------------------------------------------------- |
| Learn syntax, imports, functions, control flow     | [references/typst/basics.md](references/typst/basics.md)          |
| Learn data types, operators, string/array methods  | [references/typst/types.md](references/typst/types.md)            |
| Style pages, headings, figures, layout             | [references/typst/styling.md](references/typst/styling.md)        |
| Tables, grids, cell spans, borders, data tables    | [references/typst/tables.md](references/typst/tables.md)          |
| Math formulas, fonts, accents, matrices, vectors   | [references/typst/math.md](references/typst/math.md)              |
| Academic papers, bibliography, theorems, equations | [references/typst/academic.md](references/typst/academic.md)      |
| Convert from Markdown or LaTeX                     | [references/typst/conversion.md](references/typst/conversion.md)  |
| Use Typst CLI commands and build options           | [references/typst/cli.md](references/typst/cli.md)                |
| Extract data from documents, multi-pass builds     | [references/typst/query.md](references/typst/query.md)            |
| State, counters, in-document `query()`, XML        | [references/typst/advanced.md](references/typst/advanced.md)      |
| Create a reusable template function                | [references/typst/template.md](references/typst/template.md)      |
| Create or publish a package                        | [references/typst/package.md](references/typst/package.md)        |
| Verify output (HTML/PNG/pdftotext, repr)           | [references/typst/debug.md](references/typst/debug.md)            |
| Profile performance (--timings, hotspots)          | [references/typst/perf.md](references/typst/perf.md)              |

### Tier 2: Full Official Documentation (`references/typst-author/`)
A complete mirror of the official Typst documentation, organized by category:

- **Tutorial**: `references/typst-author/tutorial/writing-in-typst.md` -- Getting started
- **Guides**: `references/typst-author/guides/` -- Page setup, tables, page-setup, etc.
- **Reference**: `references/typst-author/reference/` -- Full API reference by category:
  - `foundations/` -- Array, dictionary, content, module, etc.
  - `model/` -- Heading, figure, table, footnote, etc.
  - `text/` -- Text, linebreak, highlight, etc.
  - `math/` -- Equation, math.equation, math.attach, etc.
  - `visualize/` -- Line, rect, circle, path, image, etc.
  - `layout/` -- Block, box, grid, stack, etc.
  - `scripting.md` / `context.md` / `styling.md` -- Scripting, context, styling
  - `introspection/` -- Counter, state, query, etc.
  - `data-loading/` -- csv, json, xml, etc.
  - `symbols/` -- sym, emoji, etc.

### Tier 3: Touying Presentations (`references/touying-author/`)
Specialized documentation and examples for creating slide decks with the Touying package.

| When you need to...                         | Read                                                                    |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| Get started with Touying basics             | [references/touying-author/start.md](references/touying-author/start.md)          |
| Multi-file slide deck structure             | [references/touying-author/multi-file.md](references/touying-author/multi-file.md) |
| Slide layout and headings                   | [references/touying-author/layout.md](references/touying-author/layout.md)        |
| Animations and dynamic content              | [references/touying-author/dynamic/](references/touying-author/dynamic/)         |
| Theme-specific APIs                         | [references/touying-author/themes/](references/touying-author/themes/)           |
| Speaker notes and presenter tools           | [references/touying-author/external/](references/touying-author/external/)       |
| Integrations (CeTZ, Fletcher, MiTeX)        | [references/touying-author/integration/](references/touying-author/integration/) |
| Working examples                            | [references/touying-author/examples/](references/touying-author/examples/)                |

## Finding Packages

Search the embedded index of Typst Universe packages:

```bash
python3 scripts/search-packages.py "what you need"
python3 scripts/search-packages.py "chart" --category visualization
python3 scripts/search-packages.py --category cv --top 5
python3 scripts/search-packages.py --list-categories
```

## API Reference Search

Search the embedded index of Typst API functions, methods, and constructors:

```bash
python3 scripts/search-api.py "image width fit"
python3 scripts/search-api.py "color lighten" --kind method
python3 scripts/search-api.py --name str.position -v
python3 scripts/search-api.py "rightarrow" --kind symbol   # LaTeX names work
python3 scripts/search-api.py "path" --channel 0.14.2      # legacy Typst 0.14 API
python3 scripts/search-api.py --list-categories
```

## Workflows

### Creating a New Document

1. Copy the closest starter from [assets/examples/](assets/examples/) or use the minimal document above → 产出：确定的 starter 路径
2. Read the relevant reference docs for the task → 产出：按上方 Tier 1 表选 1–2 份，不要通读 `references/typst/` 全部 14 份
3. 🔴 CHECKPOINT：写文件之前，如果用户没有指定模板或版式，先说明你从 `assets/examples/` 里挑了哪一个 starter、为什么挑它，等用户确认再动手
4. Run post-edit formatting checks (see below) → 产出：`typstyle --check` 通过，或已向用户说明为何跳过
5. Validate with `typst compile` → 产出：exit code 0 且 stderr 无 `error`；有 `warning` 需向用户说明

### Editing Existing Documents

🛑 STOP：要覆写或删除已存在的 `.typ` 文件之前，必须先向用户确认，不要直接覆盖。

1. Locate the target text and apply changes → 产出：改动前后的 diff 摘要
2. Verify syntax against reference docs when needed
3. Run post-edit formatting checks
4. Validate with `typst compile` → 产出：exit code 0 且无 `error`；未通过则走「失败回边」

### Creating Presentations with Touying

1. Start from `references/touying-author/examples/simple.typ` or `references/touying-author/examples/default.typ`
2. Import Touying and a theme, apply with `#show: <theme>.with(...)`
3. Use headings to create slides; use `#slide` for custom layouts or animations
4. For multi-file decks: `globals.typ` + `main.typ` + `content.typ` pattern
5. `typst compile deck.typ` 验证；导出 `-f png` 抽查首页版式

```typst
#import "@preview/touying:0.6.1": *
#import themes.simple: *

#show: simple-theme.with(
  aspect-ratio: "16-9",
  footer: [Simple slides],
)
```

### 失败回边（如果 X 失败 → 做 Y）

工作流不是单向的。下列任一条触发时，必须按对应分支执行，**不允许静默跳过或静默失败**。

| 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|
| `typst compile` 报语法错 | 查下方 Common Errors 表 | 读 `references/typst/debug.md`；用 `-f html --features html` 定位出错元素 |
| 编译连续 3 次不过 | 停下，贴出完整 error + 最小复现代码问用户 | 不要继续盲改，不要改无关代码试运气 |
| `search-api.py` / `search-packages.py` 报 FileNotFoundError | 确认 cwd 在 skill 根目录；`ls references/typst/data/*.json` 确认索引在 | 直接 `grep` 对应 JSON 手工查找 |
| `python3` 不存在或版本过低 | 试 `python` | 跳过脚本，改用 Tier 1/2 文档，并声明「索引不可用」 |
| 导出 PNG 但读不到图像内容 | 改用 HTML 导出 + `pdftotext` | 只声明「编译通过」，明确说「未做视觉验证」 |
| `@preview/<pkg>` 报版本不存在 | `search-packages.py "<pkg>"` 查真实版本号 | 降到上一个可用版本，并在输出里注明版本 |
| 中文变方框 / 字体缺失 | 加 `--font-path`，或换 `"Noto Serif CJK SC"` 等系统字体 | 告知用户字体未找到，不要静默回退 |
| 中文 `*粗体*` 看起来没变粗 | 见 [references/typst/styling.md](references/typst/styling.md) 的 cuti 方案 | 明确告知「字体无粗体字面」，不要谎称已加粗 |
| Tier 2 路径打不开 | `ls references/typst-author/` 看真实结构 | 用 `search-api.py` 代替，不要猜路径 |

三条工作流的末步后统一适用：**若 `typst compile` 失败，进入本表第 1 行，不要直接结束任务。**

## Common Errors

| Error                                            | Cause                        | Fix                                                  |
| ------------------------------------------------ | ---------------------------- | ---------------------------------------------------- |
| "unknown variable"                               | Undefined identifier         | Check spelling, ensure `#let` before use             |
| "expected X, found Y"                            | Type mismatch                | Check function signature in docs                     |
| "file not found"                                 | Bad import path              | Paths resolve relative to current file               |
| "unknown font"                                   | Font not installed           | Use system fonts or web-safe alternatives            |
| "maximum function call depth exceeded"           | Deep recursion               | Use iteration instead                                |
| "can only be used when context is known"         | Missing `context` wrapper    | Wrap in `context { ... }`                            |
| "unexpected argument"                            | `=` instead of `:` for args  | Named args use `:` syntax: `func(name: value)`       |
| "variables from outside are read-only"           | Mutating captured variable   | Use loop accumulation or `state()` -- see advanced.md |
| "expected content, found string" (or vice versa) | Content/string type mismatch | Use `[#str-var]` to embed string in content          |
| set/show rule has no effect                      | Rule placed after content    | Place set/show rules before the content they target  |

## Critical Syntax Distinctions

- **Arrays**: `(item1, item2)` (parentheses). Typst has NO tuples.
- **Dictionaries**: `(key: value, key2: value2)` (parentheses with colons).
- **Content blocks**: `[markup content]` (square brackets).
- **Hash usage**: Use `#` to start code in markup (e.g., `#figure[...]`). Do NOT use `#` inside code contexts (e.g., `figure(image("x.png"))` -- no `#` before `image`).
- **set vs show**: `set` configures element defaults; `show` transforms or replaces element output.
- **LaTeX syntax**: Do NOT use `\begin{...}`, `\section`, or other LaTeX commands in Typst.

## Post-Edit Formatting Checks

1. Check whether `typstyle` is available with `command -v typstyle`. Skip if unavailable.
2. After each `.typ` file modification, run `typstyle --check <file>`.
3. If `typstyle --check` fails, inspect with `typstyle --diff <file>`.
4. Apply formatting with `typstyle -i <file>` only when changes are limited to newly created/edited code.
5. 🛑 STOP：当 `typstyle -i` 会改动你并未触碰的既有代码时，停下来问用户，不要直接执行。

## 反例清单（不要做什么）

以下是实测中最高频的踩坑，逐条都是「看起来对、实际错」的写法。

- ❌ 不要在代码上下文里写 `#`：`figure(...)` 而非 `#figure(...)`。
- ❌ 不要用 LaTeX 命令：`\section`、`\begin{}`、`\usepackage`、`\bfseries` 在 Typst 里都不存在。
- ❌ 不要凭记忆写包版本号 —— 用 `scripts/search-packages.py` 查。写错版本是最高频的编译失败源。
- ❌ 不要对用户既有文件直接跑 `typstyle -i`，它会重排你没碰过的代码。
- ❌ 不要在没有 `typst compile` 通过的情况下宣称「已完成」。
- ❌ 不要假设 Tier 2 的路径一定存在，先 `ls references/typst-author/` 看真实结构再读。
- ❌ 不要把 PDF 当唯一验证手段 —— agent 读不到 PDF 内容，用 `-f html` 或 `-f png`。
- ❌ 不要在 `.typ` 里用 Markdown 语法：`**bold**` 是普通字符，Typst 用 `*bold*`。
- ❌ 不要以为中文 `*粗体*` 和 `_斜体_` 会生效 —— 详见 [references/typst/styling.md](references/typst/styling.md) 的「CJK 伪粗体与伪斜体」一节，这是 Typst 里最隐蔽的静默失败。

## Probing Uncertain Behavior

- Use a probe when bundled docs do not settle runtime or evaluation behavior.
- Prefer fileless probes through stdin: `printf '#metadata(1 + 2) <probe>\n' | typst query - "<probe>" --field value --one`
- See `references/typst/query.md` and `references/typst-author/reference/introspection/query.md` for details.

## 校验与性能脚本

| 脚本 | 用途 | 依赖 |
| --- | --- | --- |
| `scripts/search-api.py` | 检索内置的 Typst API 索引（函数/方法/符号，支持 `--channel`） | 无 |
| `scripts/search-packages.py` | 检索内置的 Typst Universe 包索引 | 无 |
| `scripts/validate-examples.py` | 校验文档内所有 ```typst 代码块能否编译 | `markdown-it-py` |
| `scripts/perf-timings.py` | 解析 `typst compile --timings` 轨迹，输出热点表 | 无 |

- `validate-examples.py` 默认只校验本 skill 自身的 20 个 md；加 `--all` 才会扫上游文档镜像
  （`references/typst-author/` 等，约 1100 个代码块，耗时数十分钟）。
- `perf-timings.py` 吃的是 JSON 轨迹，不是 `.typ` 源文件：
  `typst compile --timings trace.json doc.typ doc.pdf && python3 scripts/perf-timings.py trace.json --self-time`
- 脚本不可用时的降级路径见上方「失败回边」表。

## Ecosystem Tools

- **tinymist** -- LSP/editor integration
- **typstyle** -- Code formatter
- **typst-package-check** -- Package validator
- **tytanic** -- Visual regression test runner

## Dependencies

- **typst CLI 0.15+** recommended: https://typst.app
  - macOS: `brew install typst`
  - Linux: `cargo install typst-cli`
  - Windows: `winget install typst`
- **pdftotext** (optional): For text-level output verification
- **Python 3.10+** (optional): For package search and validation scripts
- **typstyle** (optional): For code formatting checks
