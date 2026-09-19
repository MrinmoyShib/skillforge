# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-09-19

### Security
- Disabled DevFallbackEngine in production mode
- Fixed AUTH_COOKIE_SECURE flag placement in SIMPLE_JWT settings
- Added URL sanitization to prevent XSS via portfolio social links
- Added rate limiting (10/min) on authentication endpoints
- Blacklisted outstanding JWT tokens on password change
- Removed hardcoded fallback passwords from production Docker Compose
- Protected OpenAPI/Swagger docs behind DEBUG flag
- Fixed Nginx add_header inheritance trap and added CSP headers

### Fixed
- Empty test cases no longer auto-award ACCEPTED verdict
- Health check endpoint returns HTTP 503 when database or Redis is disconnected
- Fixed IntegrityError on concurrent profile updates
- Fixed email normalization inconsistency in user registration
- Fixed frontend SPA routing in production Nginx (try_files)
- Fixed 401 refresh token race condition in Axios interceptor
- Fixed memory leak from setInterval polling in ProblemDetailPage
- Fixed Spinner component ignoring size prop

### Performance
- Rewrote dashboard selectors from 150+ queries to ~5 grouped aggregations
- Fixed admin analytics N+1 milestone count query
- Implemented bulk_create for submission results
- Added Celery task time_limit (120s) and soft_time_limit (90s)
- Cached level requirements for 24 hours
- Set CONN_MAX_AGE=600 for persistent DB connections
- Added React.lazy() code splitting for all route pages

### Added
- Monaco Editor integration replacing textarea in code challenges
- ErrorBoundary component with branded error recovery screen
- Toast notification system replacing window.alert() calls
- Centralized language detection utility (languageUtils.js)
- Structured LOGGING configuration for Django
- .dockerignore files for backend and frontend
- CONTRIBUTING.md, SECURITY.md, CHANGELOG.md
- GitHub issue templates and PR template
- Dependabot configuration

### Changed
- Memoized AuthContext value with useMemo/useCallback
- Added useAuth hook guard clause
- Moved migrations out of container entrypoint
- Enforced LF line endings for shell scripts in .gitattributes

## [1.0.0] - 2026-09-18

### Added
- Initial release of SkillForge platform
- Django 5.2 backend with 11 modular apps
- React 19 frontend with Tailwind CSS v4
- 300 curated algorithmic challenges across Python, JavaScript, and C++ tracks
- Judge0 CE sandboxed code execution with Celery task queue
- Gamified progression engine with XP, levels, streaks, and achievements
- Global leaderboard with dense ranking
- Guided engineering projects with milestone tracking
- Public developer portfolio with social sharing
- Enterprise admin backoffice with problem studio
- Docker Compose development and production stacks
- CI/CD pipeline with GitHub Actions
- 68 automated backend tests
