# typst-skill

> 多平台 Agent Skill — 让 AI 精准驾驭 Typst 排版语言

[English](README.md)

## 这是什么？

`typst-skill` 是一个兼容 **Claude Code、CodeX、Gemini CLI、Cursor、OpenCode** 等多款 AI 编程助手的 Agent Skill（智能技能包）。它让 AI 编程助手能像 Typst 专家一样工作——不再凭空猜测语法，而是基于内建的三层文档体系，精确生成和调试 Typst 代码。

### 为什么需要它？

Typst 是一门新兴的排版语言，语法与 LaTeX / Markdown 有显著差异。大部分 AI 模型对 Typst 的训练数据有限，容易出现：
- 混用 LaTeX 语法（如 `\begin{}`、`\section`）
- 混淆 Typst 的数据类型（数组用 `()` 而非 `[]`）
- 不知道 Typst 特有的函数和参数

这个 skill 将 **完整的 Typst 官方文档、Touying 幻灯片文档、API 索引、包搜索索引** 都打包进本地，AI 在处理任务时会自动查阅这些资料，确保输出代码准确可用。

### 它能做什么？

| 场景 | 说明 |
|---|---|
| 📄 创建文档 | 从空白开始，或基于内置模板（备忘录、报告、学术论文等）快速生成 `.typ` 文档 |
| 📊 数学公式 | 全面的数学公式速查表，涵盖字体变体、重音符号、矩阵、分段函数等 |
| 🎬 幻灯片 (Touying) | 使用 Touying 创建演示文稿，支持主题、动画、多文件组织 |
| 🔍 API 搜索 | 基于 BM25 的全文搜索引擎，快速查找 Typst 函数和参数 |
| 📦 包搜索 | 搜索 Typst Universe 包仓库，支持分类和兼容性过滤 |
| ✅ 代码验证 | 验证文档中的内联 Typst 示例代码 |
| ⚡ 性能分析 | 分析 Typst 编译耗时，优化复杂文档 |

### 触发条件

当你在对话中提及以下任意内容时，skill 会自动激活：
- 操作 `.typ` 文件
- 提到 `typst`、`typst-cli`、`typst.toml`
- 创建/编辑 Typst 文档、模板或包
- 用 Touying 制作幻灯片
- 将 Markdown / LaTeX 转换为 Typst
- 排查 Typst 编译或语法问题

---

## 安装

### 方式一：直接导入

1. 克隆本仓库
2. 将整个项目目录放入 AI 助手的 skills 目录中
3. 重启 AI 助手，skill 将自动被识别

```bash
git clone https://github.com/childishtree/typst-skill.git
# 然后将 typst-skill 目录移动到 AI 助手的 skills 目录
```

### 方式二：手动复制

将整个 `typst-skill/` 目录（包含 `SKILL.md`、`references/`、`scripts/`、`assets/` 等）复制到 AI 助手的 skills 目录下。

---

## 文档体系（三层架构）

| 层级 | 目录 | 内容 | 适用场景 |
|---|---|---|---|
| **Tier 1** | `references/typst/` | 任务导向的精简指南 | 快速查阅：语法、表格、学术论文、数学公式等 |
| **Tier 2** | `references/typst-author/` | 官方文档完整镜像 | 深度参考：全部 API、教程、版本变更记录 |
| **Tier 3** | `references/touying-author/` | Touying 幻灯片专项文档 | 创建演示文稿：主题、动画、集成等 |

### Tier 1 指引速查

| 你需要... | 查阅文档 |
|---|---|
| 学习语法、导入、函数、控制流 | `references/typst/basics.md` |
| 了解数据类型和运算符 | `references/typst/types.md` |
| 数学公式、字体、重音、矩阵 | `references/typst/math.md` |
| 样式设置：页面、标题、图表 | `references/typst/styling.md` |
| 表格、网格、单元格合并 | `references/typst/tables.md` |
| 学术论文、参考文献、定理 | `references/typst/academic.md` |
| Markdown / LaTeX 转 Typst | `references/typst/conversion.md` |
| CLI 命令和构建选项 | `references/typst/cli.md` |
| 数据提取、多轮编译 | `references/typst/query.md` |
| 状态管理、计数器、XML | `references/typst/advanced.md` |
| 创建可复用模板 | `references/typst/template.md` |
| 开发与发布包 | `references/typst/package.md` |
| 输出验证（HTML/PNG/pdftotext） | `references/typst/debug.md` |
| 性能分析（--timings） | `references/typst/perf.md` |

---

## 环境要求

- **Typst CLI 0.15+**（推荐）: https://typst.app
  - macOS: `brew install typst`
  - Linux: `cargo install typst-cli`
  - Windows: `winget install typst`
- **Python 3.10+**（可选）: 用于搜索和验证脚本
  - 只有 `scripts/validate-examples.py` 需要 `markdown-it-py`（`pip install markdown-it-py`），
    其余三个脚本仅依赖标准库。
- **pdftotext**（可选）: 文本级输出验证
- **typstyle**（可选）: 代码格式化

---

## 快速上手

```bash
# 编译文档
typst compile document.typ

# 搜索包
python3 scripts/search-packages.py "chart" --category visualization

# 搜索 API 参考
python3 scripts/search-api.py "image width fit"

# 验证文档中的示例代码
python3 scripts/validate-examples.py

# 分析编译性能（需先生成轨迹）
typst compile --timings trace.json document.typ document.pdf
python3 scripts/perf-timings.py trace.json --self-time --top 10
```

---

## 目录结构

```
typst-skill/
├── SKILL.md                  # Skill 定义与主指南
├── README.md                 # 本文件
├── LICENSE                   # MIT 许可证
├── assets/
│   └── examples/             # 可运行的示例模板
│       ├── basic-document.typ
│       ├── academic-paper.typ
│       ├── math-cheatsheet.typ
│       ├── touying-presentation.typ
│       └── ...
├── references/
│   ├── typst/                # Tier 1: 任务导向指南
│   │   ├── basics.md / types.md / math.md / styling.md
│   │   ├── tables.md / academic.md / conversion.md
│   │   ├── cli.md / query.md / advanced.md
│   │   ├── template.md / package.md / debug.md / perf.md
│   │   ├── agents/           # 子 Agent 定义
│   │   └── data/             # API 和包搜索索引 (JSON)
│   ├── typst-author/         # Tier 2: 官方文档完整镜像
│   │   ├── tutorial/         # 入门教程
│   │   ├── guides/           # 专题指南
│   │   ├── reference/        # 完整 API 参考（按分类）
│   │   └── changelog/        # 版本变更记录
│   └── touying-author/       # Tier 3: Touying 幻灯片文档
│       ├── examples/         # 主题示例
│       ├── themes/           # 主题 API
│       ├── dynamic/          # 动画系统
│       └── integration/      # 集成（CeTZ, Fletcher 等）
└── scripts/
    ├── search-packages.py    # 基于 BM25 的包搜索
    ├── search-api.py         # API 参考搜索
    ├── validate-examples.py  # 示例代码验证
    └── perf-timings.py       # 性能轨迹分析
```

---

## 致谢

本项目基于以下优秀开源项目构建：

- **[claude-skill-typst](https://github.com/lucifer1004/claude-skill-typst)** by [lucifer1004](https://github.com/lucifer1004) — 原始 Typst skill for Claude Code，提供了基础 skill 结构、参考指南、搜索脚本和示例文档。
- **[typst-skills](https://github.com/apcamargo/typst-skills)** by [apcamargo](https://github.com/apcamargo) — Typst Agent Skills 合集，提供了完整的 Typst 官方文档镜像和 Touying 文档。

### 本 Skill 的增强

- 兼容 **Claude Code、CodeX、Gemini CLI、Cursor、OpenCode** 等 AI 编程助手
- 集成 **Touying** 幻灯片创建支持
- 新增完整的 **数学公式** 速查表和参考文档
- 修复路径引用问题，清理冗余文件
- 采用三层文档架构，高效组织

---

## License

MIT © 2026 lucifer1004
