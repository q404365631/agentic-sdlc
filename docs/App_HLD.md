# App_HLD.md
# MVP Appointment Booking Application — High-Level Design (HLD)

## Document Control

| **Version** | **Date**   | **Author**            | **Changes**          |
|-------------|------------|-----------------------|----------------------|
| 1.0         | 2026-03-24 | AI Architecture Agent | Initial Draft        |

**Related Documents:**

| **Document**     | **Location**            | **Description**                              |
|------------------|-------------------------|----------------------------------------------|
| BRD              | `docs/BRD.md`           | Business Requirements Document               |
| Epics            | `docs/Epics.md`         | Product Epics (EP-001 to EP-005)             |
| Features         | `docs/Features.md`      | 25 MVP Features (F-001 to F-025)             |
| Data Model       | `docs/App_DataModel.md` | Physical & Logical Data Model                |

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Technology Stack](#3-technology-stack)
4. [System Components](#4-system-components)
5. [API Design](#5-api-design)
6. [Security Design](#6-security-design)
7. [Data Flow Diagrams](#7-data-flow-diagrams)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Deployment Architecture](#9-deployment-architecture)
10. [Integration Points](#10-integration-points)
11. [Constraints & Assumptions](#11-constraints--assumptions)
12. [Risks & Open Issues](#12-risks--open-issues)

---

## 1. System Overview

### 1.1 Purpose

This High-Level Design document describes the technical architecture and design of the **MVP Appointment Booking Application**. It translates the business requirements defined in `BRD.md`, the epics in `Epics.md`, and the 25 features in `Features.md` into a concrete, implementable technical blueprint that a team of 4–5 developers can execute within an 8–10 week timeline targeting Q2 2026.

### 1.2 Scope

This HLD covers:

- The layered application architecture (Presentation → Application/Business Logic → Data)
- All six system modules: Authentication, Doctor Search, Appointment Booking, Appointment Management, Admin, and Email
- RESTful API design for all 25 features across 5 epics
- Security design including authentication, session management, and rate limiting
- Data flow for critical business processes
- Deployment architecture on a single-server configuration
- Non-functional requirements and how they are realized

**Out of Scope (MVP boundary — see BRD §4.2):**  
Payment processing, SMS/email reminders (beyond confirmation), telemedicine, EHR integration, multi-location support, social login, 2FA, native mobile apps, calendar integrations, recurring appointments, waitlists, patient reviews, multi-language support, and advanced analytics are explicitly excluded from this design.

### 1.3 Key Design Decisions

| **Decision**                             | **Choice**                                   | **Rationale**                                                                 |
|------------------------------------------|----------------------------------------------|-------------------------------------------------------------------------------|
| Backend Framework                        | Python / Flask                               | Lightweight, rapid development; team familiarity; adequate for MVP scale      |
| Database                                 | SQLite with WAL mode                         | Zero-ops, embedded, sufficient for 100 concurrent users; clear upgrade path   |
| Authentication                           | Session cookies + bcrypt                     | Secure; Flask-Session simplifies implementation; JWT optional extension       |
| Slot model                               | Dynamic generation from working_hours        | Flexible; no pre-materialization overhead; supports blocking and exceptions   |
| Booking ID format                        | `BK-YYYYMMDD-NNNN`                           | Human-readable; supports audit; aligns with F-015 requirement                 |
| Template engine                          | Jinja2 (server-side rendering)               | Reduces frontend complexity; full page SEO; no separate SPA build pipeline    |
| Email delivery                           | SendGrid or AWS SES (configurable)           | Reliable delivery; free tier sufficient for MVP volume                        |
| Race condition prevention                | DB-level UNIQUE constraint + SELECT FOR UPDATE | Prevents double-booking without distributed locks; SQLite WAL supports this   |
| Admin role                               | `is_admin` flag on `users` table             | Simplest approach for single-practice MVP; no separate RBAC tables needed     |
| HIPAA                                    | Deferred                                     | MVP collects no PHI; basic GDPR data privacy applied                          |

---

## 2. Architecture Overview

### 2.1 Architectural Style

The application follows a **Layered (N-Tier) Architecture** with three logical tiers:

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  HTML / CSS / JavaScript  +  Jinja2 Server-Side Templates│    │
│  │  Responsive Web UI (Bootstrap or custom CSS)             │    │
│  │  Form validation (client-side pre-flight)                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         ▲         │                              │
│                   HTTP Response   │ HTTP Request (HTTPS)         │
│                         │         ▼                              │
├──────────────────────────────────────────────────────────────────┤
│                  APPLICATION / BUSINESS LOGIC LAYER              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   NGINX Reverse Proxy                    │   │
│  │  (SSL termination, static file serving, rate-limiting)   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Flask Application (Gunicorn WSGI)              │   │
│  │  ┌──────────┐ ┌─────────────┐ ┌────────────────────┐    │   │
│  │  │  Auth    │ │  Doctor     │ │  Appointment       │    │   │
│  │  │  Module  │ │  Search     │ │  Booking Module    │    │   │
│  │  │(EP-001)  │ │  Module     │ │  (EP-003, EP-004)  │    │   │
│  │  │          │ │  (EP-002)   │ │                    │    │   │
│  │  └──────────┘ └─────────────┘ └────────────────────┘    │   │
│  │  ┌──────────┐ ┌─────────────┐                            │   │
│  │  │  Admin   │ │  Email      │                            │   │
│  │  │  Module  │ │  Service    │                            │   │
│  │  │ (EP-005) │ │  Module     │                            │   │
│  │  └──────────┘ └─────────────┘                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                     │
├──────────────────────────────────────────────────────────────────┤
│                       DATA LAYER                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            SQLite Database (WAL Mode)                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌────────────┐ ┌───────────┐   │   │
│  │  │  users  │ │ doctors │ │appointments│ │  blocked  │   │   │
│  │  │         │ │         │ │            │ │  _slots   │   │   │
│  │  └─────────┘ └─────────┘ └────────────┘ └───────────┘   │   │
│  │  ┌─────────────────────┐  ┌──────────────────────────┐   │   │
│  │  │ doctor_working_hours │  │       audit_log          │   │   │
│  │  └─────────────────────┘  └──────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                     │
├──────────────────────────────────────────────────────────────────┤
│                    EXTERNAL SERVICES                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   Email Service (SendGrid API / AWS SES)                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Design Patterns Used

| **Pattern**                    | **Where Applied**                                           | **Purpose**                                               |
|-------------------------------|-------------------------------------------------------------|-----------------------------------------------------------|
| Repository Pattern            | Database access layer (each module's DB queries)            | Decouples business logic from SQL; simplifies unit testing |
| Blueprint Pattern (Flask)     | Each module registered as a Flask Blueprint                 | Modular route registration; clear separation of concerns   |
| Service Layer Pattern         | Business logic methods in dedicated service classes         | Keeps route handlers thin; reusable business logic         |
| Template Method Pattern       | Slot generation algorithm                                   | Consistent slot computation with override points           |
| Decorator Pattern             | `@login_required`, `@admin_required` decorators             | Clean cross-cutting concern enforcement on routes          |
| Optimistic Locking            | UNIQUE constraint on `doctor_id + appointment_date + start_time` | Prevent double-booking without pessimistic DB locks    |
| Soft Delete                   | `status='cancelled'` on appointments                        | Preserve audit history; support reporting                  |
| Audit Log Pattern             | `audit_log` table populated on CREATE / CANCEL / UPDATE     | Traceability; compliance readiness                         |

---

## 3. Technology Stack

### 3.1 Core Stack

| **Layer**          | **Technology**              | **Version** | **Justification**                                               |
|--------------------|-----------------------------|-------------|-----------------------------------------------------------------|
| Language           | Python                      | 3.11+       | Team skill; strong ecosystem; Flask native                      |
| Web Framework      | Flask                       | 3.x         | Lightweight; minimal boilerplate; Blueprint support             |
| WSGI Server        | Gunicorn                    | 21.x        | Production-grade; multi-worker; Unix socket support             |
| Reverse Proxy      | NGINX                       | 1.24+       | SSL termination; static file serving; connection buffering      |
| Template Engine    | Jinja2 (bundled with Flask) | 3.x         | Server-side rendering; secure; no SPA complexity for MVP        |
| Database           | SQLite                      | 3.40+       | Zero-ops embedded DB; WAL mode for concurrency; upgrade path    |
| ORM / DB Access    | SQLAlchemy Core or raw SQL  | 2.x         | Lightweight; explicit SQL; easy SQLite→PostgreSQL migration      |
| Password Hashing   | bcrypt (Flask-Bcrypt)       | 1.x         | Industry-standard; cost factor 12; brute-force resistant        |
| Session Management | Flask-Session + secure cookies | 0.5+    | Server-side session with signed cookies; 7-day TTL              |
| Email              | SendGrid SDK / Boto3 (SES)  | Latest      | Configurable at deploy; free tier sufficient for MVP volume      |
| CSS Framework      | Bootstrap 5                 | 5.3         | Responsive; rapid UI development; well-documented               |
| JavaScript         | Vanilla ES6+                | —           | No build pipeline; minimal client-side logic; AJAX for slots    |

### 3.2 Development & Operations Tools

| **Tool**          | **Purpose**                                        |
|-------------------|----------------------------------------------------|
| Git               | Version control                                    |
| pytest            | Unit and integration testing                       |
| python-dotenv     | Environment-specific configuration (`.env` files)  |
| Alembic           | Database schema migration management               |
| pre-commit hooks  | Linting (flake8), formatting (black)               |
| Gunicorn          | WSGI production server                             |
| NGINX             | Reverse proxy, static assets                       |

### 3.3 SQLite Configuration

SQLite is configured with the following pragmas for the MVP:

```sql
PRAGMA journal_mode = WAL;      -- Write-Ahead Logging: better concurrency
PRAGMA synchronous = NORMAL;    -- Balance of durability and performance
PRAGMA foreign_keys = ON;       -- Enforce referential integrity
PRAGMA busy_timeout = 5000;     -- 5-second wait on locked DB (WAL reduces frequency)
PRAGMA cache_size = -16000;     -- 16 MB page cache
```

**Why WAL mode matters for MVP:**  
SQLite WAL (Write-Ahead Logging) allows multiple readers to proceed concurrently with a single writer, which is critical for 100 concurrent users. Standard SQLite journal mode would serialize all reads behind any write.

---

## 4. System Components

### 4.1 Web Application Server (Flask)

**Blueprint structure:**

```
app/
├── __init__.py             # Application factory (create_app)
├── config.py               # Config classes (Development, Production)
├── extensions.py           # SQLAlchemy, bcrypt, session init
├── blueprints/
│   ├── auth/               # EP-001 — Authentication
│   │   ├── __init__.py
│   │   ├── routes.py       # Route handlers (thin)
│   │   ├── services.py     # Business logic
│   │   └── forms.py        # WTForms validation
│   ├── doctors/            # EP-002 — Doctor Discovery
│   │   ├── routes.py
│   │   └── services.py
│   ├── appointments/       # EP-003, EP-004 — Booking & Management
│   │   ├── routes.py
│   │   └── services.py
│   ├── admin/              # EP-005 — Provider Administration
│   │   ├── routes.py
│   │   └── services.py
│   └── email_service/      # Shared email utility
│       └── service.py
├── models/                 # SQLAlchemy models / SQL schema definitions
│   └── database.py
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── auth/
│   ├── doctors/
│   ├── appointments/
│   └── admin/
└── static/                 # CSS, JS, images
```

**Application Factory Pattern:**  
Flask's `create_app()` factory enables environment-specific configuration and testability by instantiating the app object with dependencies injected.

### 4.2 Authentication Module (EP-001, F-001 to F-005)

**Responsibilities:**
- User registration with bcrypt password hashing (cost factor 12)
- Login with credential validation, session creation, and "Remember Me" support
- Logout and session invalidation
- Session management (7-day TTL via Flask-Session)
- Profile retrieval (F-005)
- Rate limiting and account lockout (F-002: 5 attempts → 15-min lockout)

**Key Design Decisions:**
- Passwords are **never stored in plain text**; bcrypt hash stored in `users.password_hash`
- Sessions use **server-side storage** with signed cookie containing only the session ID
- `@login_required` decorator applied to all protected routes
- Generic error messages ("Invalid email or password") prevent account enumeration
- Rate limiting implemented via in-memory counter (IP + email key) with Redis upgrade path

**Session Lifecycle:**

```
POST /api/auth/login
  → validate credentials
  → verify bcrypt hash
  → create server-side session
  → set httpOnly + Secure cookie (session_id)
  → return 200 + user profile JSON

GET /api/auth/profile (with session cookie)
  → validate session exists and not expired
  → return user data

POST /api/auth/logout
  → delete server-side session
  → clear cookie
  → return 200
```

### 4.3 Doctor Search Module (EP-002, F-006 to F-010)

**Responsibilities:**
- Full-text partial name search (F-006: LIKE query, case-insensitive, 2+ chars)
- Specialty filtering via dropdown (F-007)
- Availability filtering by date (F-008: checks working_hours + blocked_slots + appointments)
- Doctor profile view (F-009)
- Paginated search results (F-010: 20 per page)

**Search Query Design:**

```sql
SELECT d.* FROM doctors d
WHERE d.status = 'active'
  AND (d.full_name LIKE '%:query%' OR :query IS NULL)
  AND (d.specialty = :specialty OR :specialty IS NULL)
ORDER BY d.full_name
LIMIT 20 OFFSET :offset;
```

**Availability Filter Logic (F-008):**  
A doctor is considered "available on date X" if:
1. They have a working hours record for that day of week (`doctor_working_hours.is_active = 1`)
2. At least one 30-minute slot within those hours is not blocked (`blocked_slots`)
3. At least one slot is not already booked (`appointments` with status='confirmed')

This is computed in the service layer without materializing all slots in the DB.

**Index Strategy:**  
- `doctors(status)` — filter inactive doctors
- `doctors(specialty)` — specialty filter
- `doctors(full_name)` — LIKE search (partial; full-text search extension if needed at scale)

### 4.4 Appointment Booking Module (EP-003, F-011 to F-016)

**Responsibilities:**
- Generate available 30-minute slots for a doctor on a given date (F-011, F-012)
- Enforce atomic booking with race condition prevention (F-014)
- Generate unique Booking ID in `BK-YYYYMMDD-NNNN` format (F-015)
- Send confirmation email (F-016)
- Display booking confirmation screen (F-013)

**Slot Generation Algorithm (F-011, F-022):**

```
FUNCTION get_available_slots(doctor_id, date):
  1. Get day_of_week from date (0=Monday, 6=Sunday)
  2. Query doctor_working_hours WHERE doctor_id = ? AND day_of_week = ?
     AND is_active = 1 → (start_time, end_time)
  3. If no record → return [] (doctor not working that day)
  4. Generate all 30-min slots from start_time to end_time:
       e.g. 09:00→09:30, 09:30→10:00, ..., 16:30→17:00
  5. Exclude slots in blocked_slots WHERE doctor_id=? AND blocked_date=?
  6. Exclude slots in appointments WHERE doctor_id=? AND appointment_date=?
       AND status != 'cancelled'
  7. Return remaining slots as [{start_time, end_time, available: true}]
```

**Double-Booking Prevention (F-014):**

The booking operation executes in a single SQLite transaction with the following steps:

```
BEGIN IMMEDIATE TRANSACTION;
  1. SELECT 1 FROM appointments
     WHERE doctor_id = :doctor_id
       AND appointment_date = :date
       AND start_time = :start_time
       AND status != 'cancelled'
     LIMIT 1 → if row exists, ROLLBACK and return 409 Conflict

  2. SELECT 1 FROM blocked_slots
     WHERE doctor_id = :doctor_id
       AND blocked_date = :date
       AND start_time = :start_time → if exists, ROLLBACK and return 409

  3. INSERT INTO appointments (...) VALUES (...)
  4. INSERT INTO audit_log (...) VALUES (...)
COMMIT;
```

The UNIQUE constraint on `appointments(doctor_id, appointment_date, start_time)` provides the final safety net — if two concurrent requests both pass step 1, only one INSERT will succeed; the other receives a UNIQUE constraint violation and returns 409.

**Booking ID Generation (F-015):**

```
FUNCTION generate_booking_id(date):
  date_str = date.strftime('%Y%m%d')           # e.g. "20260324"
  SELECT COUNT(*) FROM appointments
  WHERE booking_id LIKE 'BK-20260324-%'
  → seq = count + 1
  → return f"BK-{date_str}-{seq:04d}"          # e.g. "BK-20260324-0001"
```

**Note:** This generation runs inside the booking transaction to prevent gaps under concurrency.

### 4.5 Appointment Management Module (EP-004, F-017 to F-020)

**Responsibilities:**
- View upcoming appointments in chronological order (F-017)
- View past appointments in reverse chronological order (F-018)
- Cancel appointment with 24-hour restriction (F-019)
- Appointment detail view (F-020)

**Cancellation Logic (F-019):**

```
FUNCTION cancel_appointment(appointment_id, cancelled_by_user_id):
  1. Fetch appointment WHERE id = :id AND patient_id = :user_id
  2. If not found → 404 Not Found
  3. If status != 'confirmed' → 400 (already cancelled/completed)
  4. appointment_datetime = combine(appointment_date, start_time)
  5. If appointment_datetime - now() < 24 hours → 400
     (cancellation window expired)
  6. BEGIN TRANSACTION
     UPDATE appointments SET status='cancelled',
       cancelled_by=:user_id, updated_at=NOW()
     WHERE id=:id
     INSERT INTO audit_log (entity_type='appointment', action='CANCELLED', ...)
  7. COMMIT
  8. Send cancellation confirmation email (async/background task)
  9. Return 200 OK
```

**Soft Delete Pattern:**  
Appointments are never hard-deleted. The `status` field transitions: `confirmed → cancelled` or `confirmed → completed`. This preserves the audit history and supports the past appointments view (F-018).

### 4.6 Admin Module (EP-005, F-021 to F-025)

**Responsibilities:**
- CRUD doctor profiles (F-021)
- Configure working hours by day-of-week (F-022)
- Block specific slots with reason (F-023)
- View all appointments for a doctor, filterable by date (F-024)
- Admin dashboard: total doctors, today's appointments, this week's appointments (F-025)

**Access Control:**  
All admin routes are protected by `@admin_required` decorator:
```
def admin_required(f):
  @login_required
  def decorated(*args, **kwargs):
    if not current_user.is_admin:
      return 403 Forbidden
    return f(*args, **kwargs)
```

**Dashboard Queries (F-025):**

```sql
-- Total active doctors
SELECT COUNT(*) FROM doctors WHERE status = 'active';

-- Appointments today
SELECT COUNT(*) FROM appointments
WHERE appointment_date = DATE('now')
  AND status = 'confirmed';

-- Appointments this week
SELECT COUNT(*) FROM appointments
WHERE appointment_date BETWEEN DATE('now', 'weekday 0', '-7 days')
  AND DATE('now', 'weekday 0')
  AND status = 'confirmed';
```

### 4.7 Email Service Module (F-016, F-019)

**Responsibilities:**
- Send booking confirmation email after successful booking (F-016)
- Send cancellation notification after appointment cancellation (F-019)

**Design:**
- Configurable provider: SendGrid (primary) or AWS SES (alternative)
- Email rendered from Jinja2 templates (HTML + plain text)
- Email sending is **non-blocking** — failures are logged but do not fail the booking transaction
- Email queue: for MVP, sent synchronously in a background thread; upgrade path to Celery + Redis

**Confirmation Email Content (F-016):**
```
To: patient@email.com
Subject: Appointment Confirmed — BK-20260324-0001

Booking Reference: BK-20260324-0001
Doctor: Dr. Jane Smith (Cardiology)
Date: Monday, March 24, 2026
Time: 09:00 AM — 09:30 AM
Patient: John Doe

To cancel: Visit [link] (must be 24+ hours before appointment)
```

---

## 5. API Design

All API endpoints follow REST conventions. Requests and responses use `application/json` unless serving HTML (Jinja2 routes). All endpoints require HTTPS. Authentication is enforced via session cookie.

### 5.1 Authentication APIs (EP-001)

| **Method** | **Endpoint**           | **Feature** | **Auth Required** | **Description**                              |
|------------|------------------------|-------------|-------------------|----------------------------------------------|
| `POST`     | `/api/auth/register`   | F-001       | No                | Register new user account                    |
| `POST`     | `/api/auth/login`      | F-002       | No                | Authenticate user, create session            |
| `POST`     | `/api/auth/logout`     | F-003       | Yes               | Invalidate session, clear cookie             |
| `GET`      | `/api/auth/profile`    | F-005       | Yes               | Retrieve current user's profile              |

**POST /api/auth/register**
```json
// Request
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "5551234567",
  "password": "SecurePass1!",
  "confirm_password": "SecurePass1!"
}

// Response 201 Created
{
  "message": "Account created successfully",
  "user": { "id": 1, "full_name": "John Doe", "email": "john@example.com" }
}

// Error Responses
// 400 — Validation errors (missing fields, weak password, invalid email)
// 409 — Email already registered
```

**POST /api/auth/login**
```json
// Request
{
  "email": "john@example.com",
  "password": "SecurePass1!",
  "remember_me": true
}

// Response 200 OK (sets httpOnly session cookie)
{
  "message": "Login successful",
  "user": { "id": 1, "full_name": "John Doe", "is_admin": false }
}

// Error Responses
// 401 — Invalid credentials (generic message)
// 423 — Account locked (rate limit exceeded)
```

**GET /api/auth/profile**
```json
// Response 200 OK
{
  "id": 1,
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "5551234567",
  "created_at": "2026-03-24T10:00:00Z"
}
```

### 5.2 Doctor Discovery APIs (EP-002)

| **Method** | **Endpoint**                      | **Feature** | **Auth Required** | **Description**                                |
|------------|-----------------------------------|-------------|-------------------|------------------------------------------------|
| `GET`      | `/api/doctors`                    | F-006–F-010 | Yes               | Search/filter doctors with pagination          |
| `GET`      | `/api/doctors/{id}`               | F-009       | Yes               | Retrieve specific doctor's profile             |
| `GET`      | `/api/doctors/{id}/availability`  | F-011       | Yes               | Get available 30-min slots for a date          |

**GET /api/doctors**
```
Query Parameters:
  q          string   Partial name search (2+ chars, case-insensitive)
  specialty  string   Filter by specialty name
  date       string   Filter doctors available on date (YYYY-MM-DD)
  page       integer  Page number (default: 1)
  per_page   integer  Results per page (default: 20, max: 20)

// Response 200 OK
{
  "doctors": [
    {
      "id": 1,
      "full_name": "Dr. Jane Smith",
      "specialty": "Cardiology",
      "bio": "Board-certified cardiologist with 15 years experience.",
      "photo_url": "/static/doctors/jane-smith.jpg",
      "status": "active"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 45,
    "total_pages": 3
  }
}
```

**GET /api/doctors/{id}/availability**
```
Query Parameters:
  date  string  Required. Date to check (YYYY-MM-DD)

// Response 200 OK
{
  "doctor_id": 1,
  "date": "2026-03-24",
  "slots": [
    { "start_time": "09:00", "end_time": "09:30", "available": true },
    { "start_time": "09:30", "end_time": "10:00", "available": false },
    { "start_time": "10:00", "end_time": "10:30", "available": true }
  ]
}
```

### 5.3 Appointment Booking APIs (EP-003)

| **Method** | **Endpoint**              | **Feature** | **Auth Required** | **Description**                        |
|------------|---------------------------|-------------|-------------------|----------------------------------------|
| `POST`     | `/api/appointments`       | F-014–F-016 | Yes               | Create new appointment booking         |
| `GET`      | `/api/appointments`       | F-017–F-018 | Yes               | Get patient's appointments             |
| `GET`      | `/api/appointments/{id}`  | F-020       | Yes               | Get specific appointment detail        |
| `DELETE`   | `/api/appointments/{id}`  | F-019       | Yes               | Cancel appointment (soft delete)       |

**POST /api/appointments**
```json
// Request
{
  "doctor_id": 1,
  "appointment_date": "2026-03-24",
  "start_time": "09:00"
}

// Response 201 Created
{
  "booking_id": "BK-20260324-0001",
  "appointment_id": 42,
  "doctor": { "id": 1, "full_name": "Dr. Jane Smith", "specialty": "Cardiology" },
  "appointment_date": "2026-03-24",
  "start_time": "09:00",
  "end_time": "09:30",
  "status": "confirmed",
  "message": "Appointment confirmed. Confirmation sent to john@example.com"
}

// Error Responses
// 400 — Invalid input (missing fields, past date, invalid time)
// 404 — Doctor not found or inactive
// 409 — Slot no longer available (race condition)
// 422 — Slot outside working hours or blocked
```

**GET /api/appointments**
```
Query Parameters:
  type  string  'upcoming' (default) or 'past'

// Response 200 OK
{
  "appointments": [
    {
      "id": 42,
      "booking_id": "BK-20260324-0001",
      "doctor": { "full_name": "Dr. Jane Smith", "specialty": "Cardiology" },
      "appointment_date": "2026-03-24",
      "start_time": "09:00",
      "end_time": "09:30",
      "status": "confirmed"
    }
  ]
}
```

**DELETE /api/appointments/{id}**
```json
// Response 200 OK
{
  "message": "Appointment BK-20260324-0001 has been cancelled.",
  "cancellation_confirmed": true
}

// Error Responses
// 400 — Cannot cancel within 24 hours of appointment
// 400 — Appointment already cancelled or completed
// 403 — Not your appointment
// 404 — Appointment not found
```

### 5.4 Admin APIs (EP-005)

All admin endpoints require `is_admin = true` in the session; otherwise `403 Forbidden`.

| **Method** | **Endpoint**                                   | **Feature** | **Description**                              |
|------------|------------------------------------------------|-------------|----------------------------------------------|
| `GET`      | `/api/admin/doctors`                           | F-021       | List all doctors (including inactive)        |
| `POST`     | `/api/admin/doctors`                           | F-021       | Create new doctor profile                    |
| `PUT`      | `/api/admin/doctors/{id}`                      | F-021       | Update doctor profile                        |
| `DELETE`   | `/api/admin/doctors/{id}`                      | F-021       | Deactivate doctor (soft delete)              |
| `POST`     | `/api/admin/doctors/{id}/working-hours`        | F-022       | Set/replace working hours for doctor         |
| `POST`     | `/api/admin/doctors/{id}/blocked-slots`        | F-023       | Block a specific slot with reason            |
| `DELETE`   | `/api/admin/doctors/{id}/blocked-slots/{slotId}` | F-023     | Remove a blocked slot                        |
| `GET`      | `/api/admin/appointments`                      | F-024       | View all appointments (filterable by doctor/date) |
| `PUT`      | `/api/admin/appointments/{id}/cancel`          | F-024       | Admin cancel appointment on patient's behalf |
| `GET`      | `/api/admin/dashboard`                         | F-025       | Get dashboard summary statistics             |

**POST /api/admin/doctors**
```json
// Request
{
  "full_name": "Dr. Jane Smith",
  "specialty": "Cardiology",
  "bio": "Board-certified cardiologist...",
  "photo_url": "https://cdn.example.com/doctors/jane-smith.jpg",
  "email": "jane.smith@clinic.com",
  "phone": "5559876543",
  "status": "active"
}
// Response 201 Created — doctor object

// Response 400 — Validation errors
```

**POST /api/admin/doctors/{id}/working-hours**
```json
// Request — replaces all working hours for this doctor
{
  "working_hours": [
    { "day_of_week": 0, "start_time": "09:00", "end_time": "17:00" },
    { "day_of_week": 1, "start_time": "09:00", "end_time": "17:00" },
    { "day_of_week": 2, "start_time": "09:00", "end_time": "13:00" },
    { "day_of_week": 4, "start_time": "10:00", "end_time": "18:00" }
  ]
}
// Response 200 OK — updated working_hours array
```

**POST /api/admin/doctors/{id}/blocked-slots**
```json
// Request
{
  "blocked_date": "2026-03-25",
  "start_time": "14:00",
  "end_time": "14:30",
  "reason": "Staff meeting"
}
// Response 201 Created — blocked_slot object
// Response 409 — Slot already has a confirmed appointment
```

**GET /api/admin/dashboard**
```json
// Response 200 OK
{
  "total_active_doctors": 12,
  "appointments_today": 34,
  "appointments_this_week": 178,
  "generated_at": "2026-03-24T08:00:00Z"
}
```

### 5.5 HTTP Status Code Reference

| **Status** | **Meaning**           | **Usage**                                           |
|------------|-----------------------|-----------------------------------------------------|
| 200        | OK                    | Successful GET, PUT, DELETE                         |
| 201        | Created               | Successful POST (resource created)                  |
| 400        | Bad Request           | Validation errors, business rule violations         |
| 401        | Unauthorized          | No valid session / not logged in                    |
| 403        | Forbidden             | Authenticated but insufficient permissions          |
| 404        | Not Found             | Resource does not exist                             |
| 409        | Conflict              | Duplicate resource (slot taken, email exists)       |
| 422        | Unprocessable Entity  | Semantically invalid (slot outside working hours)   |
| 423        | Locked                | Account temporarily locked (rate limiting)          |
| 500        | Internal Server Error | Unhandled exceptions (logged, generic message shown)|

---

## 6. Security Design

### 6.1 Authentication Flow

```
Patient Browser                Flask App              SQLite DB
      │                             │                      │
      │  POST /api/auth/login       │                      │
      │ ─────────────────────────► │                      │
      │                             │  SELECT * FROM users │
      │                             │  WHERE email=?       │
      │                             │ ────────────────────►│
      │                             │ ◄────────────────────│
      │                             │  bcrypt.verify(pw)   │
      │                             │  create session      │
      │  200 OK + Set-Cookie        │                      │
      │ ◄─────────────────────────  │                      │
      │  (httpOnly; Secure;         │                      │
      │   SameSite=Lax; 7-day TTL) │                      │
      │                             │                      │
      │  GET /api/appointments      │                      │
      │  Cookie: session=abc123     │                      │
      │ ─────────────────────────► │                      │
      │                             │  validate session    │
      │                             │  load user           │
      │  200 OK + appointments      │                      │
      │ ◄─────────────────────────  │                      │
```

### 6.2 Session Management (F-004)

| **Parameter**       | **Value**                              |
|---------------------|----------------------------------------|
| Session storage     | Server-side (Flask-Session + filesystem or SQLite) |
| Cookie flags        | `httpOnly=True`, `Secure=True`, `SameSite=Lax` |
| Default TTL         | 24 hours                               |
| "Remember Me" TTL   | 7 days                                 |
| Session ID          | Cryptographically random UUID          |
| Session rotation    | On login (prevent session fixation)    |
| Logout              | Server-side session deletion + cookie clear |

### 6.3 Password Security (F-001)

| **Control**           | **Implementation**                          |
|-----------------------|---------------------------------------------|
| Hashing algorithm     | bcrypt, cost factor 12                      |
| Minimum length        | 8 characters                                |
| Complexity rules      | Uppercase + lowercase + digit + special char |
| Storage               | Hash only; plain text never stored/logged   |
| Comparison            | Constant-time bcrypt.checkpw()              |
| Rotation              | Manual for MVP (reset flow deferred)        |

### 6.4 Rate Limiting (F-002)

| **Endpoint**            | **Limit**                                 | **Action on Breach**           |
|-------------------------|-------------------------------------------|---------------------------------|
| `POST /api/auth/login`  | 5 attempts per email per 15 minutes       | 423 Locked for 15 minutes      |
| `POST /api/auth/register` | 3 attempts per IP per hour             | 429 Too Many Requests          |
| All other endpoints     | 100 req/min per IP (NGINX level)          | 429 with Retry-After header    |

**Implementation:** In-memory dictionary with timestamp-based window (for MVP). Upgrade path: Redis for distributed rate limiting.

### 6.5 Input Validation

All inputs validated at two levels:

**Client-Side (Jinja2 + JS):**
- HTML5 `required`, `pattern`, `minlength` attributes
- JavaScript real-time validation on form fields
- Password strength meter (F-001)

**Server-Side (Flask + WTForms):**
- WTForms validators for all form inputs
- Parameterized SQL queries (no string concatenation)
- Email format validation (RFC 5322)
- Phone validation (10-digit US format)
- Date/time range checks (no past bookings)
- Enum validation (status values, day_of_week range)

### 6.6 HTTPS & Transport Security

- All traffic over TLS 1.2+ enforced by NGINX
- HSTS header: `Strict-Transport-Security: max-age=31536000`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Content-Security-Policy` header (restrict JS/CSS sources)
- CORS: restricted to own domain only (no external API consumers for MVP)

### 6.7 Data Privacy (GDPR Considerations)

- No PHI collected in MVP (per BRD §4.2)
- PII stored: name, email, phone only
- User data deletable on request (admin operation for MVP)
- SQLite database file encrypted at filesystem level (OS/hosting-layer encryption)
- Audit log retained for 90 days

---

## 7. Data Flow Diagrams

### 7.1 User Registration Flow (F-001)

```
Browser              NGINX            Flask/Auth            SQLite
  │                    │                   │                    │
  │──POST /register───►│                   │                    │
  │                    │──forward──────────►│                    │
  │                    │                   │──validate inputs   │
  │                    │                   │──check email ─────►│
  │                    │                   │◄──────────────────│
  │                    │                   │  (unique check)    │
  │                    │                   │──bcrypt hash(pw)   │
  │                    │                   │──INSERT users ────►│
  │                    │                   │◄──────────────────│
  │                    │                   │──create session    │
  │◄─201+Set-Cookie────│◄──────────────────│                    │
  │  (redirect search) │                   │                    │
```

### 7.2 Search & Book Appointment Flow (F-006 to F-016)

```
Browser              NGINX          Flask            SQLite         Email SVC
  │                    │               │                 │               │
  │──GET /doctors?q=──►│               │                 │               │
  │                    │──────────────►│                 │               │
  │                    │               │──SELECT doctors►│               │
  │                    │               │◄────────────────│               │
  │◄──200 doctor list──│◄──────────────│                 │               │
  │                    │               │                 │               │
  │──GET /doctors/1───►│               │                 │               │
  │◄──doctor profile───│◄──────────────│──SELECT doctor─►│               │
  │                    │               │◄────────────────│               │
  │                    │               │                 │               │
  │──GET /availability─►│              │                 │               │
  │  ?date=2026-03-24  │───────────────►│                │               │
  │                    │               │──working_hours─►│               │
  │                    │               │──blocked_slots─►│               │
  │                    │               │──appointments──►│               │
  │                    │               │◄────────────────│               │
  │                    │               │  compute slots  │               │
  │◄──available slots──│◄──────────────│                 │               │
  │                    │               │                 │               │
  │──POST /appointments►│              │                 │               │
  │  {doctor_id,date,  │───────────────►│                │               │
  │   start_time}      │               │──BEGIN TXN─────►│               │
  │                    │               │──check slot────►│               │
  │                    │               │──INSERT appt───►│               │
  │                    │               │──INSERT audit──►│               │
  │                    │               │──COMMIT────────►│               │
  │                    │               │◄────────────────│               │
  │                    │               │                 │──send email──►│
  │◄──201 booking_id───│◄──────────────│                 │               │
```

### 7.3 Cancel Appointment Flow (F-019)

```
Browser              Flask              SQLite           Email SVC
  │                    │                    │                 │
  │──DELETE /appts/42──►│                   │                 │
  │                    │──SELECT appt──────►│                 │
  │                    │◄───────────────────│                 │
  │                    │  check 24hr rule   │                 │
  │                    │  check ownership   │                 │
  │                    │──BEGIN TXN────────►│                 │
  │                    │──UPDATE status────►│                 │
  │                    │  ='cancelled'      │                 │
  │                    │──INSERT audit_log─►│                 │
  │                    │──COMMIT───────────►│                 │
  │                    │◄───────────────────│                 │
  │                    │──────────────────────────────────────►│
  │                    │  (send cancellation email, async)    │
  │◄──200 confirmed────│                    │                 │
```

### 7.4 Admin Manage Doctor Flow (F-021 to F-022)

```
Admin Browser        Flask/Admin          SQLite
  │                    │                    │
  │──POST /admin/doctors│                   │
  │  {name,specialty,..}►│                  │
  │                    │──@admin_required   │
  │                    │──validate inputs   │
  │                    │──INSERT doctors───►│
  │                    │──INSERT audit_log─►│
  │◄──201 doctor obj───│◄───────────────────│
  │                    │                    │
  │──POST /admin/doctors│                   │
  │  /1/working-hours  │                   │
  │  [{day,start,end}] ►│                  │
  │                    │──DELETE old hours─►│
  │                    │──INSERT new hours─►│
  │◄──200 hours obj────│◄───────────────────│
  │                    │                    │
  │──POST /admin/doctors│                   │
  │  /1/blocked-slots  │                   │
  │  {date,time,reason}►│                  │
  │                    │──check conflicts──►│
  │                    │──INSERT blocked───►│
  │◄──201 slot obj─────│◄───────────────────│
```

---

## 8. Non-Functional Requirements

### 8.1 Performance (from BRD §2.2, §2.3)

| **Requirement**                      | **Target**                  | **Design Realization**                                                 |
|--------------------------------------|-----------------------------|------------------------------------------------------------------------|
| Concurrent users                     | 100                         | Gunicorn with 4–8 workers; SQLite WAL mode for concurrent reads        |
| Monthly booking volume               | 10,000 bookings/month       | ~14 bookings/hour avg; SQLite handles comfortably                      |
| Page load time                       | < 2 seconds                 | NGINX static file serving; minimal JS; indexed DB queries              |
| Booking completion time              | < 3 minutes (user flow)     | Streamlined 3-step flow; instant slot feedback                         |
| API response time (p95)              | < 500ms                     | Simple SQL queries; DB indexes on all filter columns                   |
| Zero double-bookings                 | 0 incidents                 | DB UNIQUE constraint + transactional booking (§4.4)                    |
| Uptime during business hours         | 99%                         | Single-server with process supervisor (systemd); daily backups         |

### 8.2 Availability

- **Target:** 99% uptime during 8 AM – 8 PM business hours
- **Approach (MVP):** Single-server deployment with systemd process supervision; Gunicorn auto-restart
- **Backup:** Nightly SQLite database file backup to cloud storage (AWS S3 or equivalent)
- **Monitoring:** Basic uptime monitoring (UptimeRobot or similar free tier)
- **Recovery:** SQLite file restore from backup; RTO target: 2 hours

### 8.3 Scalability

**MVP Limits (designed for):**
- 100 concurrent users
- 10,000 bookings/month
- SQLite with WAL mode: adequate for this load

**Scale-Out Path (post-MVP):**

```
MVP (Current)              Phase 2                    Phase 3
────────────               ─────────────────          ──────────────────────
Single VPS                 → PostgreSQL               → Horizontal Flask scaling
SQLite WAL                 → Redis cache              → Load balancer
Gunicorn 4 workers         → Celery task queue        → Read replicas
NGINX                      → CDN for static files     → Kubernetes deployment
```

**SQLite → PostgreSQL Migration Trigger:** >50 concurrent writers or >50,000 bookings/month (see Data Model §11).

### 8.4 Maintainability

- Flask Blueprints enforce module boundaries
- Service layer separates business logic from route handlers
- Alembic manages schema migrations (SQLite → PostgreSQL compatible)
- python-dotenv for environment configuration
- Comprehensive logging with Python's `logging` module
- pytest for unit and integration test coverage (target: 70%+)

---

## 9. Deployment Architecture

### 9.1 Single-Server Deployment (MVP)

```
┌──────────────────────────────────────────────────────────┐
│                  Production Server (VPS/Cloud VM)        │
│  OS: Ubuntu 22.04 LTS                                   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ NGINX (Port 80/443)                               │  │
│  │  • SSL termination (Let's Encrypt)                │  │
│  │  • Static file serving (/static/)                 │  │
│  │  • Proxy to Gunicorn (Unix socket)                │  │
│  │  • Rate limiting (100 req/min per IP)             │  │
│  └──────────────────────┬─────────────────────────────┘  │
│                         │ Unix socket                    │
│  ┌──────────────────────▼─────────────────────────────┐  │
│  │ Gunicorn WSGI Server                              │  │
│  │  • Workers: 4–8 (2 × CPU cores)                  │  │
│  │  • Worker class: sync                             │  │
│  │  • Timeout: 30s                                   │  │
│  │  • Managed by: systemd                            │  │
│  └──────────────────────┬─────────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────▼─────────────────────────────┐  │
│  │ Flask Application                                 │  │
│  │  • Python 3.11                                    │  │
│  │  • Virtual environment                            │  │
│  │  • Blueprints: auth, doctors, appointments, admin │  │
│  └──────────────────────┬─────────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────▼─────────────────────────────┐  │
│  │ SQLite Database File                              │  │
│  │  • Location: /var/app/data/appointments.db        │  │
│  │  • WAL mode enabled                               │  │
│  │  • Daily backup via cron to S3                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Filesystem                                        │  │
│  │  • /var/app/         — Application code           │  │
│  │  • /var/app/data/    — SQLite file                │  │
│  │  • /var/app/logs/    — Application logs           │  │
│  │  • /var/app/static/  — Static assets (NGINX)      │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘

External: Email Service API (SendGrid / AWS SES)
External: Backup Storage (AWS S3 / equivalent)
```

### 9.2 systemd Service Configuration

The Flask application is managed by systemd for automatic restart on failure:

```
[Unit]
Description=Appointment Booking App (Gunicorn)
After=network.target

[Service]
User=appuser
WorkingDirectory=/var/app
Environment="PATH=/var/app/venv/bin"
ExecStart=/var/app/venv/bin/gunicorn \
  --workers 4 \
  --bind unix:/var/app/run/gunicorn.sock \
  --timeout 30 \
  --log-file /var/app/logs/gunicorn.log \
  "app:create_app()"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 9.3 Environment Configuration

All secrets and environment-specific settings are managed via `.env` file (never committed to source control):

```
FLASK_ENV=production
SECRET_KEY=<cryptographically-random-256-bit-key>
DATABASE_URL=sqlite:////var/app/data/appointments.db
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=<key>
FROM_EMAIL=noreply@appointmentapp.com
SESSION_COOKIE_SECURE=True
RATE_LIMIT_STORAGE=memory
```

### 9.4 Cloud Deployment Options (Future)

| **Platform** | **Recommended Services**                                          |
|--------------|-------------------------------------------------------------------|
| AWS          | EC2 t3.small, RDS PostgreSQL (migration), SES, S3, CloudFront    |
| Azure        | App Service (B1), Azure Database for PostgreSQL, SendGrid        |
| GCP          | Cloud Run (Flask container), Cloud SQL PostgreSQL, Cloud Storage  |
| Heroku       | Eco Dyno (MVP), PostgreSQL addon, SendGrid addon                  |

---

## 10. Integration Points

### 10.1 Email Service Integration (MVP)

| **Attribute**       | **Detail**                                            |
|---------------------|-------------------------------------------------------|
| Primary Provider    | SendGrid (transactional email API)                    |
| Alternative         | AWS SES (lower cost at volume)                        |
| Trigger Events      | Booking confirmed (F-016), Appointment cancelled (F-019) |
| Delivery Mode       | Synchronous with background thread (MVP); Celery queue (future) |
| Failure Handling    | Log failure; do not fail the booking transaction      |
| Template Format     | HTML + plain text (Jinja2 templates)                  |
| Volume (MVP)        | ~10,000 emails/month (within free tier of both providers) |

**SendGrid Integration:**
```
HTTP POST https://api.sendgrid.com/v3/mail/send
Headers: Authorization: Bearer {SENDGRID_API_KEY}
Body: {
  "personalizations": [{"to": [{"email": patient_email}]}],
  "from": {"email": "noreply@appointmentapp.com"},
  "subject": "Appointment Confirmed — {booking_id}",
  "content": [{"type": "text/html", "value": rendered_template}]
}
```

### 10.2 Planned Future Integrations (Post-MVP)

The following are **not implemented in MVP** but the architecture accommodates them:

| **Integration**         | **Future Feature**            | **MVP Hook Point**                          |
|-------------------------|-------------------------------|---------------------------------------------|
| SMS / Push Notifications | Appointment reminders         | Email service abstracted behind interface    |
| Calendar (Google/Outlook)| Calendar sync                 | `booking_id` as stable reference key         |
| Payment Gateway          | Appointment deposits          | `appointments` table has no payment fields yet |
| EHR Systems              | Medical history               | Patient identified by `user.id` as anchor    |
| Analytics Platform        | Business reporting           | `audit_log` and `appointments` as data source |

---

## 11. Constraints & Assumptions

### 11.1 Technical Constraints

| **Constraint**                   | **Impact**                                                             |
|----------------------------------|------------------------------------------------------------------------|
| SQLite for MVP                   | Single writer at a time; WAL mode mitigates but limits write throughput |
| No distributed caching           | Rate limiting is in-memory; does not survive restarts or multi-server  |
| Synchronous email                | Email failure in background thread will not fail booking but adds latency |
| No background job queue          | Scheduled tasks (e.g., slot cleanup) must be cron-based for MVP        |
| Single timezone (MVP)            | All times stored and displayed in single configured timezone            |
| 30-minute slot duration fixed    | No support for variable appointment lengths in MVP                      |
| No file upload in MVP            | Doctor `photo_url` is a URL string; no file storage service configured  |

### 11.2 Business Assumptions

| **Assumption**                                     | **Source**         |
|----------------------------------------------------|--------------------|
| Single healthcare practice (one admin)             | BRD §4.1           |
| All doctors in same timezone                       | BRD §4.2           |
| Patients self-register (no staff-assisted booking) | BRD §3.2           |
| 30-minute appointment slots are universal          | BRD §4.2 / Epics   |
| HIPAA compliance deferred to Phase 2               | BRD §4.2           |
| No payment at booking time                         | BRD §4.2           |
| Doctor profiles managed by admin only              | EP-005             |
| Single admin user for MVP                          | EP-005             |
| English language only                              | BRD §4.2           |
| US phone number format for MVP                     | F-001              |

### 11.3 Data Constraints

- SQLite maximum database size: effectively unlimited (up to 281 TB), well within MVP scope
- SQLite WAL mode: supports multiple concurrent readers; single concurrent writer
- Appointment history retained indefinitely (soft delete only) for MVP
- No data archival or purge strategy for MVP (post-MVP consideration)

---

## 12. Risks & Open Issues

### 12.1 Risk Register

| **Risk ID** | **Risk Description**                              | **Probability** | **Impact** | **Mitigation Strategy**                                       |
|-------------|---------------------------------------------------|-----------------|------------|---------------------------------------------------------------|
| R-001       | SQLite write contention under peak concurrent load | Medium          | High       | WAL mode; queue writes; monitor; migrate to PostgreSQL if triggered |
| R-002       | Email delivery failures (SendGrid outage)          | Low             | Medium     | Log failures; user sees booking confirmation on screen; retry queue in Phase 2 |
| R-003       | Rate limiting bypass (distributed IP spoofing)     | Low             | Medium     | NGINX IP-based limits; upgrade to Redis rate limiting for Phase 2 |
| R-004       | Session fixation / hijacking                       | Low             | High       | Session rotation on login; httpOnly+Secure cookies; HTTPS enforced |
| R-005       | Double-booking under extreme concurrency           | Very Low        | High       | DB UNIQUE constraint as final safety net; tested under load   |
| R-006       | Scope creep extending 8–10 week timeline           | Medium          | High       | Strict MVP feature boundary; change control process            |
| R-007       | SQLite file corruption                             | Very Low        | High       | WAL mode reduces risk; daily backups; integrity check on startup |

### 12.2 Open Issues

| **Issue ID** | **Description**                                    | **Status**   | **Owner**  |
|--------------|----------------------------------------------------|--------------|------------|
| OI-001       | Password reset flow (deferred) — communicate to users | Open      | Product    |
| OI-002       | Email template design not finalized                | Open         | UX         |
| OI-003       | Static doctor photo storage (URL vs. upload)       | Decision needed | Arch    |
| OI-004       | Backup restore procedure to be documented          | Open         | DevOps     |
| OI-005       | US phone format only — international expansion     | Deferred MVP | Product    |

---

*End of App_HLD.md — Version 1.0*  
*Cross-reference: `docs/App_DataModel.md` for physical database schema*  
*Cross-reference: `docs/BRD.md` §2–§4 for business requirements*  
*Cross-reference: `docs/Epics.md` EP-001 to EP-005*  
*Cross-reference: `docs/Features.md` F-001 to F-025*
