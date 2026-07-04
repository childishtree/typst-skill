// Touying 演示文稿示例
// 使用 typst compile 编译为 PDF

#import "@preview/touying:0.6.1": *
#import themes.simple: *

#show: simple-theme.with(
  aspect-ratio: "16-9",
  footer: [Typst + Touying 演示],
)

// ===== 标题页 =====
#title-slide[
  = Typst 入门之旅
  #v(1.5em)

  从标记语言到专业排版

  #v(3em)

  Your Name #h(2em)
  2026 年 7 月
]

// ===== Section 1: 快速入门 =====
= 快速入门

== 什么是 Typst？

- 新一代基于标记的排版系统
- 比 LaTeX 更简洁，比 Word 更强大
- 内置现代排版引擎，开箱即用
- 支持数学公式、表格、图表、参考文献等

#focus-slide[
  _Typst = 标记语言 + 函数式编程 + 专业排版_
]

== 一个最小的文档

```typst
#set page(paper: "a4", margin: 2cm)
#set text(size: 11pt, lang: "zh")

= 我的第一份文档

欢迎使用 Typst！这是一个 *加粗* 和 _斜体_ 的示例。

$ E = m c^2 $
```

只需三行设置，就能开始写作！

== 安装方式

#slide(composer: (1fr, 1fr))[
  *macOS*
  ```bash
  brew install typst
  ```

  *VS Code*
  ```bash
  安装 Tinymist Typst 插件
  ```

  *在线版*
  ```bash
  https://typst.app/
  ```
][
  *Windows*
  ```bash
  winget install typst
  ```

  *Linux*
  ```bash
  cargo install typst-cli
  ```

  *编译命令*
  ```bash
  typst compile main.typ
  ```
]

// ===== Section 2: 核心语法 =====
= 核心语法

== 标记模式 vs 代码模式

#slide(composer: (1fr, 1fr))[
  *标记模式* (默认)

  - `= 标题`
  - `== 二级标题`
  - `*加粗*` 和 `_斜体_`
  - `- 列表项`
  - `+ 编号列表`

  #pause

  标记模式下用 `#` 进入代码模式：
  ```typst
  今天的日期是 #datetime.today()
  ```
][
  *代码模式* (`#` 开头)

  ```typst
  #let x = 42
  #if x > 10 {
    [大于 10]
  }
  #for name in ("A", "B") {
    [#name 号选手]
  }
  ```

  #pause

  代码块内直接写函数，不需要 `#`：
  ```typst
  #figure(
    table(columns: 2, [A], [B]),
    caption: [简单表格]
  )
  ```
]

== 常用元素速览

#table(
  columns: 3,
  table.header[*元素*, *语法*, *说明*],
  [标题], [`= 一级标题`], [最多到四级 `====`],
  [列表], [`- item` / `+ item`], [无序 / 有序],
  [图片], [`#image("pic.png")`], [支持 PNG/JPG/SVG],
  [表格], [`#table(...)`], [见 `table` / `grid`],
  [链接], [`#link("url")[text]`], [可点击的超链接],
  [公式], [`$x^2 + y^2 = 1$`], [内联和块级公式],
  [引用], [`@label`], [配合 `#bibliography`],
)

== 数学公式

$ f(x) = sum_(n=0)^oo (f^((n))(a)) / (n!) (x - a)^n $

#v(1em)

#pause

$
  F(omega)
  &= integral_(-oo)^oo f(t) e^(-i omega t) dif t \
  &= F(f)(omega)
$

#v(1em)

#pause

$
  mat(
    1, 0, 0;
    0, 1, 0;
    0, 0, 1;
  )
$

// ===== Section 3: 进阶功能 =====
= 进阶功能

== 动画与分步展示

#slide[
  第一件事：导入数据

  #pause

  第二件事：处理数据

  #pause

  第三件事：展示结果

  #v(1em)

  #only("4-")[
    *结论*：三步走策略清晰高效！
  ]
]

== 分栏布局

#slide(composer: (1fr, 1fr))[
  = 左栏

  - 优点 1
  - 优点 2
  - 优点 3

  #v(1em)

  左栏适合放摘要信息
][
  = 右栏

  #lorem(30)

  右栏适合放详细说明
]

== 代码与表格结合

#slide[
  *性能对比*

  #table(
    columns: 4,
    table.header[*方案*, *速度*, *内存*, *评分*],
    [A], [`120ms`], [`8MB`], [#sym.star #sym.star #sym.star],
    [B], [`85ms`], [`12MB`], [#sym.star #sym.star #sym.star #sym.star],
    [C], [`200ms`], [`5MB`], [#sym.star #sym.star],
  )

  #v(1em)

  #pause

  方案 B 综合表现最优，推荐使用。
]

// ===== Section 4: 总结 =====
= 总结

== Typst 的优势

#slide[
  + *语法简洁*：标记语言 + 函数式编程
  + *编译快速*：增量编译，毫秒级响应
  + *开箱即用*：无需安装宏包
  + *脚本支持*：强大的 `#query` 和 `#locate`
  + *社区生态*：丰富的 `@preview` 包
]

== 下一步

#slide[
  1. 安装 Typst 并编译你的第一个文档
  2. 阅读官方文档：https://typst.app/docs
  3. 浏览 Typst Universe：https://typst.app/universe
  4. 尝试 Touying 制作自己的演示文稿
]

#focus-slide[
  _开始你的 Typst 之旅吧！_

  #v(1em)

  `typst compile main.typ`
]
