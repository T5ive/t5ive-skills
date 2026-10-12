# Todo Diagrams — ภาพรวมและ scenario ของระบบ todo

เอกสารประกอบไดอะแกรมของระบบ `todo/` — ฉบับละเอียดกว่าที่ฝังไว้ใน README
ต้นฉบับ `.mmd` อยู่ที่ `assets/todo-lifecycle-th.mmd` และ `assets/todo-scenario-th.mmd`
(แก้ไดอะแกรมแล้ว sync ทั้งไฟล์นี้และ `.mmd` ทั้งสองด้วยมือ — ไม่มี build step)

## 1. Lifecycle ของ task (stateDiagram-v2)

```mermaid
stateDiagram-v2
    [*] --> todo: triage สร้างไฟล์
    todo --> preop: dev รอข้อมูลหรือผลทดสอบ
    preop --> todo: dev ได้ข้อมูล แต่ยังต้องเตรียมต่อ
    preop --> mise: dev ได้ข้อมูลและเตรียมพร้อม
    todo --> mise: dev เติมรายละเอียดครบ
    mise --> wip: เริ่มงาน — todo-next/AI
    wip --> probe: งานเสร็จ จบ session — AI
    probe --> wip: ไม่ผ่าน — จดเหตุผลใน Progress
    probe --> gate: dev ยืนยันว่าทดสอบผ่าน — todo-finish --pass หรือบอร์ด
    gate --> wip: Tester ไม่ผ่าน — จดเหตุผลใน Progress
    gate --> fin: Jira Done / ผู้ใช้ยืนยันจบ — todo-finish --done หรือบอร์ด
    todo --> fin: ไม่มี ticket ผู้ใช้ประกาศจบ
    fin --> [*]: sweep เก็บ archive/YYYY-MM
    note right of gate
        Jira เป็น manual
        ไฟล์ไม่ mirror สถานะ Jira
    end note
```

### แต่ละ state คืออะไร

| State | ความหมาย | ดูที่ไหน |
|---|---|---|
| `stage: todo` | ไฟล์ที่ todo-triage สร้าง รอ dev เติมรายละเอียด; AI ไม่อ่านเนื้อหา | views **All**, **Todo** |
| `stage: preop` | dev รอข้อมูลหรือผลทดสอบระยะสั้น; AI ไม่อ่านเนื้อหา | view **Preop** |
| `stage: mise` | dev เตรียมรายละเอียดครบ พร้อมให้ AI เริ่มงาน | view **Mise** |
| `stage: wip` | เริ่มแล้วยังไม่จบ — รวมงานที่ถูกคืนกลับมาแก้ (Tester/dev-test ไม่ผ่าน) | view **WIP** |
| `stage: probe` | AI ทำเสร็จ รอ dev ทดสอบ | view **Probe** |
| `stage: gate` | dev ยืนยันว่าผ่านแล้ว รอ Jira/Tester หรือตรวจรับสุดท้าย | view **Gate** |
| `status: fin` | ปิดแล้ว — หายจากบอร์ดทันที (filter `status != "fin"`) รอ sweep เก็บ | ไม่แสดงบนบอร์ด |

### แต่ละเส้น transition ใครทำ ด้วยอะไร

| เปลี่ยน | ทริกเกอร์ | ผู้ทำ | เครื่องมือ |
|---|---|---|---|
| todo → preop / mise | รอข้อมูล / เตรียมพร้อม | dev | แก้ stage ในไฟล์หรือบอร์ด |
| preop → todo / mise | ได้ข้อมูลแล้ว แต่ยังต้องเตรียม / พร้อมเริ่ม | dev | แก้ stage ในไฟล์หรือบอร์ด |
| mise → wip | เริ่มทำงาน | AI | todo-next step 6 / dev ระบุไฟล์เอง |
| wip → probe | จบ session ที่งานเสร็จ | AI | ใน session / todo-parallel step 5 |
| probe → gate | dev ยืนยันว่าทดสอบผ่าน | dev หรือ AI ตามคำสั่ง | บอร์ด Probe หรือ `finish.py --pass` พร้อมบันทึกผลใน Progress |
| probe / gate → wip | dev test หรือ Tester ไม่ผ่าน | dev หรือ AI | แก้ stage ในบอร์ดหรือ `finish.py --revert` พร้อมเหตุผลใน `## Progress` |
| gate → fin | Jira Done (หรืองานไม่มี ticket และผู้ใช้ประกาศจบ) | dev หรือ script | `todo-finish --done` หรือแก้ cell ใน view Gate |
| fin → archive | เก็บกวาด | AI ตามคำสั่ง | todo-sweep — `git mv` ไป `todo/archive/YYYY-MM/` |

**ข้อควรระวังตอนปิดงานมือในบอร์ด:** ใส่คอลัมน์ `done` (วันที่) **ก่อน** เปลี่ยน `status: fin` —
row จะหายจากบอร์ดทันทีที่ status เป็น fin จาก filter ระดับบน ถ้าพลิกสลับลำดับจะตั้งวันที่ไม่ทัน
(ใช้ `todo-finish` แล้วจบในคำสั่งเดียว ไม่มีปัญหานี้)

**Jira:** transition ฝั่ง Jira (In progress → Test, Test → Done) เป็น manual ของ dev/Tester เสมอ —
`jira.md` เป็นแค่รายการอ่าน (JQL) และไฟล์งานไม่ mirror สถานะ Jira กลับเข้ามา (RULES ข้อ 1)

## 2. Scenario ของ 1 งาน (sequenceDiagram)

เส้นทางของ 1 งาน ครบทุกกิ่ง — loop dev test ไม่ผ่าน (7.2), Tester ไม่ผ่าน (8.1) และการปิดงาน 2 แบบ (8.2 / 8.3) ตัวเลขในวงเล็บ (n) กำกับขั้นตอนตาม flow ที่กำหนดไว้

```mermaid
sequenceDiagram
    autonumber
    actor Dev
    participant AI as AI session
    participant F as ไฟล์งาน .md
    participant G as Git
    participant J as Jira
    actor T as Tester

    Dev->>AI: (1) todo-init — ครั้งเดียวต่อโปรเจกต์ใหม่
    Dev->>AI: (2-3) รับ req ลูกค้า ลง inbox.md → todo-triage
    AI->>F: สร้างไฟล์งาน stage: todo
    alt (4) ข้อมูลพร้อม
        Dev->>F: เติมรายละเอียด — Related files / Skills ticks → stage: mise
    else (4.1) รอข้อมูลหรือผลทดสอบระยะสั้น
        Dev->>F: stage: preop — AI ยังไม่อ่านเนื้อหา
        Dev->>F: ได้ข้อมูลแล้ว เติมรายละเอียด → stage: mise
    end
    Dev->>AI: (5) todo-next หรือระบุไฟล์เอง
    AI->>F: (6) stage: mise → wip — เริ่มทำงาน
    opt (5.1) งานไม่เกี่ยวกัน 2-3 งาน
        Dev->>AI: todo-parallel — แยกเป็น subagents
    end
    AI->>F: (6) จบ session งานเสร็จ: append Progress + stage: probe — ยังไม่ commit
    opt ผู้ใช้สั่งสรุปก่อน–หลัง
        Dev->>AI: recap
        AI->>F: เพิ่มรายงานลงวันที่ใน Before / After ตามกฎ AGENTS
        AI-->>Dev: สรุปสั้นพร้อมลิงก์รายงาน
    end
    Dev->>F: (7) dev test
    loop (7.2) ไม่ผ่าน — แจ้ง AI ใน session นั้น แก้จนกว่าจะผ่าน
        Dev->>AI: ยังไม่ผ่าน — เพราะ ...
        AI->>F: stage: wip + append Progress เหตุผลไม่ผ่าน
        AI->>F: แก้เสร็จ → stage: probe
        Dev->>F: dev test ใหม่
    end
    Dev->>AI: dev test ผ่าน — ระบุงานที่ผ่านและงานที่ให้ commit
    AI->>F: todo-finish --pass: probe → gate + append Progress
    AI->>G: commit แยกเฉพาะงานที่ระบุ
    Dev->>J: (7.1) ผ่าน: In progress → Test — manual บน Jira, AI ช่วยไม่ได้
    T-->>Dev: ตรวจรับ: ผ่าน / ไม่ผ่าน
    alt (8.1) Tester ไม่ผ่าน
        Dev->>F: บอร์ด Gate: แก้ stage gate → wip
        Dev->>F: append Progress: Tester ไม่ผ่าน เพราะ xxx
        Note over F: ขึ้น view WIP — todo-next เจอและจัดอันดับให้ทำต่อ
    else (8.2 / 8.3) Tester ผ่าน
        Dev->>J: Jira → Done — manual ก่อนปิดไฟล์งาน
        opt (8.2) ปิดมือในบอร์ด
            Dev->>F: ใส่ done date ก่อน แล้ว status: fin — row หายทันที
        end
        opt (8.3) เรียก todo-finish
            Dev->>AI: ปิดงาน (todo-finish)
            AI->>F: status: fin + done: วันนี้
        end
        Dev->>AI: เก็บกวาด (todo-sweep)
        AI->>F: git mv → todo/archive/YYYY-MM/
    end
```

### อ่าน scenario ทีละช่วง

- **(1) ติดตั้ง:** todo-init ครั้งเดียวต่อโปรเจกต์ — สร้าง `todo/`, บอร์ด 7 views และกฎใน AGENTS.md
- **(2–4) รับและเตรียมงาน:** req ลง `inbox.md` → todo-triage สร้างไฟล์ `stage: todo` → dev เติม Related files / Skills ticks แล้วตั้ง `mise`; ถ้ารอข้อมูลระยะสั้น dev ตั้ง `preop` ก่อน AI ไม่อ่านเนื้อหาของ `todo`/`preop`
- **(5–6) เลือกและลงมือ:** todo-next เสนอเฉพาะ `mise`/`wip` หรือระบุไฟล์ที่พร้อมเอง → `mise → wip` — งานไม่เกี่ยวกัน 2–3 งานใช้ todo-parallel (5.1) ได้ → จบ session ที่งานเสร็จ AI append `## Progress` + `stage: probe` โดยยังไม่ commit
- **(7) dev test:** ไม่ผ่าน (7.2) → `stage: wip` พร้อมจดเหตุผลใน Progress แล้วแก้จนกลับ `probe`; ผ่านแล้ว dev เปลี่ยน `probe → gate` ในบอร์ดหรือสั่ง todo-finish --pass พร้อมบันทึก Progress แล้วระบุงานที่จะ commit โดยแยกหนึ่ง commit ต่องาน จากนั้นย้าย Jira เป็น Test **manual บน Jira — AI ช่วยไม่ได้**
- **(8.1) Tester ไม่ผ่าน:** dev แก้ stage เป็น wip ในบอร์ด (หรือ `finish.py --revert`) + **แนบเหตุผลลง `## Progress` เสมอ** — งานขึ้น view WIP แล้ว todo-next จัดอันดับให้ทำต่อ (วนกลับไปขั้นแก้งาน)
- **(8.2 / 8.3) Tester ผ่านและ Jira Done (หรืองานไม่มี ticket ผู้ใช้ประกาศจบ) — เลือกทางหนึ่ง:** ปิดมือในบอร์ด (8.2: ใส่ done date **ก่อน** status: fin เพราะ row หายทันที) หรือเรียก todo-finish (8.3: `status: fin` + done วันนี้ในคำสั่งเดียว)
- **(ปิดท้าย) เก็บกวาด:** todo-sweep ย้ายไฟล์ไป `todo/archive/YYYY-MM/` ตามเดือนของวันที่ done

เมื่อผู้ใช้สั่ง `recap` จะสรุปก่อน–หลังและบันทึกตามปลายทางที่ผู้ใช้กำหนดหรือกฎ AGENTS; ค่าเริ่มต้นของโปรเจกต์ todo ใหม่คือไฟล์งานนั้น รายงานไม่เปลี่ยน stage/status และ automated tests ผ่านไม่แทนคำยืนยัน dev test

## 3. Render ดูละเอียด (pretty-mermaid)

`.mmd` ใน `assets/` render เป็นไฟล์ใหญ่ดูได้ทุกขนาด:

```bash
node <skill-root ของ pretty-mermaid>/scripts/render.mjs \
  --input assets/todo-scenario-th.mmd \
  --output scenario.png --format png --width 2400 --theme github-light
```

GitHub และ Obsidian ก็ render บล็อก mermaid ในเอกสารนี้ให้เอง — เปิดไฟล์นี้ใน Obsidian ก็ดูได้เลย
