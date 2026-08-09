---
document_id: ksdft2effmass.harness.001.004.000
task_id: harness-current.evidence
parent: ksdft2effmass.harness.001.000.000
status: current
sphinx: included
---

# Validation and evidence

The current harness combines small generic validation actions with project-local
composition and maintained validation scripts. Each result has a bounded claim;
a successful process exit alone does not make a nested observation pass.

## Generic validators

The generic package validates supplied resource manifests, ownership records,
checkpoint sets, chains, checksums, skill descriptors, and evidence identifiers.
Issues use stable codes and deterministic ordering. A failed prerequisite stage
returns no partially trusted primary result.

`IdentifierAuditor` currently parses caller-supplied Python module bytes
and applies explicit profile marker, scope, namespace, range, and protected-gap
rules. It is an evidence-identifier audit, not a general evidence repository or
semantic test reviewer.

## Local composition

`LocalRepositoryValidator` invokes applicable generic validators over an explicit
local context and explicitly adapted records. It preserves generic severity and
returns ordered named results. Local replay scripts run selected maintained
validators and require both successful execution and the expected structured
pass observation.

## Focused validation and full reconciliation

Current checks are distributed, but their purposes remain distinct:

- **Focused validation** checks the files, records, fixtures, or public behavior
  affected by one bounded change. It should be fast and should identify the
  failing contract directly.
- **Full reconciliation** confirms that cross-record identities, manifests,
  ownership, route selection, capability inventories, documentation, and
  completion state agree before a durable boundary is accepted.

A focused pass cannot replace full reconciliation when the task changes a shared
identity or relation. Full reconciliation should not be used as a substitute for
a precise local oracle.

## Evidence classes

| Class | Meaning |
|---|---|
| Software verification | The implementation satisfies a documented software contract. |
| Numerical verification | A numerical implementation agrees with independently derived mathematics. |
| Scientific validation | A declared model and use agree with independent scientific reference evidence. |
| Uncertainty quantification | Declared uncertainty sources are propagated by an authorized method. |

Harness mechanics normally produce software verification. Successful harness
validation does not establish scientific validation or UQ.

## Test-evidence ownership

The generic primary kinds are `class_owned` and `artifact_owned`. Technical
agreements, mappings, schemas, fixtures, package surfaces, and commands are
artifact-owned rather than a third generic boundary kind. Maintained tests use
the current module headings, semantic test names, stable evidence identifiers,
explicit parameter IDs, and independently reviewable oracles.

## Navigation

- **Index:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Parent:** [Current harness architecture](ksdft2effmass.harness.001.000.000.md)
- **Previous:** [Python implementation](ksdft2effmass.harness.001.003.000.md)
- **Next:** <a href="ksdft2effmass.harness.001.005.000.md">Agent and ownership inventory</a>
