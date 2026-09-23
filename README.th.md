# t5ive-skills

Plugin สำหรับ Codex และ Claude Code รวมสกิลช่วยเลือก workflow, รีวิวงาน, grill แนวคิดด้วยตัวเลือก และเขียน commit message ภาษาไทย

## สกิล

| Skill | หมวด | หน้าที่ |
|---|---|---|
| `skill-navigator` | Engineering | เลือกและเริ่มใช้ workflow ที่เหมาะกับงาน |
| `git-commit` | Engineering | เขียน Conventional Commit พร้อม emoji เป็นภาษาไทย |
| `review-with-choice` | Engineering | แสดงตัวเลือกวิธีรีวิว แนะนำวิธีที่เหมาะ แล้วเริ่มวิธีที่ผู้ใช้เลือก |
| `skill-guide` | Productivity | แนะนำสกิลหรือลำดับใช้ แล้วรอผู้ใช้ตัดสินใจ |
| `grill-with-choice` | Productivity | ใช้ workflow `grilling` ของ Matt โดยถามแต่ละรอบเป็นตัวเลือกที่กดได้ (ต้องมีสกิลนี้ใน host) |

## ติดตั้ง

### Codex

```bash
codex plugin marketplace add T5ive/t5ive-skills
codex
```

เปิด `/plugins` เลือก marketplace `t5ive-skills` แล้วติดตั้ง plugin `t5ive-skills` รายการเดียว

### Claude Code

```text
/plugin marketplace add T5ive/t5ive-skills
/plugin install t5ive-skills@t5ive-skills
```

คำสั่งสกิลใน Claude Code ใช้ namespace `/t5ive-skills:<skill>`

### ติดตั้งเฉพาะ Skills

```bash
npx skills add T5ive/t5ive-skills
```

### พัฒนา plugin ในเครื่อง

Codex:

```bash
codex plugin install .
```

Claude Code:

```bash
claude --plugin-dir .
```
