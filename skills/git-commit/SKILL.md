---
name: git-commit
description: "Use when the user says \"commit\", \"git commit\", \"create commit message\", or calls /git-commit. Also triggers when asked to summarize code changes into a commit message in any form."
allowed-tools: Bash
---

# Git Commit Message Skill

Generate commit messages following Conventional Commits + emoji. Commit content (title/body) is written in Thai.

---

## Workflow

### 1. Analyze diff

```bash
# Prefer staged diff
git diff --staged

# If nothing staged, fall back to working tree
git diff

git status --porcelain
```

### 2. Stage files (if needed)

```bash
git add path/to/file
git add -p   # interactive, for partial staging
```

**Never stage:** `.env`, credentials, private keys, secrets.

### 3. Generate message → commit

```bash
git commit -m "$(cat <<'EOF'
<type>(<emoji><scope>): <title>

<body>

<footer>
EOF
)"
```

---

## Format

### Short (no body)
```
<type>(<emoji><scope>): <title>
```

### Full (with body)
```
<type>(<emoji><scope>): <title>

<body — what changed and why>

<footer>
```

- **Title**: max 72 chars, Thai language, present tense imperative ("เพิ่ม" ไม่ใช่ "เพิ่มแล้ว")
- **Body**: use real line breaks (not literal `\n`), include when there are important details
- **Scope**: include when the change targets a specific module/feature (optional)
- **Footer**: always include Co-authored-by; add issue refs when relevant

---

## Types

| Type | Emoji | When to use |
|------|-------|-------------|
| `feat` | ✨ | New feature |
| `fix` | 🐞 | Bug fix |
| `refactor` | ♻️ | Code restructure without fixing bug or adding feature |
| `perf` | ⚡ | Performance improvement |
| `docs` | 📝 | Add or update documentation |
| `test` | 🧪 | Add or fix tests |
| `style` | 🎨 | Formatting, whitespace (no logic impact) |
| `build` | 📦 | Build system or external dependencies |
| `ci` | 🤖 | CI/CD configuration |
| `chore` | 🔧 | Other tasks that don't affect src/test |
| `revert` | ⏪ | Revert a previous commit |

---

## Breaking Change

When a change breaks an existing API/interface:

```
feat(✨auth)!: เปลี่ยน token format เป็น JWT

BREAKING CHANGE: token รูปแบบเดิมใช้ไม่ได้แล้ว
ต้อง re-login เพื่อรับ token ใหม่
```

- Append `!` after type/scope
- Add `BREAKING CHANGE:` in footer describing the impact

---

## Footer

### Co-authored-by

Always include the AI agent's own standard co-author tag. Examples:

```
Co-authored-by: Claude <noreply@anthropic.com>
Co-authored-by: Codex <noreply@openai.com>
Co-authored-by: GitHub Copilot <noreply@github.com>
Co-authored-by: gemini-code-assist[bot] <176961590+gemini-code-assist[bot]@users.noreply.github.com>
```

### Issue references (when applicable)

```
Closes #123
Refs #456
```

---

## Multiple Commits

If changes span multiple concerns, split into separate commits:
- 1 commit = 1 concern
- Order by dependency (depended-on items first)

---

## Safety Rules — NEVER skip these

- **`git reset` is FORBIDDEN without explicit user confirmation every time** — even if the user approved it before, ask again. Prior approval does not carry over.
- **Never commit secrets** — `.env`, credentials, private keys, API tokens
- **Never skip hooks** (`--no-verify`) unless user explicitly asks
- **Never force push to main/master**
- **If commit fails due to pre-commit hook** — fix the issue, create a NEW commit (never `--amend`)

---

## Examples

```
feat: ✨ เพิ่ม UserService สำหรับจัดการ user

Co-authored-by: Claude <noreply@anthropic.com>
```

```
fix(🐞pick-slip): แก้ null reference ใน GetUserById

เกิดจาก user ที่ถูกลบแล้วยังถูก query อยู่
เพิ่ม null check ก่อน map ข้อมูล

Co-authored-by: Claude <noreply@anthropic.com>
```

```
feat(✨auth)!: เปลี่ยน token format เป็น JWT

BREAKING CHANGE: token รูปแบบเดิมใช้ไม่ได้แล้ว
ต้อง re-login เพื่อรับ token ใหม่

Closes #89

Co-authored-by: Claude <noreply@anthropic.com>
```
