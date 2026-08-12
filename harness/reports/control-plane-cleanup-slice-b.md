# Control-plane cleanup Slice B

## Status

Slice B is complete from base revision `684e9f61cfc3a2c727d50f30c7469e58ff7b1483`. It removed only history-role
surfaces authorized by the committed Slice A inventory. Slice C remains pending
and has not begun.

## Disposition

The machine-readable [deletion manifest](control-plane-cleanup-slice-b-deletions.json)
records every candidate and precondition result.

- Candidates considered: 635
- Deleted: 388
- Retained: 247
- Unresolved in the Slice B manifest: 0

Results by ownership family:

| Family | Deleted | Retained |
|---|---:|---:|
| Archive | 2 | 75 |
| Chain | 2 | 5 |
| Checkpoint | 0 | 49 |
| Evidence | 384 | 98 |
| Ownership | 0 | 20 |

All resolved checkpoints were retained because Slice A recorded inbound edges
from retained reachable control state. Most archived Task/intake records were
also retained for the same reason. Ownership validator fixtures were retained
under the explicit Slice B test/fixture exclusion after family-level dynamic
resolution exposed a Slice A edge omission. Six evidence files were reclassified
as retained because current chains or maintained harness documentation still
reference them.

Git history is the sole retention layer for deleted records. No replacement
archive, tombstone, alias, or historical catalog was created.

## Remaining tracked control families

Counts before deterministic projection regeneration:

- Live Task records: 112
- Chain records: 7
- Checkpoint records/schema: 51
- Evidence files: 100
- Archive files: 77
- Generated Task pages: 112

## Boundaries

No Task record or generated Task page was deleted. No agent, skill, runtime
Python module, CLI, schema, fixture, test, current resource, scientific artifact,
dependency, or lockfile was deleted or modified. The immutable Slice A
reachability report remains retained as evidence.
