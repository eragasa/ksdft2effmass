# Workflow architecture gate

## Status

**Architecture and authorized source implementation complete; local software verification and independent implementation review found no blocking findings.**

The gate sequence and its implementation boundary are shown in the
[scientific Workflow schematic](../workflow/schematic.md#architecture-gate).

## Human decision

Recorded: 2026-10-03

Verbatim human response:

> architectural gate approved

## Interpretation

The approval accepts the architecture-gate procedure stated immediately before the
response:

1. plan the persistent corrections for all consolidated Workflow defects before source
   implementation;
2. document the target class contracts, inheritance, authority, plan/binding split,
   migration map, public API changes, and required evidence;
3. reconcile those class contracts into one consistent package architecture; and
4. perform one coordinated implementation run only after the documentation gate is
   complete.

The approval does not assert that the class-contract documentation is already complete
and does not close `DEFECT00001`, `DEFECT00002`, or `DEFECT00003`. The defects remain
open until their documented closure conditions and applicable software evidence are
satisfied.

## Authority boundary

This decision authorizes architecture documentation and planning within the stated
Workflow scope. It does not itself authorize source implementation, periodic-1D replay,
external or protected execution, persistence migration, pushing, release, or
publication.

## Completion condition

The documentation gate is complete only when:

- every target class has an authoritative class-owned contract and schematic;
- all consolidated defects map to those contracts without contradiction;
- the package inheritance and dependency schematic is coherent;
- current-to-target public API and migration changes are explicit;
- required software evidence is specified; and
- no unresolved architectural choice remains before the coordinated implementation
  run.

## Subsequent nominal-ABC decision

Recorded: 2026-10-03

Verbatim human response:

> NO PROTOCOLS MUST BECOME ABCs

This is interpreted from the immediately preceding Protocol inventory as: maintained
Python source must expose no `typing.Protocol` classes; every current structural
Protocol migrates to a nominal ABC in its owning package. Target abstract class names
use the `Abstract...` prefix, concrete implementations inherit nominally, and retired
Protocol names receive no compatibility aliases.

This decision expands the coordinated migration beyond Workflow-only contracts to the
calculator, operator-representation, and shared persistence ports identified by the
inventory. The architecture gate is therefore reopened until every affected class has
an owning class contract, schematic, crosswalk entry, dependency-impact analysis, and
required software evidence.

## Quantum ESPRESSO Workflow scope correction

Recorded: 2026-10-03

The human first considered `AbstractQuantumEspressoSimulationTask`, corrected that to
`AbstractQuantumEspressoSimulationWorkflow`, and then selected the shorter
`AbstractQeSimulationWorkflow` name. The subsequent instruction supersedes the entire
proposed class migration:

> ignore QeWorkflows because there are already imprlmented in solutions

Accordingly, this migration introduces no QE-specific Workflow ABC and does not
redesign the separately implemented QE Workflow family. The existing
`QuantumEspressoSimulation` composition receives only the nominal-ABC reference
changes required by the repository-wide Protocol decision; it is not mapped to a Task,
Workflow, or runtime-binding replacement in this scope.

## Expanded migration artifacts

The [repository-wide Protocol-to-ABC crosswalk](../protocol-to-abc-migration.md)
records all thirteen current Protocols, target nominal ABCs, concrete implementation
and test impacts, public-name removal, implementation order, and required evidence.
Each target has an owning `index.md` and `schematic.md` under `calculators/`,
`operators/`, `persistence/`, or `workflows/`.

The [writer consistency pass](../protocol-to-abc-architecture-consistency-review.md)
records successful class-presence, link, terminology, engine-signature, QE-scope, and
diff checks. Initial independent review run `5756838a-fd7c-43a9-b009-041344bfdcd3` reported no
blocking finding. Fresh post-commit review run
`3df10313-3b16-4599-90f2-69a32bab33e3` found four documentation contradictions; those
were corrected, and follow-up review run `09b97f2a-a6be-496f-b59f-ce91f7c7347f`
reported no blocking finding. The expanded documentation gate is complete. This
documentation work does not authorize source implementation.

## Coordinated implementation completion

The subsequently authorized coordinated implementation replaced all thirteen
maintained Protocol contracts with nominal ABCs and implemented the three persistent
Workflow corrections. Local evidence passed Ruff formatting and lint, strict mypy,
strict Sphinx, 455 local architecture links, package-wheel checks, and the complete
Python suite with 4,645 passes and three unavailable external-QE fixture skips.
Independent read-only implementation review run
`b050cedf-9857-4999-b727-c635a4126051` reported `NO_BLOCKING_FINDINGS`; its one
nonblocking terminology note was corrected before closure. These checks establish
software conformance only and authorize no external calculation, replay, release, or
publication.

## Prior completion record

The [Workflow consistency review](migration/architecture-consistency-review.md)
completed the earlier Workflow-only gate. It is retained as bounded historical
evidence but no longer closes the expanded repository-wide gate. The consolidated
Workflow defect corrections are now closed by the implementation and evidence above.
