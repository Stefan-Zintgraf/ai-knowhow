# Graph Report - .  (2026-05-27)

## Corpus Check
- 119 files · ~90,204 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 240 nodes · 303 edges · 31 communities (22 shown, 9 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Distill-Idea Test Fixtures|Distill-Idea Test Fixtures]]
- [[_COMMUNITY_Skill Development Pipeline|Skill Development Pipeline]]
- [[_COMMUNITY_Code Quality Guardrails|Code Quality Guardrails]]
- [[_COMMUNITY_Phase Skill Test Fixtures|Phase Skill Test Fixtures]]
- [[_COMMUNITY_Design Decision Framework|Design Decision Framework]]
- [[_COMMUNITY_Idea Phase Guardrails|Idea Phase Guardrails]]
- [[_COMMUNITY_Skill Tooling Concepts|Skill Tooling Concepts]]
- [[_COMMUNITY_Triage Engine|Triage Engine]]
- [[_COMMUNITY_Prototype Phase Rules|Prototype Phase Rules]]
- [[_COMMUNITY_TDD and Module Depth|TDD and Module Depth]]
- [[_COMMUNITY_Prototype Guardrail|Prototype Guardrail]]
- [[_COMMUNITY_Phase Transition Controls|Phase Transition Controls]]
- [[_COMMUNITY_Claude Mode Config|Claude Mode Config]]
- [[_COMMUNITY_Status Script Pipeline|Status Script Pipeline]]
- [[_COMMUNITY_Claude Permissions Config|Claude Permissions Config]]
- [[_COMMUNITY_Claude Hooks Config|Claude Hooks Config]]
- [[_COMMUNITY_Issue Tracker Agents|Issue Tracker Agents]]
- [[_COMMUNITY_Knowledge Graph Tools|Knowledge Graph Tools]]
- [[_COMMUNITY_Skills Registry|Skills Registry]]
- [[_COMMUNITY_B10 Exploration Budget|B10 Exploration Budget]]
- [[_COMMUNITY_Phase Skill A1|Phase Skill A1]]
- [[_COMMUNITY_Phase Skill A4|Phase Skill A4]]
- [[_COMMUNITY_Phase Skill A6|Phase Skill A6]]
- [[_COMMUNITY_Distill-Idea Suite Hyperedge|Distill-Idea Suite Hyperedge]]
- [[_COMMUNITY_JWT Auth Migration Test|JWT Auth Migration Test]]
- [[_COMMUNITY_Direct-Edit Field Test|Direct-Edit Field Test]]

## God Nodes (most connected - your core abstractions)
1. `distill-idea Test Plan` - 23 edges
2. `Phase Skill Test Plan` - 13 edges
3. `Idea Guardrail` - 10 edges
4. `Test Plan: triage-idea Skill` - 9 edges
5. `draft-skill-tests Skill` - 8 edges
6. `draft-skill-input SKILL.md` - 7 edges
7. `coding_plan.md — Operationalization Tracker` - 7 edges
8. `Review Guardrail` - 7 edges
9. `Alignment Guardrail` - 6 edges
10. `gr_idea.md (Idea Requirements Source)` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Graphify Pre-Tool Bash Hook` --implements--> `CLAUDE.md — Project Instructions`  [INFERRED]
  .claude/settings.json → CLAUDE.md
- `Skills Registry (skills.json)` --references--> `coding_plan.md — Operationalization Tracker`  [INFERRED]
  .claude/skills/status/skills.json → coding_plan.md
- `Get-NextAction PowerShell Script` --references--> `A12 phase Skill`  [INFERRED]
  .claude/skills/status/Get-NextAction.ps1 → coding_plan.md
- `ai_mail Run Idea Goals` --semantically_similar_to--> `Coding Workflow Idea Goals`  [INFERRED] [semantically similar]
  skills/run/plan/ai_mail/idea.md → plan/coding_workflow/idea.md
- `Get-ActiveWI PowerShell Script` --references--> `ACTIVE WI Pointer File (plan/ACTIVE)`  [EXTRACTED]
  .claude/skills/status/Get-ActiveWI.ps1 → coding_plan.md

## Hyperedges (group relationships)
- **Status Dashboard Script Pipeline** — get_active_wi, get_skill_freshness, get_map_and_test_freshness, get_next_action [EXTRACTED 1.00]
- **Skill Authoring Chain (draft → compile)** — draft_skill_input, compile_skill, template_skill_in [EXTRACTED 1.00]
- **Phase Transition Infra (ACTIVE + phase_status.md)** — active_wi_pointer, phase_status_md, phase_skill_a12 [EXTRACTED 1.00]
- **Skill Build Pipeline (draft → compile → test → verify)** — make_skill_skill, draft_skill_tests_skill, test_skill_skill, run_skill_skill [EXTRACTED 1.00]
- **Core Guardrail Set (architecture, governance, coding style, brownfield)** — gr_architecture, gr_governance, gr_brownfield, gr_coding_style, gr_ddd [INFERRED 0.85]
- **Alignment and Documentation Cluster** — gr_algn, gr_adr, gr_domain_language, concept_grill_with_docs, concept_ubiquitous_language, concept_adr [INFERRED 0.85]
- **HITL-Required Phase Guardrails** — gr_idea_idea_guardrail, gr_proto_prototype_guardrail, gr_qa_manual_qa_guardrail [EXTRACTED 1.00]
- **distill-idea Skill Chain (input -> output)** — skills_input_distill_idea_in, plan_cw_idea_coding_workflow_idea, gr_idea_idea_guardrail [EXTRACTED 1.00]
- **phase Skill Chain (input -> log -> output -> log)** — skills_input_phase_in, skills_input_log_phase_000, skills_output_phase, skills_output_log_phase_000 [EXTRACTED 1.00]
- **Status Skill PowerShell Pipeline** — skills_status_get_active_wi, skills_status_get_skill_freshness, skills_status_get_map_test_freshness, skills_status_get_next_action [EXTRACTED 1.00]
- **Artifact Retirement at QA Gate** — gr_qa_ephemeral_artifact_retirement, gr_res_sprint_scoped_research, gr_idea_status_idea_artifact [EXTRACTED 1.00]
- **distill-idea Input/Output Fixture Pairs** — distillidea_input000, distillidea_output000, distillidea_input001, distillidea_output001, distillidea_input002, distillidea_output002, distillidea_input003, distillidea_output003, distillidea_input004, distillidea_output004, distillidea_input005, distillidea_output005, distillidea_input006, distillidea_output006, distillidea_input007, distillidea_output007, distillidea_input008, distillidea_output008, distillidea_input009, distillidea_output009 [EXTRACTED 1.00]
- **distill-idea Source Documentation** — distillidea_gr_idea, distillidea_guardrails, distillidea_phases [EXTRACTED 1.00]
- **Phase Skill Test Fixture Pairs** — phase_input001, phase_output001, phase_input002, phase_output002, phase_input003, phase_output003, phase_input004, phase_output004, phase_input005, phase_output005, phase_input006, phase_output006 [EXTRACTED 1.00]
- **Triage-Idea Skill Test Fixture Pairs** — triageidea_input000, triageidea_output000, triageidea_input001, triageidea_output001, triageidea_input002, triageidea_input003, triageidea_input004, triageidea_input005 [INFERRED 0.95]
- **Phase Guardrail Enforcement Mechanisms** — phase_tripwire_halt, phase_mode_legal_guard, phase_exit_artifact_guard, phase_statusreadonly, phase_next_phase_computed [INFERRED 0.85]
- **Triage-Idea Test Suite (Outputs 002–005 + Test Plan)** — output002_triage_complex_auth_full, output003_triage_tripwire_public_api, output004_triage_remode_concurrency, output005_triage_budget_exceeded, triageidea_testplan [EXTRACTED 1.00]
- **Core Triage Mechanisms (4-Axis, Tripwire, HITL, Budget, Remode)** — four_axis_triage, tripwire_surface_detection, hitl_mode_confirmation, exploration_budget, remode_flag [EXTRACTED 1.00]
- **Prototype Workflow + Template Pair (wf_proto + tpl_var_pres)** — wf_proto, tpl_var_pres, variant_presentation_c6, pro_no_recommendation, hidden_constraint_check, proto_sandbox_deletion, proto_flavors [EXTRACTED 1.00]

## Communities (31 total, 9 thin omitted)

### Community 0 - "Distill-Idea Test Fixtures"
Cohesion: 0.09
Nodes (35): Plan Artifact Retirement at WI Close (3.33), Concept Sharpening for Vague Notions (Idea12), Implementation Detail Stripping, IDE-time Exploration Budget (≤5 Reads, Idea10), idea.md + status_idea.md Persistence to plan/<WI>/, Goal Count Rule (3-6 Major Goals), gr_idea.md (Idea Requirements Source), guardrails.md (Guardrails Source) (+27 more)

### Community 1 - "Skill Development Pipeline"
Cohesion: 0.16
Nodes (22): ACTIVE WI Pointer File (plan/ACTIVE), AI_Coding_Workflow.md — Planning Workflow Guide, coding_plan.md — Operationalization Tracker, compile-skill SKILL.md, draft-skill-input SKILL.md, Get-ActiveWI PowerShell Script, Get-MapAndTestFreshness PowerShell Script, Get-NextAction PowerShell Script (+14 more)

### Community 2 - "Code Quality Guardrails"
Cohesion: 0.11
Nodes (21): Gray-Box Labor Partition (M3a), Module Depth Guardrail, Module Depth Heuristics (M11), Definition of Done (Op3), No Fabrication Rule (Op13), Operational and Agent Execution Guardrail, Parallel Isolation and Sequential Integration Queue (Op16), Push vs Pull Standards Delivery (Op14b) (+13 more)

### Community 3 - "Phase Skill Test Fixtures"
Cohesion: 0.13
Nodes (20): Phase Exit Artifact Guard, Phase Test Input 001 - Exit IDE with HITL Ack, Phase Test Input 002 - Status No Active WI, Phase Test Input 003 - Status needs_research=true, Phase Test Input 004 - Status tripwire_halt=true, Phase Test Input 005 - Enter ALN Rejected direct-edit, Phase Test Input 006 - Exit IDE Missing idea.md, next_phase Computed at Read Time (+12 more)

### Community 4 - "Design Decision Framework"
Cohesion: 0.14
Nodes (19): Architectural Decision Record (ADR), context.md Durable Domain Doc, DAG-based Implementation Plan, Grill-With-Docs Pattern, Human-in-the-Loop (HITL), Ubiquitous Language / context.md, Vertical Slice Enforcement, Domain Docs Agent Guide (+11 more)

### Community 5 - "Idea Phase Guardrails"
Cohesion: 0.17
Nodes (19): Concept Sharpening (Sub-Brief Input), Goal Distillation (3-6 Major Goals), ide Phase (Entry Phase), Idea Guardrail, Mode Transitions (Symmetric HITL-Approved), status_idea.md Artifact, Triage Matrix (4-axis mode selection), Workflow Modes (direct-edit / mini / full) (+11 more)

### Community 6 - "Skill Tooling Concepts"
Cohesion: 0.22
Nodes (15): coding_plan.md, Frozen Reference Files, guardrails.md, LLM-as-Judge Evaluation, Rule-to-Skill Map, skills/output/ Folder, skills/test/ Folder, Test Fixture Pair (input/output) (+7 more)

### Community 7 - "Triage Engine"
Cohesion: 0.29
Nodes (13): Exploration Budget (≤5 File Reads), 4-Axis Triage Scoring, HITL Mode Confirmation, Triage Output: Complex Auth Replacement → Full Mode, Triage Output: Tripwire Public API Forces Full, Triage Output: --remode Mid-WI Upgrade on Concurrency Tripwire, Triage Output: Exploration Budget Exceeded → Auto-Recommend Mini, --remode Mid-WI Upgrade Flag (+5 more)

### Community 8 - "Prototype Phase Rules"
Cohesion: 0.24
Nodes (10): Hidden Constraint Check (Pro7), Idea Goal List Artifact (C8), Pro4: No Agent Self-Judging (No Recommendation Field), Prototype Flavors: FE / Architecture / Integration, Pro3: Sandbox Deletion Precondition, status_idea.md State Machine, Template: Idea Goal List (C8), Template: Prototype Variant Presentation (C6) (+2 more)

### Community 9 - "TDD and Module Depth"
Cohesion: 0.22
Nodes (9): Deep Modules Principle, Direct-Edit Mode TDD Exemption (TDD11), Mock Discipline (TDD6), Red-Green-Refactor TDD Loop, TDD Guardrail, Characterization Tests for Legacy (T4), Testing and Verification Guardrail, Verification Plan Before Implementation (T1) (+1 more)

### Community 10 - "Prototype Guardrail"
Cohesion: 0.32
Nodes (8): Caller Persists Pattern (Pro5), pro Phase (Prototype Phase), Prototype Guardrail, Prototype Three Flavors (FE / Architecture / Integration), Throwaway by Construction (Pro3), Research File Provenance (owner-issue, date, source), Research Guardrail, Sprint-Scoped Research Artifact

### Community 11 - "Phase Transition Controls"
Cohesion: 0.29
Nodes (7): Phase Mode-Legal Entry Guard, Four-Axis Triage Model, HITL Mode Confirmation Requirement, Triage-Idea Test Input 000 - Trivial Typo Fix, Triage-Idea Test Input 001 - Email Validation Mini, Triage-Idea Test Output 000 - Direct-Edit Mode Criteria, Triage-Idea Test Output 001 - Mini Mode Criteria

### Community 12 - "Claude Mode Config"
Cohesion: 0.40
Nodes (5): Caveman Mode — Terse Response Style, CLAUDE.md — .claude Subfolder Instructions, CLAUDE.md — Project Instructions, Graphify Pre-Tool Bash Hook, Socrates Mode — Socratic Mentor Style

### Community 13 - "Status Script Pipeline"
Cohesion: 0.70
Nodes (5): Status Skill PowerShell Script Interfaces, Get-ActiveWI.ps1 Script, Get-MapAndTestFreshness.ps1 Script, Get-NextAction.ps1 Script, Get-SkillFreshness.ps1 Script

### Community 14 - "Claude Permissions Config"
Cohesion: 0.50
Nodes (3): permissions, additionalDirectories, allow

### Community 16 - "Issue Tracker Agents"
Cohesion: 0.67
Nodes (3): GitHub Issues as Issue Tracker, Issue Tracker Agent Guide, Triage Labels Agent Guide

### Community 17 - "Knowledge Graph Tools"
Cohesion: 0.67
Nodes (3): Community Detection, Knowledge Graph, graphify Skill

## Knowledge Gaps
- **26 isolated node(s):** `PreToolUse`, `allow`, `additionalDirectories`, `created_at`, `skills` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 4 inferred relationships involving `Test Plan: triage-idea Skill` (e.g. with `Exploration Budget (≤5 File Reads)` and `4-Axis Triage Scoring`) actually correct?**
  _`Test Plan: triage-idea Skill` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PreToolUse`, `allow`, `additionalDirectories` to the rest of the system?**
  _67 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Distill-Idea Test Fixtures` be split into smaller, more focused modules?**
  _Cohesion score 0.08739495798319327 - nodes in this community are weakly interconnected._
- **Should `Code Quality Guardrails` be split into smaller, more focused modules?**
  _Cohesion score 0.10952380952380952 - nodes in this community are weakly interconnected._
- **Should `Phase Skill Test Fixtures` be split into smaller, more focused modules?**
  _Cohesion score 0.13157894736842105 - nodes in this community are weakly interconnected._
- **Should `Design Decision Framework` be split into smaller, more focused modules?**
  _Cohesion score 0.14035087719298245 - nodes in this community are weakly interconnected._