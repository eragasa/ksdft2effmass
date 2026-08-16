# V2-ISSUE-007: Selection identity closure

**Severity:** High
**Scope:** Generic and Workflow-level enablement, selection, firing, and replay provenance
**Status:** Open

## Current conflict

The firing record does not retain one identity-closed derivation from exact enablement through generic or Workflow-level selection to firing. Generic selection, `any_of`, `all_of`, direct invocation, scientific-decision ingress, and permitted directives therefore cannot all produce the exact identified selection that the firer and replay contract claim to validate.

## Affected contracts

- [`docs/architecture/v2/petrinet/colored.md`](../petrinet/colored.md) — firing input omits the enablement-result, identified-selection, and optional directive identities required by the firer's validation claim.
- [`docs/architecture/v2/workflow/task-and-colored-petri-net-adapter.md`](../workflow/task-and-colored-petri-net-adapter.md) — Workflow gate policies, direct invocation, and decision ingress derive bindings without one common identified-selection derivation.
- [`docs/architecture/v2/workflow/workflow-run.md`](../workflow/workflow-run.md) — transition history retains firing input as replay evidence, so the identity gap reaches replay.
- [`docs/architecture/v2/workflow/control-plane.md`](../workflow/control-plane.md) — direct and decision-origin ingress introduce bindings outside the generic selector path.
- [`docs/architecture/v2/identity-version-and-failure-contracts.md`](../identity-version-and-failure-contracts.md) — replay sufficiency and exact identity binding are claimed without the missing selection identities.

## Missing contract

One closed contract is missing for binding the exact enablement result, selector result, optional directive, and deterministic `any_of`, `all_of`, direct-invocation, and decision-ingress derivations through firing input, firing result, transition history, and replay.

## Exclusions and claim boundary

Exact field names and wire spelling are excluded. This record does not define implementation, verification, protected-execution authority, scientific validation, uncertainty quantification, or human acceptance.
