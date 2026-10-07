# TX-ADE Course Shell (Clean Standalone Delivery)

This directory contains the self-contained, production-ready **Texas Adult Driver Education (TX-ADE)** Course Shell, curriculum lessons, modular assessments, and secure server-side grading engine.

---

## How to Run

### Option 1: 1-Click Launch (Windows)
Double-click `run.bat` (or `start.bat`).  
This starts the local grading server on port 8080 and automatically opens `http://localhost:8080/index.html` in your default browser.

### Option 2: Command Line
```powershell
cd C:\tx_dmv\course_shell
python serve.py
```

### Option 3: Direct Browser Launch
Open `index.html` directly in any modern web browser.

---

## Folder Structure

```
course_shell/
├── index.html              # Main Course Shell (TDLR 6-Hour Timer, Sidebar, Assessments)
├── course-shell.html       # Direct mirror/alias to index.html
├── run.bat                 # 1-Click Windows launcher
├── start.bat               # Launcher alias
├── serve.py                # Zero-dependency Python HTTP server & REST Grading API
├── final_exam_engine.py    # TDLR 16 TAC §84.503 Final Exam Generator (Bank A & Bank B)
├── README.md               # Quick start documentation
├── final_course_export/    # 75 Complete curriculum lessons & visual assets
│   ├── L01-T01.html ... L09-T01.html  (All 75 TDLR curriculum topics)
│   └── assets/
│       └── 2_5d/           (44 architectural 2.5D diorama previews)
└── mcqs/                   # Decoupled assessment suite & zero-leak question banks
    ├── L01-T01.html ... L09-T01.html  (75 Topic knowledge checks, 5 Qs each)
    ├── final_exam.html     # 30-Question TDLR Final Exam (15 Signs + 15 Laws)
    ├── master_answer_keys.json # Private server-side key repository (not sent to browser)
    └── modular_mcqs/       # Standalone question modules (375 questions)
        ├── questions/      # L01-T01_Q1.json ... L09-T01_Q5.json (Zero keys in JSON)
        ├── server_keys/    # Private answer keys for backend grading
        ├── first_question_shell.html # Master Shell for Question 1
        └── question_shell_template.html
```

---

## Pedagogical & Assessment Workflow

1. **Lesson Exploration**:
   The student studies the current curriculum unit loaded in the main frame (`./final_course_export/${id}.html`). The outer course shell continuously tracks active instructional minutes towards the mandatory 6 clock hours (360 minutes).
2. **"TAKE A TEST ON THIS TOPIC"**:
   Upon reviewing the lesson, the student clicks the primary orange button in the bottom navigation bar:
   `TAKE A TEST ON THIS TOPIC` (or `TAKE FINAL EXAM (30 QUESTIONS)` on Module 09).
3. **Mastery Gate Modal**:
   A focused modal opens with the 5 topic questions (or 30 exam questions).
4. **Zero Front-End Leakage & Server-Side Evaluation**:
   Options are selected and evaluated by the server via `POST /api/v1/lessons/:topicId/grade`.
   No plain-text answers or hashes exist in the front-end DOM or JavaScript.
5. **Topic Completion & Progression**:
   Upon scoring mastery (≥ 70%), the student receives an instant verification toast, the topic is marked completed in the sidebar with a green `[PASSED]` badge, and the footer transitions to `NEXT TOPIC`.

---

## State Compliance Standards

- **TDLR 16 TAC § 84.500**: Active instructional timer with 5-minute inactivity idle detection and window blur pause.
- **TDLR 16 TAC § 84.503**: Final examination of 30 questions drawn equally from Bank A (15 Highway Signs) and Bank B (15 Traffic Laws), requiring a 70.0% passing threshold (21 of 30).
- **September 1, 2026 Mandate (HB 1884)**: Dedicated coverage and questions on highway construction and maintenance work zones (TTC § 472.022, § 542.404, § 545.157).
