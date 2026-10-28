---
name: typst-skill
description: 'Typst document creation, editing, debugging, package development, and presentation slides (Touying). Use when: (1) Working with .typ files, (2) User mentions typst, typst.toml, or typst-cli, (3) Creating/editing Typst documents, templates, or packages, (4) Creating presentation slides with Touying, (5) Converting Markdown/LaTeX to Typst, (6) Troubleshooting Typst compilation or syntax issues. 中文触发：Typst 排版、Typst 模板、用 Typst 写论文、Typst 幻灯片/PPT（Touying）、Typst 公式排版、typst 编译报错、中文粗体/斜体不生效、.typ 文件。'
---

# Typst Skill

Comprehensive skill for Typst document authoring, package development, and presentation creation. Combines detailed reference guides, a full mirror of official Typst documentation, Touying presentation support, and searchable API/package indexes. Targets Typst 0.15+ by default.

## Quick Start: Compilation

```bash
typst compile document.typ              # compile once -> PDF
typst compile document.typ output.pdf   # explicit output path
typst compile document.typ "page-{p}.png" -f png   # PNG; 多页必须带 {p} 占位符
typst compile src/main.typ --root .     # set project root for /path imports
typst watch document.typ                # recompile on change
```

**Agent verification methods** (see [references/typst/debug.md](references/typst/debug.md) for details):

| Method      | Command                                                    | Best for                                  |
| ----------- | ---------------------------------------------------------- | ----------------------------------------- |
| HTML export | `typst compile doc.typ out.html -f html --features html`   | Text content, structure, headings, tables |
| PNG export  | `typst compile doc.typ "page-{p}.png" -f png`              | Visual layout, alignment, spacing, fonts  |
| pdftotext   | `typst compile doc.typ && pdftotext doc.pdf -`             | Fallback for page-specific content        |

⚠️ 两条实测出来的坑：

- HTML 导出的输出路径写真实文件（`out.html`）；要接管道就写 `-`（走 stdout，实测可用）。
  **不要**写 `/dev/stdout` —— 那个路径在 Windows 上不存在，会 `error: failed to write HTML
  file (os error 3)`；如果同时加了 `2>/dev/null`，这条错误会被吞掉，agent 会以为导出成功了。
- 多页文档导出 PNG 必须带页码占位符 `{p}`，否则报
  `cannot export multiple images without a page number template`。单页文档两种写法都行，
  统一写 `"page-{p}.png"` 可以省掉一次判断。

## Minimal Document

```typst
#set page(paper: "a4", margin: 2cm)
#set text(size: 11pt, lang: "en")

= Title
== Section

Content goes here. #lorem(50)
```

中文文档改成这样（CJK 字族名随发行版而异，先 `typst fonts | grep -i noto` 确认本机装的是 `Noto Serif SC` 还是 `Noto Serif CJK SC`）：

```typst
#set page(paper: "a4", margin: 2cm)
#set text(size: 11pt, lang: "zh", font: ("Noto Serif SC", "Libertinus Serif"))
```

⚠️ 中文的 `_斜体_` **几乎总是静默失效**（CJK 字体基本没有 italic 字面），要接 cuti。
中文 `*粗体*` 则**看字体**：`Noto Serif SC`（可变 200–900）/ `Noto Sans SC` 正常，
`SimSun` 这类单字重字体静默失效。先跑 `typst fonts --variants` 看有没有 ≥600 的字重，
再决定要不要一起接伪粗体——详见 [references/typst/styling.md](references/typst/styling.md) 的「CJK 伪粗体与伪斜体」一节。

## Documentation Structure

This skill uses a **three-tier documentation system**:

> 文档索引就在下方（Tier 1 / Tier 2）。唯一不在本文件的是 **starter 模板对照表**（7 个 example 分别适合什么场景），见 [`references/typst/SKILL.md`](references/typst/SKILL.md) 的 Examples 一节。

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

> 镜像里的交叉引用已从站点绝对路径（`/docs/reference/model/strong/`）**本地化为相对路径**
> （`../model/strong.md`），2402 条全部可直接打开。若从上游重新同步过镜像，跑一次
> `python3 scripts/localize-mirror-links.py` 重新本地化（幂等，可重复跑）。
> 注意：URL 里的 `#anchor` 是文档站点从 frontmatter 生成的，本地 markdown 不会生成同样的
> 锚点，所以片段可能跳不过去——落到了正确的文件里，用页内搜索找参数名即可。

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

1. Select the closest starter from [assets/examples/](assets/examples/), or use the minimal document above → 产出：选定的 starter 路径。**本步只选不写盘**
2. Read the relevant reference docs for the task → 产出：按上方 Tier 1 表选 1–2 份，不要通读 `references/typst/` 全部 14 份
3. 🔴 CHECKPOINT：**仅当**用户未指定模板/版式、且所选 starter 会明显改变成稿外观（模板类、论文类、CV、幻灯片，或任何自带页眉页脚/版式设定的 starter）时，先说明选了哪个 starter、为什么，等确认再落盘。用户已指定版式、或只是要一份普通文档时跳过本步，直接第 4 步
4. Create the `.typ` file(s)：复制第 1 步选定的 starter 或写入上面的 Minimal Document，然后填入正文 → 产出：落盘的 `.typ` 路径
5. Run post-edit formatting checks (see below) → 产出：`typstyle --check` 通过，或已向用户说明为何跳过
6. Validate with `typst compile` → 产出：exit code 0 且 stderr 无 `error`；出现 `warning` 时先判断是否与本次改动相关，**但字体/缺字类 warning 一律要说明**（那正是「中文变方框」的早期信号）

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
5. `typst compile deck.typ` 验证；再 `typst compile deck.typ "page-{p}.png" -f png --pages 1` 导出首页抽查版式（幻灯片必然多页，`-f png` 不带 `{p}` 会直接报错）

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
| 同一处 error 连续 2 次修复都失败（在回复里明写「第 N 轮修复」，第 2 轮仍失败即停；这就是跨调用的计数器） | 把出错片段抽成最小 `.typ` 单独编译，定位真正的触发点 | 停下，贴出完整 error + 最小复现代码问用户，不要继续盲改或改无关代码试运气 |
| `search-api.py` / `search-packages.py` 报 FileNotFoundError | 确认 cwd 在 skill 根目录；`ls references/typst/data/*.json` 确认索引在 | 直接 `grep` 对应 JSON 手工查找 |
| `python3` 不存在或版本过低 | 试 `python` | 跳过脚本，改用 Tier 1/2 文档，并声明「索引不可用」 |
| 导出 PNG 但读不到图像内容 | 改用 HTML 导出 + `pdftotext` | 只声明「编译通过」，明确说「未做视觉验证」 |
| `@preview/<pkg>` 报版本不存在 | `search-packages.py "<pkg>"` 查真实版本号 | 降到上一个可用版本，并在输出里注明版本 |
| 中文变方框 / 字体缺失 | 跑 `typst fonts` 查出本机真实的 CJK 字族名（`Noto Serif SC` / `Source Han Sans` / `SimSun`），或加 `--font-path` | 告知用户字体未找到，不要静默回退 |
| 中文 `*粗体*` / `_斜体_` 看起来没变粗/没倾斜（编译却通过） | 按 [references/typst/styling.md](references/typst/styling.md) 的「CJK 伪粗体与伪斜体」一节接 cuti | 先问用户能否换字族（serif→sans 会改变外观）；同意后换 `Noto Sans SC` / `Source Han Sans` 重试；仍无效则告知该字体无粗体字面，不要谎称已加粗 |
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
| 中文 `*粗体*` 没变粗、`_斜体_` 没倾斜（且不报错）      | CJK 字体无粗体/斜体字面，Typst 不做合成 | 用 `@preview/cuti` 伪粗体/伪斜体，见 [styling.md](references/typst/styling.md) 的「CJK 伪粗体与伪斜体」一节 |

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

以下是实测中最高频的踩坑，逐条都是「看起来对、实际错」的写法。纯语法层面（`#` 用法、LaTeX 命令）见上方 Critical Syntax Distinctions，此处不重复。

- ❌ 不要凭记忆写包版本号 —— 用 `scripts/search-packages.py` 查。写错版本是最高频的编译失败源。
- ❌ 不要对用户既有文件直接跑 `typstyle -i`，它会重排你没碰过的代码。
- ❌ 不要在没有 `typst compile` 通过的情况下宣称「已完成」。
- ❌ 不要假设 Tier 2 的路径一定存在，先 `ls references/typst-author/` 看真实结构再读。
- ❌ 不要把 PDF 当唯一验证手段 —— agent 读不到 PDF 内容，用 `-f html` 或 `-f png`。
- ❌ 不要在 `.typ` 里用 Markdown 语法：`**bold**` 是普通字符，Typst 用 `*bold*`。
- ❌ 不要以为中文 `*粗体*` 和 `_斜体_` 会生效 —— 详见 [references/typst/styling.md](references/typst/styling.md) 的「CJK 伪粗体与伪斜体」一节，这是 Typst 里最隐蔽的静默失败。

## Probing Uncertain Behavior

- Use a probe when bundled docs do not settle runtime or evaluation behavior.
- Typst 0.15+ 用 `typst eval --in`：

  ```bash
  printf '#metadata(1 + 2) <probe>\n' > /tmp/probe.typ
  typst eval --in /tmp/probe.typ 'query(<probe>).first().value'   # -> 3
  ```

- `typst query -` 也能 fileless 直接喂 stdin（`printf ... | typst query - "<probe>" --field value --one`），
  但 0.15 起会打 `warning: the typst query subcommand is deprecated`。要跑 Typst 0.14 才用它。
  注意 `typst eval` **不接受** `-` 当输入，必须给 `--in <文件>`。
- See `references/typst/query.md` and `references/typst-author/reference/introspection/query.md` for details.

## 校验与性能脚本

| 脚本 | 用途 | 依赖 |
| --- | --- | --- |
| `scripts/search-api.py` | 检索内置的 Typst API 索引（函数/方法/符号，支持 `--channel`） | 无 |
| `scripts/search-packages.py` | 检索内置的 Typst Universe 包索引 | 无 |
| `scripts/validate-examples.py` | 校验文档内所有 ```typst 代码块能否编译 | `markdown-it-py` |
| `scripts/perf-timings.py` | 解析 `typst compile --timings` 轨迹，输出热点表 | 无 |
| `scripts/localize-mirror-links.py` | 把上游镜像里的站点绝对链接本地化为相对路径（幂等，重同步后跑）；`--check` 只报告，未本地化时 exit 1 | 无 |

- `validate-examples.py` 默认只校验本 skill 自身的 md（根目录 `*.md` + `references/typst/` 下全部 md，具体文件数由脚本自行枚举）；加 `--all` 才会扫上游文档镜像
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
