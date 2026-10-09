# 🧭 TEXAS ADULT DRIVER EDUCATION (ADE-1317)
### Master Repository Blueprint & AI Agent Guide

> **🚨 CRITICAL NOTICE FOR ALL AI AGENTS & CONTRIBUTORS 🚨**  
> This repository contains multiple historical folders and generation artifacts from earlier project iterations.  
> **DO NOT** edit, reference, or read legacy experiments. Always adhere strictly to the **ACTIVE SOURCE OF TRUTH** mapped below.

---

## 🎯 ACTIVE SOURCE OF TRUTH (ONLY TOUCH THESE 3 FOLDERS)

| Component | Active Folder | Production Target & Tech Stack |
| :--- | :--- | :--- |
| **🌐 Web Application** | [`course_shell/`](file:///c:/tx_dmv/course_shell) | **Live on Vercel**: [`https://courseshell.vercel.app`](https://courseshell.vercel.app)<br>• 3D Cyber Hero Landing Page (`index.html`)<br>• TDLR Virtual Classroom Player (`player.html`)<br>• 9 Modules & 75 Completed Topics (`final_course_export/`)<br>• Modular Quizzes & Answer Keys (`mcqs/`)<br>• Cloud Sync Bridge (`cloud_sync.js`) |
| **⚙️ Backend API** | [`server/`](file:///c:/tx_dmv/server) | **Live on Google Cloud Run**: [`https://tx-ade-api-1004296326114.us-central1.run.app`](https://tx-ade-api-1004296326114.us-central1.run.app)<br>• Express.js + PostgreSQL (Cloud SQL) + Redis<br>• Google OAuth 2.0 (`/api/v1/auth/google`)<br>• 100% Promo Code Engine (`/api/v1/billing/validate-coupon`)<br>• Statutory 30s Heartbeats & Telemetry (`/api/v1/student/heartbeat`) |
| **📱 Mobile Application** | [`tx_adult_driver_ed_flutter/`](file:///c:/tx_dmv/tx_adult_driver_ed_flutter) | **Cross-Platform Flutter (iOS / Android / Mobile Web)**<br>• Phone-optimized single-column ergonomics & touch targets<br>• Responsive Syllabus Drawer (`CurriculumDrawer`)<br>• Sticky Statutory Timer (16 TAC § 84.500)<br>• 90-Second PVQ Identity Challenge Sheet |

---

## ⛔ INACTIVE / LEGACY FOLDERS (DO NOT TOUCH OR MODIFY)

The following folders are preserved for historical audit only and must be **IGNORED** by AI agents:
- `course-player-app/` *(Old Vite/React prototype — DEPRECATED)*
- `frontend/` *(Old Next.js/React scratch workspace — DEPRECATED)*
- `stripe-backend/` *(Old scratch backend — Superceded by `server/`)*
- `interactive_course_build/`, `stitch_downloads/`, `stitch_exports/` *(Stitch asset scratch files)*
- `gaps/`, `rebuilds/`, `New folder/`, `db/` *(Temporary data dumps)*
- Loose root Python scripts (`audit.py`, `build_*.py`, `clean*.py`, `check_*.py`, etc.) *(Legacy batch generators)*

---

## 📜 CORE STATUTORY & COMPLIANCE RULES

1. **Course Identification**:
   - Course Approval Code: **ADE-1317**
   - TDLR Driver Training School License: **#C3284**
   - Statutory Authority: **Texas Administrative Code (16 TAC § 84.500)**
2. **Statutory Time & Curriculum**:
   - Total Course Duration: **6 Hours (360 Clock Minutes)** across **9 Modules & 75 Topics**.
   - Topic Timers: Mandatory countdown before advancement is permitted.
   - Heartbeats: Client sends active telemetry every 30 seconds to Cloud Run.
3. **Student Identity & PVQ**:
   - Mandatory Google Sign-In registration required before instruction begins.
   - Personal Verification Questions (PVQ) challenge must be answered within **90 seconds**.
4. **Pricing & Access Control**:
   - **Module 1**: Free preview for unpaid registered students.
   - **Modules 2–9**: Locked unless enrolled or 100% OFF code is redeemed.
   - **Admin 100% OFF Code**: **`TEXAS100`** *(also accepts `FREE100`, `TEXASVIP`, `TDLRADMIN`)*.

---

## 🚀 QUICK DEPLOYMENT REFERENCE

### 1. Web Frontend (Vercel)
```bash
cd c:\tx_dmv\course_shell
npx vercel --prod --yes
```
- Live Domain: `https://courseshell.vercel.app`
- Direct Classroom: `https://courseshell.vercel.app/player.html`

### 2. Cloud Run Backend (Google Cloud)
```bash
$env:CLOUDSDK_PYTHON = "C:\Users\lokes\AppData\Local\Programs\Python\Python310\python.exe"
& "c:\tx_dmv\google-cloud-sdk\bin\gcloud.cmd" run deploy tx-ade-api `
  --source c:\tx_dmv\server `
  --region us-central1 `
  --allow-unauthenticated `
  --project dmv-texas `
  --quiet
```

### 3. Flutter Mobile App
```bash
cd c:\tx_dmv\tx_adult_driver_ed_flutter
flutter pub get
flutter run
```

---

## 📌 GIT & REPOSITORY SYNC
- **GitHub**: [`https://github.com/lokeshpolkam/tx-adult-driver-ed`](https://github.com/lokeshpolkam/tx-adult-driver-ed)
- **Branch**: `main`
