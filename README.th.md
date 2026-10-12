# t5ive-skills

Plugin สำหรับ Codex และ Claude Code รวมสกิลช่วยเลือก workflow, รีวิวงาน, grill แนวคิดด้วยตัวเลือก เขียน commit message ภาษาไทย และจัดการงานผ่านระบบ `todo/` แบบ markdown

## สกิล

| Skill | หมวด | หน้าที่ |
|---|---|---|
| `skill-navigator` | Engineering | เลือกและเริ่มใช้ workflow ที่เหมาะกับงาน |
| `git-commit` | Engineering | เขียน Conventional Commit พร้อม emoji เป็นภาษาไทย |
| `review-with-choice` | Engineering | แนะนำและเริ่มวิธีรีวิวที่เลือก แล้วเสนอตัวเลือกดำเนินการกับ findings |
| `recap` | Engineering | สรุปก่อน–หลังเมื่อผู้ใช้สั่ง แบบสั้นเป็นค่าเริ่มต้น และเพิ่มรายละเอียดโค้ดได้ |
| `skill-guide` | Productivity | แนะนำสกิลหรือลำดับใช้ แล้วรอผู้ใช้ตัดสินใจ |
| `grill-with-choice` | Productivity | ใช้ workflow `grilling` ของ Matt โดยถามแต่ละรอบเป็นตัวเลือกที่กดได้ (ต้องมีสกิลนี้ใน host) |
| `todo-init` | Productivity | ติดตั้งระบบ `todo/` พร้อมบอร์ด All/Todo/Preop/Mise/WIP/Probe/Gate และกฎใน AGENTS.md |
| `todo-triage` | Productivity | แยกโน้ตใน `todo/inbox.md` เป็นไฟล์ `stage: todo` และคง header inbox |
| `todo-triage-chat` | Productivity | เปลี่ยนบทสนทนาเป็น task โดยถามข้อมูลที่ขาด หรือใช้ Matt `grilling` เมื่อไม่มีบริบทโจทย์ |
| `todo-next` | Productivity | เสนอเฉพาะงาน `mise`/`wip`, แยกคิว `probe` รอ dev test และ `gate` รอตรวจรับ และข้ามเนื้อหา `todo`/`preop` |
| `todo-audit` | Productivity | รายงาน Related files ที่ขาดนอก `todo`/`preop` และวันที่ done ที่ขาด |
| `todo-sweep` | Productivity | ย้ายไฟล์ `status: fin` ลง `todo/archive/YYYY-MM/` พร้อมเสนอ commit |
| `todo-parallel` | Productivity | รัน 2-3 งาน `mise`/`wip` ที่ไม่เกี่ยวกันเป็น subagents; commit เฉพาะงานที่ผู้ใช้เลือกหลัง dev test ผ่าน |
| `todo-finish` | Productivity | บันทึก dev ผ่าน (`probe → gate`), ปิดงาน Gate หรือคืนงานไป `wip` พร้อม Progress |

ไดอะแกรม workflow ของระบบ todo (วงจรงาน + scenario ตัวอย่างจริง): [skills/references/todo-diagrams.md](skills/references/todo-diagrams.md) — ต้นฉบับ `.mmd` อยู่ใน `assets/`

### Recap

`recap` สรุปสิ่งที่เปลี่ยนก่อน–หลัง พร้อมผลกระทบและหลักฐาน ค่าเริ่มต้นเน้นพฤติกรรมและผลลัพธ์; สั่ง “แบบละเอียด” เพื่อเพิ่ม logic, API, dependencies และโครงสร้าง ตอบในแชตหรือบันทึกเอกสารตามคำสั่งผู้ใช้และกฎ AGENTS

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
