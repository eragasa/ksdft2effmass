---
document_id: ksdft2effmass.harness.001.003.000
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
| `checkpoints.py` | Checkpoint records, pure explicit decision transformation, and structural checkpoint-set validation. |
| `chains.py` | Task/chain records and deterministic chain-state evaluation. |
| `checksums.py` | Checksum records and explicit-root byte validation. |
| `evidence.py` | Evidence-identifier occurrence records and caller-supplied source auditing. |
| `human_review.py` | Immutable explicit-input review targets, observations, candidate findings, packet results, and deterministic packet preparation. |

The package boundary exports public names from
`ksdft2effmass.harness.pi`; callers do not depend on private module imports.
Records are immutable, actions are fieldless, and expected invalid external
input is represented as structured findings when the public action contract
specifies that behavior.

## Human-review packet boundary

The package exports `HumanReviewTarget`, `HumanReviewObservation`,
`HumanReviewFinding`, `HumanReviewPacket`, `HumanReviewDecision`,
`HumanReviewPreparer`, and `HumanReviewDecisionRecorder`. The records own intrinsic
lexical and immutable-state invariants. `HumanReviewPreparer` owns target membership,
identifier relationships, canonical ordering, and packet-status derivation. A failed
observation produces `blocked_by_failed_observation`; other intrinsically valid
observation statuses produce `ready_for_human_review`. Neither status is a human
disposition or acceptance.

`HumanReviewDecisionRecorder` requires canonical prepared packet state and stores the
exact immutable packet with explicit response, disposition, and scope values. The
module consumes only explicit records and text. It performs no repository or
filesystem discovery, Git execution, clock access, network or subprocess activity,
database persistence, natural-language interpretation, correction, or successor
activation. Its records are not members of the wire-record union, and it defines no
serialization contract.

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

`CheckpointRecord` remains the generic serialized checkpoint decision view.
`CheckpointDecisionResolutionRequest` and
`CheckpointDecisionResolutionResult` are runtime DataObjects and are not members
of `HarnessWireRecord`; no cross-process wire requirement exists for them.
Project-local checkpoint JSON also contains fields outside the generic view, so
no generic CLI rewrites local checkpoint files. A future authorized local adapter
must patch those records without discarding local fields.

## Checkpoint decision boundary

| Responsibility | Owner |
|---|---|
| Human-intent interpretation, ambiguity detection, and verbatim response selection | `resolve-human-checkpoint` |
| Pure immutable transformation of one generic checkpoint decision view | `CheckpointDecisionResolver` |
| Project-local JSON patching, validation, persistence, Git operations, and task resumption | Separately authorized root/local workflow |

`CheckpointDecisionResolver` receives all decision-bearing values explicitly. It
uses no repository, filesystem, clock, serializer, task/chain mutation, Git, or
successor behavior. A successful repeat with identical values is an unchanged
idempotent result; conflicts are deterministic checkpoint findings. Neither the
ActionObject nor its tests establish human acceptance or task resumption.

## Deliberate exclusions

The implementation provides no SQLite repository, command runner, Git mutation,
scheduler, plugin registry, scientific workflow engine, network fetch, or
implicit package-resource discovery. These exclusions are current facts, not
missing scientific capabilities.

## Navigation

- **Index:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Parent:** [Current harness architecture](ksdft2effmass.harness.001.000.000.md)
- **Previous:** [Resources, profiles, and skills](ksdft2effmass.harness.001.002.000.md)
- **Next:** [Validation and evidence](ksdft2effmass.harness.001.004.000.md)
