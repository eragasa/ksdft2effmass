# V2-ISSUE-024: Publication requirement policy, artifact-store publication, and reconciliation closure

**Severity:** High
**Scope:** Publication obligations, no-publication decisions, artifact-store effects, receipts, and reconciliation
**Status:** Open

## Current conflict

Result ingress must create every required publication obligation or an explicit no-publication disposition, but no immutable policy owns that determination. The publisher and reconciler also lack the authoritative store observation, conditional or idempotent write, receipt, access/confinement, and partial-state contracts required to enforce the publication obligation.

## Affected contracts

- [`docs/architecture/v2/principles.md`](../principles.md) — no-lost-publication is preserved without a complete policy and store capability boundary.
- [`docs/architecture/v2/workflow/control-plane.md`](../workflow/control-plane.md) — result ingress must choose obligations or explicit no-publication without an identified immutable policy owner.
- [`docs/architecture/v2/workflow/artifact-and-provenance-model.md`](../workflow/artifact-and-provenance-model.md) — publication and reconciliation are required while store observations, receipts, idempotency, and access behavior remain deferred.
- [`docs/architecture/v2/workflow/service-model.md`](../workflow/service-model.md) — publisher and reconciler services lack closed store-facing results.
- [`docs/architecture/v2/composition-root.md`](../composition-root.md) — composition does not supply the policy and authoritative store capability needed by ingress and reconciliation.
- [`docs/architecture/v2/separation-of-harness-and-workflow.md`](../separation-of-harness-and-workflow.md) — bounded scientific publication effects lack a complete ownership path from obligation policy through store observation.

## Missing contract

The publication lifecycle lacks an immutable versioned requirement policy, identified no-publication semantics, authoritative destination and store observations, conditional/idempotent writes, content-bound receipts, access and confinement failures, partial-state classification, and reconciliation results tied to committed obligations.

## Exclusions and claim boundary

Exact URI spelling and physical artifact-store design are excluded. This record does not authorize publication or establish implementation, verification, scientific validation, uncertainty quantification, or human acceptance.
