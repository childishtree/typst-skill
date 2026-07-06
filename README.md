# typst-skill

> Multi-Platform Agent Skill — Empowering AI to master the Typst typesetting language

[中文版](README.zh-CN.md)

## What Is This?

`typst-skill` is an Agent Skill compatible with **Claude Code, CodeX, Gemini CLI, Cursor, OpenCode**, and other AI coding assistants. It enables AI coding assistants to work like Typst experts — no more guessing syntax from patchy training data. Instead, it draws on a built-in three-tier documentation system to generate and debug Typst code with precision.

### Why Do You Need It?

Typst is a relatively new typesetting language. Its syntax differs significantly from LaTeX and Markdown. Most AI models have limited Typst knowledge and tend to:
- Mix in LaTeX syntax (e.g., `\begin{}`, `\section`)
- Confuse Typst data types (arrays use `()` not `[]`)
- Hallucinate function names or parameters

This skill bundles the **complete Typst official documentation, Touying slide docs, API index, and package search index** locally. The AI consults these resources automatically before writing code, ensuring accurate, runnable output.

### What Can It Do?

| Use Case | Description |
|---|---|
| 📄 Document Creation | Create `.typ` docs from scratch or from built-in templates (memos, reports, academic papers, etc.) |
| 📊 Math Formulas | Comprehensive math cheatsheet covering font variants, accents, matrices, piecewise functions, and more |
| 🎬 Slides (Touying) | Create presentation decks with Touying — themes, animations, multi-file organization |
| 🔍 API Search | BM25-based full-text search across the entire Typst API |
| 📦 Package Search | Search Typst Universe with category and compatibility filters |
| ✅ Code Validation | Validate inline Typst examples in documentation |
| ⚡ Performance Profiling | Analyze Typst compilation timings to optimize complex documents |

### Trigger Conditions

The skill activates automatically when you mention:
- Working with `.typ` files
- `typst`, `typst-cli`, or `typst.toml`
- Creating/editing Typst documents, templates, or packages
- Making presentation slides with Touying
- Converting Markdown / LaTeX to Typst
- Troubleshooting Typst compilation or syntax issues

---

## Installation

### Option 1: Direct Import

1. Clone this repository
2. Move the entire project directory into your AI assistant's skills folder
3. Restart your AI assistant — the skill will be recognized automatically

```bash
git clone https://github.com/childishtree/typst-skill.git
# Then move typst-skill into your AI assistant's skills directory
```

### Option 2: Manual Copy

Copy the entire `typst-skill/` directory (including `SKILL.md`, `references/`, `scripts/`, `assets/`, etc.) into your AI assistant's skills directory.

---

## Documentation System (Three-Tier Architecture)

| Tier | Directory | Content | Best For |
|---|---|---|---|
| **Tier 1** | `references/typst/` | Task-oriented concise guides | Quick lookup: syntax, tables, academic papers, math, etc. |
| **Tier 2** | `references/typst-author/` | Full official docs mirror | Deep reference: all APIs, tutorials, changelogs |
| **Tier 3** | `references/touying-author/` | Touying slide-specific docs | Creating presentations: themes, animations, integrations |

### Tier 1 Quick Reference

| When you need to... | Read |
|---|---|
| Learn syntax, imports, functions, control flow | `references/typst/basics.md` |
| Understand data types and operators | `references/typst/types.md` |
| Math formulas, fonts, accents, matrices | `references/typst/math.md` |
| Style pages, headings, figures | `references/typst/styling.md` |
| Tables, grids, cell spans | `references/typst/tables.md` |
| Academic papers, bibliography, theorems | `references/typst/academic.md` |
| Convert Markdown / LaTeX to Typst | `references/typst/conversion.md` |
| CLI commands and build options | `references/typst/cli.md` |
| Data extraction, multi-pass builds | `references/typst/query.md` |
| State management, counters, XML | `references/typst/advanced.md` |
| Create reusable templates | `references/typst/template.md` |
| Develop and publish packages | `references/typst/package.md` |
| Output verification (HTML/PNG/pdftotext) | `references/typst/debug.md` |
| Performance profiling (--timings) | `references/typst/perf.md` |

---

## Requirements

- **Typst CLI 0.15+** (recommended): https://typst.app
  - macOS: `brew install typst`
  - Linux: `cargo install typst-cli`
  - Windows: `winget install typst`
- **Python 3.10+** (optional): For search and validation scripts
- **pdftotext** (optional): Text-level output verification
- **typstyle** (optional): Code formatting

---

## Quick Start

```bash
# Compile a document
typst compile document.typ

# Search packages
python3 scripts/search-packages.py "chart" --category visualization

# Search the API reference
python3 scripts/search-api.py "image width fit"

# Validate inline examples in docs
python3 scripts/validate-examples.py

# Analyze compilation performance
python3 scripts/perf-timings.py document.typ
```

---

## Directory Structure

```
typst-skill/
├── SKILL.md                  # Skill definition & main guide
├── README.md                 # This file (English)
├── README.zh-CN.md           # 中文版
├── LICENSE                   # MIT License
├── assets/
│   └── examples/             # Runnable starter templates
│       ├── basic-document.typ
│       ├── academic-paper.typ
│       ├── math-cheatsheet.typ
│       ├── touying-presentation.typ
│       └── ...
├── references/
│   ├── typst/                # Tier 1: Task-oriented guides
│   │   ├── basics.md / types.md / math.md / styling.md
│   │   ├── tables.md / academic.md / conversion.md
│   │   ├── cli.md / query.md / advanced.md
│   │   ├── template.md / package.md / debug.md / perf.md
│   │   ├── agents/           # Sub-agent definitions
│   │   └── data/             # API & package search indices (JSON)
│   ├── typst-author/         # Tier 2: Full official docs mirror
│   │   ├── tutorial/         # Getting started
│   │   ├── guides/           # Topic guides
│   │   ├── reference/        # Complete API reference (by category)
│   │   └── changelog/        # Version changelogs
│   └── touying-author/       # Tier 3: Touying slide docs
│       ├── examples/         # Theme examples
│       ├── themes/           # Theme APIs
│       ├── dynamic/          # Animation system
│       └── integration/      # Integrations (CeTZ, Fletcher, etc.)
└── scripts/
    ├── search-packages.py    # BM25-based package search
    ├── search-api.py         # API reference search
    ├── validate-examples.py  # Example code validation
    └── perf-timings.py       # Performance trace analysis
```

---

## Acknowledgements

This project is built upon the following excellent open-source projects:

- **[claude-skill-typst](https://github.com/lucifer1004/claude-skill-typst)** by [lucifer1004](https://github.com/lucifer1004) — The original Typst skill for Claude Code, providing the foundational skill structure, reference guides, search scripts, and example documents.
- **[typst-skills](https://github.com/apcamargo/typst-skills)** by [apcamargo](https://github.com/apcamargo) — A collection of Typst Agent Skills, providing the complete mirror of official Typst documentation and Touying documentation.

### Enhancements in This Skill

- Compatible with **Claude Code, CodeX, Gemini CLI, Cursor, OpenCode**, and other AI coding assistants
- Integrated **Touying** presentation creation support
- Added comprehensive **math formula** cheatsheet and reference
- Fixed path references and cleaned up redundant files
- Organized with an efficient three-tier documentation architecture

---

## License

MIT © 2026 lucifer1004
