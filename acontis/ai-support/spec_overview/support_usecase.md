---
marp: true
theme: default
size: 16:9
paginate: true
---

<!-- _class: lead -->
# Support use case
## Zammad, RAG, and human review

Draft answers from internal knowledge — **every customer reply is human-approved.**

# Goal

- **Faster support** — draft from internal knowledge and historical tickets.
- **Privacy** — keep PII out of the RAG/LLM path where possible.
- **Control** — no customer sees a reply until a **human engineer** approves it.

---

# Actors and systems

| Component | Role |
|-----------|------|
| **Zammad** | Ticketing, assignment, notes, customer comms |
| **AI agent user** | Zammad user that "owns" tickets during automation |
| **Anonymization** | Strips/masks customer-specific data before RAG/LLM |
| **Local RAG** | On-prem; indexes processed tickets + company knowledge |
| **LLM** | Drafts answers from retrieved context |
| **Human engineer** | Reviews draft, sends final answer to customer |

---

# Automated processing

1. **Ticket intake** — new ticket assigned to the **AI agent user** (explicit, traceable).
2. **Read & anonymize** — strip PII (names, emails, addresses, account IDs, ...) before anything hits logs, prompts, or retrieval.
3. **Local RAG retrieval** — anonymized question retrieves passages from **historical tickets** and **company knowledge**.
4. **LLM draft** — retrieved context + anonymized text form an augmented prompt; LLM produces a **proposed answer**.
5. **Store draft** — saved as **internal note** on the ticket (not sent to customer); preserves context and audit trail.

---

# Human review and reply

6. **Handoff** — ticket reassigned to a human engineer (or routed per group/queue rules).
7. **Review & send** — engineer reviews the note, edits as needed, sends the **final answer** through Zammad.

```text
New ticket → Assign (AI) → Read → Anonymize → Local RAG → LLM → Internal note
                                                                    ↓
                                    Assign (human) → Review note → Reply to customer
```

