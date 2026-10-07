# REST API Reference & Endpoint Contract Specification
## Zero-Ambiguity API Schemas for Frontend, Workers & Mobile Clients
**Document Reference:** `cloud_architecture_spec/06_API_SPECIFICATION.md`  
**Base URL:** `https://api.texasade.org/api/v1`  
**Authentication Scheme:** `Cookie: tx_session=<JWT>` OR `Authorization: Bearer <JWT>`  

---

## 1. Authentication & Onboarding Endpoints

### 1.1 `POST /auth/google`
Exchanges a signed Google Identity Services ID Token for an internal session cookie.

- **Request Body (`application/json`):**
```json
{
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ij... [Google JWT]"
}
```

- **Response (200 OK):**
```json
{
  "success": true,
  "user": {
    "id": "usr_9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "email": "student@example.com",
    "full_name": "Lokesh Polkaml",
    "enrollment_status": "ACTIVE",
    "profile_image": "https://lh3.googleusercontent.com/a/..."
  }
}
```
- **Response Headers:**
  `Set-Cookie: tx_session=eyJhb...; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=604800`

---

### 1.2 `POST /onboarding/pvq`
Saves the student's 5 personal validation answers during initial profile creation.

- **Request Body (`application/json`):**
```json
{
  "answers": [
    { "question_key": "mother_maiden_name", "answer": "Harrison" },
    { "question_key": "first_pet", "answer": "Buster" },
    { "question_key": "childhood_street", "answer": "Oakridge Drive" },
    { "question_key": "birth_city", "answer": "Austin" },
    { "question_key": "high_school_mascot", "answer": "Tigers" }
  ]
}
```

- **Response (200 OK):**
```json
{
  "success": true,
  "message": "Personal Validation Questions recorded and hashed successfully."
}
```

---

## 2. Billing & Stripe Webhook Endpoints

### 2.1 `POST /billing/create-checkout-session`
Initializes a Stripe Hosted Checkout Session for the state-approved course.

- **Request Body (`application/json`):**
```json
{
  "tier": "STANDARD",
  "client_origin": "https://app.texasade.org"
}
```
*(Optionally `"tier": "EXPRESS"` to include $9.99 same-day certificate delivery)*

- **Response (200 OK):**
```json
{
  "success": true,
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_live_a1b2c3d4..."
}
```

---

### 2.2 `POST /webhooks/stripe`
Receives asynchronous payment settlement webhooks from Stripe.

- **Headers Required:** `stripe-signature: t=1728250000,v1=...`
- **Handled Events:** `checkout.session.completed`
- **Internal Action:**
  - Verifies signature using `STRIPE_WEBHOOK_SECRET`.
  - Sets `enrollments.status = 'ACTIVE'`.
  - Unlocks first topic `L01-T01` in `topic_progress`.

---

## 3. Curriculum Access & Gated Content Endpoints

### 3.1 `GET /student/progress`
Returns the comprehensive course progress telemetry for the Course Shell.

- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "student_name": "Lokesh Polkaml",
    "enrollment_status": "ACTIVE",
    "completed_topics": [
      "L01-T01",
      "L01-T02",
      "L01-T03"
    ],
    "unlocked_topic_id": "L02-T01",
    "completed_topics_count": 3,
    "total_topics": 75,
    "progress_percentage": 4.0,
    "instructional_seconds": 3840,
    "required_seconds": 21600,
    "is_course_completed": false,
    "certificate_serial": null
  }
}
```

---

### 3.2 `POST /lessons/:topicId/ticket`
Generates a short-lived (60-second) cryptographically signed ticket allowing the child iframe to load a single lesson.

- **URL Parameter:** `topicId` (e.g., `L01-T01`)
- **Authorization:** Session Cookie required.

- **Response (200 OK):**
```json
{
  "success": true,
  "topicId": "L01-T01",
  "ticket": "usr_123:L01-T01:nonce_8f4b2a:1728250060.7d8a9f3b2c1e4...",
  "stream_url": "https://api.texasade.org/api/v1/lessons/L01-T01?ticket=usr_123:L01-T01:nonce_8f4b2a:1728250060.7d8a9f3b2c1e4..."
}
```

- **Error Response (403 Forbidden - Topic Locked):**
```json
{
  "success": false,
  "error": "TOPIC_LOCKED",
  "message": "Topic L02-T03 is locked. Complete Topic L02-T02 first."
}
```

---

### 3.3 `GET /lessons/:topicId`
Streams the raw HTML curriculum payload from private R2 storage into the iframe.

- **Query Parameters:** `?ticket=<signed_ticket_string>`
- **Response Headers:**
  - `Content-Type: text/html; charset=utf-8`
  - `X-Frame-Options: SAMEORIGIN`
  - `Content-Security-Policy: frame-ancestors 'self' https://app.texasade.org;`
  - `Cache-Control: private, no-store, max-age=0`

---

### 3.4 `POST /student/heartbeat`
Transmits active 30-second instructional telemetry to the server-side timer engine.

- **Request Body (`application/json`):**
```json
{
  "topicId": "L01-T01",
  "deltaSeconds": 30
}
```

- **Response (200 OK):**
```json
{
  "success": true,
  "totalInstructionalSeconds": 1420,
  "remainingSeconds": 20180,
  "pvqDue": false
}
```

---

### 3.5 `POST /lessons/:topicId/complete`
Marks a topic as completed after verifying instructional duration and formative quiz completion.

- **Request Body (`application/json`):**
```json
{
  "topicId": "L01-T01"
}
```

- **Response (200 OK):**
```json
{
  "success": true,
  "completedTopicId": "L01-T01",
  "nextUnlockedTopicId": "L01-T02",
  "overallProgress": {
    "completedCount": 1,
    "percent": 1.3
  }
}
```

---

## 4. Assessment & Quiz Endpoints

### 4.1 `GET /quizzes/:moduleId`
Retrieves assessment questions for a module (sanitized; correct answer indices stripped).

- **URL Parameter:** `moduleId` (1 through 9)
- **Response (200 OK):**
```json
{
  "moduleId": 1,
  "title": "Module 01 Knowledge Assessment",
  "passThresholdPercent": 70.0,
  "questions": [
    {
      "id": "q1",
      "prompt": "What is the primary statutory purpose of Texas Adult Driver Education under TTC § 521.1601?",
      "options": [
        { "key": "A", "text": "To replace on-road practice entirely" },
        { "key": "B", "text": "To establish core statutory and safety competencies" },
        { "key": "C", "text": "To issue commercial driver endorsements" },
        { "key": "D", "text": "To bypass the DPS vision screening" }
      ]
    }
  ]
}
```

---

### 4.2 `POST /quizzes/submit`
Submits student answers for evaluation against the secure server-side answer key.

- **Request Body (`application/json`):**
```json
{
  "moduleId": 1,
  "answers": {
    "q1": "B",
    "q2": "C",
    "q3": "A"
  }
}
```

- **Response (200 OK - Passed):**
```json
{
  "success": true,
  "scorePercent": 80.0,
  "correctCount": 8,
  "totalQuestions": 10,
  "passed": true,
  "nextUnlockedTopicId": "L02-T01",
  "message": "Congratulations! You passed the Module 01 Assessment."
}
```

- **Response (200 OK - Failed):**
```json
{
  "success": true,
  "scorePercent": 60.0,
  "correctCount": 6,
  "totalQuestions": 10,
  "passed": false,
  "nextUnlockedTopicId": null,
  "message": "You scored 60%. State regulations require >= 70% to proceed. Please review the module and retake."
}
```

---

## 5. Certification & Public Verification Endpoints

### 5.1 `GET /certificates/me`
Retrieves issued certificate metadata and signed download URL.

- **Response (200 OK):**
```json
{
  "success": true,
  "certificate": {
    "serialNumber": "ADE1317-2026-00042",
    "studentName": "Lokesh Polkaml",
    "completionDate": "2026-10-06",
    "totalClockHours": 6.05,
    "finalExamScore": 86.7,
    "downloadUrl": "https://api.texasade.org/api/v1/certificates/ADE1317-2026-00042/download",
    "verificationUrl": "https://verify.texasade.org/cert/ADE1317-2026-00042"
  }
}
```

---

### 5.2 `GET /public/verify/:serialNumber`
Public, unauthenticated verification endpoint utilized by Texas DPS agents.

- **URL Parameter:** `serialNumber` (e.g., `ADE1317-2026-00042`)
- **Response (200 OK):**
```json
{
  "valid": true,
  "serialNumber": "ADE1317-2026-00042",
  "studentLegalName": "Lokesh Polkaml",
  "schoolLicense": "TDLR School #C3284",
  "completionDate": "2026-10-06",
  "status": "OFFICIALLY_RECORDED_AND_VALID"
}
```
