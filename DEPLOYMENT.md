# 🚀 Texas Adult Driver Education (ADE-1317) - Official Deployment Runbook

> **CRITICAL RULE FOR ALL DEVELOPERS & AI AGENTS**:  
> The official, authoritative production URL is **`https://tx-drive.vercel.app`**.  
> **DO NOT** deploy to `courseshell.vercel.app` or project `txdrive`. That is a deprecated legacy deployment target.

---

## 📋 Production Environment Targets

| Service | Target Project / Domain | Live Production URL | Source Code Directory |
| :--- | :--- | :--- | :--- |
| **Frontend Web App (Vercel)** | `dogbyte-dels-projects/tx-drive` | **`https://tx-drive.vercel.app`** | [`c:\tx_dmv\course_shell`](file:///c:/tx_dmv/course_shell) |
| **Virtual Classroom Player** | `tx-drive` | `https://tx-drive.vercel.app/player.html` | [`course_shell/player.html`](file:///c:/tx_dmv/course_shell/player.html) |
| **Student Identity Verification (PVQ)** | `tx-drive` (1-Page Checkpoint) | `https://tx-drive.vercel.app/final_course_export/L09-T01.html` | [`course_shell/final_course_export/L09-T01.html`](file:///c:/tx_dmv/course_shell/final_course_export/L09-T01.html) |
| **State Final Exam (30 MCQs)** | `tx-drive` (Untouched Exam) | `https://tx-drive.vercel.app/mcqs/final_exam.html` | [`course_shell/mcqs/final_exam.html`](file:///c:/tx_dmv/course_shell/mcqs/final_exam.html) |
| **Backend API (Cloud Run)** | `tx-ade-api` (`dmv-texas`) | `https://tx-ade-api-1004296326114.us-central1.run.app` | [`c:\tx_dmv\server`](file:///c:/tx_dmv/server) |

---

## 🛠️ Step-by-Step Frontend Deployment Process

### Prerequisites:
- Node.js & npm installed
- Logged into Vercel CLI (or team token active under `dogbyte-dels-projects`)
- PowerShell / Command prompt opened in Windows

### Command Sequence (Windows PowerShell):

```powershell
# 1. Navigate to the course_shell directory (the single source of truth for the web frontend)
cd c:\tx_dmv\course_shell

# 2. Ensure project is linked to 'tx-drive' (DO NOT link to 'txdrive')
npx --yes vercel link --project tx-drive --yes

# 3. Deploy directly to production
# Note: $env:VERCEL_NO_UPDATE_CHECK="1" prevents the CLI from freezing on interactive version update checks
$env:VERCEL_NO_UPDATE_CHECK="1"; npx --yes vercel --prod --yes
```

---

## 🔍 Post-Deployment Verification Checklist

After running the deployment command, immediately verify each live URL:

1. **Verify Classroom Player**:
   ```powershell
   curl -I https://tx-drive.vercel.app/player.html
   ```
   *Expected*: HTTP `200 OK`.

2. **Verify Module 9 Identity Verification (PVQ)**:
   ```powershell
   curl -s https://tx-drive.vercel.app/final_course_export/L09-T01.html | Select-String "Student Identity Verification Checkpoint"
   ```
   *Expected*: Returns matching title with 15 questions bank and 5 slots on 1 page.

3. **Verify State Final Exam (Untouched)**:
   ```powershell
   curl -I https://tx-drive.vercel.app/mcqs/final_exam.html
   ```
   *Expected*: HTTP `200 OK`. Exam contains 30 questions without any injected question 0 or question 1 duplicates.

---

## ⚠️ Key Architecture Constraints & Gotchas

1. **Vercel Project Name Ambiguity**:
   - The team `dogbyte-dels-projects` contains **two** similarly named projects:
     - `txdrive` ❌ -> Maps to `courseshell.vercel.app` (Deprecated)
     - `tx-drive` ✅ -> Maps to `https://tx-drive.vercel.app` (Live Production)
   - Ensure [`course_shell/vercel.json`](file:///c:/tx_dmv/course_shell/vercel.json) has:
     ```json
     {
       "name": "tx-drive",
       "version": 2,
       "cleanUrls": true,
       ...
     }
     ```

2. **CLI Freezing / Hanging**:
   - Vercel CLI often prompts `Update available X -> Y. Run npm i -g vercel to update` which hangs non-interactive agent shells on Windows.
   - Always run with `$env:VERCEL_NO_UPDATE_CHECK="1"` to bypass this check.

3. **Student Experience & TDLR Rules**:
   - **NO In-Lesson Popups**: Never introduce popups, modals, or timed ambush dialogs while students are reading topics.
   - **Personal Verification Questions (PVQ)**: Must remain in **Module 9, Topic 1** (`L09-T01`), presenting 5 question slots on **one single page**, selectable from the 15-question bank.
   - **Untouched Final Exam**: Never prepend questions to [`course_shell/mcqs/final_exam.html`](file:///c:/tx_dmv/course_shell/mcqs/final_exam.html). It must remain strictly 30 DPS questions.

---

## ⚙️ Backend API Deployment (Google Cloud Run)

If server routes or backend tables are updated:

```powershell
$env:CLOUDSDK_PYTHON = "C:\Users\lokes\AppData\Local\Programs\Python\Python310\python.exe"
& "c:\tx_dmv\google-cloud-sdk\bin\gcloud.cmd" run deploy tx-ade-api `
  --source c:\tx_dmv\server `
  --region us-central1 `
  --allow-unauthenticated `
  --project dmv-texas `
  --quiet
```
Live Backend URL: `https://tx-ade-api-1004296326114.us-central1.run.app`
