# Harness architecture history in v1

This page consolidates the former numbered pages under `docs/harness/`. It preserves
their architectural sequence and current disposition without treating plans, review
packets, generated Task views, or historical status prose as current authority. Exact
historical text remains available from Git history and retained Task, checkpoint, and
evidence records.

## Incubation and implemented architecture

The H0–H4 incubation sequence established the generic/project-local dependency
boundary, immutable generic records and actions, versioned resources, the Python
reference implementation, and project-local validation composition. The implemented
result is documented by the current v1 Harness pages:

- [`ksdft2effmass.harness`](index.md);
- [`ksdft2effmass.harness.pi`](pi/index.md);
- [development model](pi/development-harness.md);
- [control plane](pi/control-plane.md); and
- [resources and validation](pi/resources-and-validation.md); and
- [human-review objects](pi/human-review.md).

The former current-architecture documents were incorporated as follows:

| Former document | Incorporated owner |
|---|---|
| `ksdft2effmass.harness.000.000.000` | v1 Harness index and this history |
| `ksdft2effmass.harness.001.000.000` | v1 Harness and Pi package indexes |
| `ksdft2effmass.harness.001.001.000` | v1 Harness index and resources/validation |
| `ksdft2effmass.harness.001.002.000` | resources/validation |
| `ksdft2effmass.harness.001.003.000` | Pi package index and resources/validation |
| `ksdft2effmass.harness.001.004.000` | resources/validation |
| `ksdft2effmass.harness.001.006.000` | development model, resources/validation, and this history |

## Simplification sequence

The simplification program explored unified state, evidence extraction, durable roles,
maintained execution, capability ownership, Task serialization, and documentation
migration. Its retained resource procedure is `develop-harness-resources`; other
implemented procedures are documented by their current owners. Implemented capabilities remain documented with their current owners;
rejected, superseded, deferred, or inactive designs remain historical rather than
parallel architecture.

| Former document | Disposition |
|---|---|
| `002.000.000` — Harness simplification plan | Historical program index; not authority as a whole |
| `002.001.000` — First simplification round | Historical workstream index |
| `002.001.001` — Unified state model | Superseded proposal; later SQLite projection is documented by its implemented owner |
| `002.001.002` — Extractable evidence subsystem | Deferred proposal; no separate evidence repository was accepted |
| `002.001.003` — Durable agent architecture | Implemented role boundary summarized in Pi subagent architecture |
| `002.001.004` — Create durable Harness roles | Completed implementation history |
| `002.001.005` — Simplify durable project roles | Completed implementation history |
| `002.001.006` — Executable tool placement | Implemented command-placement history |
| `002.001.007` — Maintained execution interface | Inactive command-runner proposal |
| `002.001.008` — Capability ownership rationalization | Completed and deferred slices retained as implementation history |
| `002.001.009` — Incremental migration plan | Superseded by maintained v1-to-v2 migration pages |
| `002.001.010` — HarnessTask contract and migration review | Stage history; the accepted version-3 Task contract remains |
| `002.001.011` — HarnessTask model contract | Accepted contract history |
| `002.001.012` — HarnessTask implementation and hardening | Core implementation retained; migration framework removed |
| `002.001.013` — Serial six-file Task migration | Deferred and inactive |
| `002.002.005` — Documentation/control correction | Completed correction history |

Generated Markdown under the former `docs/harness/tasks/` duplicated maintained Task
JSON under `harness/tasks/`. It was removed rather than incorporated into architecture.
The Task JSON remains the durable record whenever managed work is explicitly used.

## Human-review sequence

The initial human-review work introduced explicit immutable review targets,
observations, findings, packets, preparation, decisions, and decision recording. The
implemented pure Python boundary is documented in [human-review objects](pi/human-review.md).
Persistence, natural-language interpretation, checkpoint mutation, Git mutation,
automatic acceptance, and successor activation were not added.

| Former document | Disposition |
|---|---|
| `003.000.000` — Human review interface | Program history |
| `003.001.000` — Initial review round | Corrected pilot history |
| `003.001.001` — Human Review Packet and Decision Workflow | Bounded packet API implemented; broader workflow remained inactive |
| `003.001.002` — Human decision recording | Pure explicit-input runtime representation implemented |

## Telemetry sequence

`ksdft2effmass.harness.004.000.000` described an inactive telemetry and effectiveness
program. Only its bounded session-inventory history was completed. No live telemetry
extension, normalized-event contract, telemetry database, effectiveness conclusion,
or benchmark program became part of the maintained Harness architecture. Operational
efficiency was never evidence of software correctness or scientific validity.

## Historical index

`ksdft2effmass.harness.090.000.000` previously indexed incubation, shadow replay,
cutover, renames, and documentation migration. Current package boundaries are now
stated directly in v1 architecture; retained reports and Git history preserve the
original observations. Historical replay or evidence cannot activate work or override
current source and policy.
