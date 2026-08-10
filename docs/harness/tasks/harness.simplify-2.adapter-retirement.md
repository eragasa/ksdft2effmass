<!-- Generated from SQLite control state; do not edit. -->
# Audit and decompose project-local adapters

[Task index](index.md) · [Previous](./harness.simplify-2.md) · [Next](./harness.simplify-2.cli-consolidation.md)

## Status

`completed`: completed post-review reconciliation: 9 adapters audited, 9 relocated, 0 removed, 9 public imports preserved, and 9 execute signatures preserved; no successor activated

## Objective

Audit and decompose project-local adapters by assigning each adapter behavior to its contract owner while preserving the supported nine-name public surface and compatibility facade.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.control-decomposition`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Audit the nine public ActionObjects formerly implemented together in `python/src/ksdft2effmass/harness/pi/local/adapters.py`: `TaskRecordAdapter`, `ChainRecordAdapter`, `CheckpointRecordAdapter`, `AgentRecordAdapter`, `OwnershipManifestAdapter`, `ChecksumCatalogAdapter`, `SkillInventoryAdapter`, `EvidenceOwnershipManifestAdapter`, and `EvidenceModuleSelector`.
- For each adapter, distinguish its maintained internal production caller, maintained command or script caller, supported public import, current input format, retained historical input, actual compatibility obligation, and final R2.2 disposition.
- Record the completed accounting exactly: 9 adapters audited, 9 adapters relocated, 0 adapters removed, 9 public imports preserved, and 9 `execute` signatures preserved.
- Treat repository inspection as evidence of maintained internal use or non-use. A currently exported public API remains a compatibility obligation; removal requires a separately authorized compatibility or deprecation decision. Repository non-use alone neither authorizes nor permanently prohibits removal.
- Treat retained historical bytes as evidence of prior formats and behavior, not by their mere existence as proof that a live public adapter remains necessary.
- Assign the nine implementations to five contract-specific modules for Task, control-record, ownership, resource, and evidence behavior, while retaining `local/adapters.py` as the compatibility facade and introducing no generic adapter framework.
- Keep R2.1 `dbcontrol` ownership separate and preserve historical traceability without changing adapter behavior, public imports, execute signatures, defining modules, dependencies, or lockfiles.

## Completion criteria

- The nine-row matrix distinguishes maintained internal production callers, maintained command or script callers, supported public imports, current input formats, retained historical inputs, actual compatibility obligations, and final dispositions for all nine adapters.
- Disposition totals are exact: 9 audited, 9 relocated, 0 removed, 9 public imports preserved, and 9 `execute` signatures preserved.
- R2.2 decomposed the adapter monolith into five contract-specific modules and retained a compatibility facade. It did not reduce the nine-name public adapter surface.
- Repository non-use is recorded without claiming proof about third-party consumers or treating retained bytes alone as a live compatibility requirement.
- No adapter behavior is hidden in `dbcontrol`, no generic adapter framework is created, and no reverse dependency from generic harness behavior to project-local state is introduced.
- The completed work package remains completed without activating its successor.

## Exclusions

- Do not remove or deprecate a public adapter in this correction; such a change requires a separately authorized compatibility or deprecation decision.
- Do not treat repository non-use as either deletion authority or a permanent prohibition on later authorized removal.
- Do not treat the mere existence of archived bytes as proof that a live public adapter remains necessary.
- Do not modify adapter behavior, tests, imports, signatures, defining modules, dependencies, lockfiles, or the duplicated private helper functions.
- Do not reopen R2.1, reactivate R2.2, modify or activate R2.3 through R2.7, create a checkpoint, or perform protected or release actions.

## Historical source

No archived source.
