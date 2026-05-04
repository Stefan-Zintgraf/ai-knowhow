# Architecture: <Plan Title>

## Goal

<One paragraph. What structure this document fixes.>

This is the structural counterpart to [<plan_name>.strategy.md](<plan_name>.strategy.md) (remove line if not used). It fixes boundaries between planning artifacts, scripts, and runtime.

## Problem boundary

- <hard constraint 1>
- <hard constraint 2>

## Pipeline overview

```text
<ASCII or mermaid diagram of the end-to-end flow>
```

## Single source of truth: `<artifact>`

<Describe the authoritative data artifact: schema, fields, status machines, invariants.>

## Module and script boundaries

| Artifact | Responsibility |
|----------|----------------|
| `<path>` | <role> |
| `<path>` | <role> |

## Matching / normalization / shared logic

<Describe any cross-cutting logic that multiple scripts must share.>

## Corpus / external system alignment

<How this plan's artifacts align with existing systems; do not introduce competing semantics.>

## File map (implementation deliverables)

| File | Role |
|------|------|
| `<path>` | <role> |

## Storage policy

<What is committed, what is ignored, lifecycle.>

## Key decisions

| # | Question | Resolution |
|---|----------|------------|
| 1 | <question> | <resolution> |

## Risk-driven constraints

- <constraint>

## Rejected alternatives

| Option | Why rejected |
|--------|--------------|
| <option> | <reason> |
