# Resources and validation in v1

## Generic and project-local boundary

Reusable contracts live under `python/src/ksdft2effmass/harness/pi/` and
`harness/pi/`. Repository-specific composition lives under
`python/src/ksdft2effmass/harness/pi/local/` and `harness/local/`. The permitted
dependency direction is project-local to generic; generic code and resources do not
import local policy, project Task identities, or scientific conventions.

Callers supply roots, records, bytes, manifests, profiles, and observations
explicitly. Neither layer discovers the repository through the current directory,
Git, environment variables, parent traversal, or package fallback.

## Resources and profiles

`harness/pi/resource-manifest.json` inventories generic schemas, fixtures, skills,
references, and profiles by stable identity, relative path, format version, SHA-256
content identity, and dependency identities. `harness/local/resource-manifest.json`
extends that inventory without replacing a generic identity or path.

The project profile under `harness/local/profiles/` binds the selected generic and
local manifests and records supported resource formats, skill behavior versions,
evidence scopes, markers, and local extensions. Manifest versions, resource format
versions, schema versions, skill behavior versions, and Python public-contract
versions remain separate boundaries.

Reusable skills live under `harness/pi/skills/`; concise skill entry points refer to
the detailed conventions they require. Project-local extensions configure generic
behavior rather than copying or weakening it.

## Python implementation

The generic package owns immutable identities, records, results, strict JSON actions,
profiles, resources, ownership, checkpoints, chains, checksums, evidence conformance,
human-review values, and bounded Task-state inspection. The project-local package
owns explicit-root context composition, repository adapters, the version-3
`HarnessTask` model, direct domain validation composition, and the SQLite control
projection compatibility boundary.

Public records use exact semantic types and closed versions. Serialization belongs to
named actions rather than records. Expected invalid external input is represented as
structured findings when the public action contract requires it.

## Validation meaning

Generic validators inspect caller-supplied resources, ownership, checkpoints, chains,
checksums, skills, and Python evidence structure. Project-local `HarnessValidator`
composes six ordered checks: `python_evidence`, `resources`, `task_graph`,
`checkpoints`, `skills`, and `control_state`.

`HarnessControlMigrator` is the sole publisher of maintained SQLite, deterministic
SQL, the projection manifest, the Task graph, resource-manifest projections, and the
Python evidence module inventory. `HarnessControlVerifier` reconstructs the same
candidate without publication and compares integrity, schema, normalized content,
SQL, manifest, and owned projections. Generated projections do not target `docs/`.

A validation `PASS` establishes only the stated structural or software contract. It
does not establish Task authority, scientific correctness, numerical verification,
scientific validation, uncertainty quantification, release readiness, or human
acceptance.

## Maintained commands

- `python/src/cli/validate_local_harness_resources.py` validates explicitly selected
  roots, manifests, and profile composition.
- `python/src/cli/validate_harness.py` renders aggregate repository validation.
- `python/src/cli/harness_projection.py` synchronizes or checks maintained control
  projections; `harness_control.py` remains temporary migration compatibility.

These commands do not gain authority from process exit status and do not execute
scientific calculations.
