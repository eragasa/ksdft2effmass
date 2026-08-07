---
document_id: ksdft2effmass.harness.001.030.000
task_id: harness-current.python
parent: ksdft2effmass.harness.001.000.000
status: current
sphinx: included
---

# Python implementation

The Python harness is implemented under
`python/src/ksdft2effmass/harness/pi/`. Python is the current reference
implementation; intended Rust representations do not imply that a Rust harness
exists.

## Generic modules

| Module | Responsibility |
|---|---|
| `identity.py` | Identifiers, path meanings, versions, and internal error boundary. |
| `validation.py` | Validation records, wire kinds, canonical JSON actions, and result types. |
| `profiles.py` | Strict project-profile record and explicit profile loading. |
| `resources.py` | Resource records, resolution, manifest validation, and skill-resource validation. |
| `ownership.py` | Agent and ownership records plus non-overlap and binding validation. |
| `checkpoints.py` | Checkpoint records and structural checkpoint-set validation. |
| `chains.py` | Task/chain records and deterministic chain-state evaluation. |
| `checksums.py` | Checksum records and explicit-root byte validation. |
| `evidence.py` | Evidence-identifier occurrence records and caller-supplied source auditing. |

The package boundary exports public names from
`ksdft2effmass.harness.pi`; callers do not depend on private module imports.
Records are immutable, actions are fieldless, and expected invalid external
input is represented as structured findings when the public action contract
specifies that behavior.

## Project-local modules

`python/src/ksdft2effmass/harness/pi/local/` contains:

- models for roots, local contexts, routes, adaptations, observations, and local
  results;
- parsers and adapters for selected project records;
- explicit context composition;
- generic-validator composition;
- pure route selection and rollback actions;
- shadow-observation comparison.

The local package consumes generic interfaces but the generic package never
imports it.

## Wire and path contracts

Public JSON records are strict: required fields, closed versions, exact semantic
types, duplicate-key and unknown-field rejection, canonical output, and no
implicit conversion of Boolean or numeric strings. Resource, ownership-scope,
and diagnostic paths share strict lexical safety while retaining distinct
meanings.

## Deliberate exclusions

The implementation provides no SQLite repository, command runner, Git mutation,
scheduler, plugin registry, scientific workflow engine, network fetch, or
implicit package-resource discovery. These exclusions are current facts, not
missing scientific capabilities.

See [the architecture overview](./ksdft2effmass.harness.001.000.000.md) and
[current limitations](./ksdft2effmass.harness.001.060.000.md).
