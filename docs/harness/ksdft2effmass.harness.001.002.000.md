---
document_id: ksdft2effmass.harness.001.020.000
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

## Validation route

`harness/local/validation-route.json` selects the maintained local route and
retains a legacy rollback value. The current replay entry point invokes declared
validators and fails if a required observation is missing, malformed, nonzero,
or does not report the required pass condition.

See [generic and local boundaries](./ksdft2effmass.harness.001.010.000.md) and
[validation and evidence](./ksdft2effmass.harness.001.040.000.md).
