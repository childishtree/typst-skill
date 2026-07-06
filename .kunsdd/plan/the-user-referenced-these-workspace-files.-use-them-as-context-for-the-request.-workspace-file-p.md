# Rewrite README.md & README.zh-CN.md

## Summary

Rewrite both `README.md` (English) and `README.zh-CN.md` (Chinese) for the `typst-skill` repository, blending the best content from the current versions with concise phrasing from `OLD_REAMED.md`. The current READMEs are already solid — the rewrite focuses on tightening language, improving flow, fixing minor issues, and incorporating the "Package Development" emphasis from the old version.

## Changes

### README.md — English version

1. **Intro section** — Combine the concise subtitle from OLD_REAMED.md ("A comprehensive CodeBuddy skill for Typst document authoring, package development, and presentation creation") with the current "What Is This?" explanation. Keep the "Why Do You Need It?" AI-training-data rationale — it's valuable context.

2. **Features table** — Add a dedicated row for "📦 Package Development" (currently only mentioned implicitly). Move the emoji icons to the Description column or keep them — decide during write. The old version treated Package Development as a separate feature, which is accurate.

3. **Reorder sections** — Move the "Trigger Conditions" section before Installation (it flows better: What → Triggers → Install → Use). Keep "Documentation System" after Installation as it's a detailed reference.

4. **Tier 1 Quick Reference table** — Keep as-is, it's excellent. Add a note that `SKILL.md` in the references/typst/ directory provides the overview (mentioned in old version's structure).

5. **Directory Structure** — Keep current, it's more accurate than the old one. Fix the root directory name: already `typst-skill/` (correct).

6. **Acknowledgements** — Keep at bottom (standard placement). Enhance slightly to match old version's phrasing.

7. **Tone & length** — Slightly tighten prose throughout. Current README is ~8000 chars; target ~7500-8000.

### README.zh-CN.md — Chinese version

1. Mirror all structural changes from the English version.

2. **Fix directory structure bug** — The Chinese version currently lists `├── README.md                 # 本文件` but is missing the `├── README.zh-CN.md           # 中文版` entry. Fix this.

3. **Ensure consistency** — All section headings, table structures, and content should parallel the English version.

### Both files

- Verify each file references the other correctly (`[中文版](README.zh-CN.md)` / `[English](README.md)`)
- Ensure no broken relative paths in directory listings
- Keep `MIT © 2026 lucifer1004` license footer
- Delete `OLD_REAMED.md` after rewrite is confirmed

## Files to modify

| File | Action |
|---|---|
| `README.md` | Rewrite |
| `README.zh-CN.md` | Rewrite |
| `OLD_REAMED.md` | Delete (optional, after rewrite approved) |

## What is NOT changed

- No changes to `SKILL.md`, `references/`, `scripts/`, `assets/`, `LICENSE`, `.gitignore`
- No content changes to the actual documentation or scripts
- The three-tier architecture descriptions remain intact

## Risks

- Low risk — this is a documentation-only rewrite
- Verify that the Chinese translation is natural and consistent with the English version
- Ensure no information loss from the current READMEs (they are comprehensive)
