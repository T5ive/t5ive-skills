# t5ive-skills

## โครงสร้าง

Skills อยู่ใน `skills/`

แต่ละ skill มี directory ของตัวเอง ประกอบด้วย `SKILL.md` (มี YAML frontmatter — `name` และ `description`) และไฟล์ reference ที่ bundle มาด้วย

## ติดตั้ง

### Codex

เพิ่ม marketplace:

```bash
codex plugin marketplace add T5ive/t5ive-skills
codex
```

เปิด `/plugins`, เลือก marketplace `t5ive-skills`, แล้วติดตั้ง `t5ive-skills`

### Claude Code

```bash
/plugin marketplace add T5ive/t5ive-skills
/plugin install skill-navigator
/plugin install git-commit
```

### Skills only

```bash
npx skills add T5ive/t5ive-skills
```

### Local plugin development

Codex:
```bash
codex plugin install .
```

Claude Code:
```bash
claude --plugin-dir ./t5ive-skills
```

## Skills

- **[skill-navigator](./skills/skill-navigator/SKILL.md)** — แมป situation ไปยัง skill chain ที่เหมาะสม บอกสถานการณ์ที่เจออยู่ (เริ่ม feature, เจอ bug, อยากจะ review) แล้ว AI จะแนะนำว่าควรใช้ skill ไหน

  **Quick map (v1.0):**

  | สถานการณ์ | Skill chain |
  |---|---|
  | ไม่รู้จะใช้ skill ไหน | `/ask-matt` |
  | Feature ใหม่, ยังไม่มี codebase | `/grill-me` → `/tdd` |
  | Feature ใหม่, มี codebase อยู่แล้ว | `/setup-matt-pocock-skills` → `/grill-with-docs` → `/tdd` |
  | Bug (reproduce ได้) | `/debug-mantra` → `/post-mortem` |
  | Bug (ยาก / flaky / perf) | `/diagnosing-bugs` → `/post-mortem` |
  | Review / ก่อน merge | `/scrutinize` |
  | Review diff หา over-engineering | `/ponytail-review` |
  | Architecture review | `/improve-codebase-architecture` |
  | แตก spec เป็น issue | `/to-prd` → `/to-issues` |
  | Context window เต็ม | `/handoff` |
  | เขียน code แบบ minimal | `/ponytail` |
  | ตอบภาษาไทย ประหยัด token | `/pordee` |

  decision tree เต็ม: [`references/situations.md`](./skills/skill-navigator/references/situations.md)

- **[git-commit](./skills/git-commit/SKILL.md)** — สร้าง commit message ตามแบบ Conventional Commits + emoji เขียน title/body เป็นภาษาไทย trigger ด้วย `/git-commit` หรือเมื่อขอให้ commit
