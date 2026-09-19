# SkillForge ⚔️

[![CI / Quality Gates](https://github.com/MrinmoyShib/skillforge/actions/workflows/ci.yml/badge.svg)](https://github.com/MrinmoyShib/skillforge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)]()
[![Django 5.2 LTS](https://img.shields.io/badge/Django-5.2_LTS-092E20?logo=django&logoColor=white)]()
[![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)]()
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?logo=tailwindcss&logoColor=white)]()
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)]()
[![Redis 7](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)]()
[![Judge0 CE](https://img.shields.io/badge/Judge0_CE-v1.13.1-black?logo=docker&logoColor=white)]()

> **SkillForge** is an enterprise-grade competitive programming, skill assessment, and developer learning platform with zero external subscription costs ($0 budget). It features real-time sandboxed code execution, an in-browser Monaco IDE, multi-language tracks, guided engineering projects, anti-farming progression mechanics, and a dual admin command center with an in-studio sandbox verification runner.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start (Docker)](#-quick-start-docker)
- [Default Login Credentials](#-default-login-credentials)
- [Service URLs & Ports](#-service-urls--ports)
- [Repository Structure](#-repository-structure)
- [Development vs. Production](#-development-vs-production)
- [Testing & Quality Gates](#-testing--quality-gates)
- [API Documentation](#-api-documentation)
- [License](#-license)

---

## ⚡ Key Features

### 1. 🐍 Multi-Language Tracks & 300 Curated Challenges
- **3 Dedicated Tracks**: Python 3 (`python`), JavaScript (`javascript`), and C++ (`cpp`).
- **100 Challenges Per Track (300 Total)**:
  - **Level 1 (Apprentice)**: Syntax, control flow, math, basic strings, loops.
  - **Level 2 (Scout)**: Two-pointers, hash maps, prefix sum, binary search.
  - **Level 3 (Craftsman)**: Intervals, sliding window, stacks/queues, backtracking, dynamic programming.
  - **Level 4 (Architect)**: Heaps, BST, trees, graph BFS/DFS, topological sort, LCS.
  - **Level 5 (Grandmaster)**: Trapping rain water, LIS, shortest paths, bitmask DP, N-Queens.
- **1,200 Test Cases**: Sample visible test cases and private hidden evaluation test cases.

### 2. 🛡️ Isolated Sandboxed Execution (Judge0 CE)
- **Self-Hosted Judge0 CE**: Linux `isolate` sandboxing using kernel cgroups, memory limits, and strict CPU time caps.
- **Asynchronous Evaluation**: Dispatched via Celery workers backed by Redis, with resilience fallback (`DevFallbackEngine`) for offline environments.
- **Anti-Leak Protection**: Hidden evaluation test cases are strictly masked from student API responses.

### 3. 💻 In-Browser Monaco IDE & Live Verdicts
- Full-featured code editor powered by **Monaco Editor** (VS Code engine).
- Integrated test case drawer with custom inputs, sample execution, and real-time execution telemetry (runtime in ms, memory in KB).
- Formatted compile error and runtime error diagnostics.

### 4. 📈 Progression & Anti-Farming XP Engine
- **Progression Tiers**: Apprentice, Scout, Craftsman, Architect, Grandmaster.
- **Anti-Farming DB Protection**: Composite database uniqueness constraints prevent users from repeatedly farming XP on already-solved problems.
- **Activity Audit Trail**: Every solve, XP delta, and level-up is immutably logged with timestamps.

### 5. 📊 Live Telemetry Dashboard & Track Mastery
- Real-time developer metrics: Solved problems, remaining challenges, and points earned per language track.
- Direct deep-links to the next recommended unsolved challenge.
- Recent submissions audit stream with status badges.

### 6. 🏆 Achievements & Dense-Rank Global Leaderboard
- **Automated Achievement Engine**: Unlocks platform badges based on solve milestones and track completion.
- **Dense-Rank Leaderboard**: Accurate tie-handling dense ranking with a Top 3 Podium and sticky user placement card.

### 7. 🛠️ Guided Engineering Projects & Labs
- Multi-milestone guided labs designed to simulate real-world software engineering tasks.
- In-workspace milestone test harnesses verifying developer code step-by-step.
- Enrolled project progress tracking integrated into the live student dashboard.

### 8. 👤 Developer Profile & Account Settings
- **Industry-Standard Settings (`/settings`)**: Avatar picker (preset developer avatars + custom image URLs), editable display name, username, email address, contact phone number, location, and bio.
- **Security Tab**: Password change with current-password validation and automatic JWT cookie rotation.
- **Public Developer Portfolio (`/portfolio/:username`)**: Multi-channel sharing (WhatsApp, LinkedIn, Twitter/X, Gmail, copy link).

### 9. 🎛️ Dual Enterprise Admin Backoffice (Options A + C)
- **Option A (React Command Center at `/admin/*`)**:
  - Protected by `AdminRoute` (enforces `is_staff`).
  - **Cluster Telemetry**: Real-time heartbeat checks for PostgreSQL, Redis, and Judge0 sandbox.
  - **Problem Studio**: Full CRUD with Markdown editor and **In-Studio Sandbox Verification Runner** (`POST /api/v1/admin/problems/:id/verify/`) testing author solutions against test cases before publishing!
  - **Guided Projects Curator**: Author projects, milestones, and automated test harnesses.
  - **Developer Moderation**: Searchable directory, student intel drilldown, staff privilege toggles, and atomic manual XP adjustments.
  - **Submissions Audit**: Global real-time submission stream with code inspector and one-click re-judging.
- **Option C (Enhanced Django Admin at `http://localhost:8000/admin/`)**:
  - Inlined `TestCaseInline` and `ProjectMilestoneInline` for direct database management.
  - Bulk actions: `publish_selected` and `unpublish_selected`.

---

## 🏗️ System Architecture

```
                                  [ User Traffic (Port 80 / 5173) ]
                                                  │
                                                  ▼
                      ┌───────────────────────────────────────────────────────┐
                      │              Nginx Reverse Proxy / Vite               │
                      │  - SSL Termination / Security Headers                 │
                      │  - Gzip / Brotli Compression                          │
                      │  - Static Asset Cache (1 Year Immutable)              │
                      │  - Client-Side SPA Routing (try_files)                │
                      └───────────────┬───────────────────────┬───────────────┘
                                      │                       │
                      Static / Cached Assets       /api/* and /admin/*
                                      │                       │
                                      ▼                       ▼
                        ┌────────────────────────┐  ┌───────────────────┐
                        │   Compiled React 19    │  │   Gunicorn / DRF  │
                        │   SPA (/usr/share/     │  │   Django 5.2 LTS  │
                        │     nginx/html)        │  │   (3 Workers)     │
                        └────────────────────────┘  └─────────┬─────────┘
                                                              │
                                                   ┌──────────┴──────────┐
                                                   ▼                     ▼
                                              PostgreSQL 16           Redis 7
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

| Layer | Technology | Version | Rationale |
|---|---|---|---|
| **Backend Framework** | Django + DRF | 5.2 LTS / 3.15 | Rock-solid ORM, built-in security, standard service/selector architecture |
| **Frontend Framework** | React + Vite | 19.0 / 6.0 | Latest React concurrency, blazing fast HMR with Vite |
| **Styling** | Tailwind CSS | v4.0 | Zero-config CSS-first engine, dark cyber theme (`#0b0f19`, `#131b2e`) |
| **Code Editor** | Monaco Editor | 4.7 | VS Code in-browser editing experience with syntax highlighting |
| **Code Execution** | Judge0 CE | 1.13.1 | Self-hosted, IOI-grade sandboxing using Linux `isolate` cgroups ($0 budget) |
| **Database** | PostgreSQL | 16-alpine | ACID-compliant relational database with JSONField support |
| **Cache & Broker** | Redis | 7-alpine | In-memory store for Celery task dispatch and fast session caching |
| **Task Queue** | Celery | 5.4+ | Distributed asynchronous submission evaluation and Judge0 polling |
| **Auth** | SimpleJWT | 5.5 | `HttpOnly`, `SameSite=Lax` cookies with silent token refresh (XSS protection) |

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

### 2. Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```
*(The default values in `.env.example` work out-of-the-box for local development).*

### 3. Start the Application Stack
```bash
# Start PostgreSQL, Redis, Django API, Celery Worker, and React Frontend
docker compose -f docker/docker-compose.yml up -d
```

### 4. Start the Judge0 Code Execution Sandbox
```bash
# Start Judge0 Server, Worker, PostgreSQL, and Redis (privileged isolate sandbox)
docker compose -f docker/docker-compose.judge0.yml up -d
```

### 5. Seed Initial Data
Run database migrations and seed users and the 300-problem curriculum:
```bash
# Apply migrations
docker exec -it skillforge-django python manage.py migrate

# Seed Admin and Student accounts
docker exec -it skillforge-django python manage.py seed_dev_users

# Seed the 300 problems and 1,200 test cases
docker exec -it skillforge-django python manage.py seed_problems
```

---

## 🔑 Default Login Credentials

| Role | Username | Email | Password | Access Level |
|---|---|---|---|---|
| **Administrator** | `admin` | `admin@skillforge.dev` | `AdminPassword123!` | Full Admin Command Center (`/admin`), Problem Studio, Django DB Backdoor |
| **Student (Demo)** | `student` | `student@skillforge.dev` | `StudentPassword123!` | Level 2 developer with 100 XP on C++ track |

---

## 🌐 Service URLs & Ports

| Service | URL | Description |
|---|---|---|
| **SkillForge Web App** | [http://localhost:5173](http://localhost:5173) | Main React 19 Frontend (Student platform & Dashboard) |
| **Admin Command Center** | [http://localhost:5173/admin](http://localhost:5173/admin) | Cyber React Admin Studio (Requires `admin` login) |
| **Django Direct DB Admin** | [http://localhost:8000/admin/](http://localhost:8000/admin/) | Django Model Administration (Option C) |
| **REST API Base** | [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) | Backend REST API endpoints |
| **Swagger API Docs** | [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/) | Interactive OpenAPI 3 / Swagger documentation |
| **Redoc API Docs** | [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/) | ReDoc API documentation viewer |
| **Judge0 Sandbox API** | [http://localhost:2358](http://localhost:2358) | Self-hosted Judge0 CE code execution server |

---

## 📁 Repository Structure

```text
SkillForge/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI quality gates (pytest + build)
├── backend/                    # Django 5.2 LTS Backend
│   ├── apps/
│   │   ├── accounts/           # Auth, JWT HttpOnly cookies, settings & user profiles
│   │   ├── achievements/       # Badges & automated achievement unlock engine
│   │   ├── admin_api/          # Admin backoffice, telemetry, problem & project studio
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
│   │   ├── components/         # Layouts, UI primitives, Monaco editor, modals
│   │   ├── context/            # AuthContext with silent token refresh
│   │   ├── pages/              # Dashboard, Challenges, Projects, Leaderboard, Admin, Settings
│   │   ├── routes/             # AppRoutes, ProtectedRoute, AdminRoute
│   │   ├── services/           # Axios client & domain API services
│   │   └── utils/              # Formatters, constants, helpers
│   ├── Dockerfile              # Development Dockerfile
│   └── Dockerfile.prod         # Multi-stage production Dockerfile (Nginx + static build)
├── docker/
│   ├── docker-compose.yml      # Development Compose stack
│   ├── docker-compose.prod.yml # Production Compose stack (Gunicorn + Nginx)
│   ├── docker-compose.judge0.yml # Judge0 CE Compose stack
│   ├── judge0.conf             # Judge0 isolate sandbox configuration
│   └── nginx/
│       └── nginx.prod.conf     # Production Nginx reverse proxy & caching configuration
├── docs/
│   └── architecture.md         # Key architecture decisions and rationale
├── .env.example                # Development environment template
├── .env.prod.example           # Production environment template
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
In production mode, Django runs under **Gunicorn WSGI** (3 workers, 2 threads per worker) with `DEBUG=False` and strict security headers, behind an **Nginx reverse proxy** serving the compiled React 19 SPA directly from memory with gzip compression and 1-year immutable caching for `/assets/`:
```bash
# 1. Copy production environment variables
cp .env.prod.example .env.prod
# (Fill in your strong passwords and production domain in .env.prod)

# 2. Build and launch the production stack
docker compose -f docker/docker-compose.prod.yml up -d --build
```

---

## 🧪 Testing & Quality Gates

The codebase includes an extensive automated test suite covering authentication, permissions, anti-farming constraints, problem authoring, sandbox verification, leveling, and admin moderation:

### Running Backend Unit Tests in Docker
```bash
docker exec -it skillforge-django pytest -v
```
**Result**: **68 / 68 tests passing** across all apps.

### Verifying Frontend Production Build
```bash
docker exec -it skillforge-frontend npm run build
```
**Result**: Clean compilation with **0 errors**.

### Automated GitHub Actions CI
On every `push` and `pull_request` to `main`, [`.github/workflows/ci.yml`](.github/workflows/ci.yml) automatically:
1. Provisions PostgreSQL 16 and Redis 7 service containers in GitHub Actions.
2. Executes Django system checks and migrations.
3. Runs the full 68-test `pytest` suite with code coverage.
4. Performs a clean `npm ci` and verifies the frontend production build.

---

## 📖 API Documentation

SkillForge includes automated OpenAPI 3 schema generation via `drf-spectacular`:
- **Swagger UI**: Visit [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/) to interactively test endpoints.
- **ReDoc**: Visit [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/) for structured API reference documentation.
- **OpenAPI Schema**: Download raw OpenAPI 3 JSON schema at `http://localhost:8000/api/schema/`.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
