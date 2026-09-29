# Simulation-first Task-program migration

The current human instruction selects a simulation-first computational bootstrap
and confirms project-local `HarnessTask` schema version 3 with required
`superseded_by_task_ids`. This record preserves the identity and
dependency migration; it does not activate a Task or authorize Quantum ESPRESSO,
Wannier90, external, scientific, or protected execution.

## Program boundary

The bootstrap reproduces bounded silicon tutorial calculations, inventories the
observed artifacts, defines extraction records from those observations, develops
direct-spectral and Wannier-mediated tight-binding paths, compares the resulting
models, and verifies the composed workflow. Production Stages 02--04 retain their
own scientific settings, convergence, validation, and execution gates.

The deferred CPN-persistence Task does not block the main bootstrap path.

## Identity mapping

| Existing Task | Canonical replacement Task or Tasks |
|---|---|
| `P3` | `cpn.workflow.persistence` |
| `P4` | `bulk-silicon.records.periodic.extraction` |
| `P5` | `bulk-silicon.simulation.qe.reference`; `bulk-silicon.artifacts.qe.inventory`; `bulk-silicon.records.periodic.extraction` |
| `P6` | `bulk-silicon.records.periodic.extraction` |
| `P7` | `bulk-silicon.tight-binding.direct-spectral.fitting` |
| `P8` | `bulk-silicon.tight-binding.wannier.bridge` |
| `P9` | `bulk-silicon.tight-binding.wannier.extraction` |
| `P10` | `bulk-silicon.workflow.extracted-model-verification` |
| `P11` | `bulk-silicon.simulation.qe.reference` |

`bulk-silicon.tight-binding.comparison-reduction` is a new explicit
responsibility without one direct predecessor.

## Version-3 supersession semantics

`superseded_by_task_ids` is a sorted, unique array of canonical replacement Task
identifiers. It records identity succession only. It does not:

- activate a replacement;
- satisfy a prerequisite;
- establish parentage;
- authorize execution;
- establish completion or acceptance; or
- rewrite archived source material.

The Task graph contains matching `superseded_by` edges. The ignored SQLite index
copies those edges for queries and reports; it remains derived and non-authoritative.

## State disposition

`P3`--`P11` are superseded records. Their archived Markdown remains byte-identical.
The eight main bootstrap Tasks are inactive or blocked, and
`cpn.workflow.persistence` is `deferred_inactive`. Every executable
Task requires separate explicit activation. Automatic successor activation remains
disabled, and neither tutorial nor production execution is authorized by this
migration.
