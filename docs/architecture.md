# SkillForge — Architecture Decisions

This document records the key architectural decisions made for SkillForge, including the reasoning, trade-offs, and alternatives considered for each.

---

## Table of Contents

1. [JWT in HttpOnly Cookies](#1-jwt-in-httponly-cookies)
2. [Service & Selector Pattern](#2-service--selector-pattern)
3. [Self-Hosted Judge0 CE](#3-self-hosted-judge0-ce)
4. [Celery Polling (Not Webhooks)](#4-celery-polling-not-webhooks)
5. [Separate Docker Compose Stacks](#5-separate-docker-compose-stacks)
6. [JavaScript (Not TypeScript)](#6-javascript-not-typescript)
7. [Tailwind CSS v4](#7-tailwind-css-v4)

---

## 1. JWT in HttpOnly Cookies

**Decision:** Store JWT access and refresh tokens in `HttpOnly`, `Secure`, `SameSite=Lax` cookies instead of `localStorage` or `sessionStorage`.

**Why:**

- **XSS protection.** JavaScript cannot read `HttpOnly` cookies. If an XSS vulnerability is exploited, the attacker cannot exfiltrate tokens. With `localStorage`, a single `<script>` injection gives full access to the token.
- **Automatic transmission.** The browser attaches cookies to every request automatically — no need to wire up `Authorization` headers manually in every API call.
- **CSRF is manageable.** Django's built-in CSRF middleware plus `SameSite=Lax` provides strong CSRF protection with minimal effort. CSRF is a simpler threat to mitigate than XSS token theft.

**Trade-offs:**

- Slightly more complex server setup (cookie configuration, CSRF handling).
- Cross-origin requests require careful `CORS` and `withCredentials` configuration.

**Alternatives considered:**

- `localStorage` + `Authorization` header — simpler to implement, but vulnerable to XSS.
- Session-based auth — viable, but less suitable for a stateless API consumed by an SPA.

---

## 2. Service & Selector Pattern

**Decision:** Encapsulate business logic in **service functions** (commands/writes) and **selector functions** (queries/reads). Views/serializers remain thin — they validate input, call a service, and return a response.

**Why:**

- **Testability.** Services are plain Python functions that can be unit-tested without HTTP request/response machinery. No need to spin up the full DRF pipeline for a logic test.
- **Separation of concerns.** Views handle HTTP; services handle business rules; selectors handle data retrieval. Each layer has a single responsibility.
- **Reusability.** The same service can be called from a view, a Celery task, or a management command without duplication.
- **Readability.** New contributors can find all business logic for a domain in `services.py` and all query logic in `selectors.py`, rather than hunting through fat views or model methods.

**Pattern in practice:**

```
apps/submissions/
├── services.py      # create_submission(), poll_judge0_result()
├── selectors.py     # get_user_submissions(), get_submission_detail()
├── views.py         # Thin: validate → call service → respond
├── serializers.py   # Input/output schemas only
└── models.py        # Data and constraints, no business logic
```

**Trade-offs:**

- More files per app than the typical Django "fat models" approach.
- Requires discipline to keep views thin.

**Alternatives considered:**

- Fat models — common in Django, but models become hard to test and grow unwieldy.
- Django's `ViewSet` logic — couples business rules to HTTP layer.

---

## 3. Self-Hosted Judge0 CE

**Decision:** Run Judge0 Community Edition as a self-hosted Docker service rather than using Judge0's hosted API or building a custom sandbox.

**Why:**

- **Free and unlimited.** The hosted Judge0 API has rate limits and requires a paid plan for production usage. Self-hosting removes those constraints.
- **IOI-grade isolation.** Judge0 uses `isolate`, the same sandboxing technology used at the International Olympiad in Informatics. Code runs in resource-limited, network-isolated containers with strict CPU, memory, and time limits.
- **Full control.** We configure sandbox limits, supported languages, and authentication tokens ourselves. No dependency on a third-party SaaS for a core feature.
- **Network-local.** Submissions travel over a Docker bridge network, not the public internet. Lower latency, no egress costs.

**Trade-offs:**

- Requires `privileged: true` Docker containers (necessary for `isolate` cgroups).
- Adds operational complexity — another stack to monitor.
- Consumes host resources for code execution.

**Alternatives considered:**

- Judge0 hosted API — simpler, but rate-limited and adds a paid dependency.
- Custom sandbox (Docker-in-Docker, Firecracker) — massive engineering effort, reinventing a solved problem.

---

## 4. Celery Polling (Not Webhooks)

**Decision:** After submitting code to Judge0, use a Celery task to **poll** the Judge0 API for results rather than configuring Judge0 to send a webhook callback.

**Why:**

- **Simpler for v1.** Polling requires no public URL, no ingress configuration, and no webhook endpoint. The Celery worker simply calls `GET /submissions/:token` in a loop with exponential backoff.
- **No callback infrastructure.** In local development and Docker-only deployments, there is no reliable public URL for Judge0 to call back to. Polling works in any environment.
- **Resilient.** If the Django server restarts, pending Celery tasks resume polling. With webhooks, a missed callback means a lost result unless you also implement polling as a fallback.

**Implementation:**

```python
# Simplified flow
@shared_task(bind=True, max_retries=10)
def poll_submission_result(self, submission_id, judge0_token):
    result = judge0_client.get_submission(judge0_token)
    if result["status"]["id"] <= 2:  # Queued or Processing
        raise self.retry(countdown=2 ** self.request.retries)
    # Process final result
    update_submission(submission_id, result)
```

**Trade-offs:**

- Slightly higher latency than instant webhook delivery.
- More Judge0 API calls (mitigated by exponential backoff).

**Migration path:** In a future version, we can add a webhook endpoint and configure Judge0's `CALLBACKS_URL`. The Celery polling can remain as a fallback.

---

## 5. Separate Docker Compose Stacks

**Decision:** Run the application services (Django, Celery, Postgres, Redis, Frontend) and Judge0 services in **separate** Docker Compose files connected via a shared external network.

**Why:**

- **Security isolation.** Judge0 requires `privileged: true` to run `isolate` sandboxes. Keeping it in a separate Compose file means a `docker compose down` on the app stack doesn't touch the privileged Judge0 containers, and vice versa.
- **Independent lifecycles.** Judge0 rarely needs restarting. The app stack may be rebuilt frequently during development. Decoupling them avoids unnecessary downtime.
- **Operational clarity.** It's immediately obvious which services are "trusted" (app stack) and which run untrusted code (Judge0 stack).
- **Shared networking.** Both stacks join `skillforge-net`, so Django can reach `judge0-server:2358` seamlessly.

**File layout:**

```
docker/
├── docker-compose.yml           # App: postgres, redis, django, celery, frontend
├── docker-compose.judge0.yml    # Judge0: server, worker, judge0-db, judge0-redis
└── judge0.conf                  # Judge0 environment configuration
```

**Trade-offs:**

- Two `docker compose up` commands instead of one.
- Shared network must be created by the app stack first (or manually).

---

## 6. JavaScript (Not TypeScript)

**Decision:** Use plain JavaScript (ES2022+) with JSX for the React frontend instead of TypeScript.

**Why:**

- **Scope management.** SkillForge is a learning/portfolio project with a solo or small-team developer base. TypeScript adds significant configuration overhead (`tsconfig.json`, type declarations, `@types/*` packages) and a steeper onboarding curve.
- **Faster iteration.** No type-checking build step, no wrestling with complex generic types for React components, stores, or API layers. Focus stays on shipping features.
- **Vite handles it.** Vite's HMR and build pipeline work identically with `.jsx` files. There is zero performance difference in the dev experience.
- **Migration-friendly.** The codebase is structured (dedicated `api/`, `stores/`, `components/` directories) so that a future TypeScript migration can be done incrementally by renaming `.jsx` → `.tsx` and adding types file by file.

**Trade-offs:**

- No compile-time type safety — bugs that TypeScript would catch at build time may surface at runtime.
- Fewer IDE auto-complete hints without type annotations.

**Mitigation:** Use PropTypes for component props, JSDoc comments for complex functions, and thorough test coverage.

---

## 7. Tailwind CSS v4

**Decision:** Use Tailwind CSS v4 for styling instead of Tailwind v3, CSS Modules, or a component library.

**Why:**

- **No configuration file.** Tailwind v4 eliminates `tailwind.config.js` entirely. All configuration is done in CSS using `@theme` directives. One less config file to maintain.
- **CSS-first approach.** Theme tokens, custom utilities, and variants are defined in standard CSS syntax. This feels more natural and reduces the JavaScript-in-config pattern.
- **Performance.** Tailwind v4 uses the Oxide engine (written in Rust) for detection and compilation. Build times are significantly faster than v3.
- **Automatic content detection.** No need to configure `content` paths — Tailwind v4 automatically detects template files in the project.
- **Simplified import.** A single `@import "tailwindcss"` replaces the v3 `@tailwind base/components/utilities` directives.

**Trade-offs:**

- Tailwind v4 is newer, so community resources (tutorials, Stack Overflow answers) still primarily reference v3 syntax.
- Some v3 plugins may not yet be compatible.

**Alternatives considered:**

- Tailwind v3 — battle-tested, but the config-heavy approach is unnecessary boilerplate.
- CSS Modules — good isolation, but verbose for rapid prototyping and lacks the utility-first speed.
- shadcn/ui — considered for component primitives; may be adopted later for complex UI elements (modals, dropdowns) but not as the base styling system.
