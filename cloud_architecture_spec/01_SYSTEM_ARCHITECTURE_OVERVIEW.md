# TX-ADE Cloud Infrastructure & Production Architecture Specification
## Target Scale: Phase 1 — 10,000 Enrolled Students
**Regulatory Compliance:** Texas Department of Licensing & Regulation (TDLR) 16 TAC § 84.500 / TTC § 521.1601  
**Author:** Principal Cloud Architect & Security Engineer  
**Purpose:** Implementation Blueprint for Autonomous LLM & Engineering Teams  

---

## 1. System Vision & Zero-Trust Core Principle

The Texas Adult Driver Education (TX-ADE) platform is an edge-native, zero-trust learning management system (LMS) designed to serve 10,000+ active adult learners seeking their Texas Driver License (TDLR ADE-1317 Course). 

### The Core Security Invariant: Private Gated Content
Under no circumstances can raw course materials be exposed as public static files.
- If an unauthorized user or unauthenticated visitor navigates directly to `https://learn.texasade.org/lesson/L01-T01` or `https://learn.texasade.org/final_course_export/L01-T01.html`, they **MUST RECEIVE AN IMMEDIATE `403 FORBIDDEN` or `401 UNAUTHORIZED`**.
- Content files (75 HTML lessons + 44 2.5D visual assets + 76 interactive quizzes) reside in **100% Private Cloud Storage (Cloudflare R2 or GCP Private Bucket)**.
- Every byte of course HTML is served exclusively through an **Edge Authorization Proxy Worker**. The worker cryptographically validates:
  1. Active Google Sign-In JWT token.
  2. Verified Stripe payment/enrollment record.
  3. Strict sequential curriculum unlocking (student cannot skip ahead to topic $N$ without completing topic $N-1$).
  4. Server-verified TDLR instructional time requirement.

---

## 2. High-Level System Architecture Diagram

```mermaid
flowchart TD
    subgraph ClientLayer ["1. Client Tier (Browser)"]
        A["Student Browser (Desktop/Mobile)"]
        B["Course Shell (Parent Frame)"]
        C["Secure Lesson Iframe (Child Frame)"]
        A --> B
        B -->|Embeds & Sandbox Controls| C
    end

    subgraph EdgeRouting ["2. Cloudflare Edge Network (Global CDN / DNS)"]
        D["Cloudflare Pages: app.texasade.org (Static Shell, Auth, Dashboard)"]
        E["Cloudflare Edge Worker: api.texasade.org (API Gateway & Content Proxy)"]
    end

    subgraph AuthTier ["3. Identity & Payment Layer"]
        F["Google Identity Services (OAuth 2.0 / Firebase Auth)"]
        G["Stripe Billing Engine ($38 Course + $9.99 Express Upsell)"]
    end

    subgraph DataStorage ["4. Storage & Persistence Tier"]
        H[("Cloudflare D1 / Cloud SQL PostgreSQL (Primary Database)")]
        I[("Cloudflare KV / Redis (High-Speed Session & Heartbeat Cache)")]
        J["Private R2 Bucket: tx-dmv-private-lessons (75 Lessons, Quizzes, Dioramas)"]
    end

    subgraph ComplianceWorker ["5. TDLR Compliance & Certificate Engine"]
        K["PVQ Challenge Engine (Personal Validation Questions)"]
        L["Server-Side Instructional Timer (6-Hour Enforcer)"]
        M["ADE-1317 PDF Certificate Generator & Serial Issuer"]
    end

    %% Client Interactions
    A -->|1. Sign in with Google| F
    F -->|2. Returns ID Token / JWT| A
    A -->|3. Stripe Checkout| G
    G -->|4. Webhook: checkout.session.completed| E
    
    %% Shell and API Interactions
    B -->|5. Authenticated RPC & Heartbeat (JWT)| E
    C -->|6. GET /api/v1/lessons/:topicId (Bearer JWT)| E

    %% Edge Verification Pipeline
    E -->|Verify Token & Expiry| F
    E -->|Check Enrollment & Topic Lock State| H
    E -->|Read Active Heartbeat Cache| I
    E -->|Fetch Private Content & Stream to Iframe| J

    %% Compliance Pipelines
    E --> K
    E --> L
    E --> M
```

---

## 3. Technology Stack Selection (Built for Scale & Low Latency)

| Component | Selected Technology | Technical Justification |
|:---|:---|:---|
| **Identity / Auth** | **Firebase Auth / Google OAuth 2.0** | 1-click Google Sign-In, instant mobile login, battle-tested JWT issuance, zero credential storage liability. |
| **Edge API & Gatekeeper** | **Cloudflare Workers (TypeScript)** | Sub-15ms cold start, runs across 300+ edge locations, built-in edge cache, natively streams private R2 assets. |
| **Static Shell Frontend** | **Cloudflare Pages (`tx-dmv-theme`)** | Global distribution, automatic SSL, existing wrangler project `d96f5a789a0cde34666a220708d38f53`. |
| **Private Content Store** | **Cloudflare R2 (`tx-dmv-private-curriculum`)** | Zero egress fees, seamless S3 API compatibility, 100% private bucket (no public URL). |
| **Primary Relational DB** | **Cloudflare D1 (or Supabase / Cloud SQL)** | Serverless SQL, edge replicas, supports 10,000+ active records with zero provisioning, sub-10ms queries. |
| **Fast Session / Timer Cache** | **Cloudflare Workers KV** | Key-value store with sub-5ms read speeds for real-time 30-second instructional heartbeat validation. |
| **Payment Gateway** | **Stripe Checkout & Webhooks** | Already structured in `C:\tx_dmv\stripe-backend`, handles $38 base + $9.99 certificate upsell with PCI compliance. |
| **Certificate Engine** | **Cloudflare Worker PDF / Node.js Puppeteer** | Generates tamper-proof TDLR Form ADE-1317 PDFs with SHA-256 verification QR codes. |

---

## 4. End-to-End User Journey (The 5 Lifecycle Stages)

### Stage 1: Landing & Frictionless Google Sign-In
1. Student lands on `https://texasade.org`.
2. Student clicks **"Sign In with Google"** (Google One-Tap or button).
3. Client receives Google OAuth ID token, calls `POST /api/v1/auth/google`.
4. Server validates token with Google token info endpoint, checks user table in DB:
   - If new user: Inserts into `users` table with `status = "PENDING_ENROLLMENT"`.
   - If existing user: Returns student session JWT and profile payload.

### Stage 2: Enrollment & Stripe Payment Gate
1. Student views Course Overview & Checkout page ($38.00 TDLR Approved Adult Driver Ed).
2. Student initiates checkout -> Server calls `stripe.checkout.sessions.create()`.
3. Student completes checkout on Stripe hosted page.
4. Stripe fires webhook `checkout.session.completed` to `https://api.texasade.org/api/v1/webhooks/stripe`.
5. Webhook verifies signature `stripe.webhooks.constructEvent()`, queries DB:
   - Updates `enrollments` status to `ACTIVE`.
   - Records `paid_at`, `amount_cents = 3800`, `stripe_session_id`.
   - Initializes `topic_progress` table with `L01-T01` unlocked; all other 74 topics locked.
   - Prompts student to answer **5 Mandatory Personal Validation Questions (PVQs)** required by Texas law before starting Lesson 1.

### Stage 3: Secure Course Shell & Gated Lesson Delivery
1. Student accesses `https://app.texasade.org/course-shell.html`.
2. Parent shell requests student telemetry: `GET /api/v1/student/progress`.
   - Returns: completed topics, unlocked topic ID, elapsed instructional time, overall percentage.
3. Shell loads the active unlocked lesson into the iframe:
   ```html
   <iframe src="https://api.texasade.org/api/v1/lessons/L01-T01?token=JWT_EPHEMERAL_NONCE"></iframe>
   ```
4. **Edge Worker Verification**:
   - Parses the ephemeral signed token.
   - Verifies user is enrolled and `L01-T01` is marked `UNLOCKED`.
   - Pulls `L01-T01.html` from private R2 bucket.
   - Injects security headers (`X-Frame-Options: SAMEORIGIN`, `Content-Security-Policy: frame-ancestors 'self' https://app.texasade.org`).
   - Streams HTML payload to browser.

### Stage 4: TDLR Active Instructional Time & PVQ Verification
1. Every 30 seconds of active reading/interaction in the lesson, client sends:
   `POST /api/v1/student/heartbeat` with `{ activeTopicId, deltaSeconds: 30, interactionHash }`.
2. Server validates that the heartbeat interval is realistic ($\le 35$ seconds since last ping) and user is not idle.
3. Server increments `instructional_seconds` in database.
4. **Random PVQ Intercept**:
   - TDLR mandates periodic identity checks.
   - Server checks if a PVQ challenge is due (every 45-60 min or module boundary).
   - Server responds with `{ pvqRequired: true, questionId: "pvq_3", prompt: "What is your father's middle name?" }`.
   - The shell freezes the lesson iframe and presents a 90-second countdown modal.
   - Student submits answer -> Server verifies against bcrypt hash in DB.
   - Correct: Unfreezes lesson. Incorrect (after 3 attempts): Temporarily locks account for instructor verification per TDLR regulations.

### Stage 5: Module Quizzes, Final Exam & ADE-1317 Certification
1. At the conclusion of Module 1 (`L01-T03`), student is presented with the **Module 01 Quiz** (10 questions).
2. Submits answers to `POST /api/v1/quizzes/submit`.
3. Server evaluates answers securely (correct answers are NEVER sent to the client).
4. Score $\ge 70\%$: Unlocks Module 2 (`L02-T01`).
   Score $< 70\%$: Student must review module topics and retake the quiz.
5. After Module 8, student completes `L09-T01` (Official DPS Knowledge Test Simulator, 30 questions).
6. Upon passing with $\ge 70\%$ AND accumulating $\ge 21,600$ verified instructional seconds (6 full clock hours):
   - Server updates course status to `COMPLETED`.
   - Generates official **TDLR Form ADE-1317 Certificate** with a unique sequential serial number.
   - Saves certificate PDF in private R2 storage.
   - Student receives instant PDF download and automated verification email.
