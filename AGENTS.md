# AGENT & DEVELOPER INSTRUCTIONS (TX-DMV ADE-1317)

## 🚨 MANDATORY DEPLOYMENT PROCESS & RULES

### 1. Authoritative Production Target
- **Live URL**: **`https://tx-drive.vercel.app`**
- **Vercel Project**: `dogbyte-dels-projects/tx-drive`
- **DO NOT** deploy to `courseshell.vercel.app` or project `txdrive`. Those are legacy targets.

### 2. Exact Deployment Command (Windows PowerShell)
Always deploy from `c:\tx_dmv\course_shell`:
```powershell
cd c:\tx_dmv\course_shell
npx --yes vercel link --project tx-drive --yes
$env:VERCEL_NO_UPDATE_CHECK="1"; npx --yes vercel --prod --yes
```
*Note*: Always set `$env:VERCEL_NO_UPDATE_CHECK="1"` to prevent non-interactive agent shells from freezing on CLI update prompts.

### 3. Student Experience & Anti-Distraction Constraints
- **NO IN-LESSON POPUPS**: Never add popup modals or timed challenge interruptions while students are reading course slides.
- **PVQ Checkpoint**: Located strictly in **Module 9, Topic 1** (`L09-T01.html`).
  - All 5 questions must be rendered on **1 single page** (no pagination or wizards).
  - Students choose their 5 questions from the bank of 15 easy questions.
- **Untouched Final Exam**: Located in **Module 9, Topic 2** (`course_shell/mcqs/final_exam.html`).
  - Contains strictly the 30 state exam questions. Never prepend personal questions to the exam.
