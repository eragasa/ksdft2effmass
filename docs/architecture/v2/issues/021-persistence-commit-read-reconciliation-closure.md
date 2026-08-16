# V2-ISSUE-021: Persistence commit, read, idempotency, reconciliation, and domain reconstruction closure

**Severity:** Critical
**Scope:** Domain commit validation and serialization binding, shared revision reads, domain reconstruction, commit reconciliation, and idempotency
**Status:** Open

## Current conflict

The selected domain repositories must invoke and bind their exact validators and serializers before store commit, but live workflow and decision pages still describe repositories as only committing units validated elsewhere. Independently, `AtomicRevisionStore.load` cannot distinguish absence from operational, corrupt, incompatible, or indeterminate state; identity-bound reconciliation is required but unsupported by the read contract; idempotency collision and replay semantics are incomplete; and domain repositories have no corresponding reconstruction-time serializer, validator, and identity binding.

## Affected contracts

- [`docs/architecture/v2/persistence/index.md`](../persistence/index.md) — `load` returns only a revision or absence despite represented-version failures and identity-bound reconciliation requirements.
- [`docs/architecture/v2/workflow/persistence.md`](../workflow/persistence.md) — write-time serializer and validator binding has no equivalent reconstruction contract.
- [`docs/architecture/v2/harness/persistence.md`](../harness/persistence.md) — HarnessState loading does not close byte, schema, source-provenance, deserialization, and domain-validation checks.
- [`docs/architecture/v2/identity-version-and-failure-contracts.md`](../identity-version-and-failure-contracts.md) — operations require closed failures and represented incompatible-version outcomes that `load` cannot express.
- [`docs/architecture/v2/human-decisions.md`](../human-decisions.md) — retains the former passive-repository wording and also lacks an identity-bound read path after an indeterminate decision commit.
- [`docs/architecture/v2/workflow/task-and-colored-petri-net-adapter.md`](../workflow/task-and-colored-petri-net-adapter.md) — still describes repositories as committing already-validated successors rather than invoking and binding the selected validator and serializer.
- [`docs/architecture/v2/analysis/analysis-and-disposition.md`](../analysis/analysis-and-disposition.md) — describes an already-validated recording transaction and cannot propagate or reconcile the selected store's indeterminate commit outcome.

## Missing contract

The architecture lacks one consistent domain commit boundary in which repositories invoke and bind their exact validators and serializers to the candidate bytes before store commit. It also lacks closed latest/explicit-revision read results, identity-bound commit reconciliation, idempotency replay and collision rules, load-time byte/content/schema/revision checks, deserialization and domain validation, and lossless propagation of incompatible, corrupt, operational, and indeterminate outcomes.

## Exclusions and claim boundary

Physical SQLite layout, byte spelling, retention, and compaction are excluded. This record establishes no implementation, verification, scientific validation, uncertainty quantification, or human acceptance.
