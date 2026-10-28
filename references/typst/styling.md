# Styling and Layout

For language basics (syntax, functions), see [basics.md](basics.md). For data types and operators, see [types.md](types.md). For reusable template creation, see [template.md](template.md).

## Set Rules

Configure element defaults:

```typst
#set page(paper: "a4", margin: (top: 2.5cm, bottom: 2cm, x: 2cm), numbering: "1")
#set text(font: "Libertinus Serif", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.65em, first-line-indent: 1em)
#set heading(numbering: "1.1")
#set list(indent: 1em, marker: [•])
#set enum(indent: 1em, numbering: "1.")
#set figure(placement: auto, gap: 1em)
```

## Show Rules

Transform how elements are rendered.

### Show-Set (Targeted Styling)

```typst
#show heading: set text(font: "Helvetica")
#show heading.where(level: 1): set align(center)
#show raw: set text(font: "Fira Code", size: 9pt)
#show link: set text(fill: blue)
```

### Show-Transform (Custom Rendering)

```typst
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  align(center, text(18pt, strong(it.body)))
  v(1em)
}

#show figure.caption: it => text(size: 9pt, style: "italic", it)
```

## Page Layout

### Headers and Footers

```typst
#set page(
  header: context {
    let page = counter(page).get().first()
    if page > 1 { [Title #h(1fr) Page #page] }
  },
  footer: context { align(center, counter(page).display()) },
)
```

### Page Breaks

```typst
#pagebreak()              // Force page break
#pagebreak(weak: true)    // Only if not at page start
#pagebreak(to: "odd")     // Break to next odd page
```

## Built-in Counters

```typst
#context counter(page).display()    // Current page
#counter(page).update(1)            // Reset to 1
#context counter(heading).display() // Heading number
```

For custom counters and state tracking, see [advanced.md](advanced.md).

## Heading Customization

### Numbering Formats

```typst
#set heading(numbering: "1.1")   // 1.1, 1.2, ...
#set heading(numbering: "1.a")   // 1.a, 1.b, ...
#set heading(numbering: "I.1")   // I.1, I.2, ...
```

### Outline (Table of Contents)

```typst
#outline(title: [Contents], indent: auto, depth: 3)
```

## Images

```typst
#image("diagram.png")                    // Full width
#image("diagram.png", width: 80%)        // Scaled
#image("photo.jpg", width: 5cm, height: 4cm, fit: "cover")  // Crop to fit
#image("icon.svg")                       // SVG supported natively
```

Paths resolve relative to the current file (see [basics.md](basics.md) for path rules).

Prefer SVG for diagrams (scales cleanly), PNG/JPG for photos. Use `fit: "contain"` (default) to preserve aspect ratio, `"cover"` to crop, `"stretch"` to distort.

## Font Configuration

```typst
#set text(font: "Libertinus Serif")                        // Single font
#set text(font: ("Noto Serif SC", "Libertinus Serif"))     // Fallback chain: 缺字时按顺序往下找
#set text(font: "Fira Code", size: 9pt)                    // Monospace for code
```

CJK 字族名随发行版而异：Google 版本叫 `Noto Serif SC` / `Noto Sans SC`，Adobe/系统版可能叫
`Noto Serif CJK SC` / `Source Han Serif SC`，Windows 上还有 `SimSun` / `Microsoft YaHei`。
写死一个名字前先 `typst fonts | grep -i` 确认本机装了哪个，否则只会得到
`warning: unknown font family` 并静默回退到默认字体。

```bash
# List available fonts
typst fonts

# Search for a font
typst fonts | grep -i "noto"

# Add font directory
typst compile document.typ --font-path ./fonts
```

If `typst fonts` does not list the font you need, install it system-wide or use `--font-path` to point to a directory containing `.ttf`/`.otf` files.

### Variable Fonts (Typst 0.15+)

Use `typst fonts --variants` to inspect weights, stretches, and variable axes. Set standard axes through `weight` / `stretch`; use `variations` for custom OpenType axes such as `wght`, `GRAD`, or `MONO` when the selected font supports them.

Inline pattern: `#set text(font: "Your Variable Font", weight: 650, variations: (GRAD: 0.4))`.

## CJK 伪粗体与伪斜体（中文加粗/斜体不生效）

### 症状

中文的 `*粗体*` 和 `_斜体_` 可能**静默失效**：拉丁字母正常变粗/变斜，汉字纹丝不动，
而且**不报任何错误**——编译 exit 0，看起来一切正常。

但这两件事的成因不同，**不要一概而论**：

| | 会不会失效 | 怎么判断 |
|---|---|---|
| `*粗体*` | **看字体**。带 Bold 字面、或是有 weight 轴的可变字体 → 正常；只有 Regular 一个字面 → 静默失效 | `typst fonts --variants` 看该字族有没有 ≥600 的字重 |
| `_斜体_` | **几乎总是失效**。CJK 字体基本不提供 italic 字面 | 同上，看有没有 `Style: Italic` |

本机实测（typst 0.15）：

| 字族 | 字重 | 中文粗体 | 中文斜体 |
|---|---|---|---|
| `Noto Serif SC` | 可变 200–900 | ✅ 正常（默认 200，`*粗体*` 按 `strong` 的 delta 往上抬） | ❌ 失效 |
| `Noto Sans SC` | 400 / 500 / 700 | ✅ 正常 | ❌ 失效 |
| `Source Han Sans` | 多字重 | ✅ 正常 | ❌ 失效 |
| `SimSun` | 只有 400 | ❌ **静默失效** | ❌ 失效 |

所以：**伪斜体基本是必需品，伪粗体只在字体确实缺粗体字面时才需要。**

### 根因

Typst 按字重/字形去找字体，**不做合成（synthetic）粗斜体**。找不到对应的字面时：

- 粗体：要么保持 Regular（完全不加粗），要么跳到**另一个字体家族**的 Bold。
  后者更糟：同一行里有的字粗、有的字不粗（当替代字体缺简体字形时）。
- 斜体：CJK 字体没有 italic 字面，`_强调_` 里的汉字保持正体。

从 LaTeX 迁过来的人最容易踩——xeCJK / fontspec 会自动做假粗体，Typst 不会。

### 复现与验证

```typst
#set text(font: "SimSun")   // 只有 400 一个字面
*中文粗体测试* ABC           // ABC 变粗，汉字不变
_中文斜体测试_ ABC           // ABC 倾斜，汉字不变
```

换成 `Noto Serif SC` 再跑一次，`*中文粗体测试*` 就正常了，`_中文斜体测试_` 仍然失效。

⚠️ **不要用 PDF 的 md5 判断加粗是否生效**。实测：即使汉字完全没变粗，PDF 的 md5
也和纯文本版**不同**（因为 strong 触发了字体回退）。正确做法是导出 PNG 用眼睛看：

```bash
typst compile doc.typ "page-{p}.png" -f png --ppi 200
```

先确认字体有没有粗体字面：`typst fonts --variants`。

### 解决方案：cuti

```typst
#import "@preview/cuti:0.4.0": show-cn-fakebold, show-cn-fakeitalic

#show strong: it => show-cn-fakebold(it)   // 仅当字体没有粗体字面时才需要
#show emph: it => show-cn-fakeitalic(it)
```

**只缺斜体时不要接 `show-cn-fakebold`** —— 字体本来能正常加粗，叠一层伪粗体反而会把汉字
压回 regular 再描边，成稿更难看。先按「症状」那张表确认缺的是哪个。

原理（读 cuti 0.4.0 源码确认）：

- 伪粗体 = 把汉字压到 `weight: "regular"` 阻断按字重回退，再加描边
  `stroke: 0.02857em + text.fill`（描边色跟随字色）
- 伪斜体 = `box(skew(ax: -18.4deg, reflow: false, ...))`

### 四个坑（全部实测过）

**坑 1：`show-cn-fakebold` 只挂 `weight: "bold"`。**
它的实现是 `show text.where(weight: "bold").or(strong)`。如果你的模板全程用
`weight: "semibold"`（常见于配合 Libertinus 这类有 Semibold 字面的拉丁字体），
它**不会生效**。自己挂一条即可（实测生效）：

```typst
#import "@preview/cuti:0.4.0": regex-fakebold
#let han-re = "[\p{script=Han}！-･〇-〰—。、]+"
#show text.where(weight: "semibold"): it => regex-fakebold(reg-exp: han-re, it, weight: "regular")
```

这条不会自递归：`regex-fakebold` 对匹配到的汉字输出 `text(weight: "regular", ...)`，
输出里不再有 `semibold` 的 `text` 元素，匹配不到自己。拉丁的 semibold 由外层 `text`
继承下来，也不会丢。

模板若同时用 `strong`，且字体**确实**缺粗体字面，再把下方「第二种情况」那条 `show strong`
一起加上——两条规则作用于不同元素，不冲突。字体本来能加粗就别加，原因见下方 ⚠️。

**坑 2：`show-cn-fakeitalic` 名字里有 `cn`，但会把拉丁词一起 skew。**
它内部调的 `fakeitalic` 正则同时匹配「非 CJK 的单词」和「单个 CJK 字符」。
若拉丁字体已有真斜体，再 skew 一次就成了**双重倾斜**，比正体还难看。
实测对比：`show-cn-fakeitalic` 下 `ABC` 明显比基线更斜。

处理办法：用下方「中英混排的推荐写法」里的 `han-char-re` 版 `show emph`，
不要用 `show-cn-fakeitalic`。

**坑 3：`regex-fakebold` 的默认正则 `.+` 是贪婪的。**
不限定范围会匹配全部内容，把拉丁字母也压成 Regular + 描边——实测：默认正则下
`*ABC 中文*` 的 `ABC` 变成带毛边的描边体，而不是字体自带的 Bold 字面。
必须显式传 `reg-exp`。

**坑 4：`#show emph: it => emph(...)` 会无限递归。**
报错 `maximum show rule depth exceeded`——show 规则匹配到了自己的输出。
斜体要用 `text(style: "italic", ...)`，不要用 `emph(...)`。

（顺带排除一个常见误判：`#show strong: it => regex-fakebold(...)` **不会**丢拉丁粗体。
实测 cuti 0.4.0 下，未匹配的拉丁内容保持原字重，加不加外层 `text(weight: "bold", ...)`
渲染结果一致。真正会毁掉拉丁粗体的是坑 3 的贪婪正则。）

### 中英混排的推荐写法

只对汉字做伪斜体/伪粗体，拉丁保持真字面——这也是 LaTeX 上游 `\bfseries` 的语义。

**第一种情况（最常见）：粗体正常，只有斜体坏。** 只挂斜体那一条：

```typst
#import "@preview/cuti:0.4.0": regex-fakeitalic

#let han-char-re = "[\p{script=Han}！-･〇-〰—。、]"   // 逐字

#show emph: it => regex-fakeitalic(reg-exp: han-char-re, ang: -18.4deg, it)
```

**第二种情况：字体确实没有粗体字面。** 再补一条 `show strong`：

```typst
#import "@preview/cuti:0.4.0": regex-fakebold, regex-fakeitalic

#let han-re      = "[\p{script=Han}！-･〇-〰—。、]+"   // 汉字 + 全角标点
#let han-char-re = "[\p{script=Han}！-･〇-〰—。、]"     // 逐字

#show strong: it => regex-fakebold(reg-exp: han-re, it, weight: "regular")
#show emph:   it => regex-fakeitalic(reg-exp: han-char-re, ang: -18.4deg, it)
```

⚠️ **字体本来能加粗时，不要加 `show strong` 那条。** 伪粗体的做法是把汉字压回
`weight: "regular"` 再描边，在能正常加粗的字体上反而比真 Bold 字面更细、更糊。
先按「症状」那张表确认缺的是粗体还是斜体，只补缺的那个。

- 字类里带上全角标点（`！-･〇-〰—。、`），否则会出现「汉字斜、标点正」的割裂。
  注意 `。`（U+3002）和 `、`（U+3001）**不在** `！-･`（U+FF01–U+FF65）区间里，容易漏。
- 逐字 vs 整串匹配：`box` 本身不可断行，所以默认用逐字（正则末尾不加 `+`）。
  Typst 0.15 + cuti 0.4.0 实测两种写法的换行表现一致，改成整串匹配也不会坏；
  但逐字粒度更保守，除非你确知整串匹配更合适，否则不要改。

### 什么时候不用 cuti

按「症状」那张表判断：字族带 ≥600 字重（如 `Noto Serif SC` 可变 200–900、
`Noto Sans SC` 有 700）→ 粗体不用管。但**斜体基本一定要**——CJK 字体几乎不提供
italic 字面，`_强调_` 里的汉字会保持正体。

## Figure Customization

```typst
#set figure(numbering: "1")
```

For per-chapter numbering, see [template.md](template.md).

## Labels and References

### Creating Labels

```typst
= Introduction <intro>

#figure(image("fig.png"), caption: [A figure]) <fig:main>
```

### Programmatic Labels

```typst
// Create label from string
#let key = "my-key"
#[Some content #label("ref-" + key)]

// Reference with link
#link(label("ref-" + key))[See here]
```

To query labels programmatically, see the Query System in [advanced.md](advanced.md).

## Multi-Region Documents

### Front/Main Matter

```typst
// Front matter: Roman numerals
#set page(numbering: "i")
#outline()
#pagebreak()

// Main matter: Arabic, reset counter
#set page(numbering: "1")
#counter(page).update(1)
```

### Appendix

```typst
#counter(heading).update(0)
#set heading(numbering: "A.1")
```

## Multi-Column Layout

```typst
// Whole document
#set page(columns: 2)

// Specific section
#columns(2, gutter: 12pt)[
  First column text...
  #colbreak()
  Second column text...
]
```

### Full-Width Element in Two-Column

```typst
#set page(columns: 2)

#place(top + center, scope: "parent", float: true)[
  #figure(
    image("wide-figure.png", width: 100%),
    caption: [Wide figure spanning both columns],
  )
]
```

## Quick Patterns

| Pattern         | Code                                                |
| --------------- | --------------------------------------------------- |
| Title page      | `#align(center + horizon)[...]` then `#pagebreak()` |
| Bibliography    | `#bibliography("refs.bib", style: "ieee")`          |
| Horizontal rule | `#line(length: 100%)`                               |
