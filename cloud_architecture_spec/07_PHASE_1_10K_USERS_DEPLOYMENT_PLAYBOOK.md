# Phase 1: 10,000 Students Production Deployment Playbook
## Step-by-Step Implementation & Infrastructure Provisioning Guide
**Document Reference:** `cloud_architecture_spec/07_PHASE_1_10K_USERS_DEPLOYMENT_PLAYBOOK.md`  
**Target:** Building LLM & Lead DevOps Engineers  

---

## 1. Cloud Infrastructure & Cost Analysis (10,000 Users Scale)

One of the greatest benefits of this edge-native architecture (Cloudflare Workers + R2 + D1 + Firebase Auth) is that Phase 1 (10,000 active enrolled students) runs with **sub-20ms global latency** at an exceptionally low operating expenditure:

| Resource | Usage at 10,000 Students | Monthly Cost |
|:---|:---|:---|
| **Cloudflare Workers (Edge Compute)** | ~15 Million invocations (heartbeats + lesson proxy) | ~$10.00 / mo |
| **Cloudflare R2 (Private Curriculum)** | 750,000 lesson reads, **0 Egress Fees** | ~$0.30 / mo |
| **Cloudflare D1 (Database)** | ~500 MB data, 25 Million rows read | ~$5.00 / mo |
| **Cloudflare Workers KV (Heartbeats)** | High-speed cache for 30s pings | ~$5.00 / mo |
| **Firebase / Google Identity Auth** | 10,000 Monthly Active Users (MAUs) | **$0.00 (Free Tier)** |
| **Stripe Payment Gateway** | Transaction-based ($38.00 per student) | 2.9% + 30¢ per checkout |
| **Total Cloud Infra Overhead** | **Full LMS Infrastructure for 10,000 Students** | **< $30.00 / month** |

---

## 2. Environment Variables & Secrets Matrix

Store these secrets in Cloudflare Workers using `wrangler secret put <KEY>`:

```ini
# ==============================================================================
# TX-ADE PRODUCTION SECRETS (CLOUDFLARE WORKERS)
# ==============================================================================

# Google OAuth 2.0 Identity
GOOGLE_CLIENT_ID="105862609227988682159-xxxxxxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="GOCSPX-xxxxxxxxxxxxxxxxxxxx"

# Internal Cryptographic Keys
JWT_SECRET="tx_prod_jwt_super_secure_random_key_64_bytes_minimum_hex"
TICKET_SECRET="tx_ephemeral_lesson_ticket_signing_secret_64_bytes_hex"

# Stripe Live Keys
STRIPE_SECRET_KEY="<REPLACE_WITH_YOUR_STRIPE_SECRET_KEY>"
STRIPE_WEBHOOK_SECRET="<REPLACE_WITH_YOUR_STRIPE_WEBHOOK_SECRET>"

# TDLR Official School Licensing
TDLR_SCHOOL_CODE="C3284"
TDLR_COURSE_APPROVAL="ADE-1317"
SUPPORT_EMAIL="support@texasade.org"

# Frontend Domains
CLIENT_ORIGIN="https://app.texasade.org"
API_ORIGIN="https://api.texasade.org"
```

---

## 3. Step-by-Step Provisioning Guide (Command Line)

### Step 1: Install Wrangler CLI & Authenticate
```powershell
npm install -g wrangler@latest
wrangler login
# Authenticates with your Cloudflare account (Polkamlokesh@gmail.com / Account ID: d96f5a789a0cde34666a220708d38f53)
```

### Step 2: Provision Cloudflare D1 Database
```powershell
# Create the primary production relational database
wrangler d1 create tx_ade_production_db

# Note the database_id returned by Wrangler, e.g.:
# database_id = "8f3b9a12-4c2d-4e5f-9a0b-1c2d3e4f5a6b"
```

### Step 3: Run Database Migrations
Execute the SQL DDL defined in `03_DATABASE_SCHEMA_AND_MODELS.md`:
```powershell
wrangler d1 execute tx_ade_production_db --file=./cloud_architecture_spec/03_DATABASE_SCHEMA_AND_MODELS.md
```

### Step 4: Provision Private Cloudflare R2 Bucket
```powershell
# Create the private bucket for 75 topics and visual assets
wrangler r2 bucket create tx-dmv-private-curriculum
```

### Step 5: Provision Workers KV Namespaces (High-Speed Heartbeat & Session Cache)
```powershell
# Namespace for 30s instructional time throttle
wrangler kv namespace create HEARTBEAT_KV

# Namespace for single-use ephemeral lesson tickets
wrangler kv namespace create TICKET_KV
```

### Step 6: Sync Curriculum Files to Private R2
Run the sync script from `04_SECURE_CONTENT_DELIVERY_PIPELINE.md`:
```powershell
npx ts-node ./scripts/sync_curriculum_to_r2.ts
```

---

## 4. Production `wrangler.toml` Configuration File

Create this file in the worker service root directory:

```toml
name = "tx-ade-edge-gateway"
main = "src/index.ts"
compatibility_date = "2026-10-01"
compatibility_flags = ["nodejs_compat"]

# Cloudflare D1 Binding
[[d1_databases]]
binding = "DB"
database_name = "tx_ade_production_db"
database_id = "YOUR_D1_DATABASE_ID_FROM_STEP_2"

# Cloudflare R2 Bucket Binding
[[r2_buckets]]
binding = "CURRICULUM_R2"
bucket_name = "tx-dmv-private-curriculum"

# Workers KV Bindings
[[kv_namespaces]]
binding = "HEARTBEAT_KV"
id = "YOUR_HEARTBEAT_KV_ID_FROM_STEP_5"

[[kv_namespaces]]
binding = "TICKET_KV"
id = "YOUR_TICKET_KV_ID_FROM_STEP_5"

# Environment Variables (Public)
[vars]
TDLR_SCHOOL_CODE = "C3284"
TDLR_COURSE_APPROVAL = "ADE-1317"
SUPPORT_EMAIL = "support@texasade.org"
CLIENT_ORIGIN = "https://app.texasade.org"

# Production Routes
routes = [
  { pattern = "api.texasade.org/*", zone_name = "texasade.org" },
  { pattern = "app.texasade.org/api/*", zone_name = "texasade.org" },
  { pattern = "app.texasade.org/lesson/*", zone_name = "texasade.org" }
]
```

---

## 5. Stripe Webhook Production Configuration

1. Log into your [Stripe Dashboard](https://dashboard.stripe.com/webhooks).
2. Click **Add Endpoint**.
3. Endpoint URL: `https://api.texasade.org/api/v1/webhooks/stripe`
4. Events to send:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `charge.refunded`
5. Reveal Signing Secret (`whsec_...`) and store via Wrangler:
   ```powershell
   wrangler secret put STRIPE_WEBHOOK_SECRET
   ```

---

## 6. Zero-Downtime Deployment & Health Check Verification

### Deploy Worker:
```powershell
wrangler deploy
```

### Health Check Verification:
```powershell
# 1. API Health Check
curl -i https://api.texasade.org/api/v1/health

# 2. Verify Gated Route (Must Return 401 Unauthorized)
curl -i https://api.texasade.org/api/v1/lessons/L01-T01

# 3. Verify Direct URL Trap (Must Return 404 or Redirect to Login)
curl -i https://app.texasade.org/final_course_export/L01-T01.html
```

---

## 7. Next Steps for Autonomous Coding Agent

With this playbook and the accompanying 6 specifications, the building LLM has complete architectural instructions to:
1. Implement the TypeScript Edge Worker router in `src/index.ts`.
2. Connect `course_shell/index.html` to invoke `/api/v1/student/progress`, `/api/v1/student/heartbeat`, and `/api/v1/lessons/:topicId/ticket`.
3. Deploy the D1 schema and migrate all 75 clean curriculum HTML files to R2.
