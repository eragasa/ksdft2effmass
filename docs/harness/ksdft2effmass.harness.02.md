# PI Harness Contract and Versioning

## Contract objective

The harness contract defines the smallest stable interface required to validate and coordinate project control-plane records without importing project-domain semantics.

The contract must be approved before generic functionality is extracted. Existing scripts are evidence of requirements, not automatically the desired public API.

## Accepted minimum H1 surface

H0 accepted the following as planning authority for H1:

- `ArtifactIdentity`, `ResourceReference`, `ResourceManifest`,
  `ProjectProfile`, and `SkillDescriptor` records;
- `ValidationIssue` and `ValidationResult` structured results;
- narrow ownership, checkpoint, task/chain-view, checksum, command-result, and
  decision-boundary records; and
- stateless loaders, resolvers, and validators using explicit roots and
  profiles.

Exact public names, serialized fields, and compatibility policy remain H1
decisions. No interface should be introduced solely because it might be useful
later. Orchestration, dispatch, subprocess/Git/package operations, scientific
CPNs, domain adapters, package publication, Graphify, universal filename rules,
and a duplicate evidence grammar are outside the accepted minimum.

## State and action separation

Durable records should be immutable data objects. Validation, loading, and transformation should be stateless action objects.

For a generic validation action $V$ acting on a record $x$ and an explicit project profile $p$,

$$
V(x,p) \longrightarrow R,
$$

where $R$ is a structured result containing stable issues and no hidden mutation of $x$ or $p$.

The action must not acquire project state from the current directory,
environment-specific global state, or an implicit `.pi` search. Generic
validation must be reproducible from a clean revision plus declared inputs.
Optional project-local pre-commit checks may inspect an explicitly supplied
worktree, but their results must remain distinct from clean-revision validation
and must not turn personal working notes into harness inputs.

## Configuration contract

A data-only project profile may supply:

- repository-relative roots;
- evidence-ID prefixes;
- pytest markers;
- schema locations;
- skill locations;
- validation policies;
- permitted local extensions.

It must not supply credentials, open file handles, mutable clients, subprocess handles, or executable closures.

Profile parsing must reject unknown or malformed versioned fields according to the approved compatibility policy.

## Resource identity

Every reusable resource requires enough identity to distinguish incompatible revisions. The approved contract should define:

- resource identifier;
- resource kind;
- schema or format version;
- content identity or checksum where required;
- declared dependencies;
- compatibility requirements.

Filesystem location is not durable identity.

## Version layers

The harness should distinguish:

| Version | Meaning |
| --- | --- |
| Harness implementation version | Release identity of the future package |
| Public contract version | Compatibility of Python-facing records and actions |
| Profile schema version | Shape and meaning of project configuration |
| Resource-manifest version | Shape of the resource inventory |
| Skill version | Behavioral identity of an operational skill |

A change in one layer does not automatically require a change in every layer.

## Failure contract

Expected invalidity must produce structured diagnostics rather than untyped process failure. Diagnostics should include a stable code, path or subject, related identities where applicable, and a human-readable message.

Unexpected programming defects may still raise exceptions. The contract must distinguish malformed input from internal failure.

## Human checkpoint

H1 closes only after human acceptance of:

- the public internal API;
- version boundaries;
- resource-loading rules;
- structured errors;
- profile semantics;
- the extraction boundary.

## Navigation

- [Previous: Architecture and ownership](./ksdft2effmass.harness.01.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Python implementation boundary](./ksdft2effmass.harness.03.md)
