# Guardrail: Security and Compliance

Purpose: protect against vulnerabilities, data leaks, and regulatory violations.

---

## Apply When

- Authentication or authorization logic is touched.
- Secrets, tokens, keys, credentials, or certificates are handled.
- Input from external sources (users, APIs, files, queues) is processed.
- Cryptography (hashing, signing, encryption) is used.
- External interfaces, network calls, or third-party services are involved.
- Logging or telemetry of user data is changed.
- Compliance requirements apply (GDPR, HIPAA, PCI, safety standards, export control).

---

## Rules

### S1. No Hardcoded Secrets
Secrets, tokens, keys, passwords, or credentials must never appear in source, tests, fixtures, configuration committed to the repo, logs, or commit history. Use a secret manager or env var indirection.

### S2. Validate All External Input
Input from users, APIs, files, queues, or any non-trusted source is validated at the boundary before reaching domain logic.

### S3. Authorization at Every Sensitive Operation
Authorization checks happen at every boundary where access could be granted. No reliance on UI hiding, prior checks elsewhere, or "the caller should have checked."

### S4. Authentication Logic Is Not Modified Casually
Auth flows (login, session, token issuance, password handling) require explicit human approval before change. See `gr_governance.md`.

### S5. Use Vetted Cryptography
The agent does not invent crypto, implement a primitive by hand, or change algorithms. Use the project's existing crypto library and standard algorithms.

### S6. No Sensitive Data in Logs
Passwords, tokens, full payment data, PII beyond what compliance permits, and similar must never appear in logs, error messages, or telemetry.

### S7. Least Privilege
New code requests the minimum scope, permission, role, or capability it needs. No broad service accounts or wildcard scopes by default.

### S8. Safe Defaults
Defaults are secure: encrypted, authenticated, restricted. Insecure modes require explicit opt-in.

### S9. Dependency Security
New or upgraded dependencies are checked for known vulnerabilities and license compatibility (see `gr_dependencies.md`).

### S10. Safety-Critical No-Go Zones
Code marked safety-critical (regulated, hazardous, life-affecting) is off-limits for autonomous AI change. Human approval is mandatory and explicit.

### S11. Compliance Constraints Are Surfaced
If a change interacts with a known compliance regime, the agent names the regime and the relevant constraint before implementing.

### S12. No Disabling of Security Checks to Make Tests Pass
The agent must not weaken validators, lower auth requirements, or disable security middleware to fix a failing test.

---

## Anti-Patterns

- `apiKey = "sk_live_..."` in a fixture file.
- Logging the full request body including the `Authorization` header.
- `SELECT * FROM users WHERE id = ${userInput}` style string concatenation.
- Catching an auth error and continuing.
- Replacing bcrypt with MD5 because tests run slowly.
- "Temporary" disabling of CSRF for local debugging that lands on main.
