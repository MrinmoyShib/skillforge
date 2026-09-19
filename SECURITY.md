# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| v1.x.x  | :white_check_mark: |
| < v1.0  | :x:                |

## Reporting a Vulnerability

Please do **NOT** report security vulnerabilities via public GitHub issues.

Instead, please send an email to security@example.com (placeholder).

### Expected Response Timeline
- **Acknowledgment**: Within 48 hours of your report.
- **Resolution Target**: Within 30 days of acknowledgment, depending on severity and complexity.

### What to Include in a Report
- A detailed description of the vulnerability.
- Step-by-step reproduction instructions.
- An assessment of the potential impact.
- Any suggested mitigations if you have them.

## Responsible Disclosure Policy
We ask that you give us the opportunity to resolve the issue before disclosing it publicly. We will work with you to understand and resolve the issue quickly.

## Security Measures Already in Place
- HttpOnly JWT cookies for authentication tokens
- CSRF protection enabled
- Sandboxed code execution for programming challenges (Judge0 CE)
- Rate limiting on sensitive endpoints (e.g., authentication)
- Security headers (CSP, etc.) via Nginx
