---
document_id: ksdft2effmass.harness.001.002.000
task_id: harness-current.resources
parent: ksdft2effmass.harness.001.000.000
status: current
sphinx: included
---

# Resources, profiles, and skills

The resource layer makes agent procedures and validation inputs explicit,
versioned, and content-addressed.

## Resource manifests

`harness/pi/resource-manifest.json` inventories generic resources by stable
resource identity, resource kind, format version, relative path, SHA-256 byte
identity, and dependency identities. `harness/local/resource-manifest.json`
extends the generic manifest and may add local resources; it may not replace a
generic identity or path.

Manifest versions, resource format versions, schema versions, skill behavior
versions, and Python public-contract versions are independent boundaries.

## Project profile

The project profile under `harness/local/profiles/` supplies local policy as
data. It binds generic and local manifests and describes supported resource
formats, skill behaviors, evidence scopes and namespaces, pytest markers,
lifecycle vocabularies, local extensions, and compatibility data. It contains no
credentials, clients, executable callbacks, or machine-specific roots.

## Skills and references

Canonical reusable skills live under `harness/pi/skills/`. A concise `SKILL.md`
routes the procedure; its directly referenced convention files own detailed
rules. Current maintained capabilities include architecture-decision support,
Python test-evidence development, and Python research-software documentation.
Live project skill copies are synchronized from their canonical resources rather
than maintained as divergent implementations.

Project-local extensions configure the generic behavior. They do not copy full
generic skills or redefine generic ownership kinds.

## Schemas and fixtures

Generic schemas use Draft 2020-12 and describe strict public wire records and
resource contracts. Controlled valid and invalid fixtures provide independent
structural oracles. Passing a fixture or schema check establishes its declared
software contract only; fixtures are not scientific results.

## Current resource validation

`python/src/cli/validate_local_harness_resources.py` accepts explicit
repository, generic-resource, local-resource, profile, and manifest paths. It
uses maintained context-loading and resource-resolution Actions, emits a
structured deterministic result, propagates nested failures, and distinguishes
invalid input from an unexpected command-boundary failure. It performs no route
selection, historical replay, Git mutation, or current-directory discovery.

## Navigation

- **Index:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Parent:** [Current harness architecture](ksdft2effmass.harness.001.000.000.md)
- **Previous:** [Generic and project-local boundaries](ksdft2effmass.harness.001.001.000.md)
- **Next:** [Python implementation](ksdft2effmass.harness.001.003.000.md)
