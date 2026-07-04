# typst-skill

A comprehensive CodeBuddy skill for Typst document authoring, package development, and presentation creation. Combines detailed reference guides, a full mirror of official Typst documentation, Touying presentation support, and searchable API/package indexes.

## Acknowledgements

This skill is built upon and inspired by the following excellent open-source projects:

- **[claude-skill-typst](https://github.com/lucifer1004/claude-skill-typst)** by [lucifer1004](https://github.com/lucifer1004) — The original Typst skill for Claude Code, providing the foundational skill structure, reference guides, search scripts, and example documents.
- **[typst-skills](https://github.com/apcamargo/typst-skills)** by [apcamargo](https://github.com/apcamargo) — A collection of agent skills for Typst, providing the complete mirror of official Typst and Touying documentation.

Key enhancements in this skill:
- Adapted and optimized for **CodeBuddy** platform
- Integrated **Touying** presentation creation support
- Added comprehensive **math formula** cheatsheet and reference
- Fixed path references and removed redundant files
- Organized with a three-tier documentation architecture

## Features

- **Document Creation** — Start from scratch or use built-in examples for memos, reports, academic papers, and more
- **Package Development** — Create, validate, and publish Typst packages to Typst Universe
- **Touying Presentations** — Create slide decks with the Touying package, including theme support and animations
- **API Reference Search** — Full-text search across the Typst API with BM25 indexing
- **Package Search** — Search Typst Universe packages with compatibility filtering
- **Code Validation** — Validate inline Typst examples in documentation
- **Performance Profiling** — Analyze Typst compilation timings

## Requirements

- **Typst CLI 0.15+** (recommended): https://typst.app
  - macOS: `brew install typst`
  - Linux: `cargo install typst-cli`
  - Windows: `winget install typst`
- **Python 3.10+** (optional): For search and validation scripts
- **pdftotext** (optional): For text-level output verification
- **typstyle** (optional): For code formatting

## Quick Start

```bash
# Compile a document
typst compile document.typ

# Search for packages
python3 scripts/search-packages.py "chart" --category visualization

# Search the API reference
python3 scripts/search-api.py "image width fit"

# Validate documentation examples
python3 scripts/validate-examples.py
```

## Structure

```
typst/
├── SKILL.md                  # Skill definition and main guide
├── README.md                 # This file
├── LICENSE                   # MIT License
├── assets/
│   └── examples/             # Starter templates and examples
├── references/
│   ├── typst/                # Tier 1: Task-oriented guides
│   │   ├── SKILL.md          # Reference overview
│   │   ├── basics.md         # Language fundamentals
│   │   ├── types.md          # Data types and operators
│   │   ├── styling.md        # Page styling and layout
│   │   ├── tables.md         # Tables and grids
│   │   ├── academic.md       # Academic writing
│   │   ├── conversion.md     # Markdown/LaTeX conversion
│   │   ├── cli.md            # CLI commands
│   │   ├── query.md          # Data extraction
│   │   ├── advanced.md       # State, counters, XML
│   │   ├── template.md       # Template creation
│   │   ├── package.md        # Package development
│   │   ├── debug.md          # Output verification
│   │   ├── perf.md           # Performance profiling
│   │   └── agents/           # Sub-agent definitions
│   ├── typst-author/         # Tier 2: Official documentation mirror
│   │   ├── changelog/        # Version changelogs
│   │   ├── guides/           # Official guides
│   │   ├── reference/        # Full API reference
│   │   └── tutorial/         # Getting started tutorial
│   └── touying-author/       # Tier 3: Touying presentation docs
│       ├── examples/         # Slide deck examples
│       ├── themes/           # Theme documentation
│       ├── dynamic/          # Animations
│       └── integration/      # Integrations (CeTZ, Fletcher, etc.)
└── scripts/
    ├── search-packages.py    # Package search with BM25
    ├── search-api.py         # API reference search
    ├── validate-examples.py  # Example code validation
    └── perf-timings.py       # Performance trace analysis
```

## License

MIT © 2026 lucifer1004
