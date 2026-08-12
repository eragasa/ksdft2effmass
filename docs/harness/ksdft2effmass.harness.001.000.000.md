---
document_id: ksdft2effmass.harness.001.000.000
task_id: harness-current
parent: ksdft2effmass.harness.000.000.000
status: current
sphinx: included
---

# Current harness architecture

The current harness is an explicit-input control-plane library plus project-local
composition. It provides immutable records and results, stateless actions,
versioned textual resources, deterministic validators, project profiles, local
adapters, route selection, and shadow-comparison records. It does not discover
repository state implicitly and is not a workflow engine or scientific backend.

## Implemented surfaces

| Surface | Current owner | Responsibility |
|---|---|---|
| Generic Python | `python/src/ksdft2effmass/harness/pi/` | Records, serialization, profiles, resources, ownership, checkpoints, chains, checksums, evidence-ID auditing, and structured validation. |
| Project-local Python | `python/src/ksdft2effmass/harness/pi/local/` | Explicit-root context loading, adapters, repository validation composition, route selection, rollback values, and shadow comparison. |
| Generic resources | `harness/pi/` | Schemas, fixtures, skills, references, descriptors, manifests, and reusable validators. |
| Project-local resources | `harness/local/` | Repository profile, extensions, local fixtures, resource composition, validation route, and current replay entry point. |
| Instantiated control records | `.pi/` | Project tasks, chains, checkpoints, agents, skills, ownership, and retained evidence. |

The dependency direction is local to generic. Generic Python and resources do
not import project-local policy, domain code, task identities, or scientific
conventions.

## Public contract shape

The generic package exports concrete immutable DataObjects and ResultObjects,
closed wire-record types, validated semantic primitives, and fieldless
ActionObjects. Actions accept explicit records, bytes, profiles, or roots and
return deterministic structured results. Strict JSON serialization is owned by
named serializer and deserializer actions rather than by the records.

The local package adapts caller-supplied repository records to the generic
contract. It does not turn the generic harness into a service locator, command
runner, Git client, scheduler, or ambient `.pi` reader.

## Validation meaning

A harness `PASS` establishes only the structural contract checked by that
validator for the supplied inputs. It does not establish task authorization,
scientific correctness, scientific validation, uncertainty quantification,
release readiness, or human acceptance.

## Current documentation

| Document | Topic |
|---|---|
| [harness.001.001.000](./ksdft2effmass.harness.001.001.000.md) | Generic and project-local boundaries |
| [harness.001.002.000](./ksdft2effmass.harness.001.002.000.md) | Resources, profiles, and skills |
| [harness.001.003.000](./ksdft2effmass.harness.001.003.000.md) | Python implementation |
| [harness.001.004.000](./ksdft2effmass.harness.001.004.000.md) | Validation and evidence |
| [harness.001.006.000](ksdft2effmass.harness.001.006.000.md) | Status and limitations |

## Navigation

- **Index:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Parent:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Previous:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Next:** [Generic and project-local boundaries](ksdft2effmass.harness.001.001.000.md)
- **Children:** [001](ksdft2effmass.harness.001.001.000.md), [002](ksdft2effmass.harness.001.002.000.md), [003](ksdft2effmass.harness.001.003.000.md), [004](ksdft2effmass.harness.001.004.000.md), and [006](ksdft2effmass.harness.001.006.000.md)
