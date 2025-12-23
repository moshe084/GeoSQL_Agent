# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Geo-SQL Agent seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Where to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Email**: Send details to [your-email@example.com]
2. **Private Security Advisory**: Use GitHub's [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)

### What to Include

Please include the following information in your report:

- Type of vulnerability (e.g., SQL injection, XSS, CSRF, etc.)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies based on severity
  - Critical: 1-3 days
  - High: 3-7 days
  - Medium: 7-30 days
  - Low: 30-90 days

## Security Best Practices for Users

### API Keys
- **NEVER** commit your OpenAI API key to version control
- Always use `.env` file and add it to `.gitignore`
- Rotate API keys regularly
- Use environment-specific keys (dev, staging, prod)

### Database
- Change default database credentials in production
- Use strong passwords (minimum 16 characters)
- Restrict database network access
- Enable SSL/TLS for database connections in production
- Regularly backup database

### Docker
- Don't run containers as root (our images use non-root users)
- Keep Docker and base images updated
- Scan images for vulnerabilities regularly
- Limit container resources (CPU, memory)

### Application
- Keep dependencies updated
- Review security advisories for dependencies
- Enable rate limiting (configured by default)
- Monitor application logs
- Use HTTPS in production
- Configure CORS properly for your domain

## Security Features

This project includes several built-in security features:

### SQL Injection Prevention
- ✅ Input validation with Pydantic
- ✅ SQL query validation (only SELECT allowed)
- ✅ Blocked keywords (DROP, DELETE, INSERT, etc.)
- ✅ Multiple statement prevention

### Rate Limiting
- ✅ Configurable rate limits (default: 10 req/min)
- ✅ Per-IP limiting

### Docker Security
- ✅ Non-root user in containers
- ✅ Multi-stage builds (minimal attack surface)
- ✅ No secrets in images

### Dependencies
- ✅ Regular dependency updates
- ✅ Automated security scanning (Dependabot)
- ✅ Known vulnerability checks

## Known Limitations

### Query Safety
- While we validate SQL, the AI model could theoretically generate complex queries
- Review generated SQL before executing in production
- Monitor database performance

### API Key Exposure
- OpenAI API keys are required and must be protected
- Never expose API endpoints publicly without authentication
- Consider implementing API authentication for production

## Security Updates

Security updates will be published:
- In GitHub Security Advisories
- In CHANGELOG.md
- As GitHub releases
- In commit messages (prefixed with `[SECURITY]`)

## Acknowledgments

We appreciate the security research community's efforts in responsibly disclosing vulnerabilities.

Security researchers who have helped improve this project:
- Your name could be here!

## Contact

For security-related questions that are not vulnerabilities:
- Open a GitHub Discussion
- Tag questions with `security`

---

**Last Updated**: December 2024
