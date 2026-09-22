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

## Testing requirements and enforcement

Testing requirements are distributed by responsibility rather than owned by one
control-plane file:

| Surface | Responsibility |
|---|---|
| `AGENTS.md`, **Testing and retained evidence** | Repository policy, evidence classes, proportional procedure, and claim boundaries |
| `python/pyproject.toml` | Test dependencies, pytest discovery, command options, and marker registration |
| `harness/pi/skills/develop-python-test-evidence/` | Generic authoring and semantic-review procedure; synchronized `.pi/skills/` copies are runtime projections |
| `harness/pi/evidence/python-test-evidence-profile-matrix-v1.json` | Normative versioned evidence-profile combinations and required or optional documentation fields |
| `harness/local/profiles/ksdft2effmass-v2.json` and local evidence extensions | Project scopes, markers, evidence namespaces, compatibility inputs, and explicit exceptions |
| Public software contracts, specifications, and applicable research records | Behavior, mathematical or scientific oracle, units, and acceptance meaning for the subject under test |
| `ksdft2effmass.harness.pi.conformance.python.PythonConformanceValidator` | Deterministic structural enforcement over explicit maintained-test source bytes and ownership/profile inputs |
| Explicit affected-test and broader-suite pytest invocations | Executed software or numerical evidence; a passing invocation proves only its stated assertions |

The generated Python module inventory and SQLite projection are comparison views, not
sources of testing requirements. Numeric totals for tests, collected nodes, modules,
or exported names are observations, not stable completeness contracts.

For package export surfaces, tests may compare `__all__` with an exact expected name
inventory or assert required and prohibited names directly. They must not assert an
export count through `len(__all__)` or through the length of an inventory already
linked to `__all__`. Such counts add no semantic coverage beyond the name contract and become
stale whenever an unrelated supported export changes. `PythonConformanceValidator`
reports `TE.NUMERIC_EXPORT_COUNT` when maintained test source contains this pattern.

## Python implementation

The generic package owns immutable identities, records, results, strict JSON actions,
profiles, resources, ownership, checkpoints, chains, checksums, conformance,
human-review values, and bounded Task-state inspection. Python test-source conformance
lives under `ksdft2effmass.harness.pi.conformance.python`; its parser, immutable model,
and rule owners are siblings in that package. `ksdft2effmass.harness.pi.conformance`
is the public domain package. The former Python `ksdft2effmass.harness.pi.evidence`
facade is retired; repository evidence paths retain their separate artifact meaning.
The project-local package owns explicit-root context composition, repository adapters, the version-3
`HarnessTask` model, direct domain validation composition, and the SQLite control
projection compatibility boundary. One private canonical Python-conformance input
resolver selects the configured test modules, profile, and migration map. Validation
and repository-conformance commands consume it directly; projection input construction
composes it rather than owning or rediscovering those sources.

Public records use exact semantic types and closed versions. Serialization belongs to
named actions rather than records. Expected invalid external input is represented as
structured findings when the public action contract requires it.

## Validation meaning

Generic validators inspect caller-supplied resources, ownership, checkpoints, chains,
checksums, skills, and Python evidence structure. Project-local `HarnessValidator`
composes six ordered checks: `python_conformance`, `resources`, `task_graph`,
`checkpoints`, `skills`, and `control_state`. The former `python_evidence` check value
is retired rather than retained as an alias.

The private projection synchronizer is the sole publisher of maintained SQLite,
deterministic SQL, the projection manifest, the Task graph, resource-manifest
projections, and the Python evidence module inventory. The private check action
reconstructs the same candidate without publication and compares integrity, schema,
normalized content, SQL, manifest, and owned projections. Generated projections do
not target `docs/`.

A validation `PASS` establishes only the stated structural or software contract. It
does not establish Task authority, scientific correctness, numerical verification,
scientific validation, uncertainty quantification, release readiness, or human
acceptance.

## Maintained commands

`ksdft2effmass.harness.cli` is the sole maintained Harness command namespace. The
former repository-script and `harness.pi.local._commands` layers are retired. Its
lazy dispatcher selects one thin adapter; command adapters may parse explicit inputs,
construct requests, invoke exact ActionObject owners, render results, and map exit
status, but they do not own domain policy or mutation.

- `python3 -m ksdft2effmass.harness.cli validate-local-harness-resources` validates explicitly selected
  roots, manifests, and profile composition.
- `python3 -m ksdft2effmass.harness.cli validate-harness` renders aggregate repository validation.
- `python3 -m ksdft2effmass.harness.cli harness-projection` synchronizes or checks maintained control
  projections; the former `harness_control.py` compatibility entry point is retired.

These commands do not gain authority from process exit status and do not execute
scientific calculations.
