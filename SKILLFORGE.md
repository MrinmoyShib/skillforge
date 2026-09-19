# 🚀 SkillForge — The Complete Beginner-to-Expert Master Guide

Welcome to **SkillForge**! If you are a newcomer to programming, web development, or this specific repository, **do not worry**. This document is designed specifically for you.

By the end of this guide, you will understand:
1. **What SkillForge is** and the real-world problem it solves.
2. **The complete tech stack** (what technologies are used, why they were chosen, and how they work together).
3. **The file and folder structure** (what every single file and folder does and where specific features live).
4. **The backend architecture** (Django, REST Framework, Service & Selector pattern, Celery, Redis, PostgreSQL).
5. **The frontend architecture** (React 19, Vite, Tailwind CSS v4, React Router, Monaco Editor, Axios).
6. **How code execution works** (how user code runs safely in a sandboxed execution engine without hacking the server).
7. **How the project was made** (the step-by-step evolution of building this platform from scratch).
8. **How to clone, run, and test the project** on your own computer from GitHub.

---

## 📑 Table of Contents
- [1. What is SkillForge?](#1-what-is-skillforge)
- [2. High-Level Architecture](#2-high-level-architecture)
- [3. The Tech Stack Explained](#3-the-tech-stack-explained)
- [4. Repository Blueprint (File & Folder Guide)](#4-repository-blueprint-file--folder-guide)
  - [Root Configuration Files](#root-configuration-files)
  - [Docker Directory (`docker/`)](#docker-directory-docker)
  - [Backend Directory (`backend/`)](#backend-directory-backend)
  - [Frontend Directory (`frontend/`)](#frontend-directory-frontend)
- [5. Backend Deep-Dive: Architecture & The 11 Django Apps](#5-backend-deep-dive-architecture--the-11-django-apps)
- [6. Frontend Deep-Dive: React 19 Architecture](#6-frontend-deep-dive-react-19-architecture)
- [7. How Sandboxed Code Execution Works (Judge0 + Celery)](#7-how-sandboxed-code-execution-works-judge0--celery)
- [8. How Was This Project Made? (Build Blueprint)](#8-how-was-this-project-made-build-blueprint)
- [9. How to Clone, Setup & Run This Project (Step-by-Step)](#9-how-to-clone-setup--run-this-project-step-by-step)
- [10. Frequently Asked Questions & Troubleshooting](#10-frequently-asked-questions--troubleshooting)

---

## 1. What is SkillForge?

**SkillForge** is an open-source, full-stack, enterprise-grade developer learning and competitive programming platform. Think of it as a blend between **LeetCode**, **Duolingo**, and **GitHub**:

- 🧠 **Curated Algorithmic Problem Solving**: 300 curated challenges across 3 dedicated language tracks (**Python**, **JavaScript**, and **C++**), ranging from Level 1 (Apprentice) to Level 5 (Grandmaster).
- ⚡ **Real-Time Sandboxed Code Execution**: Users can write code directly in an in-browser code editor (Monaco Editor, the engine behind VS Code), submit their solution, and have it compiled and executed in real-time inside an isolated Linux sandbox.
- 🎮 **Gamified Progression Engine**: Users earn Experience Points (XP), gain levels, maintain daily problem-solving streaks, and automatically unlock platform achievement badges.
- 🏆 **Global Leaderboard**: A competitive ranking system calculating dense ranks and displaying top podium finishers and relative student placement.
- 🛠️ **Verified Guided Engineering Projects**: Hands-on development labs with sequential milestone testing that guide learners through building real-world software.
- 🌐 **Public Developer Portfolio**: Every developer gets a sleek, shareable public portfolio showcasing their verified solves, project completions, and social profiles (WhatsApp, LinkedIn, Twitter, Email).
- 🛡️ **Enterprise Admin Backoffice Studio**: A secure administrative command center where instructors and platform owners can manage users, inspect submissions, re-judge code, author new problems, and curate guided projects with automated sandbox testing.

---

## 2. High-Level Architecture

Here is how all the pieces of SkillForge connect with one another:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          USER'S BROWSER                                │
│                                                                        │
│    React 19 (Single Page Application) + Tailwind CSS v4                │
│    Monaco Code Editor (VS Code Engine) + React Router v7               │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │  HTTP / REST API (JSON)
                                   │  HttpOnly JWT Cookies + CSRF Token
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DJANGO REST API SERVER                          │
│                                                                        │
│    Django 5.2 LTS + Django REST Framework (DRF)                        │
│    - Authentication & Permissions (HttpOnly Cookies)                   │
│    - 11 Modular Django Apps (Problems, Submissions, Projects, etc.)   │
│    - Service & Selector Pattern (Clean Business Logic)                 │
└──────────────┬───────────────────┬──────────────────────┬──────────────┘
               │                   │                      │
       Read / Write DB     Cache / Message Broker   Dispatch Tasks
               │                   │                      │
               ▼                   ▼                      ▼
      ┌─────────────────┐ ┌─────────────────┐   ┌─────────────────┐
      │  PostgreSQL 16  │ │     Redis 7     │   │  Celery Worker  │
      │  (Relational    │ │  (In-Memory DB  │   │  (Background    │
      │   Database)     │ │   & Job Queue)  │   │   Task Queue)   │
      └─────────────────┘ └─────────────────┘   └────────┬────────┘
                                                         │
                                               Execute Code Safely
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │    Judge0 CE    │
                                                │ (Isolated Linux │
                                                │  Code Sandbox)  │
                                                └─────────────────┘
```

---

## 3. The Tech Stack Explained

### Frontend Stack (What runs in the user's browser)
1. **React 19**: The modern industry-standard JavaScript library for building user interfaces. It uses components (reusable pieces of UI) and a Virtual DOM for ultra-fast screen updates.
2. **Vite**: A next-generation frontend build tool. Unlike older tools like Webpack or Create React App, Vite uses native ES modules to start the development server in milliseconds and bundles the code efficiently for production.
3. **Tailwind CSS v4**: A utility-first CSS framework. Rather than writing traditional CSS files with hundreds of custom classes, Tailwind allows you to style elements directly using pre-defined utility classes like `flex`, `p-4`, `text-white`, and `bg-slate-900`.
4. **React Router v7**: Enables client-side navigation without page reloads. When you click "Leaderboard" or "Challenges", the page changes instantly without refreshing the browser.
5. **Axios**: A promise-based HTTP client used to send requests from the React frontend to the Django backend. It includes request and response interceptors to automatically attach CSRF tokens and silently refresh expired JWT tokens.
6. **@monaco-editor/react**: The Monaco Editor is the actual code editor that powers Microsoft VS Code. It provides syntax highlighting, auto-indentation, and line numbers directly inside the web browser.
7. **Recharts**: A composable charting library built on React components and SVG, used on the dashboard for visualizing solved challenges and XP growth.

### Backend Stack (What runs on the server)
1. **Python 3.12 & Django 5.2 LTS**: Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It handles database modeling, migrations, security, and administration out of the box.
2. **Django REST Framework (DRF)**: A powerful and flexible toolkit for building Web APIs on top of Django. DRF converts Python database models into JSON data that the React frontend can consume.
3. **PostgreSQL 16**: An enterprise-grade, open-source object-relational database system known for reliability, data integrity, and support for complex SQL queries and relational constraints.
4. **Redis 7**: An extremely fast in-memory key-value data store. In SkillForge, Redis serves two purposes:
   - It acts as the message broker for Celery (storing jobs until workers pick them up).
   - It caches frequently accessed data.
5. **Celery 5.6**: A distributed task queue. When a user submits code, evaluating it against multiple test cases can take several seconds. Instead of making the web server freeze while waiting, Django hands the job to Celery to process in the background.
6. **Judge0 Community Edition (CE)**: A robust, open-source online code execution system. It executes untrusted user code inside a Linux `isolate` sandbox with strict limits on CPU time, memory, file size, and network access (blocking malicious attempts to hack the server).
7. **SimpleJWT**: A JSON Web Token (JWT) authentication plugin for DRF. In SkillForge, JWT tokens are transmitted inside `HttpOnly`, `SameSite=Lax` cookies, protecting them against Cross-Site Scripting (XSS) attacks.
8. **drf-spectacular**: Automatically generates OpenAPI 3.0 schemas and interactive Swagger/Redoc API documentation.

### DevOps & Infrastructure
1. **Docker & Docker Compose**: Packages every piece of the application (Postgres, Redis, Django, Celery, React, Judge0) into lightweight, portable containers so the platform runs identically on Windows, Mac, or Linux without manual installation of dependencies.
2. **Nginx**: A high-performance reverse proxy and web server used in production to route traffic, serve static files, and handle SSL encryption.
3. **Gunicorn**: A Python WSGI HTTP server used in production to run multiple concurrent workers for the Django application.

---

## 4. Repository Blueprint (File & Folder Guide)

Here is a map of the repository with an explanation of every file and folder.

```
SkillForge/
├── .github/                      # GitHub configurations
│   └── workflows/
│       └── ci.yml                # Automated GitHub Actions test & build pipeline
├── backend/                      # Django Python Backend
│   ├── apps/                     # The 11 modular Django applications
│   ├── config/                   # Django project configuration & settings
│   ├── requirements/             # Python dependency requirements files
│   ├── Dockerfile                # Development Docker container definition
│   ├── Dockerfile.prod           # Production Docker container definition
│   ├── entrypoint.prod.sh        # Startup script for production backend
│   └── manage.py                 # Django command-line management tool
├── docker/                       # Docker Compose and container configs
│   ├── nginx/                    # Production Nginx reverse proxy configuration
│   ├── docker-compose.yml        # Development Docker stack (Postgres, Redis, Django, Celery, React)
│   ├── docker-compose.judge0.yml # Judge0 sandboxed code execution stack
│   ├── docker-compose.prod.yml   # Full production multi-container stack
│   ├── judge0.conf               # Sandbox security and resource limit configuration
│   └── entrypoint.prod.sh        # Container startup script
├── docs/                         # Project documentation and architectural records
│   └── architecture.md           # Architectural Decision Records (ADRs)
├── frontend/                     # React 19 Frontend
│   ├── src/                      # Application source code (components, pages, services)
│   ├── public/                   # Static assets (favicons, public images)
│   ├── Dockerfile                # Frontend development container definition
│   ├── Dockerfile.prod           # Frontend production multi-stage build container
│   ├── index.html                # Single-page application HTML entry point
│   ├── package.json              # Node.js dependencies and npm scripts
│   ├── vite.config.js            # Vite build tool and dev server configuration
│   ├── jest.config.cjs           # Jest unit testing configuration
│   └── babel.config.cjs          # Babel JavaScript transpiler configuration
├── .env.example                  # Template for development environment variables
├── .env.prod.example             # Template for production environment variables
├── .gitignore                    # Files and folders ignored by Git
├── README.md                     # High-level project overview and quickstart
└── SKILLFORGE.md                 # THIS FILE: The complete project master manual
```

---

## 5. Backend Deep-Dive: Architecture & The 11 Django Apps

### The Service & Selector Architectural Pattern
Most Django tutorials put business logic directly inside views or database models. In a large project like SkillForge, this leads to messy, unmaintainable code ("fat views" or "fat models").

Instead, SkillForge uses the **Service & Selector Pattern**:
- **Models (`models.py`)**: Define only the database schema, fields, and constraints.
- **Selectors (`selectors/`)**: Functions that only *read* data from the database (queries, filtering, analytics).
- **Services (`services/`)**: Functions that *write* or *modify* data (creating submissions, awarding XP, updating profiles).
- **Serializers (`serializers/`)**: Validate input JSON and format output JSON.
- **Views (`apis/`)**: Very thin controllers. They receive the HTTP request, call the appropriate Service or Selector, and return the response.

---

### The 11 Django Apps

#### 1. `apps.core`
The foundational app containing reusable utilities for the rest of the backend:
- `models.py`: Defines `TimeStampedModel`, an abstract base model with `created_at` and `updated_at` timestamps inherited by almost every database table.
- `pagination.py`: Defines `StandardPagination` (`page_size=20`, max 100) ensuring uniform pagination across the API.
- `exceptions.py`: Custom exception handler that wraps any DRF error into a clean, consistent JSON error envelope (`{"detail": "...", "code": "..."}`).
- `apis/views.py`: Provides the `/api/v1/` health-check endpoint that tests database connectivity.

#### 2. `apps.accounts`
Manages users, authentication, and developer profiles:
- `models.py`: Defines `UserProfile` (one-to-one with Django's `User`) storing avatars, bio, phone number, location, and social links (GitHub, LinkedIn, Twitter, Website).
- `authentication.py`: `JWTCookieAuthentication` reads JWT access tokens directly from secure `HttpOnly` cookies rather than `Authorization: Bearer` headers.
- `services/auth_services.py`: Handles user registration, profile updates, and password changes.
- `apis/views.py`: Endpoints for `CSRFTokenView`, `RegisterAPI`, `LoginAPI`, `LogoutAPI`, `CookieTokenRefreshAPI`, `MeAPI`, and `ChangePasswordAPI`.

#### 3. `apps.problems`
The competitive programming curriculum:
- `models.py`:
  - `Problem`: Challenge title, slug, description, difficulty (`easy`, `medium`, `hard`), challenge level (1–5), XP reward, time limit, memory limit.
  - `TestCase`: Input/output pairs. Test cases have an `is_sample` flag. If `is_sample=True`, students can see it as an example. If `is_sample=False`, it is a **hidden evaluation test case** used to prevent hardcoding solutions.
  - `StarterCode`: Default template code provided to students for Python, JavaScript, and C++.
  - `Language` & `Tag`: Supported programming languages and algorithmic topics (Dynamic Programming, Binary Search, Trees, etc.).
- `data/`: Contains the 100 core problems categorized by difficulty:
  - `level1.py`: 20 Apprentice challenges (Syntax, math, strings, loops).
  - `level2.py`: 20 Scout challenges (Pointers, hash maps, prefix sums, binary search).
  - `level3.py`: 25 Craftsman challenges (Sliding window, stack, backtracking, DP).
  - `level4.py`: 20 Architect challenges (Heaps, BSTs, BFS/DFS, topological sort).
  - `level5.py`: 15 Grandmaster challenges (Shortest paths, bitmask DP, N-Queens).
  - `catalog.py`: Aggregates the curriculum with starters and test cases.
- `management/commands/seed_problems.py`: Seeder script that populates the database with **300 challenges** (100 per language track) and **1,200 test cases**.

#### 4. `apps.submissions`
Handles code submissions, grading, and execution:
- `models.py`:
  - `Submission`: Stores submitted source code, language, status (`PENDING`, `PROCESSING`, `ACCEPTED`, `WRONG_ANSWER`, `TIME_LIMIT_EXCEEDED`, `COMPILATION_ERROR`, `RUNTIME_ERROR`), total execution time, and memory used.
  - `SubmissionResult`: Breakdown of the execution verdict for each individual test case.
- `tasks.py`: Celery background task `evaluate_submission_task` that runs asynchronously when a submission is created.
- `execution/`:
  - `base.py`: Abstract execution engine interface.
  - `judge0.py`: Production execution engine interfacing with the Judge0 REST API.
  - `dev_fallback.py`: Local fallback engine for development if Judge0 is offline.

#### 5. `apps.progress`
The gamification and leveling system:
- `models.py`:
  - `UserProgress`: Tracks total XP, current level, challenges solved, and active streak. Has a database constraint preventing duplicate XP farming on the same problem.
  - `LevelRequirement`: Defines XP thresholds required to reach levels 1 through 100.
  - `ActivityLog`: Records daily problem-solving activity for GitHub-style contribution heatmaps.
- `services/leveling.py`: Calculates XP awards and triggers level-up events.

#### 6. `apps.dashboard`
Aggregates telemetry for the user's home screen:
- `selectors/dashboard_selectors.py`: Gathers user level, current streak, solved counts per language track (Python, JavaScript, C++), recent submissions, and next recommended unsolved problems.
- `apis/views.py`: Exposes `GET /api/v1/dashboard/`.

#### 7. `apps.achievements`
Gamified badge system:
- `models.py`:
  - `Achievement`: Badge title, description, icon, category, and XP bonus (e.g., *First Blood*, *Code Warrior*, *Polyglot*).
  - `UserAchievement`: Records which badges a user has unlocked and when.
- `services/achievement_engine.py`: Automatically inspects user stats upon solving a problem and unlocks achievements.

#### 8. `apps.leaderboard`
Global competitive rankings:
- `selectors/leaderboard_selectors.py`: Uses PostgreSQL window functions (`DENSE_RANK()`) to rank all users by XP, returning the Top 100 and the requesting user's relative standing.
- `apis/views.py`: Exposes `GET /api/v1/leaderboard/`.

#### 9. `apps.projects`
Guided engineering labs:
- `models.py`:
  - `Project`: Real-world guided project (e.g., *Build an HTTP Server*, *KV Store*, *Markdown Parser*).
  - `ProjectMilestone`: Sequential steps required to complete the project, each with automated test suites.
  - `UserProjectProgress`: Tracks student milestone completion and enrolled status.

#### 10. `apps.portfolio`
Public developer showcase:
- `selectors/portfolio_selectors.py`: Gathers a user's verified badges, completed engineering projects, language track stats, and social links.
- `apis/views.py`: Exposes `GET /api/v1/portfolio/<username>/` (publicly accessible).

#### 11. `apps.admin_api`
Enterprise backoffice & problem studio:
- `apis/views.py`: Staff-only API endpoints for platform analytics, authoring problems, creating guided project milestones, managing users, adjusting XP, and triggering bulk re-judging of submissions.

---

## 6. Frontend Deep-Dive: React 19 Architecture

### How the Frontend Boots
1. **`index.html`**: The single HTML page loaded by the browser containing `<div id="root"></div>`.
2. **`src/main.jsx`**: The JavaScript entry point. It creates the React root, imports `src/styles/index.css`, and mounts `<App />`.
3. **`src/App.jsx`**: Wraps the entire application with `AuthProvider` (making user authentication available everywhere) and renders `AppRoutes`.

### State Management & Authentication (`AuthContext.jsx`)
SkillForge uses a dedicated React Context for authentication:
- On initial page load, `AuthContext` calls `GET /api/v1/auth/csrf/` to acquire a CSRF cookie, followed by `GET /api/v1/auth/me/` to verify if an active session exists.
- Because JWT tokens are stored in `HttpOnly` cookies, JavaScript cannot steal them via `document.cookie` (immune to XSS).
- The Axios interceptor (`axiosClient.js`) automatically detects `401 Unauthorized` responses and calls `POST /api/v1/auth/token/refresh/` to renew the access token silently in the background.

### Routing System (`src/routes/`)
- **`AppRoutes.jsx`**: Configures all client-side paths using React Router v7.
- **`ProtectedRoute.jsx`**: Route guard that checks if a user is authenticated. If not, it redirects them to `/login`.
- **`AdminRoute.jsx`**: Route guard that checks if the logged-in user has `is_staff=True`. Non-admin users see an "Access Denied" screen.

### Pages Overview (`src/pages/`)
- **`HomePage.jsx`**: Landing page showcasing platform features, stats, and call-to-action buttons.
- **`LoginPage.jsx` & `RegisterPage.jsx`**: Clean, validated forms for logging in and creating accounts.
- **`DashboardPage.jsx`**: The student's primary command center displaying level progress, track mastery boxes (Python, JS, C++), verified engineering projects, and recent activity.
- **`ProblemsPage.jsx`**: Filterable problem catalog supporting track tabs, difficulty filters, keyword search, and pagination.
- **`ProblemDetailPage.jsx`**: The coding arena! Split-screen layout with markdown problem description on the left and the Monaco code editor, test case runner, and verdict drawer on the right.
- **`LeaderboardPage.jsx`**: Top 3 Podium showcase and full ranking table with sticky placement for the logged-in user.
- **`AchievementsPage.jsx`**: Badge grid displaying locked and unlocked achievements with progress indicators.
- **`ProjectsPage.jsx` & `ProjectWorkspacePage.jsx`**: Guided project catalog and multi-step engineering milestone workspace.
- **`PortfolioPage.jsx`**: Public profile page featuring verified solves, contact info, and 1-click sharing to WhatsApp, LinkedIn, Twitter, and Email.
- **`SettingsPage.jsx`**: User profile customizer (avatar picker, bio, social links) and password changer.
- **`admin/` Pages**: Backoffice suite for platform metrics, problem authoring studio with in-browser sandbox testing, project management, developer directory, and submission logs.

---

## 7. How Sandboxed Code Execution Works (Judge0 + Celery)

Running untrusted code submitted by strangers on the internet is extremely dangerous. If not sandboxed, a user could submit Python code like `import os; os.system("rm -rf /")` and destroy the server.

Here is how SkillForge solves this safely:

```
[Student Submits Code]
         │
         ▼
1. Django API creates Submission (Status: PENDING)
         │
         ▼
2. Celery Worker picks up task asynchronously
         │
         ▼
3. Celery calls Judge0 Sandbox API (POST /submissions)
         │
         ▼
4. Judge0 runs code inside Linux "Isolate" sandbox:
   ├── CPU Time Limit: 2.0 seconds
   ├── Memory Limit: 256 MB
   ├── Network Access: DISABLED (No internet access)
   ├── Process Limit: Maximum 60 threads/subprocesses
   └── Disk Storage: Maximum 4 MB output
         │
         ▼
5. Judge0 returns execution results (stdout, stderr, exit code, time, memory)
         │
         ▼
6. Celery compares output against Expected Output:
   ├── Match? -> Verdict: ACCEPTED
   ├── Mismatch? -> Verdict: WRONG_ANSWER
   ├── Time Exceeded? -> Verdict: TIME_LIMIT_EXCEEDED
   └── Error? -> Verdict: RUNTIME_ERROR / COMPILATION_ERROR
         │
         ▼
7. If ACCEPTED: Award XP, update streak, check achievements
         │
         ▼
8. Frontend polls or receives verdict and displays results!
```

---

## 8. How Was This Project Made? (Build Blueprint)

If you want to build a platform like SkillForge from scratch, here is the exact chronological roadmap that was followed:

1. **Phase 1: Architecture & Docker Scaffolding**
   - Setup project structure, Git, and Docker Compose files.
   - Configure PostgreSQL, Redis, Django, and React development environments.
2. **Phase 2: Authentication & Security Foundation**
   - Build custom user profiles, JWT in HttpOnly cookies, and CSRF protection.
   - Setup frontend `AuthContext` and route protection.
3. **Phase 3: Curriculum & Problem Modeling**
   - Create models for Problems, TestCases, StarterCode, Languages, and Tags.
   - Build seeder scripts with 300 curated challenges across 3 language tracks.
4. **Phase 4: Code Execution & Sandbox Engine**
   - Integrate Judge0 CE and configure Linux sandbox security policies.
   - Build Celery asynchronous task queue and submission evaluation engine.
   - Build frontend Monaco Editor coding arena with verdict drawer.
5. **Phase 5: Gamification & Progression Engine**
   - Build XP calculations, level thresholds, streaks, and anti-farming database constraints.
6. **Phase 6: Dashboard & Telemetry**
   - Build dashboard selectors aggregating language track mastery and student statistics.
7. **Phase 7: Achievements & Global Leaderboard**
   - Build automated badge unlock engine and dense rank leaderboard.
8. **Phase 8: Guided Engineering Projects & Portfolios**
   - Create guided project milestones and verified developer portfolio pages with social sharing.
9. **Phase 9: Enterprise Admin Backoffice**
   - Build the staff-only admin dashboard, problem authoring studio with in-browser sandbox testing, and submission re-judge tools.
10. **Phase 10: Production Hardening & CI/CD**
    - Configure GitHub Actions CI pipeline, Nginx reverse proxy, production Dockerfiles, and Gunicorn.

---

## 9. How to Clone, Setup & Run This Project (Step-by-Step)

Follow these instructions to run the entire SkillForge platform on your own computer.

### Step 1: Prerequisites
Make sure you have the following software installed on your machine:
- **Git**: [Download Git](https://git-scm.com/)
- **Docker Desktop**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) (ensure Docker Desktop is running)

*(Note: You do not need to install Python, Node.js, PostgreSQL, or Redis on your host computer; Docker runs all of them automatically inside containers!)*

---

### Step 2: Clone the Repository
Open your terminal (PowerShell, Command Prompt, or Terminal) and run:
```bash
git clone https://github.com/MrinmoyShib/skillforge.git
cd skillforge
```

---

### Step 3: Configure Environment Variables
Create your local environment file by copying the example template:

**On Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**On macOS / Linux:**
```bash
cp .env.example .env
```

The default values in `.env.example` are pre-configured for local Docker development and will work out of the box!

---

### Step 4: Start the Application Containers
Run Docker Compose to download, build, and launch all services:
```bash
docker compose -f docker/docker-compose.yml up -d --build
```

This starts 5 containers:
1. `skillforge-db`: PostgreSQL 16 database
2. `skillforge-redis`: Redis 7 in-memory cache and task broker
3. `skillforge-django`: Django 5.2 backend API
4. `skillforge-celery`: Celery background task worker
5. `skillforge-frontend`: React 19 / Vite development server

To verify all containers are running:
```bash
docker ps
```

---

### Step 5: Initialize the Database & Curriculum
Run the database migrations and seed the 300 challenges, achievements, and projects:

```bash
# 1. Run database migrations
docker exec skillforge-django python manage.py migrate

# 2. Seed the 300-problem curriculum (Python, JS, C++ tracks)
docker exec skillforge-django python manage.py seed_problems

# 3. Seed platform achievement badges
docker exec skillforge-django python manage.py seed_achievements

# 4. Seed guided engineering projects
docker exec skillforge-django python manage.py seed_projects
```

---

### Step 6: Create an Admin Superuser
To access the Django Admin and the Enterprise Admin Backoffice:
```bash
docker exec -it skillforge-django python manage.py createsuperuser
```
Follow the prompts to enter a username, email, and password.

---

### Step 7: Access the Platform in Your Browser
You're all set! Open your browser and navigate to:

- 💻 **Frontend Web App**: [`http://localhost:5173`](http://localhost:5173)
- 🔌 **Backend REST API**: [`http://localhost:8000/api/v1/`](http://localhost:8000/api/v1/)
- 📖 **Interactive Swagger Docs**: [`http://localhost:8000/api/docs/swagger/`](http://localhost:8000/api/docs/swagger/)
- ⚙️ **Django Admin Portal**: [`http://localhost:8000/admin/`](http://localhost:8000/admin/)
- 🛡️ **Enterprise Backoffice**: [`http://localhost:5173/admin`](http://localhost:5173/admin) *(Log in with your superuser account)*

---

### Step 8: Running Automated Tests

To run the complete backend test suite (68 tests):
```bash
docker exec skillforge-django pytest
```

To run frontend tests:
```bash
docker exec skillforge-frontend npm test
```

To test building the frontend production bundle:
```bash
docker exec skillforge-frontend npm run build
```

---

## 10. Frequently Asked Questions & Troubleshooting

### Q: What if port 5432, 6379, 8000, or 5173 is already in use?
If you have local instances of PostgreSQL, Redis, or other servers running on your machine, stop them before starting Docker:
- **Windows**: Open `services.msc` and stop the local `postgresql` or `redis` service.
- Or change the published host port in `docker/docker-compose.yml` (e.g., change `"5432:5432"` to `"5433:5432"`).

### Q: How do I view logs for a specific service?
```bash
# View backend logs
docker logs -f skillforge-django

# View Celery task worker logs
docker logs -f skillforge-celery

# View frontend logs
docker logs -f skillforge-frontend
```

### Q: How do I stop all containers?
```bash
docker compose -f docker/docker-compose.yml down
```

### Q: Will my data be lost when I stop containers?
No! PostgreSQL database data is safely stored in a named Docker volume (`postgres-data`), so your users, problems, and progress will persist even after restarting your computer.

---

*SkillForge — Empowering developers through code, practice, and craft.*

