# PI Harness Migration and Shadow Replay

## Migration principle

Extraction must preserve behavior before it retires the existing implementation. File movement alone is not evidence of behavioral equivalence.

The migration therefore uses a shadow period in which the legacy and extracted implementations process the same retained inputs.

## Migration stages

### Inventory

Identify every source rule, caller, artifact, and output. Record the intended generic owner and any project-local remainder.

### Extract

Move or reimplement the generic behavior behind the accepted harness contract. Parameterize project-specific values through the local profile.

### Shadow

Run legacy and extracted implementations against identical declared inputs
without changing authoritative project state. The reproducible parity gate runs
from a clean revision. An optional project-local pre-commit replay may inspect
an explicitly supplied worktree as a separate check; it must not be substituted
for the clean-revision result.

### Compare

Compare structured results rather than console prose alone.

### Cut over

Switch authoritative routing only after parity or explicitly approved differences are demonstrated.

### Retire

Remove the duplicate implementation only after human authorization and verified rollback capability.

## Comparison surface

Shadow replay should compare:

- validation status;
- stable issue codes;
- issue paths and related identities;
- ordering;
- task state;
- checkpoint resolution;
- chain assertions;
- evidence-ID inventories;
- checksum inventories;
- exit status;
- generated structured reports.

Differences in timestamps, temporary paths, or deliberately revised presentation must be normalized only through an approved comparison rule.

## Migration traceability

Renaming files or tests changes paths and pytest node IDs. Preserve a machine-readable mapping:

```text
old path/node ID
→ new path/node ID
→ unchanged evidence ID
```

Do not describe a renamed test as new evidence when its assertions and requirement are unchanged.

## Cutover checkpoint

The cutover checkpoint must report:

- components moved;
- generic and local destinations;
- parity results;
- intentional differences;
- duplicate files proposed for retirement;
- new authoritative paths;
- rollback procedure;
- residual limitations.

Recommended decisions are:

- accept cutover and retire verified duplicates;
- retain temporary shadow mode;
- require bounded corrections;
- reject migration;
- defer.

## Historical evidence

Closed evidence remains evidence of the historical tree and tool versions. Current-tree replay may report expectation drift when later authorized files are present.

Do not rewrite historical evidence to make it appear current. Preserve the
original record and separately document replay conditions or current-tree
differences. Personal and concurrently edited working notes remain outside
harness authority; historical nonmutation observations about them are not
required replay inputs or reusable validator inputs.

## Rollback

Rollback should restore routing to the prior implementation without deleting new evidence. It must identify the exact configuration or version change required and preserve the failed migration attempt for review.

## Navigation

- [Previous: Project-local extension model](./ksdft2effmass.harness.06.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Package-extraction readiness](./ksdft2effmass.harness.08.md)
