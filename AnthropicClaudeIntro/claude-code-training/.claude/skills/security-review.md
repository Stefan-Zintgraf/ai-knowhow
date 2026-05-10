# Security Review Skill

Perform a comprehensive security review of the codebase, identifying vulnerabilities and providing actionable remediation guidance.

## Trigger

Use this skill when the user asks for a "security review", "security audit", "vulnerability scan", or "find security issues".

## Review Process

### 1. Scan for OWASP Top 10 Vulnerabilities

**Injection (A03:2021)**
- SQL injection: Raw queries with string concatenation
- Command injection: Shell commands with user input
- NoSQL injection: Unvalidated queries to document databases

**Broken Authentication (A07:2021)**
- Hardcoded credentials or API keys
- Weak password policies
- Missing rate limiting on auth endpoints

**Sensitive Data Exposure (A02:2021)**
- Secrets in source code or config files
- Unencrypted sensitive data storage
- Logging of sensitive information

**XSS - Cross-Site Scripting (A03:2021)**
- Unescaped user input in HTML output
- Dangerous use of `innerHTML` or equivalent
- Missing Content-Security-Policy headers

**Broken Access Control (A01:2021)**
- Missing authorization checks
- Insecure direct object references (IDOR)
- Path traversal vulnerabilities

**Security Misconfiguration (A05:2021)**
- Debug mode enabled in production
- Default credentials
- Overly permissive CORS settings

### 2. Output Format

For each finding, provide:

```
## [SEVERITY] Finding Title

**Category**: OWASP category
**Location**: file:line_number
**Description**: What the vulnerability is and why it matters

**Vulnerable Code**:
(show the problematic code)

**Remediation**:
(show the fixed code or describe the fix)
```

### 3. Severity Ratings

- **CRITICAL**: Immediate exploitation risk, data breach likely
- **HIGH**: Significant risk, should fix before deployment
- **MEDIUM**: Moderate risk, fix in near term
- **LOW**: Minor issue, fix when convenient
- **INFO**: Best practice suggestion, not a vulnerability

### 4. Summary Report

Conclude with:
- Total findings by severity
- Top 3 priority fixes
- Overall security posture assessment

## Example Findings

### SQL Injection Example
```python
# VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# FIXED
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Hardcoded Secret Example
```python
# VULNERABLE
API_KEY = "sk-1234567890abcdef"

# FIXED
API_KEY = os.environ.get("API_KEY")
```

## Notes

- Focus on high-impact, easily exploitable issues first
- Provide working remediation code, not just descriptions
- Consider the framework's built-in security features
- Check for missing security headers in web applications
