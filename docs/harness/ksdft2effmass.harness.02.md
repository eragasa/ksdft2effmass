# PI Harness Contract and Versioning

## Contract objective

The harness contract defines the smallest stable interface required to validate and coordinate project control-plane records without importing project-domain semantics.

The contract must be approved before generic functionality is extracted. Existing scripts are evidence of requirements, not automatically the desired public API.

## Candidate contract surfaces

H0 determines which surfaces are justified. Candidates include:

- project-profile records;
- resource references and resource manifests;
- task and chain records;
- human-checkpoint records;
- evidence and checksum records;
- validation issues and results;
- structured failures;
- deterministic validation actions;
- resource-loading actions.

No interface should be introduced solely because it might be useful later.

## State and action separation

Durable records should be immutable data objects. Validation, loading, and transformation should be stateless action objects.

For a generic validation action $V$ acting on a record $x$ and an explicit project profile $p$,

$$
V(x,p) \longrightarrow R,
$$

where $R$ is a structured result containing stable issues and no hidden mutation of $x$ or $p$.

The action must not acquire project state from the current directory, environment-specific global state, or an implicit `.pi` search.

## Configuration contract

A project profile may supply:

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
