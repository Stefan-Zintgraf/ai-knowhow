# Open Source Code Review Tools (Not Bound to GitLab Integration)

## Traditional Open-Source Code Review Platforms

### Gerrit

A web-based, self-hosted code review system originally developed at
Google.\
Supports pre-submit reviews, inline comments, approval workflows,
plugins, and fine-grained access control.\
Website: https://www.gerritcodereview.com/

### Review Board

Standalone open-source code review tool supporting Git, Mercurial, and
Subversion.\
Offers rich commenting, issue tracking, file attachments, and moved-code
detection.\
Website: https://www.reviewboard.org/

### Phabricator (Differential)

Comprehensive development suite including code review ("Differential"),
task tracking, and wiki.\
Self-hosted and not limited to Git workflows.\
Website: https://phacility.com/phabricator/

### Rietveld

Lightweight Django-based web code review tool (predecessor to Gerrit).\
Primarily used with Subversion and simple Git workflows.

### RhodeCode Community Edition

Self-hosted source code management platform (Git, Mercurial, Subversion)
with built-in code review and pull request features.\
Licensed under AGPLv3.\
Website: https://rhodecode.com/

------------------------------------------------------------------------

## Static / Automated Open-Source Review Tools

### SonarQube (Community Edition)

Open-source platform for static code analysis and quality inspection.\
Detects bugs, vulnerabilities, code smells, and security hotspots across
many languages.\
Website: https://www.sonarqube.org/

### Semgrep (OSS)

Fast, open-source static analysis tool with customizable and community
rule sets.\
Works well in CI pipelines for automated review checks.\
Website: https://semgrep.dev/

### Ruff

Ultra-fast Python linter and static analyzer.\
Useful as an automated review step in CI/CD workflows.\
Website: https://github.com/astral-sh/ruff

------------------------------------------------------------------------

## Other Open-Source Collections & Resources

### OpenApps.sh Code Review Category

Curated list of self-hosted open-source code review tools.\
Website: https://openapps.sh/categories/code-review/

### Awesome Code Review (GitHub List)

Community-maintained list of tools, guidelines, and scripts related to
code review.\
Website: https://github.com/joho/awesome-code-review

------------------------------------------------------------------------

## Integration Approaches

-   Combine human review platforms (e.g., Gerrit, Review Board) with
    automated tools (SonarQube, Semgrep).
-   Integrate automated tools into CI/CD systems (GitHub Actions,
    Jenkins, Azure DevOps, etc.).
-   Use pre-commit hooks and pipeline enforcement for quality gates.
