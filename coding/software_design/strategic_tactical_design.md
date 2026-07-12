# Strategic and Tactical Software Design — Curated Web Resources

**Link status:** every URL below was checked on 10 July 2026\. Links marked ✅ were confirmed against live search results. Links marked ⚠️ could not be confirmed in this session and may have moved — the resource exists, but verify the URL before relying on it.

The phrase "strategic and tactical design" is used in **two quite different senses** in software literature. This document covers both, because they are frequently confused.

1. **Ousterhout sense** — two *mindsets* for writing code: invest in design (strategic) vs. get it working now (tactical). From *A Philosophy of Software Design*.  
2. **DDD sense** — two *layers* of Domain-Driven Design: boundaries & language (strategic) vs. model building blocks (tactical). From Eric Evans / Vaughn Vernon.

They are unrelated in origin. Skip to whichever you need.

Terms used throughout this document are defined in [glossary.md](./glossary.md), a shared glossary also used by [software_design.md](./software_design.md).

---

## Table of Contents

- [Part 1 — General Software Design Foundations](#part-1--general-software-design-foundations)  
- [Part 2 — Ousterhout: Strategic vs. Tactical Programming](#part-2--ousterhout-strategic-vs-tactical-programming)  
- [Part 3 — Domain-Driven Design: Strategic and Tactical Design](#part-3--domain-driven-design-strategic-and-tactical-design)  
  - [3.1 Strategic DDD](#31-strategic-ddd)  
  - [3.2 Tactical DDD](#32-tactical-ddd)  
- [Part 4 — Comparing the Ousterhout and DDD Meanings](#part-4--comparing-the-ousterhout-and-ddd-meanings)  
- [Part 5 — Practical Modelling Tools & Canvases](#part-5--practical-modelling-tools--canvases)  
- [Part 6 — Curated Link Collections](#part-6--curated-link-collections)  
- [Part 7 — Books](#part-7--books)  
- [8. Suggested Reading Paths](#8-suggested-reading-paths)  
- [9. Glossary](#9-glossary)  
- [10. Verification Log](#10-verification-log)

---

## Part 1 — General Software Design Foundations

These sit underneath both senses of "strategic/tactical" and are worth reading regardless.

| ✓   | Resource                                                                        | URL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Why                                                                                                                                                                                                           |
|:--- |:------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅   | Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules* (1972) | [https://dl.acm.org/doi/10.1145/361598.361623](https://dl.acm.org/doi/10.1145/361598.361623)                                                                                                                                                                                                                                                                                                                                                                                                     | The origin of information hiding. Eight pages; still the best eight pages in the field. Key line: it is almost always wrong to decompose from a flowchart — start from the design decisions likely to change. |
| ✅   | — same paper, free PDF (author's copy)                                          | [https://www.researchgate.net/profile/David\_Parnas/publication/200085877\_On\_the\_Criteria\_To\_Be\_Used\_in\_Decomposing\_Systems\_into\_Modules/links/55956a7408ae99aa62c72622/On-the-Criteria-To-Be-Used-in-Decomposing-Systems-into-Modules.pdf](https://www.researchgate.net/profile/David_Parnas/publication/200085877_On_the_Criteria_To_Be_Used_in_Decomposing_Systems_into_Modules/links/55956a7408ae99aa62c72622/On-the-Criteria-To-Be-Used-in-Decomposing-Systems-into-Modules.pdf) | Uploaded by Parnas himself.                                                                                                                                                                                   |
| ✅   | Moseley & Marks, *Out of the Tar Pit* (2006)                                    | [https://curtclifton.net/papers/MoseleyMarks06a.pdf](https://curtclifton.net/papers/MoseleyMarks06a.pdf)                                                                                                                                                                                                                                                                                                                                                                                         | Complexity as the root cause of most software problems. Dense but rewarding.                                                                                                                                  |
| ✅   | Fowler, *Design Stamina Hypothesis*                                             | [https://martinfowler.com/bliki/DesignStaminaHypothesis.html](https://martinfowler.com/bliki/DesignStaminaHypothesis.html)                                                                                                                                                                                                                                                                                                                                                                       | The investment argument on one page, with the crossover graph. Fowler, 2007 — the same shape as Ousterhout's Figure 3.1.                                                                                      |
| ⚠️  | Fowler, *Is High Quality Software Worth the Cost?*                              | [https://martinfowler.com/articles/is-high-quality-software-worth-cost.html](https://martinfowler.com/articles/is-high-quality-software-worth-cost.html)                                                                                                                                                                                                                                                                                                                                         | Argues internal quality pays for itself faster than people assume.                                                                                                                                            |
| ⚠️  | Fowler, *TechnicalDebt* / *TechnicalDebtQuadrant*                               | [https://martinfowler.com/bliki/TechnicalDebt.html](https://martinfowler.com/bliki/TechnicalDebt.html)                                                                                                                                                                                                                                                                                                                                                                                           | Deliberate/inadvertent × prudent/reckless.                                                                                                                                                                    |
| ⚠️  | Fowler, *Yagni*                                                                 | [https://martinfowler.com/bliki/Yagni.html](https://martinfowler.com/bliki/Yagni.html)                                                                                                                                                                                                                                                                                                                                                                                                           | The necessary counterweight to over-investment in design.                                                                                                                                                     |
| ⚠️  | Brooks, *No Silver Bullet*                                                      | [https://en.wikipedia.org/wiki/No\_Silver\_Bullet](https://en.wikipedia.org/wiki/No_Silver_Bullet)                                                                                                                                                                                                                                                                                                                                                                                               | Essential vs. accidental complexity — the frame everything else sits in.                                                                                                                                      |
| ⚠️  | arc42 architecture documentation template                                       | [https://arc42.org/](https://arc42.org/)                                                                                                                                                                                                                                                                                                                                                                                                                                                         | German-origin, widely used in DE/AT/CH. Pairs well with ADRs.                                                                                                                                                 |
| ⚠️  | Architecture Decision Records                                                   | [https://adr.github.io/](https://adr.github.io/)                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Lightweight way to record *why*, which is what strategic design is really about.                                                                                                                              |

### 1.1 Example — AI-Mail

The [AI-Mail vision](C:/PROJ/ai-mail/ai-mail.pocock/docs/brainstorming/ai-mail-foundation-vision.md) spans inboxes, chat, documents, silent obligations, AI models, approvals, and audit.

A channel-by-channel decomposition would let provider rules leak into obligation detection, approval, execution, and audit. The foundations suggest a different shape:

- Hide provider SDKs and model vendors behind stable ingestion and inference modules.
- Keep essential state explicit: the obligation, evidence, proposed action, authority, approval, and outcome. Treat summaries and rankings as derived state.
- Invest early in approval and audit boundaries because the promise that nothing is sent, paid, decided, or deleted without consent is costly to retrofit.
- Record why these boundaries exist in ADRs, while using YAGNI to defer speculative channels and action types.

This does not prescribe a complete architecture. It identifies decisions likely to change and separates them from rules that must remain trustworthy.

---

## Part 2 — Ousterhout: Strategic vs. Tactical Programming

The distinction comes from Chapter 3, "Working Code Isn't Enough," in John Ousterhout's *A Philosophy of Software Design*. It describes two mindsets for approaching any programming task.

### 2.1 Tactical programming

Tactical programming optimises for the fastest path to working code. The developer implements the next feature or fix with minimal attention to the system's future structure.

Key concepts:

- **Working-code focus** — success means making the immediate requirement work.
- **Local expediency** — special cases and narrow patches are preferred when they shorten delivery.
- **Complexity accumulation** — each shortcut is small, but repeated shortcuts create change amplification, cognitive load, and unknown unknowns.
- **Tactical tornado** — a highly productive developer who ships quickly while leaving complexity for teammates to absorb.
- **Legitimate tactical work** — disposable prototypes and reversible experiments can justify short-term design, provided the shortcut is named and contained.

### 2.2 Strategic programming

Strategic programming treats working code as insufficient. The goal is a system that remains easy to understand and change, achieved through continual design investment rather than a single upfront design phase.

Key concepts:

- **Design investment** — spend roughly 10–20% of development time improving structure. Ousterhout argues that the payback often arrives within months.
- **Deep modules** — prefer a simple interface that hides substantial implementation complexity.
- **Information hiding** — conceal volatile design decisions so changes do not spread through the system.
- **Design it twice** — compare at least two plausible designs before committing.
- **Define errors out of existence** — simplify semantics so fewer exceptional conditions can arise.
- **Complexity reduction** — judge designs by whether they reduce change amplification, cognitive load, and unknown unknowns.

### 2.3 Economics and controversy

Tactical work starts faster. If complexity keeps accumulating, productivity falls and strategic work overtakes it. The crossover is less certain for an early startup racing to learn or for code intended to be discarded.

Ousterhout argues that some agile, TDD, Clean Code, and "generalise later" practices can encourage tactical programming. Many practitioners disagree; the Ousterhout–Martin debate below presents the tension directly.

### 2.4 Example — AI-Mail

Suppose AI-Mail must add a second email provider and a new language model while preserving the rule that no message is sent without the user's approval.

A tactical implementation calls both vendor SDKs directly from the reply workflow, adds provider checks throughout the code, and lets each AI path decide how approval is represented. It ships quickly but multiplies security-sensitive paths.

A strategic implementation invests in deep modules with narrow contracts:

- A channel adapter turns provider-specific messages into one internal input.
- An inference module returns evidence and a proposed action, not an external side effect.
- An authority gate is the only route to sending, paying, deciding, or deleting.
- An execution module hides provider APIs, retries, and idempotency.
- An audit module records proposals, approvals, attempts, and outcomes.

The tactical version may be appropriate for a throwaway provider spike. The strategic version is appropriate for the long-lived product described by the vision because trust rules and integrations will compound.

### 2.5 Links

| ✓   | Resource                                            | URL                                                                                                                                                                    | Notes                                                                                                                                                  |
|:--- |:--------------------------------------------------- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ✅   | *A Philosophy of Software Design* (book home)       | [https://web.stanford.edu/\~ouster/cgi-bin/book.php](https://web.stanford.edu/~ouster/cgi-bin/book.php)                                                                | Primary source. 2nd ed. (July 2021\) adds two chapters and the Clean Code comparison; a free extract of the new material is offered to 1st-ed. owners. |
| ✅   | Ousterhout's APoSD resources page                   | [https://web.stanford.edu/\~ouster/cgi-bin/aposd.php](https://web.stanford.edu/~ouster/cgi-bin/aposd.php)                                                              | Supplementary material from the author.                                                                                                                |
| ✅   | Talks at Google (video, \~1h)                       | [https://www.youtube.com/watch?v=bmSAYlu0NcY](https://www.youtube.com/watch?v=bmSAYlu0NcY)                                                                             | Aug 2018\. The best free overview. Also on the Talks at Google podcast feed.                                                                           |
| ✅   | **Ousterhout vs. "Uncle Bob" Martin — full debate** | [https://github.com/johnousterhout/aposd-vs-clean-code](https://github.com/johnousterhout/aposd-vs-clean-code)                                                         | A long, civil, written disagreement between the two authors. Unusually valuable.                                                                       |
| ✅   | The Pragmatic Engineer interview (2025)             | [https://newsletter.pragmaticengineer.com/p/the-philosophy-of-software-design](https://newsletter.pragmaticengineer.com/p/the-philosophy-of-software-design)           | Ousterhout on why design matters *more* in the AI-coding era; his objections to TDD and SRP.                                                           |
| ✅   | The Pragmatic Engineer, book review                 | [https://blog.pragmaticengineer.com/a-philosophy-of-software-design-review/](https://blog.pragmaticengineer.com/a-philosophy-of-software-design-review/)               | Good on *why* the book's claims are unusually well-grounded: he watched many teams solve the same problem.                                             |
| ✅   | CS 190 lecture notes (Winter 2019\)                 | [https://web.stanford.edu/\~ouster/cgi-bin/cs190-winter19/lecture.php?topic=intro](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter19/lecture.php?topic=intro)    | Free lecture notes. Change the year in the path for other offerings; the current-quarter page moves annually.                                          |
| ✅   | CS 190 course description                           | [https://explorecourses.stanford.edu/search?q=CS+190](https://explorecourses.stanford.edu/search?q=CS+190)                                                             | Stanford's catalogue entry. Enrolment capped at 20; every line of student code is reviewed by Ousterhout.                                              |
| ✅   | Chapter-by-chapter summary (Carsten Behrens)        | [https://carstenbehrens.com/a-philosophy-of-software-design-summary/](https://carstenbehrens.com/a-philosophy-of-software-design-summary/)                             | Includes the 10–20% investment figure and the startup caveat.                                                                                          |
| ✅   | Book review (smlx)                                  | [https://smlx.dev/posts/book-review-ousterhout-philosophy-software-design/](https://smlx.dev/posts/book-review-ousterhout-philosophy-software-design/)                 | Contrasts Ousterhout against *Clean Code* and *Effective Go*.                                                                                          |
| ✅   | Book notes (Dan Lebrero)                            | [https://danlebrero.com/2021/02/24/philosophy-of-software-design-summary/](https://danlebrero.com/2021/02/24/philosophy-of-software-design-summary/)                   | Dense one-pager: tactical tornado, deep vs. shallow modules, information hiding.                                                                       |
| ✅   | Lessons from APoSD (dev.to / thawkin3)              | [https://dev.to/thawkin3/lessons-from-a-philosophy-of-software-design-4cn7](https://dev.to/thawkin3/lessons-from-a-philosophy-of-software-design-4cn7)                 | The agile critique quoted in context.                                                                                                                  |
| ✅   | Reading notes (Maëlle Salmon)                       | [https://masalmon.eu/2023/10/19/reading-notes-philosophy-software-design/](https://masalmon.eu/2023/10/19/reading-notes-philosophy-software-design/)                   | Short, personal, honest about what did and didn't land.                                                                                                |
| ✅   | TIL: Tactical vs Strategic (dev.to)                 | [https://dev.to/menilek/til-today-i-learned-tactical-vs-strategic-programming-14ae](https://dev.to/menilek/til-today-i-learned-tactical-vs-strategic-programming-14ae) | Traces the "move fast and break things" → "move fast together" arc.                                                                                    |
| ✅   | Tactical and strategic programming (jgarivera)      | [https://jgarivera.com/posts/tactical-strategic-programming/](https://jgarivera.com/posts/tactical-strategic-programming/)                                             | Blog-length treatment focused on technical-debt accumulation.                                                                                          |
| ✅   | Two key takeaways (rlamacraft)                      | [https://rlamacraft.uk/philosophyOfSoftwareDesign.html](https://rlamacraft.uk/philosophyOfSoftwareDesign.html)                                                         | Strategic thinking \+ the interface-to-implementation ratio, in ten minutes.                                                                           |

---

## Part 3 — Domain-Driven Design: Strategic and Tactical Design

DDD uses "strategic" and "tactical" for two scopes of domain modelling. Strategic design finds the model boundaries and language; tactical design implements behaviour inside one boundary.

### 3.1 Strategic DDD

Strategic DDD answers **"what?"** and **"why?"**: what problem is being solved, where modelling effort matters, and where different models and languages must remain separate.

It identifies domains and subdomains, draws bounded contexts, develops a ubiquitous language, and maps the relationships between contexts and the teams that own them.

Evans' own three-point summary of DDD: focus on the core domain; explore models collaboratively with domain experts and developers; speak a ubiquitous language within an explicitly bounded context.

Key concepts: **Domain, Subdomain (core / supporting / generic), Bounded Context, Ubiquitous Language, Context Map, Anti-Corruption Layer, Shared Kernel, Conformist, Open Host Service, Published Language.**

| ✓   | Resource                                                        | URL                                                                                                                                                                                                                                                          | Notes                                                                                                                                                                   |
|:--- |:--------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅   | Eric Evans, **DDD Reference**                                   | [https://www.domainlanguage.com/ddd/reference/](https://www.domainlanguage.com/ddd/reference/)                                                                                                                                                               | Every definition and pattern from the 2004 book in summary form, plus three patterns that postdate it. CC-BY 4.0. The single best free artefact.                        |
| ✅   | — direct PDF                                                    | [https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD\_Reference\_2015-03.pdf](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)                                                                                 | \~50 pages. Keep it open while modelling.                                                                                                                               |
| ✅   | Domain Language, DDD resources hub                              | [https://www.domainlanguage.com/ddd/](https://www.domainlanguage.com/ddd/)                                                                                                                                                                                   | Includes the "Manager's Guided Tour" (skim the Blue Book in a few hours) and a paper on four strategies for starting DDD in a legacy estate.                            |
| ✅   | Fowler, *Bounded Context*                                       | [https://martinfowler.com/bliki/BoundedContext.html](https://martinfowler.com/bliki/BoundedContext.html)                                                                                                                                                     | Also *UbiquitousLanguage*, *DomainDrivenDesign*, *AnemicDomainModel*. Short, sharp definitions.                                                                         |
| ✅   | ddd-crew, **free-ddd-learning-resources**                       | [https://github.com/ddd-crew/free-ddd-learning-resources](https://github.com/ddd-crew/free-ddd-learning-resources)                                                                                                                                           | Maintained index of everything else that's free. Start here for breadth.                                                                                                |
| ✅   | Vaadin, *DDD Part 1: Strategic DDD*                             | [https://vaadin.com/blog/ddd-part-1-strategic-domain-driven-design](https://vaadin.com/blog/ddd-part-1-strategic-domain-driven-design)                                                                                                                       | Readable walkthrough. Honest warning against finding bounded contexts for their own sake — start with one core domain, one context, and let the rest reveal themselves. |
| ⚠️  | Vaadin, *DDD Part 2: Tactical DDD*                              | [https://vaadin.com/blog/ddd-part-2-tactical-domain-driven-design](https://vaadin.com/blog/ddd-part-2-tactical-domain-driven-design)                                                                                                                         | Direct continuation. (Title confirmed via Part 1; exact URL unverified.)                                                                                                |
| ✅   | ddd-crew, **context-mapping**                                   | [https://github.com/ddd-crew/context-mapping](https://github.com/ddd-crew/context-mapping)                                                                                                                                                                   | The relationship patterns with diagrams and a decision guide.                                                                                                           |
| ✅   | Khononov, *Learning DDD* — Part I preview                       | [https://www.oreilly.com/library/view/learning-domain-driven-design/9781098100124/part01.html](https://www.oreilly.com/library/view/learning-domain-driven-design/9781098100124/part01.html)                                                                 | Strategic \= what/why, tactical \= how.                                                                                                                                 |
| ✅   | VirtualDDD, *When to invest in strategic vs. tactical design*   | [https://virtualddd.com/sessions/when-to-invest-in-strategic-design-and-when-in-tactical-design/](https://virtualddd.com/sessions/when-to-invest-in-strategic-design-and-when-in-tactical-design/)                                                           | Corrective for people who met DDD as a programming discipline first.                                                                                                    |
| ✅   | Jakub Lambrych, *Strategic Design Explained*                    | [https://medium.com/@lambrych/domain-driven-design-ddd-strategic-design-explained-55e10b7ecc0f](https://medium.com/@lambrych/domain-driven-design-ddd-strategic-design-explained-55e10b7ecc0f)                                                               | Frames strategic patterns as problem space, tactical as the transition to solution space, with Bounded Context as the vehicle between them.                             |
| ✅   | Mosharraf Hossain, *DDD Demystified*                            | [https://medium.com/@mail2mhossain/domain-driven-design-demystified-strategic-tactical-and-implementation-layers-dad829be18f0](https://medium.com/@mail2mhossain/domain-driven-design-demystified-strategic-tactical-and-implementation-layers-dad829be18f0) | Adds a third "implementation layer" and a banking case study.                                                                                                           |
| ✅   | Nick Tune's blog                                                | [https://medium.com/nick-tune-tech-strategy-blog](https://medium.com/nick-tune-tech-strategy-blog)                                                                                                                                                           | Probably the best working writer on socio-technical / strategic DDD today. Origin of the Bounded Context Canvas.                                                        |
| ✅   | archi-lab.io, DDD course pages                                  | [https://www.archi-lab.io/infopages/ddd/ddd-crew-bounded-context.html](https://www.archi-lab.io/infopages/ddd/ddd-crew-bounded-context.html)                                                                                                                 | A German university course's practical guide to chaining the ddd-crew methods together. Includes a commented literature list.                                           |
| ⚠️  | Team Topologies                                                 | [https://teamtopologies.com/](https://teamtopologies.com/)                                                                                                                                                                                                   | Not DDD, but the standard companion — bounded contexts and team boundaries want to agree.                                                                               |
| ⚠️  | *Domain-Driven Design Quickly* (InfoQ, free)                    | [https://www.infoq.com/minibooks/domain-driven-design-quickly/](https://www.infoq.com/minibooks/domain-driven-design-quickly/)                                                                                                                               | \~100-page free summary of the Blue Book, incl. an Evans interview. Widely recommended as a first taste.                                                                |
| ✅   | ForceInjection, **domain-driven-design-skills** (agent skill)   | [https://github.com/ForceInjection/domain-driven-design-skills](https://github.com/ForceInjection/domain-driven-design-skills)                                                                                                                               | Interactive, technology-neutral coding-agent workflow: Discovery → Strategic Design → Tactical Design → Validation → Specification Bridging. Work in progress.          |
| ✅   | wondelai, **skills** — domain-driven-design skill (agent skill) | [https://github.com/wondelai/skills](https://github.com/wondelai/skills)                                                                                                                                                                                     | Technology-neutral bounded contexts, aggregates, ubiquitous language, and context-mapping strategies, packaged inside a much larger, non-DDD-specific skill pack.       |
| ✅   | SebastienDegodez, **copilot-instructions** (agent skill)        | [https://github.com/SebastienDegodez/copilot-instructions](https://github.com/SebastienDegodez/copilot-instructions)                                                                                                                                         | C#/.NET-specific: DDD paired with Clean Architecture, CQRS, a specification-pattern skill, and sociable application-layer testing.                                      |

### 3.2 Tactical DDD

Tactical DDD answers **"how?"**: how behaviour inside one bounded context is modelled and implemented.

Its patterns grew from object-oriented design and were refined for complex business domains. One useful framing is object-oriented analysis and design elaborating on Fowler's Domain Model pattern.

Key building blocks:

- **Entity** — has an identity that persists while its state changes.
- **Value Object** — is immutable and compared by structural value.
- **Aggregate and Aggregate Root** — form a consistency and transaction boundary with one external entry point.
- **Repository and Factory** — retrieve existing aggregates and create valid new ones.
- **Domain Service and Domain Event** — express behaviour that belongs to no one entity and facts meaningful to the domain.
- **Application Service** — orchestrates a use case while keeping domain rules in the model.
- **Transaction Script** — is a legitimate simpler alternative for low-complexity subdomains.

| ✓   | Resource                                                    | URL                                                                                                                                                                                                                                      | Notes                                                                                                                                                                                                                                                                                                                                                                                                             |
|:--- |:----------------------------------------------------------- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅   | Microsoft Learn, *Use Tactical DDD to Design Microservices* | [https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design)                         | Entities, value objects, aggregates, repositories, domain events, with a concrete drone-delivery example. Vendor-flavoured but precise. **(Corrected URL — the old `/tactical-ddd` path was wrong.)**                                                                                                                                                                                                             |
| ✅   | Vernon, **Effective Aggregate Design** (3 free PDFs)        | [https://www.dddcommunity.org/library/vernon\_2011/](https://www.dddcommunity.org/library/vernon_2011/)                                                                                                                                  | The definitive treatment of aggregate boundaries; the basis for the Red Book's aggregate chapter. Direct PDFs: [Part I](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf), [Part II](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_2.pdf), [Part III](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_3.pdf). |
| ✅   | Fowler, *DDD\_Aggregate*                                    | [https://martinfowler.com/bliki/DDD\_Aggregate.html](https://martinfowler.com/bliki/DDD_Aggregate.html)                                                                                                                                  | Aggregates as the unit of storage transfer; transactions should not cross aggregate boundaries. One paragraph, correctly.                                                                                                                                                                                                                                                                                         |
| ✅   | DZone, *Tactical DDD: Bringing Strategy to Code*            | [https://dzone.com/articles/tactical-domain-driven-design-bringing-strategy-to](https://dzone.com/articles/tactical-domain-driven-design-bringing-strategy-to)                                                                           | The seven core patterns plus application services. Recent (late 2025).                                                                                                                                                                                                                                                                                                                                            |
| ✅   | dev.to, *DDD Part 2 — Tactical Design*                      | [https://dev.to/axeldlv/domain-driven-design-part-2-tactical-design-243n](https://dev.to/axeldlv/domain-driven-design-part-2-tactical-design-243n)                                                                                       | Compact: value objects immutable and compared by value; entities have identity persisting through state changes.                                                                                                                                                                                                                                                                                                  |
| ✅   | Masoud Chelongar, *Tactical Design*                         | [https://medium.com/@masoud.chelongar/domain-driven-design-tactical-design-41640afa2009](https://medium.com/@masoud.chelongar/domain-driven-design-tactical-design-41640afa2009)                                                         | Good on *choosing* a pattern per subdomain rather than applying aggregates everywhere.                                                                                                                                                                                                                                                                                                                            |
| ✅   | Vaughn Vernon, **IDDD\_Samples** (Java)                     | [https://github.com/VaughnVernon/IDDD\_Samples](https://github.com/VaughnVernon/IDDD_Samples)                                                                                                                                            | The sample bounded contexts from the Red Book. One uses event sourcing \+ CQRS, one uses Hibernate \+ REST \+ RabbitMQ.                                                                                                                                                                                                                                                                                           |
| ✅   | IDDD sample in .NET                                         | [https://github.com/abdullin/iddd-sample](https://github.com/abdullin/iddd-sample)                                                                                                                                                       | C\# port with event sourcing, by Rinat Abdullin.                                                                                                                                                                                                                                                                                                                                                                  |
| ✅   | SOCADK Design Practice Repository, *Tactic DDD*             | [https://github.com/socadk/design-practice-repository/blob/master/activities/DPR-TacticDDD.md](https://github.com/socadk/design-practice-repository/blob/master/activities/DPR-TacticDDD.md)                                             | Method card: inputs, outputs, when to use, how it relates to EventStorming and use cases. Academic but practical.                                                                                                                                                                                                                                                                                                 |
| ✅   | SAP, *How to develop aggregates*                            | [https://github.com/SAP/curated-resources-for-domain-driven-design/blob/main/blog/0004-how-to-develop-aggregates.md](https://github.com/SAP/curated-resources-for-domain-driven-design/blob/main/blog/0004-how-to-develop-aggregates.md) | Includes the healthy reminder that tactical patterns are tools, not a compliance checklist — you can write good software without using every one.                                                                                                                                                                                                                                                                 |
| ✅   | James Hickey, *What are DDD aggregates?*                    | [https://www.jamesmichaelhickey.com/domain-driven-design-aggregates/](https://www.jamesmichaelhickey.com/domain-driven-design-aggregates/)                                                                                               | Starts from what an aggregate *is not*. Good antidote to jargon overload.                                                                                                                                                                                                                                                                                                                                         |
| ⚠️  | Fowler, *Event Sourcing*                                    | [https://martinfowler.com/eaaDev/EventSourcing.html](https://martinfowler.com/eaaDev/EventSourcing.html)                                                                                                                                 | Often paired with tactical DDD; not required by it.                                                                                                                                                                                                                                                                                                                                                               |
| ✅   | zudochkin, **go-clean-ddd-skill** (agent skill)             | [https://github.com/zudochkin/go-clean-ddd-skill](https://github.com/zudochkin/go-clean-ddd-skill)                                                                                                                                       | Interactive coding-agent DDD modelling loop covering bounded contexts, aggregates, invariants, and domain events, with Go-specific templates and code generation.                                                                                                                                                                                                                                                 |

**Three common traps.**

1. *Tactical DDD without strategic DDD* — aggregates and repositories bolted onto a codebase whose boundaries were never examined. The most common failure mode.  
2. *Aggregates everywhere* — generic and supporting subdomains often deserve a transaction script or plain CRUD. Reserve the expensive patterns for the core domain.  
3. *Write models as read models* — using aggregates to serve UI queries. Keep queries independent of aggregate boundaries.

### 3.3 Example — AI-Mail

The [AI-Mail vision](C:/PROJ/ai-mail/ai-mail.pocock/docs/brainstorming/ai-mail-foundation-vision.md) requires domain distinctions that a single universal "email" model would blur.

A candidate strategic design could separate these bounded contexts:

- **Communication Intake** translates email, chat, documents, voice, and watched sources into received evidence.
- **Obligation Discovery** decides what asks something of the user and when it matters.
- **Action Planning** prepares replies, bookings, claims, payments, and other proposed work.
- **Authority and Consent** decides who may approve which action for which person, household, team, or account.
- **Execution** interacts with external systems only after valid authority is established.
- **Relationship Memory** models people and conversations across channels without erasing privacy boundaries.
- **Audit and Governance** preserves the assistant's decisions for explanation, legal hold, and data requests.

This is a hypothesis to test with users and domain experts, not a final architecture. Its value is making competing meanings and responsibilities explicit.

Inside **Authority and Consent**, tactical DDD could model a `ProposedAction` aggregate. It would enforce one central invariant: an action cannot execute unless the exact proposal has valid approval from an authorised principal.

Changing the recipient, content, amount, account, or action type would invalidate approval. Value objects such as `AuthorityScope`, `ProposalDigest`, and `RiskLevel` would make those rules explicit.

Events such as `ActionProposed`, `ActionApproved`, `ApprovalInvalidated`, and `ActionRejected` would communicate decisions. Execution outcomes would remain separate because external delivery cannot be made atomic with approval.

Simple provider synchronisation and read-only queries need not use aggregates. They can use adapters, transaction scripts, and dedicated read models.

---

## Part 4 — Comparing the Ousterhout and DDD Meanings

The two vocabularies use the same labels for different axes. They can reinforce each other, but they are not competing definitions and do not form a single strategic-to-tactical pipeline.

### 4.1 Same words, different axes

**Ousterhout's axis is investment over time.** It asks how a developer approaches any design task: optimise for immediate delivery, or spend some effort now to reduce future complexity?

**DDD's axis is design scope.** It asks which design task is under discussion: shape domains, language, boundaries, and relationships, or model behaviour inside one boundary?

This makes the two distinctions orthogonal. Strategic DDD can be done with a rushed, tactical-programming mindset. Tactical DDD can be performed with patient, strategic-programming discipline.

|                           | Ousterhout: tactical programming                                                             | Ousterhout: strategic programming                                                               |
|:------------------------- |:-------------------------------------------------------------------------------------------- |:----------------------------------------------------------------------------------------------- |
| **DDD: strategic design** | Draw a context boundary quickly to unblock delivery, accepting uncertainty and later rework. | Explore language and boundaries deliberately; compare alternatives and protect the core domain. |
| **DDD: tactical design**  | Copy an aggregate or repository pattern to ship a feature, whether or not it fits.           | Design aggregates and model APIs carefully so invariants are clear and change stays local.      |

The bottom-left cell is not automatically bad. A reversible experiment can be a rational tactical move. The danger is treating a temporary shortcut as a durable design without naming or revisiting it.

### 4.2 What they have in common

Both reject “the code works” as a sufficient definition of good software. They care about the cost of understanding and changing a system after its first release.

Both value boundaries. Ousterhout uses modules to hide decisions behind simple interfaces. DDD uses bounded contexts and aggregates to limit where a model, language, or invariant must remain consistent.

Both ask teams to concentrate effort. Ousterhout invests where complexity would otherwise accumulate. DDD invests its richest modelling in the core domain and permits simpler designs elsewhere.

Both treat names and concepts as design tools. Ousterhout wants interfaces that expose the right abstraction; DDD makes domain language an explicit, shared model within a bounded context.

Both are compatible with incremental learning. Neither requires predicting the final system upfront. Their useful form is repeated discovery, design, implementation, and correction.

### 4.3 What does not map

| Question                 | Ousterhout                                                                                | DDD                                                                                                  |
|:------------------------ |:----------------------------------------------------------------------------------------- |:---------------------------------------------------------------------------------------------------- |
| **Primary concern**      | Managing software complexity and sustaining development speed.                            | Modelling a complex domain and aligning software, language, boundaries, and teams.                   |
| **Unit of attention**    | A developer's or team's approach to design, often down to modules and interfaces.         | A domain, subdomain, bounded context, relationship, aggregate, or domain concept.                    |
| **Meaning of strategic** | Invest now for lower long-term complexity.                                                | Decide domain focus, model boundaries, language, ownership, and context relationships.               |
| **Meaning of tactical**  | Prioritise the immediate result, accepting future design cost.                            | Use modelling building blocks inside a bounded context. It says nothing about haste or quality.      |
| **Applicability**        | Broad: libraries, infrastructure, products, embedded code, and business systems.          | Selective: strongest where business rules, terminology, and organisational boundaries are complex.   |
| **Typical output**       | Deep modules, simpler interfaces, hidden information, fewer exceptions, better factoring. | Context maps, ubiquitous language, aggregates, value objects, repositories, and domain events.       |
| **Failure mode**         | Complexity accumulates through locally expedient changes.                                 | Patterns are applied without domain insight, or one model is stretched across incompatible contexts. |

Ousterhout does not supply a method for finding business domains or team boundaries. DDD does not supply a general theory of module depth, interface complexity, or design investment.

DDD's tactical patterns are not a substitute for good code design. An aggregate can still expose a shallow, confusing interface. A repository can still leak storage details throughout the model.

Conversely, a well-designed deep module may have no DDD role at all. A compression library, device driver, parser, or scheduling engine can benefit greatly from Ousterhout without having a business domain model.

### 4.4 Ambiguities and category errors

**“Strategic” does not always mean architecture.** Ousterhout's strategic programming also applies to a small method or class. DDD strategic design can affect architecture, but begins with domain distinctions rather than technology choices.

**“Tactical” does not always mean short-sighted.** Tactical DDD is simply the more local modelling toolbox. Applying it carefully may be strategic programming in Ousterhout's sense.

**DDD's boundary is porous.** A bounded context is called strategic, yet it constrains code, APIs, data, deployment, and ownership. Aggregates are called tactical, yet poor aggregate boundaries can damage system-wide behaviour.

**Ubiquitous language spans both levels.** It helps discover contexts at the strategic level and names entities, value objects, commands, and events at the tactical level.

**Simple does not mean tactical.** Choosing a transaction script for a stable, low-complexity subdomain can be an intentional strategic investment. Adding elaborate aggregates there may increase complexity instead.

**More design is not always more strategic.** Speculative abstractions, universal models, and pattern-heavy frameworks can create the very cognitive load Ousterhout wants to remove.

### 4.5 Which concepts fit which problems?

| Product or problem                                           | Ousterhout concepts                                                                                     | Strategic DDD                                                                                            | Tactical DDD                                                                                                        |
|:------------------------------------------------------------ |:------------------------------------------------------------------------------------------------------- |:-------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------- |
| **Prototype or disposable experiment**                       | Work tactically and keep shortcuts reversible. Design only interfaces needed to test the idea.          | Use lightweight domain language or EventStorming if the experiment tests problem understanding.          | Usually defer; use plain data and transaction scripts unless a rule is the experiment.                              |
| **Early startup seeking product–market fit**                 | Bias toward learning and delivery; invest where a design choice would be costly to reverse.             | Useful for clarifying users, capabilities, and competing meanings. Avoid premature context architecture. | Use selectively around the few rules that already define the product.                                               |
| **Simple CRUD or administrative system**                     | Use clear, deep application or data-access modules and keep accidental complexity low.                  | A shared glossary and one explicit boundary may be enough.                                               | Prefer transaction scripts and value objects; aggregates may add little.                                            |
| **Complex, differentiating business product**                | Use strategic programming continuously; complexity will compound over a long product life.              | Central: find the core domain, bounded contexts, language, ownership, and relationships.                 | Central inside the core; use aggregates and domain events where rules and invariants justify them.                  |
| **Integration platform or distributed estate**               | Hide protocols and failure handling behind stable interfaces; define avoidable errors out of existence. | Strong fit for context maps, published languages, anti-corruption layers, and ownership boundaries.      | Apply within services that contain real domain behaviour, not merely because they are services.                     |
| **Technical library, compiler, database, or infrastructure** | Strong fit: module depth, information hiding, design-it-twice, and low cognitive load are primary.      | Limited unless distinct domain languages or organisational models genuinely compete.                     | Entities or value objects may help, but the full pattern set is rarely the starting point.                          |
| **Regulated or safety-critical domain**                      | Invest heavily in explicit interfaces, local reasoning, and designs that eliminate invalid states.      | Strong fit for precise language, responsibility boundaries, and separation of external models.           | Useful for invariants and auditable domain events, but not a substitute for formal assurance or safety engineering. |
| **Legacy system under active change**                        | Improve strategically in small steps; hide unstable decisions and reduce change amplification.          | Map existing language and boundaries before redrawing them; use an anti-corruption layer around seams.   | Introduce patterns only where a concrete rule or change pressure needs them.                                        |

Domain complexity and software complexity are separate variables. DDD mainly addresses the first; Ousterhout mainly addresses the second. A system can have either one without the other, or both at once.

The expected lifetime and cost of change determine the level of Ousterhout-style investment. Domain differentiation and rule complexity determine the level of DDD investment.

### 4.6 How to combine them

1. **Classify the problem.** Estimate product lifetime, reversibility, software complexity, domain complexity, and business differentiation. Do not infer one from another.
2. **Use strategic DDD to choose where modelling matters.** Identify the core domain, language boundaries, context relationships, and ownership. Keep this lightweight when the domain is simple or still unknown.
3. **Allocate design effort deliberately.** Apply Ousterhout's investment mindset most strongly to long-lived, high-change, or high-risk areas. Make tactical shortcuts explicit and reversible.
4. **Choose the simplest adequate implementation model.** Use tactical DDD for complex rules and invariants; use transaction scripts, CRUD, or technical modules where they communicate the problem better.
5. **Design each implementation well.** Apply information hiding, deep interfaces, design-it-twice, and complexity reduction whether the code contains aggregates, adapters, or ordinary modules.
6. **Revisit both kinds of boundary.** Domain learning may change contexts and aggregates; implementation learning may reveal shallow modules, leaked decisions, or avoidable coupling.

A useful shorthand is: **DDD helps decide what must be modelled together and what must remain separate; Ousterhout helps make each resulting piece easier to understand and change.**

Neither vocabulary is a maturity ladder. “Strategic” is not always superior, and “tactical” is not always inferior. The right choice depends on what is uncertain, expensive, differentiating, and likely to change.

### 4.7 Combined example — AI-Mail

Consider an invoice email with changed bank details. AI-Mail must understand the request, detect possible fraud, prepare a payment, obtain explicit approval, execute safely, and preserve an audit trail.

**Strategic DDD** separates Communication Intake, Obligation Discovery, Action Planning, Authority and Consent, Execution, and Audit because each has a distinct language, responsibility, and rate of change.

**Tactical DDD** gives `ProposedAction` an invariant: only the exact proposal approved by an authorised principal may execute. A changed recipient, amount, bank account, or document digest invalidates approval.

**Ousterhout-style strategic programming** makes each context a deep module. Model prompts, fraud providers, mailbox APIs, payment retries, and audit storage stay behind small interfaces with domain-level inputs and outputs.

One possible flow is:

1. Intake converts the provider message and attachment into evidence.
2. Obligation Discovery identifies an invoice, due date, and suspicious bank-detail change.
3. Action Planning produces a proposal and explains the risk; it cannot move money.
4. Authority and Consent binds approval to the proposal digest and the user's authority scope.
5. Execution accepts only an approved action, performs the payment idempotently, and returns an outcome.
6. Audit records the evidence, model result, proposal, approval, attempt, and outcome.

An **Ousterhout-style tactical** spike is still useful when testing a new payment or model provider. Keep it behind the intended interface, mark it as provisional, and decide explicitly whether to discard or deepen it after learning.

DDD decides which meanings, rules, and ownership boundaries belong together. Ousterhout guides how much design investment to make and how to keep each resulting module simple to understand and change.

---

## Part 5 — Practical Modelling Tools & Canvases

Where DDD stops being reading and starts being work. All free, all CC-licensed, all from the **ddd-crew** ([https://github.com/ddd-crew](https://github.com/ddd-crew)).

| ✓   | Tool                                | URL                                                                                                                                                                                                                                          | What it's for                                                                                                                                                                                                                                                                                             |
|:--- |:----------------------------------- |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅   | **DDD Starter Modelling Process**   | [https://ddd-crew.github.io/ddd-starter-modelling-process/](https://ddd-crew.github.io/ddd-starter-modelling-process/)                                                                                                                       | An 8-step loop: business model → discovery → subdomains → bounded contexts → connections → team organisation → code. Explicitly a beginner scaffold to reduce cognitive load, *not* a linear best practice. Extends Evans' Whirlpool process by aiming at socio-technical architecture.                   |
| ✅   | — GitHub repo                       | [https://github.com/ddd-crew/ddd-starter-modelling-process](https://github.com/ddd-crew/ddd-starter-modelling-process)                                                                                                                       | 5.8k stars. Includes the Whirlpool comparison diagram.                                                                                                                                                                                                                                                    |
| ⚠️  | **EventStorming**                   | [https://www.eventstorming.com/](https://www.eventstorming.com/)                                                                                                                                                                             | Brandolini's collaborative discovery workshop. The step you cannot skip.                                                                                                                                                                                                                                  |
| ✅   | EventStorming Glossary & Cheatsheet | [https://github.com/ddd-crew/eventstorming-glossary-cheatsheet](https://github.com/ddd-crew/eventstorming-glossary-cheatsheet)                                                                                                               | Sticky-note colour semantics in one page.                                                                                                                                                                                                                                                                 |
| ✅   | **Core Domain Charts**              | [https://github.com/ddd-crew/core-domain-charts](https://github.com/ddd-crew/core-domain-charts)                                                                                                                                             | Plot subdomains by model complexity × business differentiation. Decides where to invest. Recommended starting point for the "decompose the domain" step.                                                                                                                                                  |
| ✅   | **Bounded Context Canvas**          | [https://github.com/ddd-crew/bounded-context-canvas](https://github.com/ddd-crew/bounded-context-canvas)                                                                                                                                     | One page per context: purpose, strategic classification, domain roles, inbound/outbound messages (commands, queries, events), ubiquitous language, business rules, and — importantly — **explicit assumptions**.                                                                                          |
| ✅   | — Nick Tune's canvas write-up       | [https://medium.com/nick-tune-tech-strategy-blog/bounded-context-canvas-v2-simplifications-and-additions-229ed35f825f](https://medium.com/nick-tune-tech-strategy-blog/bounded-context-canvas-v2-simplifications-and-additions-229ed35f825f) | The reasoning behind each section. (GitHub has the current version.)                                                                                                                                                                                                                                      |
| ✅   | **Aggregate Design Canvas**         | [https://github.com/ddd-crew/aggregate-design-canvas](https://github.com/ddd-crew/aggregate-design-canvas)                                                                                                                                   | Invariant-first aggregate design. Asks you to list the invariants an aggregate enforces, the **corrective policies** needed when you relax one, and the expected command-handling rate and client count — so concurrency-driven boundary trade-offs become explicit rather than discovered in production. |
| ✅   | Domain Message Flow Modelling       | [https://github.com/ddd-crew/domain-message-flow-modelling](https://github.com/ddd-crew/domain-message-flow-modelling)                                                                                                                       | How contexts actually talk to each other. The step that surfaces hidden coupling.                                                                                                                                                                                                                         |
| ✅   | Collaborative Modelling Prep Canvas | [https://github.com/ddd-crew/como-prep-canvas](https://github.com/ddd-crew/como-prep-canvas)                                                                                                                                                 | For facilitators preparing the workshops above.                                                                                                                                                                                                                                                           |
| ✅   | Debiasing Decisions Toolkit         | [https://github.com/ddd-crew/debiasing-decisions-toolkit](https://github.com/ddd-crew/debiasing-decisions-toolkit)                                                                                                                           | Checklists and canvases for better architecture and technical-leadership decisions.                                                                                                                                                                                                                       |
| ✅   | SAP DDD Kata / curated resources    | [https://github.com/SAP/curated-resources-for-domain-driven-design](https://github.com/SAP/curated-resources-for-domain-driven-design)                                                                                                       | A worked exercise chaining EventStorming → Domain Message Flow → Bounded Context Canvas → Aggregate Canvas, plus a large annotated reading list.                                                                                                                                                          |
| ⚠️  | Miroverse DDD templates             | [https://miro.com/miroverse/](https://miro.com/miroverse/)                                                                                                                                                                                   | Search "EventStorming", "Bounded Context Canvas". Convenient for remote workshops.                                                                                                                                                                                                                        |

---

## Part 6 — Curated Link Collections

When this file is no longer enough.

| ✓   | Collection                                                                                                                                                                                                                          | URL                                                                                                                                    |
|:--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:-------------------------------------------------------------------------------------------------------------------------------------- |
| ✅   | ardalis / **awesome-ddd**                                                                                                                                                                                                           | [https://github.com/ardalis/awesome-ddd](https://github.com/ardalis/awesome-ddd)                                                       |
| ✅   | heynickc / awesome-ddd (fork with extra courses)                                                                                                                                                                                    | [https://github.com/heynickc/awesome-ddd](https://github.com/heynickc/awesome-ddd)                                                     |
| ✅   | mehdihadeli / **awesome-software-architecture**                                                                                                                                                                                     | [https://github.com/mehdihadeli/awesome-software-architecture](https://github.com/mehdihadeli/awesome-software-architecture)           |
| ✅   | ddd-crew / free-ddd-learning-resources                                                                                                                                                                                              | [https://github.com/ddd-crew/free-ddd-learning-resources](https://github.com/ddd-crew/free-ddd-learning-resources)                     |
| ✅   | SAP / curated-resources-for-domain-driven-design                                                                                                                                                                                    | [https://github.com/SAP/curated-resources-for-domain-driven-design](https://github.com/SAP/curated-resources-for-domain-driven-design) |
| ✅   | socadk / design-practice-repository                                                                                                                                                                                                 | [https://github.com/socadk/design-practice-repository](https://github.com/socadk/design-practice-repository)                           |
| ✅   | ciembor / **agent-rules-books** — design books (APoSD, DDD, PoEAA, WELC, Clean Code, …) distilled into actionable agent rule sets                                                                                                   | [https://github.com/ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books)                                           |
| ✅   | ZLStas / **skills** — closest direct alternative to `agent-rules-books`: book-based skills as slash commands, agents, and installers for Python, TypeScript, Rust, JVM, architecture, data engineering                              | [https://github.com/ZLStas/skills](https://github.com/ZLStas/skills)                                                                   |
| ✅   | nathankim0 / **clean-architecture-skills** — Clean Architecture reviews, dependency-rule validation, SOLID, Kent Beck-style simple design, code-smell detection                                                                     | [https://github.com/nathankim0/clean-architecture-skills](https://github.com/nathankim0/clean-architecture-skills)                     |
| ✅   | ForceInjection / **domain-driven-design-skills** — end-to-end DDD agent workflow: discovery → strategic → tactical → validation → spec bridging                                                                                     | [https://github.com/ForceInjection/domain-driven-design-skills](https://github.com/ForceInjection/domain-driven-design-skills)         |
| ✅   | zudochkin / **go-clean-ddd-skill** — interactive DDD modelling agent skill, Go-specific implementation and code generation                                                                                                          | [https://github.com/zudochkin/go-clean-ddd-skill](https://github.com/zudochkin/go-clean-ddd-skill)                                     |
| ✅   | SebastienDegodez / **copilot-instructions** — instructions, prompts, skills, and agent personas incl. DDD, Clean Architecture, and CQRS; strongest for C#/.NET                                                                      | [https://github.com/SebastienDegodez/copilot-instructions](https://github.com/SebastienDegodez/copilot-instructions)                   |
| ✅   | codewithmukesh / **dotnet-claude-kit** — .NET-oriented skills for DDD, Clean Architecture, and architecture assessment; explicitly warns against over-applying either where complexity doesn't justify it                           | [https://github.com/codewithmukesh/dotnet-claude-kit](https://github.com/codewithmukesh/dotnet-claude-kit)                             |
| ✅   | danmestas / **agent-skills** — mixed collection of design, testing, DevOps, and project-management agent skills                                                                                                                     | [https://github.com/danmestas/agent-skills](https://github.com/danmestas/agent-skills)                                                 |
| ✅   | VoltAgent / **awesome-agent-skills** — large curated index of agent skills across Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenCode, Windsurf                                                                               | [https://github.com/VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)                                 |
| ✅   | kodustech / **awesome-agent-skills** — smaller catalogue focused on reusable `SKILL.md` projects for software engineering                                                                                                           | [https://github.com/kodustech/awesome-agent-skills](https://github.com/kodustech/awesome-agent-skills)                                 |
| ✅   | wondelai / **skills** — Clean Architecture (Dependency Rule, SOLID) and DDD (bounded contexts, aggregates, ubiquitous language) skills inside a ~50-skill business/engineering framework pack, agentskills.io-compatible            | [https://github.com/wondelai/skills](https://github.com/wondelai/skills)                                                               |
| ✅   | MuhiminOsim / **code-refactoring-skill** — enforced, cross-agent five-phase refactoring workflow (intake → diagnose → plan → execute → wrap-up) with a stricter introduce → redirect → remove sub-protocol for architectural change | [https://github.com/MuhiminOsim/code-refactoring-skill](https://github.com/MuhiminOsim/code-refactoring-skill)                         |
| ✅   | addyosmani / **agent-skills** — 24 full-lifecycle engineering skills grounded in *Software Engineering at Google*, installable into 70+ agents                                                                                      | [https://github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)                                               |
| ✅   | github / **awesome-copilot** — GitHub's official Copilot instructions/agents/skills collection; includes a `review-and-refactor` skill that enforces a project's own `.github/instructions/*.md` standards                          | [https://github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)                                                 |
| ⚠️  | arozumenko / **sdlc-skills** — SDLC agents/skills (Jira/Atlassian integration, shared skill registry); process and tooling automation rather than a design method                                                                   | [https://github.com/arozumenko/sdlc-skills](https://github.com/arozumenko/sdlc-skills)                                                 |

For a comparison of these against `agent-rules-books`, a recommended evaluation order, and a "software design methods referenced" breakdown per repository, see [`agent-rules-github-repositories.md`](./agent-rules-github-repositories.md).

---

## Part 7 — Books

Several of these books are also distilled into actionable, tool-agnostic rule sets for coding agents by the third-party MIT-licensed [`agent-rules-books`](https://github.com/ciembor/agent-rules-books) project (each in `full` / `mini` / `nano` sizes). Those are working agreements for code generation and review, not summaries or a substitute for the book. Where one exists, the row below links both the local clone and the upstream repo.

| Book                                                    | Author                | Comment                                                                                                                                                                                                                                                                                                                     |
|:------------------------------------------------------- |:--------------------- |:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| *A Philosophy of Software Design* (2nd ed., 2021\)      | John Ousterhout       | \~190 pages. The source of the strategic/tactical *programming* distinction. **Agent rules:** [local](C:/PROJ/github/agent-rules-books/a-philosophy-of-software-design/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/a-philosophy-of-software-design)                                                 |
| *Learning Domain-Driven Design*                         | Vlad Khononov         | The best modern DDD introduction. Start here, not with Evans.                                                                                                                                                                                                                                                               |
| *Domain-Driven Design* ("Blue Book", 2004\)             | Eric Evans            | The original. Dense. Read the free Reference PDF first, or the Manager's Guided Tour. **Agent rules:** [local](C:/PROJ/github/agent-rules-books/domain-driven-design/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/domain-driven-design)                                                              |
| *Implementing Domain-Driven Design* ("Red Book", 2013\) | Vaughn Vernon         | Where the strategic/tactical framing was popularised. Practical, long. **Agent rules:** [local](C:/PROJ/github/agent-rules-books/implementing-domain-driven-design/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/implementing-domain-driven-design)                                                   |
| *Domain-Driven Design Distilled*                        | Vaughn Vernon         | \~150 pages, if the Red Book is too much. **Agent rules:** [local](C:/PROJ/github/agent-rules-books/domain-driven-design-distilled/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/domain-driven-design-distilled)                                                                                      |
| *Team Topologies*                                       | Skelton & Pais        | Bounded contexts as team boundaries.                                                                                                                                                                                                                                                                                        |
| *Software Architecture: The Hard Parts*                 | Ford, Richards et al. | Decomposition trade-offs when the neat model meets reality.                                                                                                                                                                                                                                                                 |
| *Fundamentals of Software Architecture*                 | Richards & Ford       | Broad survey; useful vocabulary.                                                                                                                                                                                                                                                                                            |
| *Patterns of Enterprise Application Architecture*       | Martin Fowler         | Source of Domain Model and Transaction Script — the choice tactical DDD assumes you've made. **Agent rules:** [local](C:/PROJ/github/agent-rules-books/patterns-of-enterprise-application-architecture/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/patterns-of-enterprise-application-architecture) |
| *Working Effectively with Legacy Code*                  | Michael Feathers      | What you actually need when applying any of the above to an existing system. **Agent rules:** [local](C:/PROJ/github/agent-rules-books/working-effectively-with-legacy-code/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/working-effectively-with-legacy-code)                                       |
| *Clean Code*                                            | Robert C. Martin      | Widely read; Ousterhout explicitly disagrees with parts of it. Read both, then read their debate, then form a view. **Agent rules:** [local](C:/PROJ/github/agent-rules-books/clean-code/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/clean-code)                                                    |

---

## 8. Suggested Reading Paths

**If you meant Ousterhout (\~4 hours):**

1. Watch the Talks at Google video.  
2. Read Dan Lebrero's notes to see the shape of the whole book.  
3. Read Fowler's *Design Stamina Hypothesis* and *Yagni* as the two poles.  
4. Read Parnas (1972). It is short and it is the foundation.  
5. Skim the Ousterhout–Uncle Bob debate to see where the consensus isn't.  
6. Buy the book (2nd edition). It is 190 pages.

**If you meant DDD (\~a weekend):**

1. Skim the Evans DDD Reference PDF for vocabulary.  
2. Read Vaadin Part 1 (strategic), then Part 2 (tactical).  
3. Read Fowler on *Bounded Context* and *DDD\_Aggregate*.  
4. Read Vernon's *Effective Aggregate Design*, Part I.  
5. Open the Bounded Context Canvas and fill one in for a system you already know.  
6. Then the Aggregate Design Canvas for one aggregate in that system.  
7. If it clicked, buy Khononov.

**If you're not sure which you meant:** read Part 4 first. Ousterhout applies broadly to software complexity. DDD is most useful when domain rules, language, boundaries, or organisational relationships are complex.

---

## 9. Glossary

Terms from both senses of "strategic and tactical design" — Ousterhout's and DDD's — are defined in the shared [glossary.md](./glossary.md): the [Ousterhout / A Philosophy of Software Design](./glossary.md#a-philosophy-of-software-design-ousterhout) section, and the [Domain-Driven Design](./glossary.md#domain-driven-design-ddd) section (split into [Strategic DDD](./glossary.md#strategic-ddd) and [Tactical DDD](./glossary.md#tactical-ddd)).

---

## 10. Verification Log

Checked 10 July 2026 against live search results.

**Corrected (previous draft was wrong):**

1. Microsoft Learn tactical DDD — was `.../microservices/model/tactical-ddd`, actual path is `.../microservices/model/tactical-domain-driven-design`.  
2. Parnas 1972 PDF — the `win.tue.nl/~wstomv/...` path could not be confirmed. Replaced with the ACM DOI plus an author-uploaded PDF.  
3. Stanford CS 190 — the `cs190-winter25` path could not be confirmed; that page rolls over each academic year. Replaced with the Winter 2019 lecture notes (stable) and the Stanford catalogue entry.

**Confirmed and unchanged:** all ddd-crew repositories, the Evans DDD Reference (page and PDF), martinfowler.com bliki pages for BoundedContext / DDD\_Aggregate / DesignStaminaHypothesis, the Talks at Google video ID, IDDD\_Samples, dddcommunity's Effective Aggregate Design PDFs, Out of the Tar Pit at curtclifton.net, and all Medium / dev.to / DZone / Vaadin Part 1 articles.

**Added during verification:** the Ousterhout–Uncle Bob debate repo, the Pragmatic Engineer interview and review, Ousterhout's aposd.php resources page, Domain Language's resources hub, the direct DDD Reference PDF, Vernon's three Effective Aggregate Design PDFs, the .NET IDDD sample, SOCADK's design practice repository, SAP's curated DDD resources, James Hickey on aggregates, archi-lab.io's course pages, and four awesome-lists.

**Marked ⚠️ (exist, URL unverified this session):** several martinfowler.com articles (is-high-quality-software-worth-cost, TechnicalDebt, Yagni, EventSourcing), eventstorming.com, Vaadin Part 2, arc42.org, adr.github.io, teamtopologies.com, miro.com/miroverse, the InfoQ *DDD Quickly* minibook, and the Brooks Wikipedia article. These are all well-known and near-certainly live, but I did not confirm them directly.

*Removed from the previous draft:* the c2.com software-architecture wiki page (couldn't confirm, and the wiki's link structure has changed over the years).  
