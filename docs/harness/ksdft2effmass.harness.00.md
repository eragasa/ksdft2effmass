# PI Harness

## Purpose

The PI harness provides the reusable control-plane machinery used to plan, authorize, verify, review, and close bounded research-software tasks. It separates generic agent-operational behavior from the scientific and project-specific meaning owned by `ksdft2effmass`.

The harness does not perform a scientific calculation merely because it can represent a task, checkpoint, or evidence record. It coordinates work and verifies software-facing contracts; scientific execution and acceptance remain separately authorized project activities.

H0 was human-accepted through `H0-HC01` on 2026-08-04. Its 316-component
inventory, generic/local boundary, six finding resolutions, H3-before-H2
sequencing recommendation, and proposed minimum H1 contract are planning
authority for H1. H1 alone is active after resolved `H1-HC01` Option B and the
exactly one bounded `DiagnosticPath` contract correction; focused reviews and
validation pass, and final acceptance at pending `H1-HC02` remains. These pages do not
authorize implementation or any successor.

## Architectural split

The accepted incubation architecture plans four source locations and uses one
current runtime-state location. The four source roots remain prospective and
absent until an authorized implementation task creates them:

| Location | Ownership |
| --- | --- |
| `python/src/ksdft2effmass/harness/pi/` | Generic Python harness functionality intended for later extraction |
| `python/src/ksdft2effmass/harness/pi/local/` | Project-specific Python configuration and extensions |
| `harness/pi/` | Generic skills, references, templates, schemas, and manifests |
| `harness/local/` | Project-specific profiles, skills, and textual extensions |
| `.pi/` | Instantiated tasks, checkpoints, chains, evidence, and current state |

The required dependency direction is

```text
project-local policy
        ↓
generic harness
```

The generic harness must not import or discover the project-local layer implicitly.

## Documentation map

- [Architecture and ownership](./ksdft2effmass.harness.01.md)
- [Contract and versioning](./ksdft2effmass.harness.02.md)
- [Python implementation boundary](./ksdft2effmass.harness.03.md)
- [Skills and textual resources](./ksdft2effmass.harness.04.md)
- [Evidence and test conventions](./ksdft2effmass.harness.05.md)
- [Project-local extension model](./ksdft2effmass.harness.06.md)
- [Migration and shadow replay](./ksdft2effmass.harness.07.md)
- [Package-extraction readiness](./ksdft2effmass.harness.08.md)

## Project sequence

The accepted dependency and authorization structure is

```text
P1 and H0 accepted
        ↓
H1 contract
        ↓
H3 skills and textual resources
        ↓
H2 generic Python core
        ↓
H4 local integration, shadow replay, and cutover
        ├── separately authorized P2
        └── separately authorized optional H5 extraction readiness
```

H4 establishes accepted project-local harness integration and cutover behavior;
it does not extract or publish a standalone package. After accepted H4, P2 still
requires accepted P1 and its own explicit human activation. Optional H5 also
requires its own explicit activation. Neither activates automatically, and H5
is not a P2 prerequisite.

## Sources of truth

These pages explain durable architecture and usage. They do not own mutable
execution state. The records under `.pi/tasks/`, `.pi/checkpoints/`, and
`.pi/chains/` are the sole authority for current task scope/status, human
decisions, dependencies, and activation. If prose here conflicts with those
records, the `.pi` records control.

- `.pi/evidence/` owns retained execution and review evidence, not live
  authorization.
- `docs/harness/` owns maintained human-readable architectural explanation.

Historical accepted evidence is not rewritten merely because the current
harness evolves. The retained H0 validator and checksum catalog attest the
pre-acceptance H0 boundary; they are not post-closeout mutable-state validators
and do not supersede current task, checkpoint, or chain records. Personal and
concurrently edited working notes are outside harness authority. H0 observations about them are historical nonmutation
provenance only, not required harness resources or reusable validator inputs.

## VVUQ boundary

Harness development requires software verification. Numerical verification applies only if the harness implements an actual numerical algorithm. Scientific validation and uncertainty quantification are not applicable to the harness itself.

The harness may help enforce correct VVUQ classification. That capability is not itself scientific-validation or UQ evidence.
