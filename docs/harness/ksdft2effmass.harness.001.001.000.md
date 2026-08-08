---
document_id: ksdft2effmass.harness.001.001.000
task_id: harness-current.boundaries
parent: ksdft2effmass.harness.001.000.000
status: current
sphinx: included
---

# Generic and project-local boundaries

The harness separates reusable mechanics from repository policy. This boundary
prevents generic validation from silently acquiring CPN, electronic-structure,
evidence-namespace, task-lifecycle, or workstation assumptions.

## Generic layer

Generic Python under `ksdft2effmass.harness.pi` owns:

- strict identities and lexical path types;
- immutable wire records and structured results;
- canonical JSON serialization and deserialization;
- explicit profile and resource processing;
- stateless validation of resources, ownership, checkpoints, chains, checksums,
  skills, and evidence identifiers.

Generic textual resources under `harness/pi/` own reusable schemas, fixtures,
skills, references, and validators. They contain no project task IDs, scientific
settings, local evidence prefixes, or implicit repository paths.

## Project-local layer

Project-local Python under `ksdft2effmass.harness.pi.local` owns:

- conversion of selected repository records into generic records;
- explicit repository/generic/local root composition;
- local validation orchestration without severity downgrade;
- route and rollback values;
- shadow-observation comparison.

Project-local textual resources under `harness/local/` own profile instances,
project namespace rules, local extensions, validation-route configuration, and
repository-specific fixture inputs.

## Runtime records

`.pi/` contains instantiated operational records. It is not package data and is
not imported by the generic library. Current human instructions and durable
control records govern work; evidence and historical reports do not activate it.

## Dependency rules

```text
.pi project records ─────────────┐
                                 ↓
harness/local ─→ harness/pi contracts
       │                 │
       ↓                 ↓
project-local Python ─→ generic Python
```

Prohibited directions include generic-to-local imports, generic-to-domain
imports, generic resource dependence on local identities, and implicit current
working directory or `.pi` discovery.

## Explicit composition

Callers provide roots, manifest/profile bytes, content identities, records, and
observations. There is no ambient global fallback. Local extensions may narrow a
project policy but may not weaken generic integrity or safety invariants.

## Navigation

- **Index:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Parent:** [Current harness architecture](ksdft2effmass.harness.001.000.000.md)
- **Previous:** [Current harness architecture](ksdft2effmass.harness.001.000.000.md)
- **Next:** [Resources, profiles, and skills](ksdft2effmass.harness.001.002.000.md)
