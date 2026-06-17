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

- **[git-commit](./skills/git-commit/SKILL.md)** — สร้าง commit message ตามแบบ Conventional Commits + emoji เขียน title/body เป็นภาษาไทย trigger ด้วย `/git-commit` หรือเมื่อขอให้ commit
