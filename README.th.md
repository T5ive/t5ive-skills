# t5ive-skills

Plugin สำหรับ Codex และ Claude Code รวมสกิลช่วยเลือก workflow, รีวิวงาน, grill แนวคิดด้วยตัวเลือก เขียน commit message ภาษาไทย และจัดการงานผ่านระบบ `todo/` แบบ markdown

## สกิล

| Skill | หมวด | หน้าที่ |
|---|---|---|
| `skill-navigator` | Engineering | เลือกและเริ่มใช้ workflow ที่เหมาะกับงาน |
| `git-commit` | Engineering | เขียน Conventional Commit พร้อม emoji เป็นภาษาไทย |
| `review-with-choice` | Engineering | แสดงตัวเลือกวิธีรีวิว แนะนำวิธีที่เหมาะ แล้วเริ่มวิธีที่ผู้ใช้เลือก |
| `skill-guide` | Productivity | แนะนำสกิลหรือลำดับใช้ แล้วรอผู้ใช้ตัดสินใจ |
| `grill-with-choice` | Productivity | ใช้ workflow `grilling` ของ Matt โดยถามแต่ละรอบเป็นตัวเลือกที่กดได้ (ต้องมีสกิลนี้ใน host) |
| `todo-init` | Productivity | ติดตั้งระบบ `todo/`: โครงโฟลเดอร์, header inbox, กฎใน AGENTS.md, `.gitignore` และ spec dashboard |
| `todo-triage` | Productivity | แยกโน้ตดิบใน `todo/inbox.md` เป็นไฟล์งานตามต้นไม้ตัดสินใจ (คง header inbox ไว้) |
| `todo-next` | Productivity | สรุปงาน open ทั้งหมด เสนองานถัดไป และทำตาม Skills ticks ในไฟล์งาน |
| `todo-audit` | Productivity | รายงานไฟล์งานที่ขาดไฟล์ที่เกี่ยวข้อง / วันที่ done — สองอย่างที่บอร์ดเห็นไม่ได้ |
| `todo-sweep` | Productivity | ย้ายไฟล์ `status: done` ลง `todo/archive/YYYY-MM/` พร้อมเสนอ commit |
| `todo-parallel` | Productivity | รัน 2-3 งานที่ไม่เกี่ยวกันเป็น subagents พื้นหลัง แล้ว commit แยกทีละงาน |

## สกิลที่ต้องใช้ร่วมกัน

ติดตั้งชุดสกิลต่อไปนี้ใน agent เดียวกันเพื่อใช้ workflow ได้ครบ โดย plugin `t5ive-skills` ติดตั้งแยกได้

| ชุดสกิล | Repository |
|---|---|
| Matt Pocock | [mattpocock/skills](https://github.com/mattpocock/skills) |
| 9arm | [ต้นฉบับ: thananon/9arm-skills](https://github.com/thananon/9arm-skills) · [fork สำหรับ Codex plugin: T5ive/9arm-skills](https://github.com/T5ive/9arm-skills) |
| Karpathy guidelines | [ต้นฉบับ: multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) · [fork สำหรับ Codex plugin: T5ive/andrej-karpathy-skills](https://github.com/T5ive/andrej-karpathy-skills) |
| Ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |

ลิงก์ต้นฉบับและ fork แสดงทั้งที่มาและช่องทางติดตั้งเป็น Codex plugin ติดตั้งแต่ละชุดเพียงครั้งเดียว; ผู้ใช้ Codex ให้ใช้ fork ของ T5ive สำหรับ 9arm และ Karpathy guidelines

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
