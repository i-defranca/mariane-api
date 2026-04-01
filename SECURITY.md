# Security Policy

## Reporting a Vulnerability
If you discover a security vulnerability in mariane-api, please report it responsibly and do **not** create a public GitHub issue.

### How to Report
Please email security details to the repository maintainer privately instead of using the public issue tracker. This allows us to:
- Assess the vulnerability
- Prepare a fix
- Release a patched version
- Coordinate disclosure timing

Include the following information in your report:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if you have one)

We will acknowledge receipt of your report within 48 hours and provide a timeline for the fix.

## Security Considerations

### Data Protection
This application handles sensitive health data (menstrual cycle tracking). We take data privacy seriously:

- **Encryption in Transit**: Always use HTTPS in production
- **Database Security**: Store database credentials in secure `.env` files (never commit them)
- **User Data**: Follow GDPR and similar privacy regulations when handling user information

### Authentication & Authorization
- JWT authentication is planned (see [Roadmap](README.md#roadmap))
- Until JWT is implemented, ensure proper access controls are in place
- Validate all user inputs on both client and server sides
- Implement proper permission checks for all API endpoints

### Dependencies
- Keep dependencies up to date by regularly running `pip list --outdated`
- Review `requirements.txt` periodically for known vulnerabilities
- Consider using tools like `pip-audit` to scan for vulnerable packages

### Environment & Configuration
- **Never commit `.env` files** or other files containing secrets to the repository
- Use `.env.example` to document required environment variables without exposing sensitive values
- Rotate database passwords periodically
- Use strong, unique passwords for database access

### Database Security
- Keep MySQL Docker container updated with the latest security patches
- Use strong root and application-level database passwords
- Restrict database access to only necessary services
- Implement proper backup procedures for user data
- Consider encrypting sensitive fields at rest

### API Security
- Implement rate limiting to prevent brute-force attacks
- Validate and sanitize all user inputs
- Enable SQL injection prevention (Django ORM provides this by default)
- Add API authentication before production deployment
- Log and monitor suspicious activity

### Testing & Code Quality
- Run tests locally before pushing: `pytest`
- Enable code coverage reporting to identify untested security-critical paths
- Use linters (black, ruff) to maintain code quality
- Review all pull requests for security implications

### CI/CD Security
- GitHub Actions secrets are used for sensitive CI/CD data
- Build and test in isolated environments
- Review workflow files for security best practices
- Keep action versions up to date

## Security Best Practices for Contributors
1. **Before Committing**:
   - Ensure no secrets are included in commits
   - Run `git diff` to review changes
   - Never commit `.env`, `*.pem`, or other sensitive files

2. **Code Review**:
   - All changes should be reviewed before merging to main
   - Pay special attention to authentication, authorization, and data handling code

3. **Testing**:
   - Write tests for security-related functionality
   - Include edge cases and error scenarios

4. **Documentation**:
   - Document any security-related decisions
   - Keep this file updated as security practices evolve

## Known Security Limitations
- JWT authentication is not yet implemented (planned feature)
- API documentation is still in development
- Production deployment guidelines are needed

## Future Security Improvements
- [ ] Implement JWT authentication
- [ ] Add API rate limiting
- [ ] Add comprehensive API logging and monitoring
- [ ] Add anomaly detection for security events
- [ ] Implement database encryption at rest
- [ ] Add automated dependency vulnerability scanning to CI
- [ ] Create incident response procedures

## Resources
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

## Version
- Created: 2026-04-01
- Last Updated: 2026-04-01

---
**Questions or suggestions?** Please reach out to the repository maintainer or open a private discussion.
