# SkillForge ⚔️

[![CI / Quality Gates](https://github.com/MrinmoyShib/skillforge/actions/workflows/ci.yml/badge.svg)](https://github.com/MrinmoyShib/skillforge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django 5.2 LTS](https://img.shields.io/badge/Django-5.2_LTS-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis 7](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Judge0 CE](https://img.shields.io/badge/Judge0_CE-v1.13.1-black?logo=docker&logoColor=white)](https://judge0.com)
[![OpenAPI 3.0](https://img.shields.io/badge/OpenAPI-3.0-85EA2D?logo=openapiinitiative&logoColor=black)](http://localhost:8000/api/docs/swagger/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **SkillForge** is an enterprise-grade competitive programming, skill assessment, and developer learning platform engineered for $0 external subscription costs. It features real-time sandboxed code execution, an in-browser Monaco IDE, multi-language tracks (**Python 3**, **JavaScript**, and **C++**), guided engineering projects, anti-farming progression mechanics, secure OTP authentication, and a dual admin command center with an in-studio sandbox verification runner.

---

## 📑 Table of Contents

- [Core Features](#-core-features)
- [Curriculum & Track Matrix](#-curriculum--track-matrix)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start (Docker)](#-quick-start-docker)
- [Default Login Credentials](#-default-login-credentials)
- [Service URLs & Port Map](#-service-urls--port-map)
- [Environment Variables Reference](#-environment-variables-reference)
- [REST API Reference](#-rest-api-reference)
- [Repository Structure](#-repository-structure)
- [Development vs. Production](#-development-vs-production)
- [Testing & Quality Gates](#-testing--quality-gates)
- [Security & Governance](#-security--governance)
- [License](#-license)

---

## ⚡ Core Features

### 1. 🐍 Multi-Language Tracks (Python, JavaScript, C++)
- **3 Dedicated Tracks**:
  - **Python 3 (`python`)**: Idiomatic Python, data structures, recursion, list comprehensions, backend algorithmic patterns.
  - **JavaScript (`javascript`)**: Modern ES6+, functional array transformations, asynchronous flow, web algorithmic logic.
  - **C++ (`cpp`)**: High-performance systems programming, STL containers, pointer manipulation, and competitive programming.
- **300 Curated Challenges (100 per track)**:
  - Spans 5 calibrated progression tiers from basic syntax to grandmaster algorithms.
- **1,200 Test Cases**:
  - Visible sample test cases for rapid in-browser testing.
  - Hidden evaluation test cases with anti-leak protection (strictly hidden from student API responses).

### 2. 🛡️ Isolated Sandboxed Execution (Judge0 CE)
- **Self-Hosted Linux `isolate` Sandbox**: Evaluates untrusted code in hardened Linux cgroups with strict memory, process, and CPU wall-clock limits.
- **Complete Network Isolation**: Student submissions cannot initiate external outbound or inbound network connections.
- **Asynchronous Processing**: Dispatched via Celery workers backed by Redis, polling Judge0 until terminal verdicts (`ACCEPTED`, `WRONG_ANSWER`, `TIME_LIMIT_EXCEEDED`, `RUNTIME_ERROR`, `COMPILATION_ERROR`).
- **Resilience Engine**: Built-in fallback protection during offline development or maintenance modes.

### 3. 💻 In-Browser Monaco IDE & Live Verdicts
- Powered by the **Monaco Editor** (the engine behind VS Code) with syntax highlighting, automatic indentation, and keyboard shortcuts.
- Interactive test case drawer supporting custom inputs, sample execution, and real-time execution telemetry (runtime in ms, memory in KB).
- Formatted compile error and runtime diagnostics rendered cleanly in the console output pane.

### 4. 📈 Anti-Farming XP Engine & Progression Tiers
- **Calibrated XP Formula**: Earn XP proportional to challenge difficulty (Level 1: 50 XP to Level 5: 300 XP).
- **Anti-Farming DB Protection**: Composite database uniqueness constraints prevent users from repeatedly farming XP on already-solved problems.
- **Activity Audit Trail**: Every submission, solve verdict, XP delta, and level-up is immutably logged with timestamps.
- **5 Mastery Levels**: *Apprentice* → *Scout* → *Craftsman* → *Architect* → *Grandmaster*.

### 5. 🛠️ Guided Engineering Projects & Labs
- Step beyond one-off algorithmic puzzles into multi-milestone software engineering projects.
- Projects include building CLI utilities, key-value stores, caching layers, and parsers.
- In-workspace milestone test harnesses verify user implementations step-by-step before unlocking subsequent milestones.

### 6. 🔐 Secure OTP Authentication & Email Verification
- **Email OTP Verification**: 6-digit one-time passcode verification on registration via SMTP (Gmail, Brevo, or local console).
- **Secure Email Change**: Re-authenticates current password, dispatches confirmation OTP to the new email, and sends a security alert to the previous email.
- **JWT in HttpOnly Cookies**: Access and refresh tokens stored in `HttpOnly`, `SameSite=Lax` cookies to prevent XSS token theft, with automatic silent refresh.

### 7. 🏆 Achievements & Dense-Rank Leaderboard
- **Automated Achievement System**: Automatically unlocks badges based on solve counts, language track milestones, and streaks.
- **Dense-Rank Global Leaderboard**: Fair tie-handling dense ranking with a Top 3 Podium and sticky user placement card.

### 8. 👤 Developer Profile & Recruiter-Ready Portfolio
- **Customizable Profile (`/settings`)**: Avatar picker, bio, skills, location, and social links with built-in URL sanitization against XSS.
- **Public Portfolio (`/portfolio/:username`)**: Recruiter-ready showcase displaying verified solve statistics, completed projects, and track mastery breakdown.
- **Multi-Channel Social Sharing**: Instant share buttons for LinkedIn, Twitter/X, WhatsApp, Gmail, and one-click link copying.

### 9. 🎛️ Dual Enterprise Admin Backoffice
- **React Command Center (`/admin/*`)**:
  - Protected by `AdminRoute` (enforces `is_staff`).
  - **Cluster Telemetry**: Real-time heartbeat checks for PostgreSQL, Redis, and Judge0 sandbox.
  - **Problem Studio**: Full CRUD with Markdown editor and **In-Studio Sandbox Verification Runner** (`POST /api/v1/admin/problems/:id/verify/`) testing author solutions against test cases before publishing.
  - **Guided Projects Curator**: Author projects, milestones, and automated test harnesses.
  - **Developer Moderation**: Searchable directory, student intel drilldown, staff privilege toggles, and atomic manual XP adjustments.
  - **Submissions Audit**: Global real-time submission stream with code inspector and one-click re-judging.
- **Django Admin (`http://localhost:8000/admin/`)**:
  - Inlined `TestCaseInline` and `ProjectMilestoneInline` for direct database management.
  - Bulk actions: `publish_selected` and `unpublish_selected`.

---

## 📊 Curriculum & Track Matrix

SkillForge features **300 total challenges** evenly divided across 3 language tracks:

| Tier | Level Name | Problems / Track | Total Problems | XP / Problem | Core Topics Covered |
|:---:|:---:|:---:|:---:|:---:|:---|
| **Level 1** | Apprentice | 20 | 60 | 50 XP | Variables, I/O, conditionals, arithmetic, loops, basic math |
| **Level 2** | Scout | 20 | 60 | 75 XP | Two-pointers, hash maps, prefix sums, binary search, basic strings |
| **Level 3** | Craftsman | 20 | 60 | 100 XP | Sliding window, intervals, stacks, queues, recursion, basic DP |
| **Level 4** | Architect | 20 | 60 | 150 XP | Trees, BST, graph BFS/DFS, topological sort, heaps, LCS |
| **Level 5** | Grandmaster | 20 | 60 | 250 XP | Dynamic programming, bitmask DP, shortest paths, advanced graphs |
| **Total** | — | **100** | **300** | — | **1,200 Test Cases** |

---

## 🏗️ System Architecture

```
                                  [ User Browser (Port 80 / 5173) ]
                                                   │
                                                   ▼
                       ┌───────────────────────────────────────────────────────┐
                       │              Nginx Reverse Proxy / Vite               │
                       │  - SSL Termination & Security Headers (CSP, HSTS)     │
                       │  - Gzip Compression & Static Asset Cache (1 Year)     │
                       │  - Client-Side SPA Routing (try_files fallback)       │
                       │  - Rate Limiting Zones (10r/m auth, 30r/m api)        │
                       └───────────────┬───────────────────────┬───────────────┘
                                       │                       │
                       Static / Cached Assets       /api/v1/* and /admin/*
                                       │                       │
                                       ▼                       ▼
                         ┌────────────────────────┐  ┌───────────────────┐
                         │   Compiled React 19    │  │   Gunicorn / DRF  │
                         │   SPA (Tailwind v4)    │  │   Django 5.2 LTS  │
                         │   (/usr/share/nginx)   │  │   (3 Workers)     │
                         └────────────────────────┘  └─────────┬─────────┘
                                                               │
                                                    ┌──────────┴──────────┐
                                                    ▼                     ▼
                                               PostgreSQL 16           Redis 7
                                               (Persistent)       (Broker & Cache)
                                                                          │
                                                                          ▼
                                                                    Celery Worker
                                                                          │
                                                                          ▼
                                                                      Judge0 CE
                                                                   (isolate sandbox)
```

---

## 💻 Tech Stack

| Layer | Technology | Version | Purpose & Rationale |
|---|---|---|---|
| **Backend Framework** | Django + DRF | 5.2 LTS / 3.15 | Robust ORM, built-in security, Service & Selector design pattern |
| **Frontend Framework** | React + Vite | 19.0 / 6.0 | Modern concurrent React, ultra-fast Hot Module Replacement (HMR) |
| **Styling** | Tailwind CSS | v4.0 | CSS-first zero-config styling with dark cyber theme (`#0b0f19`, `#131b2e`) |
| **Code Editor** | Monaco Editor | 4.7 | Desktop VS Code in-browser experience with multi-language syntax support |
| **Code Execution** | Judge0 CE | 1.13.1 | Self-hosted, IOI-grade sandboxing using Linux `isolate` cgroups ($0 budget) |
| **Database** | PostgreSQL | 16-alpine | ACID-compliant relational store with JSONField and composite constraints |
| **Cache & Broker** | Redis | 7-alpine | In-memory message broker for Celery and high-speed query caching |
| **Task Queue** | Celery | 5.4+ | Distributed asynchronous submission grading and Judge0 status polling |
| **Authentication** | SimpleJWT | 5.5 | `HttpOnly`, `SameSite=Lax` cookies with token rotation and blacklisting |
| **Email Delivery** | Django SMTP | Built-in | OTP verification emails via Gmail, Brevo, or console backend |

---

## 🚀 Quick Start (Docker)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows / macOS / Linux) with Docker Compose v2+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/MrinmoyShib/skillforge.git
cd skillforge
```

### 2. Configure Environment Variables
Copy the example configuration file:
```bash
cp .env.example .env
```
*(The default values in `.env.example` work out-of-the-box for local Docker development).*

### 3. Launch the Application Stack
```bash
# Start PostgreSQL, Redis, Django API, Celery Worker, and React Frontend
docker compose -f docker/docker-compose.yml up -d
```

### 4. Launch the Judge0 Code Execution Sandbox
```bash
# Start Judge0 Server, Worker, PostgreSQL, and Redis (privileged isolate sandbox)
docker compose -f docker/docker-compose.judge0.yml up -d
```

### 5. Apply Migrations & Seed Initial Curriculum
```bash
# Run database migrations
docker exec -it skillforge-django python manage.py migrate

# Seed default Admin and Student accounts
docker exec -it skillforge-django python manage.py seed_dev_users

# Seed all 300 problems and 1,200 test cases
docker exec -it skillforge-django python manage.py seed_problems
```

---

## 🔑 Default Login Credentials

| Role | Username | Email | Password | Access Level |
|---|---|---|---|---|
| **Administrator** | `admin` | `admin@skillforge.dev` | `AdminPassword123!` | Full Admin Command Center (`/admin`), Problem Studio, Django DB Backdoor |
| **Student (Demo)** | `student` | `student@skillforge.dev` | `StudentPassword123!` | Level 2 developer with 100 XP on C++ track |

---

## 🌐 Service URLs & Port Map

| Service | URL | Description |
|---|---|---|
| **SkillForge Web App** | [http://localhost:5173](http://localhost:5173) | Main React 19 Frontend (Student platform & Dashboard) |
| **Admin Command Center** | [http://localhost:5173/admin](http://localhost:5173/admin) | Cyber React Admin Studio (Requires staff credentials) |
| **Django Direct DB Admin** | [http://localhost:8000/admin/](http://localhost:8000/admin/) | Django Model Administration |
| **REST API Base** | [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) | Backend REST API root |
| **Swagger API Docs** | [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/) | Interactive OpenAPI 3 / Swagger documentation |
| **Redoc API Docs** | [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/) | ReDoc structured API reference |
| **Judge0 Sandbox API** | [http://localhost:2358](http://localhost:2358) | Self-hosted Judge0 CE code execution server |

---

## ⚙️ Environment Variables Reference

| Variable | Default Value | Description |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.dev` | Active Django settings module (`dev` or `prod`) |
| `SECRET_KEY` | `dev-insecure-key-...` | Django cryptographic signing key |
| `DEBUG` | `True` | Enable/disable debug mode (MUST be `False` in prod) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list of valid host headers |
| `DATABASE_URL` | `postgres://...:5432/skillforge` | PostgreSQL connection string |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Redis connection URL for Celery message broker |
| `CELERY_RESULT_BACKEND` | `redis://redis:6379/0` | Redis connection URL for Celery task results |
| `JUDGE0_URL` | `http://judge0-server:2358` | Internal Docker URL for Judge0 CE server |
| `JUDGE0_AUTH_TOKEN` | `skillforge-judge0-dev-token` | Secret authentication token for Judge0 API |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173` | Allowed origins for cross-origin resource sharing |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:5173` | Trusted origins for CSRF protection |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | Email backend (or `.console.EmailBackend` for dev) |
| `EMAIL_HOST` | `smtp.gmail.com` | SMTP host server |
| `EMAIL_PORT` | `587` | SMTP port (typically 587 for TLS) |
| `EMAIL_USE_TLS` | `True` | Enable TLS encryption for outbound email |
| `EMAIL_HOST_USER` | `""` | SMTP sender username / email address |
| `EMAIL_HOST_PASSWORD` | `""` | SMTP app password / API key |
| `DEFAULT_FROM_EMAIL` | `SkillForge <noreply@skillforge.dev>` | From address on outbound notification emails |
| `VITE_API_BASE_URL` | `http://localhost:8000/api/v1` | Frontend API base endpoint URL |

---

## 📡 REST API Reference

| Endpoint | Method | Auth | Description |
|---|:---:|:---:|---|
| **`/auth/register/`** | `POST` | Public | Register new developer and dispatch 6-digit email OTP |
| **`/auth/verify-otp/`** | `POST` | Public | Verify registration OTP and activate user account |
| **`/auth/resend-otp/`** | `POST` | Public | Request a fresh verification OTP |
| **`/auth/login/`** | `POST` | Public | Authenticate and issue `HttpOnly` JWT cookie |
| **`/auth/logout/`** | `POST` | Authenticated | Invalidate JWT cookies and blacklist refresh token |
| **`/auth/token/refresh/`** | `POST` | Cookie | Silent rotation of expired access token |
| **`/auth/me/`** | `GET, PATCH` | Authenticated | Retrieve / update current user profile |
| **`/auth/change-password/`** | `POST` | Authenticated | Change password and invalidate outstanding tokens |
| **`/auth/request-email-change/`**| `POST` | Authenticated | Re-auth password and send OTP to new email |
| **`/auth/confirm-email-change/`**| `POST` | Authenticated | Verify OTP, update email, and alert old email |
| **`/problems/`** | `GET` | Public | List curated problems with track/tier filters |
| **`/problems/:id/`** | `GET` | Public | Problem detail with sample test cases and boilerplate |
| **`/submissions/`** | `POST` | Authenticated | Submit code for sandboxed Judge0 evaluation |
| **`/submissions/:id/`** | `GET` | Authenticated | Poll execution verdict and telemetry |
| **`/projects/`** | `GET, POST` | Authenticated | Browse guided projects and enroll |
| **`/projects/:id/workspace/`** | `GET, POST` | Authenticated | Project workspace and milestone test runner |
| **`/leaderboard/`** | `GET` | Public | Global dense-rank leaderboard |
| **`/portfolio/:username/`** | `GET` | Public | Public developer portfolio and verified statistics |
| **`/dashboard/`** | `GET` | Authenticated | Live developer telemetry and track mastery stats |
| **`/admin/analytics/`** | `GET` | Staff | Platform health and cluster telemetry |
| **`/admin/problems/`** | `GET, POST` | Staff | Problem studio CRUD |
| **`/admin/problems/:id/verify/`** | `POST` | Staff | Pre-publish sandbox solution verification runner |

---

## 📁 Repository Structure

```text
SkillForge/
├── .github/
│   ├── ISSUE_TEMPLATE/         # Bug report & feature request templates
│   ├── workflows/
│   │   └── ci.yml              # GitHub Actions CI quality gates (pytest + build)
│   ├── dependabot.yml          # Automated dependency updates (pip, npm, docker)
│   └── pull_request_template.md # PR checklist and guidelines
├── backend/                    # Django 5.2 LTS Backend
│   ├── apps/
│   │   ├── accounts/           # Auth, OTP, JWT cookies, profile settings
│   │   ├── achievements/       # Badges & automated achievement unlock engine
│   │   ├── admin_api/          # Admin backoffice, telemetry, problem studio
│   │   ├── core/               # Shared models, exceptions, pagination
│   │   ├── dashboard/          # Student telemetry, track mastery & recent activity
│   │   ├── leaderboard/        # Dense rank global leaderboard & top 3 podium
│   │   ├── portfolio/          # Public developer portfolios & social sharing links
│   │   ├── problems/           # 300 problems across Python, JS, C++ (1,200 test cases)
│   │   ├── progress/           # Anti-farming XP engine, levels, activity audit logs
│   │   ├── projects/           # Guided engineering labs & milestone test harnesses
│   │   └── submissions/        # Judge0 CE integration & Celery async queue
│   ├── config/                 # Project settings (base, dev, prod), URLs, Celery
│   ├── entrypoint.prod.sh      # Production backend container entrypoint
│   ├── Dockerfile              # Development Dockerfile
│   ├── Dockerfile.prod         # Production Gunicorn Dockerfile (unprivileged user)
│   └── requirements/           # base.txt, dev.txt, prod.txt
├── frontend/                   # React 19 + Vite SPA (Tailwind CSS v4)
│   ├── src/
│   │   ├── components/         # Layouts, UI primitives, Monaco editor, Toast, Modals
│   │   ├── context/            # AuthContext with silent token refresh
│   │   ├── pages/              # Dashboard, Challenges, Projects, Leaderboard, Admin, Settings
│   │   ├── routes/             # AppRoutes (lazy loaded), ProtectedRoute, AdminRoute
│   │   ├── services/           # Axios client & domain API services
│   │   └── utils/              # Formatters, constants, language utilities
│   ├── Dockerfile              # Development Dockerfile
│   ├── Dockerfile.prod         # Multi-stage production Dockerfile (Nginx + static build)
│   └── nginx.conf              # Production Nginx SPA routing & security headers
├── docker/
│   ├── docker-compose.yml      # Development Compose stack
│   ├── docker-compose.prod.yml # Production Compose stack (Gunicorn + Nginx)
│   ├── docker-compose.judge0.yml # Judge0 CE Compose stack
│   ├── judge0.conf             # Judge0 isolate sandbox configuration
│   └── nginx/
│       └── nginx.prod.conf     # Production Nginx reverse proxy & caching configuration
├── docs/
│   └── architecture.md         # Key architecture decisions and rationale
├── CONTRIBUTING.md             # Developer setup and contribution guidelines
├── SECURITY.md                 # Vulnerability reporting and disclosure policy
├── CHANGELOG.md                # Keep a Changelog version history
├── .env.example                # Development environment template
├── .env.prod.example           # Production environment template
├── .gitattributes              # Line endings enforcement (LF for shell/docker)
├── .gitignore
└── README.md
```

---

## 🚀 Development vs. Production

### Running in Development Mode
In development mode, Django runs with `DEBUG=True` and hot-reloads via `manage.py runserver`, while Vite provides instant Hot Module Replacement (HMR) on port 5173:
```bash
docker compose -f docker/docker-compose.yml up -d
docker compose -f docker/docker-compose.judge0.yml up -d
```

### Running in Production Mode
In production mode:
- Django runs under **Gunicorn WSGI** (3 workers, 2 threads per worker) with `DEBUG=False` and strict security headers (`SECURE_SSL_REDIRECT`, `HSTS`).
- The React 19 frontend is compiled into static assets and served via an **Nginx reverse proxy** with gzip compression, `try_files` SPA routing, and 1-year immutable caching for `/assets/`.
- Rate limiting zones are enforced on `/api/v1/auth/` (10 req/min) and general API routes (30 req/min).
```bash
# 1. Copy production environment variables
cp .env.prod.example .env.prod
# (Fill in your strong passwords and production domain in .env.prod)

# 2. Build and launch the production stack
docker compose -f docker/docker-compose.prod.yml up -d --build
```

---

## 🧪 Testing & Quality Gates

SkillForge maintains an extensive automated test suite covering authentication, permissions, anti-farming constraints, problem authoring, sandbox verification, leveling, and admin moderation:

### Running Backend Unit Tests
```bash
docker exec -it skillforge-django pytest -v
```
**Status**: **68 / 68 tests passing** across all apps.

### Verifying Frontend Production Build
```bash
docker exec -it skillforge-frontend npm run build
```
**Status**: Clean compilation with **0 errors**.

### Automated GitHub Actions CI
On every `push` and `pull_request` to `main`, [`.github/workflows/ci.yml`](.github/workflows/ci.yml) automatically:
1. Provisions PostgreSQL 16 and Redis 7 service containers in GitHub Actions.
2. Executes Django system checks and database migrations.
3. Runs security scans via `pip-audit` and `npm audit`.
4. Runs the full 68-test `pytest` suite with code coverage.
5. Performs a clean `npm ci` and verifies the frontend production build.

---

## 🛡️ Security & Governance

- **Vulnerability Reporting**: See [SECURITY.md](SECURITY.md) for our responsible disclosure policy and contact details.
- **Contributing Guidelines**: See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming conventions, commit formats, and coding standards.
- **Changelog**: Detailed release notes and version history are documented in [CHANGELOG.md](CHANGELOG.md).
- **Architecture Decisions**: Deep architectural context and design rationale are available in [docs/architecture.md](docs/architecture.md).

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
