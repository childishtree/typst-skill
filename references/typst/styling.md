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

中文的 `*粗体*` 和 `_斜体_` **静默失效**：拉丁字母正常变粗/变斜，汉字纹丝不动，
而且**不报任何错误**。这是 Typst 里最隐蔽的坑——编译 exit 0，看起来一切正常。

### 根因

Typst 按字重/字形去找字体，CJK 字体通常**只有 Regular**（少数带 Bold），
**几乎不提供斜体字面**。于是：

- 粗体：找不到粗体字面 → 要么保持 Regular（完全不加粗），要么跳到**另一个字体家族**
  的 Bold。后者更糟：同一行里有的字粗、有的字不粗（当替代字体缺简体字形时）。
- 斜体：CJK 字体没有 italic 字面，`_强调_` 里的汉字保持正体。

这不是 bug，是 Typst **不做合成（synthetic）粗斜体**的设计选择。从 LaTeX 迁过来的人
最容易踩——xeCJK / fontspec 会自动做假粗体，Typst 不会。

### 复现与验证

```typst
#set text(font: "LXGW Neo ZhiSong")   // 只有 Regular 一个字面（本机没装就换任意单字重中文字体）
*中文粗体测试* ABC                     // ABC 变粗，汉字不变
_中文斜体测试_ ABC                     // ABC 倾斜，汉字不变
```

⚠️ **不要用 PDF 的 md5 判断加粗是否生效**。实测：即使汉字完全没变粗，PDF 的 md5
也和纯文本版**不同**（因为 strong 触发了字体回退）。正确做法是导出 PNG 用眼睛看：

```bash
typst compile doc.typ "page-{p}.png" -f png --ppi 200
```

先确认字体有没有粗体字面：`typst fonts --variants`。

### 解决方案：cuti

```typst
#import "@preview/cuti:0.4.0": show-cn-fakebold, show-cn-fakeitalic

#show strong: it => show-cn-fakebold(it)
#show emph: it => show-cn-fakeitalic(it)
```

原理（读 cuti 0.4.0 源码确认）：

- 伪粗体 = 把汉字压到 `weight: "regular"` 阻断按字重回退，再加描边
  `stroke: 0.02857em + text.fill`（描边色跟随字色）
- 伪斜体 = `box(skew(ax: -18.4deg, reflow: false, ...))`

### 五个坑（全部实测过）

**坑 1：`show-cn-fakebold` 只挂 `weight: "bold"`。**
它的实现是 `show text.where(weight: "bold").or(strong)`。如果你的模板全程用
`weight: "semibold"`（常见于配合 Libertinus 这类有 Semibold 字面的拉丁字体），
它**不会生效**。自己挂一条即可（实测生效）：

```typst
#import "@preview/cuti:0.4.0": regex-fakebold
#let han-re = "[\p{script=Han}！-･〇-〰—]+"
#show text.where(weight: "semibold"): it => regex-fakebold(reg-exp: han-re, it, weight: "regular")
```

这条不会自递归：`regex-fakebold` 对匹配到的汉字输出 `text(weight: "regular", ...)`，
输出里不再有 `semibold` 的 `text` 元素，匹配不到自己。拉丁的 semibold 由外层 `text`
继承下来，也不会丢（与坑 4 的 `strong` 情况相反，原因见坑 4）。

模板若同时用 `strong`，把下方推荐写法里那条 `show strong` 一起加上——两条规则作用于
不同元素，不冲突。

**坑 2：`show-cn-fakeitalic` 名字里有 `cn`，但会把拉丁词一起 skew。**
它内部调的 `fakeitalic` 正则同时匹配「非 CJK 的单词」和「单个 CJK 字符」。
若拉丁字体已有真斜体，再 skew 一次就成了**双重倾斜**，比正体还难看。
实测对比：`show-cn-fakeitalic` 下 `ABC` 明显比基线更斜。

处理办法：用下方「中英混排的推荐写法」里的 `han-char-re` 版 `show emph`，
不要用 `show-cn-fakeitalic`。

**坑 3：`regex-fakebold` 的默认正则 `.+` 是贪婪的。**
不限定范围会匹配全部内容，把拉丁字母也压成 Regular + 描边（毁掉真粗体）。
必须显式传 `reg-exp`。

**坑 4：`#show strong: it => regex-fakebold(...)` 会把拉丁的粗体一起弄丢。**
`show` 规则是**替换**而不是叠加。`strong` 的粗体挂在元素本身上，一旦渲染被
`regex-fakebold` 的 `text(...)` 替换掉，未匹配的拉丁字母就没有任何地方继承粗体了——
实测：不加 cuti 时 `ABC` 是粗的，加上反而变细。
所以要在外面包一层 `text(weight: "bold", ...)`：先给整段上真粗体，再把汉字压回 regular + 描边。
（坑 1 的 `text.where(weight: "semibold")` 不受影响，因为那里的字重来自外层继承。）

**坑 5：`#show emph: it => emph(...)` 会无限递归。**
报错 `maximum show rule depth exceeded`——show 规则匹配到了自己的输出。
斜体要用 `text(style: "italic", ...)`，不要用 `emph(...)`。

### 中英混排的推荐写法

只对汉字做伪粗体/伪斜体，拉丁保持真字面——这也是 LaTeX 上游 `\bfseries` 的语义：

```typst
#import "@preview/cuti:0.4.0": regex-fakebold, regex-fakeitalic

#let han-re      = "[\p{script=Han}！-･〇-〰—]+"   // 汉字 + 全角标点
#let han-char-re = "[\p{script=Han}！-･〇-〰—]"     // 逐字

// ⚠️ 必须在外面重新施加真粗体/真斜体，见上方坑 4、坑 5
#show strong: it => text(weight: "bold", regex-fakebold(reg-exp: han-re, it, weight: "regular"))
#show emph:   it => text(style: "italic", regex-fakeitalic(reg-exp: han-char-re, ang: -18.4deg, it))
```

- 字类里带上全角标点（`！-･〇-〰—`），否则会出现「汉字斜、逗号正」的割裂。
- 逐字 vs 整串匹配：`box` 本身不可断行，所以默认用逐字（正则末尾不加 `+`）。
  Typst 0.15 + cuti 0.4.0 实测两种写法的换行表现一致，改成整串匹配也不会坏；
  但逐字粒度更保守，除非你确知整串匹配更合适，否则不要改。

### 何时不需要 cuti

CJK 字体自带 Bold 时（如 Noto Sans CJK 有 Bold），粗体可以直接
`#set text(weight: "bold")`。但**斜体仍然没有**——CJK 字体几乎不提供 italic 字面，
所以伪斜体基本是必需品。

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
