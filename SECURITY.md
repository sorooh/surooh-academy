# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.5.x   | :white_check_mark: |
| 2.4.x   | :white_check_mark: |
| 2.3.x   | :x:                |
| < 2.3   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you believe you have found a security vulnerability in Surooh Academy, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **security@surooh-academy.com**

Please include the following information in your report:

- A clear description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any suggested fixes or mitigations
- Your contact information

### What to Expect

After you submit a vulnerability report, we will:

1. **Acknowledge** your report within 24 hours
2. **Investigate** the issue within 72 hours
3. **Provide updates** on our progress every 7 days
4. **Fix** critical vulnerabilities within 30 days
5. **Credit** you in our security advisories (if desired)

### Security Best Practices

When deploying Surooh Academy:

#### 🔐 Authentication & Authorization
- Always use strong API keys
- Implement proper JWT token management
- Enable multi-factor authentication where possible
- Regularly rotate service account keys

#### 🌐 Network Security
- Use HTTPS in production
- Configure proper firewall rules
- Implement rate limiting
- Use VPN for sensitive environments

#### 🔒 Data Protection
- Encrypt sensitive data at rest
- Use secure communication channels
- Implement proper data retention policies
- Regular security audits

#### 📦 Container Security
- Keep Docker images updated
- Scan for vulnerabilities regularly
- Use non-root users in containers
- Implement proper secrets management

#### 🏗️ Infrastructure Security
- Keep all dependencies updated
- Use infrastructure as code
- Implement proper monitoring
- Regular penetration testing

### Responsible Disclosure

We are committed to working with security researchers to verify and address security vulnerabilities. We ask that you:

- Give us reasonable time to investigate and mitigate the issue
- Avoid privacy violations, data destruction, or service disruption
- Do not access or modify data that doesn't belong to you
- Contact us before sharing vulnerability details with others

### Recognition

We maintain a hall of fame for security researchers who have helped us improve Surooh Academy's security:

- [Security Hall of Fame](https://github.com/sorooh/surooh-academy/blob/main/SECURITY_HALL_OF_FAME.md)

### Contact

For any security-related questions or concerns:

- **Security Team**: security@surooh-academy.com
- **General Contact**: support@surooh-academy.com
- **Emergency Contact**: +1-XXX-XXX-XXXX (for critical vulnerabilities)

---

**Thank you for helping keep Surooh Academy and our community safe!**