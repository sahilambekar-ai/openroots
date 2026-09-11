# OpenRoots / ProgressRooms — Agent Helper & Reference Guide

A concise, point-by-point reference document for new AI agents working across `openroots` and `progressrooms`.

---

## 1. Credentials & Configuration Reference

### Database
- **Engine**: PostgreSQL 16 (running locally on port `5432`)
- **Username**: `sahil`
- **Password**: `admin123`
- **Host**: `localhost`
- **Port**: `5432`
- **Database Name**: `progressrooms_db`
- **Async Connection String**: `postgresql+asyncpg://sahil:admin123@localhost:5432/progressrooms_db`
- **Sync Connection String**: `postgresql://sahil:admin123@localhost:5432/progressrooms_db`
- **Database Creation Command**: `CREATE DATABASE progressrooms_db;` or `createdb -U sahil progressrooms_db`
- **Seeding Script**: `python -m scripts.seed.seed_data` (from `progressrooms-api`)

### Brevo Email Service
- **Provider**: Brevo (formerly Sendinblue) REST API v3
- **Endpoint**: `https://api.brevo.com/v3/smtp/email`
- **API Key**: Configured via `BREVO_API_KEY` in `progressrooms-api/.env` (REST v3 key)
- **Sender Email**: `sahilambekar.dev@gmail.com`
- **Sender Name**: `ProgressRooms` (or `Aerial Yoga with Shivani` in client repo)
- **Status Flag**: `BREVO_ENABLED=True`

### Razorpay (Mock / Development)
- **Key ID**: `rzp_test_mock_progressrooms`
- **Key Secret**: `rzp_secret_mock_progressrooms`
- **Webhook Secret**: `rzp_webhook_secret_mock`

### Auth & JWT
- **Secret Key**: `dev-secret-key-change-in-production-progressrooms-2026`
- **Algorithm**: `HS256`
- **Access Token Expiry**: 7 days (`10080` minutes)
- **OTP Expiry**: 10 minutes

### Test Accounts & Mock Passcodes
- **Mock OTP (Development)**: `123456`
- **Super Admin**: `admin@test.progressrooms.local` (Platform Super Admin)
- **Studio Owner**: `owner@yogastudio.test` (Sahil Sharma / Sahil Yoga Studio)
- **Instructor**: `ananya@yogastudio.test` (Ananya Sen)
- **Student**: `student1@test.progressrooms.local` (Aarav Patel)

---

## 2. Cross-Project Reference (`yoga clients` / `clients` folder)

- **Source Project Location**:
  - Frontend: `/Users/sahil/Documents/work/clients/aerialyogawithshivani`
  - Backend: `/Users/sahil/Documents/work/clients/aerialyogawithshivani_backend`
- **What is fetched / referenced from the yoga client**:
  - **Credentials**: Postgres credentials (`sahil:admin123`) and Brevo credentials extracted directly from `aerialyogawithshivani_backend/.env`.
  - **Design System**: Calming nature sanctuary color palette (Forest Green `#0C2417`, Emerald `#133623`, Sage `#81A882`, Off-white background `#F4F7F4`) adapted from the Aerial Yoga client interface.
  - **Dashboard Architecture**: Sidebar layout, operational navigation tabs, and calendar/attendance tracker design modeled after `aerialyogawithshivani/src/components/dashboard`.
  - **Email Template**: Nature-styled HTML transactional email template for OTP passcode verification.

---

## 3. How Emails Are Dispatched

- **Protocol**: HTTPS REST request (not SMTP) using `httpx.AsyncClient`.
- **Headers**:
  ```json
  {
    "api-key": "xkeysib-d1574a6c...",
    "content-type": "application/json",
    "accept": "application/json"
  }
  ```
- **Payload Structure**:
  ```json
  {
    "sender": { "name": "ProgressRooms", "email": "sahilambekar.dev@gmail.com" },
    "to": [{ "email": "recipient@example.com", "name": "Recipient Name" }],
    "subject": "🌿 Your ProgressRooms Code (123456)",
    "htmlContent": "<html>...nature sanctuary styled HTML template...</html>"
  }
  ```
- **Implementation File**: `progressrooms-api/app/core/email_service.py` -> `send_otp_email()`.
- **Dev Bypass**: In local development, test OTP `123456` is pre-filled or previewed on `/login` so manual inbox checks are not required during test loops.

---

## 4. Documentation & Progress Tracking Structure

All project specifications and progress records are maintained in Markdown (`.md`) files:

```text
progressrooms/
├── docs/                           # Architectural & Domain Specs
│   ├── 01-product/                 # Domain models, subscription tiers
│   ├── 02-architecture/            # Multi-tenant design, tech stack
│   ├── 03-database/                # Schema definitions, ER diagrams
│   ├── 04-api/                     # REST API contracts & routes
│   ├── 04-user-flows/              # Authentication, booking, student flows
│   ├── 05-auth/                    # RBAC matrix (SuperAdmin, Owner, Teacher, Student)
│   ├── 06-payments/                # Payment flow & webhook handling
│   ├── 07-scheduling/              # Batch engine & recurring occurrences
│   ├── 08-websites/                # Website builder & templates
│   ├── 09-testing/                 # Test accounts & mock data
│   └── 10-deployment/              # Docker, environment setup
└── tracker/                        # Incremental Development Tracker
    ├── ROADMAP.md                  # Milestone progress
    └── features/                   # Per-feature specs & test walk-throughs
        ├── FEAT-01-nature-theme.md
        ├── FEAT-02-landing-page.md
        ├── FEAT-03-dev-test-login.md
        ├── FEAT-04-admin-portal.md
        ├── FEAT-05-scheduling-batches.md
        └── FEAT-06-attendance-sync.md
```

---

## 5. Agent Prompt: Previous Sessions Summary & Operating Directives

Copy and paste this prompt to initialize a new agent in this project:

```text
You are working on the ProgressRooms multi-tenant SaaS project inside /Users/sahil/Documents/work/openroots/progressrooms.

Here is the context, architectural baseline, and operating procedure from previous sessions:

1. WORKSPACE STRUCTURE:
   - Primary specification: /Users/sahil/Documents/work/openroots/progressrooms-script.md
   - Architecture & DB docs: progressrooms/docs/ (01-product through 10-deployment)
   - Progression tracker: progressrooms/tracker/features/ (FEAT-01 through FEAT-06)
   - Frontend: progressrooms-web (Next.js stable, Tailwind CSS, App Router)
   - Backend: progressrooms-api (FastAPI stable, SQLAlchemy 2.0 Async, PostgreSQL)

2. CORE CREDENTIALS & INTEGRATIONS:
   - Database: PostgreSQL on localhost:5432 (User: sahil, Password: admin123, DB: progressrooms_db)
   - Email Service: Brevo REST API v3 (Key configured in progressrooms-api/.env, Sender: sahilambekar.dev@gmail.com)
   - Reference project: /Users/sahil/Documents/work/clients/aerialyogawithshivani (frontend) and aerialyogawithshivani_backend (backend) for design, credentials, and dashboard patterns.

3. DESIGN & BRAND IDENTITY:
   - Nature-inspired sanctuary theme (Deep Forest #0C2417, Forest Green #133623, Sage #81A882, Canvas #F4F7F4).
   - No generic corporate blue styling.
   - Consistent typography across the landing page and dashboard.

4. USER ROLES & PERMISSIONS:
   - Super Admin (Platform / Product Owner): Manages all studios and instructors. Menu must be platform-level.
   - Studio Owner / Instructor: Manages classes, batches, memberships, attendance, student roster.
   - Student: Student portal, enrolled sessions, attendance record.
   - Test mode: One-click logins on /login with dev OTP 123456.

5. DEVELOPMENT METHODOLOGY:
   - Build incrementally step-by-step: develop one feature at a time.
   - Document every feature in progressrooms/tracker/features/FEAT-XX-[name].md containing feature ID, implementation files, and exact manual verification steps.
   - Provide clear test steps after completing each feature before moving to the next.
   - Connect frontend filters, search, and pagination directly to backend REST endpoints.
```
