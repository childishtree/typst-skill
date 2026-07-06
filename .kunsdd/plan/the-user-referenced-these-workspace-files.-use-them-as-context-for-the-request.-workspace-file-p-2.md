# Replace CodeBuddy with multi-platform references in READMEs

## Summary

Replace all mentions of "CodeBuddy" in `README.md` and `README.zh-CN.md` with references to multiple AI coding assistant platforms: **Claude Code, CodeX, Gemini CLI, Cursor, OpenCode**, etc. This makes the skill documentation platform-agnostic.

## Changes — README.md (English, 8 occurrences)

| # | Location | Current | Replacement |
|---|---|---|---|
| 1 | Subtitle | `> CodeBuddy Agent Skill — Empowering AI to master the Typst typesetting language` | `> Multi-Platform Agent Skill — Empowering AI to master the Typst typesetting language` |
| 2 | "What Is This?" | `` `typst-skill` is an Agent Skill tailored for **CodeBuddy**. `` | `` `typst-skill` is an Agent Skill compatible with **Claude Code, CodeX, Gemini CLI, Cursor, OpenCode**, and other AI coding assistants. `` |
| 3 | Installation heading | `### Option 1: Import into CodeBuddy` | `### Option 1: Direct Import` |
| 4 | Step 2 | `Move the entire project directory into CodeBuddy's skills folder` | `Move the entire project directory into your AI assistant's skills folder` |
| 5 | Step 3 | `Restart CodeBuddy — the skill will be recognized automatically` | `Restart your AI assistant — the skill will be recognized automatically` |
| 6 | Code comment | `# Then move typst-skill into your CodeBuddy skills directory` | `# Then move typst-skill into your AI assistant's skills directory` |
| 7 | Option 2 | `Copy SKILL.md … into your CodeBuddy skills directory.` | `Copy SKILL.md … into your AI assistant's skills directory.` |
| 8 | Enhancements | `- Adapted and optimized for the **CodeBuddy** platform` | `- Compatible with **Claude Code, CodeX, Gemini CLI, Cursor, OpenCode**, and other AI coding assistants` |

## Changes — README.zh-CN.md (Chinese, 8 occurrences, mirrored naturally)

| # | Current | Replacement |
|---|---|---|
| 1 | `> CodeBuddy Agent Skill — 让 AI 精准驾驭 Typst 排版语言` | `> 多平台 Agent Skill — 让 AI 精准驾驭 Typst 排版语言` |
| 2 | `` `typst-skill` 是一个为 **CodeBuddy** 定制的 Agent Skill（智能技能包） `` | `` `typst-skill` 是一个兼容 **Claude Code、CodeX、Gemini CLI、Cursor、OpenCode** 等多款 AI 编程助手的 Agent Skill（智能技能包） `` |
| 3 | `### 方式一：直接导入 CodeBuddy` | `### 方式一：直接导入` |
| 4 | `将整个项目目录放入 CodeBuddy 的 skills 目录中` | `将整个项目目录放入 AI 助手的 skills 目录中` |
| 5 | `重启 CodeBuddy，skill 将自动被识别` | `重启 AI 助手，skill 将自动被识别` |
| 6 | `# 然后将 typst-skill 目录移动到 CodeBuddy skills 目录` | `# 然后将 typst-skill 目录移动到 AI 助手的 skills 目录` |
| 7 | `将仓库中的 SKILL.md … 复制到 CodeBuddy 的 skills 目录下` | `将仓库中的 SKILL.md … 复制到 AI 助手的 skills 目录下` |
| 8 | `- 适配并优化为 **CodeBuddy** 平台` | `- 兼容 **Claude Code、CodeX、Gemini CLI、Cursor、OpenCode** 等 AI 编程助手` |

## Files to modify

- `README.md` — 8 replacements
- `README.zh-CN.md` — 8 replacements

## What is NOT changed

- `SKILL.md` (no CodeBuddy references)
- `OLD_REAMED.md` (kept as-is for reference)
- All other content, structure, cross-links

## Risks

- Minimal. Pure text replacement, no structural changes.
- Verify Chinese translation reads naturally.
- Keep the platform list concise.
