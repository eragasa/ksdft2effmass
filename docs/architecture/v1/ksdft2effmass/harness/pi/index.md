# `ksdft2effmass.harness.pi` package in v1

## Purpose

The V1 development harness selects and governs repository work. It combines canonical Task records, chain selection, human checkpoints, resources, capabilities, evidence, validation, and generated control views.

```mermaid
flowchart LR
    human["Human authority"] --> chain["Chain selection"]
    tasks["HarnessTask JSON"] --> state["Development control state"]
    chain --> state
    checkpoints["Checkpoints"] --> state
    resources["Resources and capabilities"] --> state
    evidence["Evidence"] --> state
    state --> validation["Repository validation"]
    state --> projections["Generated projections"]
```

## Implemented objects

| Object or action | Responsibility |
|---|---|
| `HarnessTask` | Immutable development work definition |
| Task serializer and deserializer | Version-3 Task JSON wire contract |
| `HarnessTaskGraphValidator` | Task relationship and graph validation |
| `TaskStateInspector` | Bounded inspection of selected Task state |
| Private projection synchronization and checking | Complete publication and read-only source-aware comparison behind `harness_projection.py` |
| `HarnessValidator` | Composition of repository-conformance checks |
| `HumanReviewTarget`, `HumanReviewObservation`, `HumanReviewFinding`, `HumanReviewPacket`, `HumanReviewDecision`, `HumanReviewPreparer`, `HumanReviewDecisionRecorder` | Explicit packet preparation and decision representation without persistence or activation |

Generic contracts are implemented under `ksdft2effmass.harness.pi`; project-local composition is implemented under `ksdft2effmass.harness.pi.local`.

## Lifecycle

A `HarnessTask` carries identity, status, parent and prerequisite relationships, explicit activation, objective, authority paths, scope, completion criteria, exclusions, intake, and optional archived-source identity. Status values are project records rather than one closed universal state machine.

Chains select active work. Task JSON defines Task content. Unresolved checkpoints represent human decision boundaries. Generated state must agree with those sources but cannot replace them.

## Package structure

```mermaid
flowchart TD
    pi["harness.pi"]
    local["harness.pi.local"]
    control["local.control"]
    dbcontrol["local.dbcontrol"]
    resources["harness.pi.resources"]
    conformance["harness.pi.conformance.python"]
    evidence["harness.pi.evidence facade"]
    wire["harness.pi.wire"]

    pi --> local
    local --> control
    local --> dbcontrol
    pi --> resources
    pi --> conformance
    pi --> evidence
    evidence --> conformance
    pi --> wire
```

## Detailed pages

- [Development harness model](development-harness.md)
- [Control-plane authority and selection](control-plane.md)
- [Resources and validation](resources-and-validation.md)
- [Human-review objects](human-review.md)
- [Project-local control compilation](local/control/index.md)
- [Project-local generated persistence](local/dbcontrol/index.md)
- [Project-local projections](local/dbcontrol/projections.md)
- [Pi harness subagents](subagents/index.md)
