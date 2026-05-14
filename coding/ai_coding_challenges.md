# Risks and Problems of Using Coding Agents in Large, Production-Critical Brownfield Systems

## 1. Typical Problem Classes

- **Context Barrier & Implicit Business Logic**  
  Legacy systems contain decades of implicit knowledge embedded in undocumented rules, side effects, and architectural decisions that an agent cannot reconstruct from the code alone.  
  → Result: syntactically correct code that violates critical invariants known only to experienced developers – potentially catastrophic in production systems.  

- **Scaling Problem of Large Repositories**  
  Once the relevant portion of the code no longer fits into the context window, agents struggle to identify the truly relevant areas, maintain existing patterns, and respect global invariants.  
  → The consequence is local fixes that break broader system assumptions elsewhere (“broken windows” effect).  

- **Technical Debt Amplification**  
  In monolithic, tightly coupled brownfield systems, agents generate code that works in isolation but ignores system interactions.  
  Studies report significantly more static warnings and increased cognitive complexity in repositories that heavily use AI-generated code.  

## 2. Concrete Examples from Practice and Studies

- **Brownfield Case Study: Failure of Coding Agents**  
  A LinkedIn article describes companies observing not the expected 30–40% productivity gains in mature brownfield systems, but instead slowdowns among senior developers because they constantly have to correct agent-generated suggestions.  
  Typical incident: an agent refactors a “harmless” payment workflow and removes seemingly dead code that actually covers regulatory edge cases.  

- **BeyondSWE-like Benchmarks / Realistic Tasks**  
  New benchmark studies on AI coding agents in more complex, realistic scenarios (e.g., repository-wide refactorings or dependency-sensitive migrations) show success rates dropping from over 80% for simple tasks to below 45%.  
  These findings underline that “solving a small open-source issue” is not comparable to large-scale interventions in production-critical legacy systems.  

- **Legacy Refactoring Experiences**  
  Practical experience reports on refactoring large legacy codebases emphasize that agents only deliver more reliable results after the code has been made “LLM-friendly”: better modularization, clearer naming, and reliable tests.  
  Without a robust testing safety net, large-scale automated refactorings with agents remain extremely risky.  

## 3. Production and Security Risks

- **Invisible Quality Degradation**  
  Long-term analyses of autonomous coding agents show significantly increasing complexity and more static warnings in repositories that heavily use AI-generated code – even though features subjectively appear to be delivered “faster.”  
  In production-critical environments (e.g., manufacturing or safety-related systems), this gradual erosion is especially dangerous because it may only become visible later through outages or security incidents.  

- **Security Vulnerabilities & Secret Leaks**  
  Security analyses of AI coding assistants highlight that insecure patterns from training data are often reproduced (e.g., missing input validation or hardcoded secrets) and that confidential information can easily end up unnoticed in code or logs.  
  In large brownfield systems, the volume of generated code becomes so large that traditional manual security reviews can hardly keep up.  

- **Lack of Governance & “Vibe Coding”**  
  A recent t3n article describes how AI agents are used in companies without clear governance and how projects fail because responsibilities, evaluation criteria, and security processes are missing.  
  In one example, large parts of a platform were generated largely by an assistant; missing reviews led to exposed databases and plaintext API keys.  

## 4. Specific Problems in Large Brownfield Production Systems

- **Complex Dependencies & Migration Waves**  
  Repository-wide changes (library upgrades, framework migrations, replacement of industrial protocol stacks) are difficult for today’s agents to execute cleanly without introducing hidden breakages.  
  Particularly critical are hidden, undocumented integration points, vendor-specific hacks, and workarounds that agents cannot detect.  

- **Safety, Standards & Regulation**  
  Agents can violate safety patterns and standards (e.g., IEC standards in industrial automation) because these are often not explicitly embedded in code, but rather in processes, toolchains, or external documentation.  
  As a result, formal compliance may be silently undermined even though unit and integration tests appear green.  

- **Operational Robustness of Agents**  
  Experience reports mention issues such as endless loops, high latencies, unstable tooling, poor observability, and the lack of reliable evaluation frameworks.  
  For 24/7 manufacturing environments with narrow maintenance windows, this operational unreliability is difficult to accept.  

## 5. High-Level Patterns for Risk Mitigation

- **Shift the Focus of Usage**  
  It is advisable to initially use agents for low-risk, high-leverage tasks such as:  
  
  - Generating and extending tests  
  - Documentation and comment improvements  
  - Static analysis, dependency mapping, and code standardization  
  
  Direct autonomous intervention in safety-critical production paths is not recommended.  

- **“LLM-ification” of the Codebase**  
  Systematically improving test coverage, modularization, and inline documentation increases the likelihood that agents can make changes without violating global invariants.  
  This includes clear API contracts, explicitly documented business rules, and automated regression testing.  

- **Strict Governance & Processes**  
  Recommended measures include:  
  
  - Mandatory reviews for AI-generated code  
  - Automated security and compliance scans in CI/CD  
  - Sandbox deployments with telemetry before rollout into production  
  - Clear policies defining domains where agents must **not** be used (e.g., safety-critical core logic or cryptographic components).  

---

## Reference Links (Collection)

- Why Your AI Coding Agents Fail in Brownfield Projects:  
  https://www.linkedin.com/pulse/why-your-ai-coding-agents-fail-brownfield-project-how-sandeep-sgv4c  

- Benchmark Study on Challenges of AI Coding Agents (BeyondSWE):  
  https://www.mind-verse.de/news/neue-benchmark-studie-herausforderungen-ki-code-agenten-entwicklungsumgebungen  

- Legacy Codebases & LLM Usage:  
  https://www.arguingwithalgorithms.com/posts/legacy-codebases.html  

- Discussions / Experiences with Legacy Refactoring Using Agents:  
  https://news.ycombinator.com/item?id=46788196  
  https://www.reddit.com/r/AI_Agents/comments/1pxhuvf/has_anyone_refactored_a_legacy_codebase_using/  

- Security Risks of AI Coding Assistants:  
  https://www.devopsdigest.com/the-rise-of-genai-code-assistants-and-the-security-risks-lurking-beneath-the-surface  
  https://www.securecodewarrior.com/article/ai-coding-assistants-with-maximum-productivity-comes-amplified-risks  
  https://www.blackduck.com/blog/ai-coding-assistant-security-risks-benefits-devsecops-2025.html  

- Governance Failures and Organizational Challenges:  
  https://t3n.de/news/nicht-das-modell-ist-das-problem-ki-agenten-1730278/  
  https://www.mm-software.com/more-the-newsroom/detail/am-problem-vorbeigebaut-warum-so-viele-ai-projekte-schon-am-start-scheitern  

- Research Paper on the Effects of Coding Agents on Code Quality:  
  https://arxiv.org/html/2601.13597
