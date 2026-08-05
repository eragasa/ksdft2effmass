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

The concrete live consumer is `.pi/skills/validate_harness.py`, and
`harness/local/validation-route.json` is the single owner of the route it uses.
At the pending H4 boundary that file selects `ValidationRoute.LEGACY`, so the
retained legacy validators remain authoritative. H4 may propose local authority,
but does not activate it. After all selected pairs are eligible, deterministic
validation and independent review pass, and the human accepts the final
checkpoint, closeout may change exactly that route selection to
`ValidationRoute.LOCAL`. No other file or ambient default changes route.

### Retire

The two old skill directories are replaced by the canonical renamed live roots,
not maintained as aliases. Other retained legacy validator commands and the
accepted H1-H3 checksum catalogs remain available through the cutover decision
and rollback period. Further duplicate retirement requires the final human H4
cutover decision and verified rollback; it is not implied by parity.

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

Differences in timestamps, temporary paths, or deliberately revised presentation must be normalized only through an approved comparison rule. Each pair is classified exactly once as `equivalent`, `intentional`, `deferred`, or `defect`. `Equivalent` has no structured differences. `Intentional` requires a cited accepted rule and may be eligible. `Deferred` and `defect` are never authoritative-cutover eligible. Aggregate local authority is permitted only when every pair is eligible.

## Migration traceability

H4's `.pi/evidence/pi-harness-incubation/H4/old-new-traceability.json` preserves
the two name mappings: `choose-next-task` to `recommend-next-task`, and
`document-research-python` to `document-python-research-software`. The rename
changes identity only, not capability. Old names may remain in historical tasks,
checkpoints, meetings, papers, retained evidence, and explicit migration prose;
they must not remain in live agent frontmatter, instructions, manifests,
descriptors, profiles, inventories, or canonical live paths.

The retained `.pi/evidence/class-owned-evidence-convention/validate.py` is a
historical replay program whose old skill path must not be rewritten. It can be
replayed only with the worktree at the pre-H4 revision where that retained path
exists; failure against the post-rename worktree does not authorize a live alias
or mutation of historical evidence.

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

`RollBackValidationRoute.execute` is a pure action that converts an explicit
local configuration back to legacy/legacy routing. It does not write
`harness/local/validation-route.json` and does not restore, delete, or otherwise
mutate filesystem resources. Operational rollback changes that single route-
owner file to `ValidationRoute.LEGACY` and reruns the identical validation
commands. If prior live resource bytes are also required, the two old skills and
the version-1 profile are restored separately with a Git revert or checkout at
the recorded H4 starting revision; the H1-H3 checksum catalogs remain the
integrity oracle for their accepted snapshots. Neither operation rewrites
history or makes the provisional local route authoritative. Any failed,
deferred, checksum-mismatched, ownership-invalid, or missing-explicit-root
replay keeps legacy authority.

## Navigation

- [Previous: Project-local extension model](./ksdft2effmass.harness.06.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Package-extraction readiness](./ksdft2effmass.harness.08.md)
