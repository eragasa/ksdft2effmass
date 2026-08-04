# PI Harness

## Purpose

The PI harness provides the reusable control-plane machinery used to plan, authorize, verify, review, and close bounded research-software tasks. It separates generic agent-operational behavior from the scientific and project-specific meaning owned by `ksdft2effmass`.

The harness does not perform a scientific calculation merely because it can represent a task, checkpoint, or evidence record. It coordinates work and verifies software-facing contracts; scientific execution and acceptance remain separately authorized project activities.

## Architectural split

The incubation architecture uses four source locations and one runtime-state location:

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

The harness incubation project is organized as

```text
P1 closeout
→ H0 inventory
→ H1 contract
→ H2 Python core
→ H3 skills and resources
→ H4 local integration and cutover
→ H5 extraction-readiness acceptance
→ separate P2 activation
```

P2 is not launched by completing the harness. It still requires a separate explicit activation after accepted P1 and accepted H5.

## Sources of truth

These pages explain durable architecture and usage. They do not own live status.

- `.pi/tasks/` owns task scope and status.
- `.pi/checkpoints/` owns human decisions.
- `.pi/chains/` owns task dependencies and authorization state.
- `.pi/evidence/` owns retained execution and review evidence.
- `docs/harness/` owns maintained human-readable explanation.

Historical accepted evidence is not rewritten merely because the current harness evolves.

## VVUQ boundary

Harness development requires software verification. Numerical verification applies only if the harness implements an actual numerical algorithm. Scientific validation and uncertainty quantification are not applicable to the harness itself.

The harness may help enforce correct VVUQ classification. That capability is not itself scientific-validation or UQ evidence.
