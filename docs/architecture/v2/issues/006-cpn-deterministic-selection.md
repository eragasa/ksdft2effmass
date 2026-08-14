# V2-ISSUE-006: Deterministic CPN transition and binding selection

**Severity:** High

**Scope:** Colored-Petri-net and scientific-workflow scheduling

## Conflict

Firing from an already selected binding is deterministic, but canonical enabled-binding ordering, selection among multiple bindings or transitions, and fairness remain unresolved. `ScientificService` nevertheless claims to advance deterministic transitions.

## Affected contracts

- `petrinet/colored/index.md` — *Contracts* and unresolved selection rules
- `workflow/service-model.md` — deterministic advancement claim
- `workflow/scientific/index.md` — external action protocol

## Required resolution

Distinguish deterministic enablement and firing from scheduling selection. Define canonical ordering and a versioned selection policy, or require an explicit caller-supplied transition and binding identity. Represent operator choice as an identified input rather than hidden nondeterminism.

## Acceptance condition

Equivalent definition, marking, and explicit operation inputs produce the same ordered enabled set and selected transition, or an explicit choice requirement.
