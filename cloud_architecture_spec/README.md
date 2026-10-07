# TX-ADE Cloud Architecture & Engineering Blueprint
## Texas Adult Driver Education (TDLR Course ADE-1317)
**Scale:** Phase 1 Target: 10,000 Enrolled Students  
**Compliance Standard:** 16 Texas Administrative Code § 84.500 & TTC § 521.1601  

---

## 📌 Purpose of this Documentation Suite

This folder contains the complete, production-grade architecture blueprints for autonomous AI coding agents and lead software engineers. It eliminates hallucinations by providing exact data models, cryptographic protocols, endpoint contracts, edge routing rules, and deployment instructions.

---

## 📚 Specification Directory

| Document | Primary Focus | Key Engineering Content |
|:---|:---|:---|
| [**`01_SYSTEM_ARCHITECTURE_OVERVIEW.md`**](file:///C:/tx_dmv/cloud_architecture_spec/01_SYSTEM_ARCHITECTURE_OVERVIEW.md) | End-to-End System Design | Zero-trust topology, Cloudflare edge compute + R2 + D1 + Google Identity flow, lifecycle stages. |
| [**`02_AUTH_AND_SECURITY_SPEC.md`**](file:///C:/tx_dmv/cloud_architecture_spec/02_AUTH_AND_SECURITY_SPEC.md) | Google Sign-In & Content Gating | Token exchange, session cookies, course locking rules, ephemeral single-use lesson tickets, direct URL prevention (`403 Forbidden`). |
| [**`03_DATABASE_SCHEMA_AND_MODELS.md`**](file:///C:/tx_dmv/cloud_architecture_spec/03_DATABASE_SCHEMA_AND_MODELS.md) | Production SQL Schema | 9 relational tables: `users`, `enrollments`, `pvq_answers`, `pvq_challenges`, `topic_progress`, `module_progress`, `quiz_attempts`, `instructional_time_logs`, `certificates`. |
| [**`04_SECURE_CONTENT_DELIVERY_PIPELINE.md`**](file:///C:/tx_dmv/cloud_architecture_spec/04_SECURE_CONTENT_DELIVERY_PIPELINE.md) | Private R2 Storage & Streaming | Zero-public-access R2 bucket layout, S3 sync script, `HTMLRewriter` DOM streaming, frame-ancestor CSP lockdown. |
| [**`05_COMPLIANCE_AND_CERTIFICATION_ENGINE.md`**](file:///C:/tx_dmv/cloud_architecture_spec/05_COMPLIANCE_AND_CERTIFICATION_ENGINE.md) | TDLR 16 TAC § 84.500 Compliance | Server-side 6-hour timer validation, 5-minute idle pause, 90-second PVQ challenge engine, 70% passing gates, Form ADE-1317 PDF generator. |
| [**`06_API_SPECIFICATION.md`**](file:///C:/tx_dmv/cloud_architecture_spec/06_API_SPECIFICATION.md) | REST API Contract & Schemas | Full JSON request/response definitions for Auth, PVQ, Billing, Progress, Heartbeats, Quizzes, and Verification. |
| [**`07_PHASE_1_10K_USERS_DEPLOYMENT_PLAYBOOK.md`**](file:///C:/tx_dmv/cloud_architecture_spec/07_PHASE_1_10K_USERS_DEPLOYMENT_PLAYBOOK.md) | Cloudflare Provisioning & Scaling | Secrets checklist, Wrangler CLI commands, D1 migrations, R2 bucket creation, Stripe webhooks, cost breakdown (<$30/mo for 10k users). |

---

## 🔒 Core Invariant: How Direct URL Access is Blocked

When an unauthenticated or unauthorized visitor enters:
```
https://www.ourdomain.com/lesson/t1l1
https://www.ourdomain.com/lesson/L01-T01
https://www.ourdomain.com/final_course_export/L01-T01.html
```

1. **Obfuscation Trap:** All internal folders (`/final_course_export/*`, `/rebuilds/*`) return **404 Not Found** at the edge worker level.
2. **Authentication Gate:** Requests to `/lesson/*` require a valid `tx_session` cookie. If missing, student is redirected to `/login.html`.
3. **Enrollment Check:** If student is signed in but unpaid, student is redirected to `/checkout.html`.
4. **Curriculum Prerequisite Check:** If student attempts to access Topic $N$ while Topic $N-1$ is incomplete, the API returns **403 Forbidden** (`TOPIC_LOCKED`).
5. **Private R2 Storage:** Raw HTML files have **zero public HTTP endpoints**. Content can only be read via the worker's internal binding `env.CURRICULUM_R2.get()`.
