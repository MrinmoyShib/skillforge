# Contributing to SkillForge

First off, thank you for considering contributing to SkillForge! It's people like you that make SkillForge such a great platform.

## Prerequisites
- Docker Desktop
- Git
- Node.js 22+
- Python 3.12+

## How to Fork and Clone
1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/SkillForge.git
   cd SkillForge
   ```
3. Add the original repository as an upstream remote:
   ```bash
   git remote add upstream https://github.com/MrinmoyShib/SkillForge.git
   ```

## Setting up the Development Environment
1. Copy the example environment files:
   ```bash
   cp .env.example .env
   ```
2. Start the development environment using Docker Compose:
   ```bash
   docker compose up --build
   ```

## Project Structure Overview
- `backend/`: Django REST Framework backend API
- `frontend/`: React 19 frontend application
- `docker/`: Docker configuration files
- `docs/`: Documentation

For a deeper dive into the architecture, please see `SKILLFORGE.md`.

## Coding Standards

### Backend
- Language: Python 3.12
- Style Guide: PEP 8 (enforced by `ruff`)
- Framework: Django & Django REST Framework
- Architecture: We follow a Service & Selector pattern to keep fat models and thin views.

### Frontend
- Framework: React (Functional Components & Hooks)
- Styling: Tailwind CSS v4
- Code Formatting: Prettier

## How to Run Tests

### Backend Tests
```bash
docker exec skillforge-django pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Branch Naming Conventions
- `feature/` - for new features
- `bugfix/` - for bug fixes
- `hotfix/` - for critical bug fixes in production
- `docs/` - for documentation updates

## Commit Message Format
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation only changes
- `refactor:` - A code change that neither fixes a bug nor adds a feature
- `test:` - Adding missing tests or correcting existing tests

## Pull Request Process
1. Ensure your code follows the coding standards and tests pass.
2. Create a Pull Request against the `main` branch.
3. Fill out the [Pull Request Template](.github/pull_request_template.md).
4. Wait for code review and approval.

## Code of Conduct
Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.
