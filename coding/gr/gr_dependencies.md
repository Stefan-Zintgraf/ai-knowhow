# Guardrail: Dependencies and Licensing

Purpose: control third-party code surface, versions, and license compatibility. Every dependency is a long-term commitment.

---

## Apply When

- A third-party package, library, framework, or service is added, removed, or upgraded.
- A transitive dependency changes in a way the agent notices.
- A new external interface is consumed (HTTP API, message broker, SaaS).

---

## Rules

### Dep1. No Silent Dependency Changes
Adding, removing, or upgrading a dependency requires explicit human approval before the change is made.

### Dep2. Justify Every New Dependency
A new dependency must come with: what it does, why it is needed, why a standard library / existing dependency is insufficient, size and maintenance signals.

### Dep3. Prefer Existing Project Dependencies
Before adding a package, check whether the project already depends on one that solves the problem.

### Dep4. Pin and Lock Versions
Versions are pinned and lockfiles are committed. The agent does not loosen version constraints to make installation succeed.

### Dep5. License Compatibility
Every new dependency's license is checked against the project's allowed-license policy. Copyleft, non-commercial, or unknown licenses require explicit approval.

### Dep6. Check Known Vulnerabilities
New or upgraded dependencies are checked against known-vulnerability databases (advisories, audit tools). High-severity findings block the change.

### Dep7. Minimal Surface
Import only the parts of a library actually used. No wildcard imports, no pulling in heavy submodules for one helper.

### Dep8. Avoid Abandoned or Single-Maintainer Risks
Maintenance signals (last release, open issues, maintainer count) are considered before adopting a dependency.

### Dep9. Upgrade Is a Behavior Change
A version upgrade may change behavior, defaults, or types. It is treated as a behavior change and verified (see `gr_testing_verification.md`).

### Dep10. Removal Is Not Free
Removing a dependency requires verifying that nothing still uses it (including indirect uses, scripts, examples, docs).

### Dep11. External Services Follow the Same Rules
A new external SaaS or API consumed by the system follows the same justification, security, license, and lock-in checks as a package dependency.

---

## Anti-Patterns

- `npm install some-package` to fix a tiny utility need that ten lines of code would solve.
- Bumping a major version without reading the changelog.
- Adding a package because "it has many stars."
- Loosening a version constraint to make the build pass.
- Adopting a GPL library in a closed-source product without legal review.
