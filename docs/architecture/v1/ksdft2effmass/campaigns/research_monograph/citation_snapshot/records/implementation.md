# Records implementation

All public records are frozen, slotted dataclasses or closed `StrEnum` values. Wrong
semantic types raise `TypeError`; correctly typed values that violate invariants raise
`ValueError`. Booleans do not satisfy integer checks.

The Request alone retains the machine-local absolute root. Its `request_id` excludes
that root. The snapshot retains only root-relative POSIX paths and content identities.
Snapshot construction checks sequence types and delegates complete replay to
`ResearchMonographCitationSnapshotIntegrityValidator`. Result construction repeats
that replay and requires its supplied `result_id` to equal the canonical projection
identity. Consequently, neither a freely constructed snapshot nor a forged Result is
an accepted owner handoff.
