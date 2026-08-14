# Development harness

## Responsibility

The development harness is owned by `ksdft2effmass.harness`. Its represented scope is limited to:

- repository changes;
- software architecture;
- implementation;
- software verification;
- repository documentation;
- development review; and
- development Task selection and closure records.

## Core records

`HarnessTask` is an immutable development work definition. It owns scope, preconditions, completion criteria, exclusions, and review requirements. `DevelopmentTaskSelection` identifies the authorized active development work and keeps automatic successor behavior explicit.

Neither object contains scientific CPN markings, calculator requests, numerical observations, scientific findings, or parameter selections.

Development-conformance scope cuts across workflow, Petri-net, calculator, scientific-domain, test, fixture, documentation, and harness paths. This cross-cutting scope does not transfer domain meaning to the harness or create runtime imports from scientific packages back to the development control plane.

## Development control

A development Task has no general phase state machine. `HarnessTask` defines the authorized outcome, `DevelopmentTaskSelection` identifies the exact work permitted to proceed, and `HarnessTaskClosure` records how that selection ended. Implementation, software verification, review, and correction are performed when the Task or process class requires them, but they are not persisted lifecycle phases. Protected or human-owned decisions remain explicit, and no record is manufactured merely to add ceremony.

The development harness may:

- observe an explicit repository root and starting revision;
- validate operation-specific repository preconditions;
- enforce the scope of explicitly selected and authorized source and documentation work;
- run [repository-wide development conformance](conformance.md) and applicable software-verification checks;
- calculate mechanical promotion eligibility without manufacturing human authority;
- project development control state through the deterministic [compiler architecture](compiler-architecture.md); and
- retain independently authorized development review and acceptance records.

It may not execute a scientific `ScientificWorkflow`, advance a `ScientificWorkflowRun`, classify a calculator result scientifically, or record a `ScientificDisposition`.

## Package boundary

`ksdft2effmass.harness` owns development-harness contracts and composition. Project scientific specifications and scientific workflow state remain outside the harness package. Harness operations receive explicit roots and inputs; they perform no ambient repository discovery.

A project specializes conformance with explicit immutable policy and validator composition. It does not subclass a nominal base conformance architecture and override inherited rules. A future ProjectKoios extraction may receive only generic behavior demonstrated by local implementation; concrete `ksdft2effmass` policy remains project-owned.

Submodule and wire-format details may be refined while preserving this package boundary.

## Unresolved issues

- Exact public fields of `HarnessTask`, `DevelopmentTaskSelection`, and `HarnessTaskClosure`.
- Closure disposition and authority rules.
- Representation of development review and acceptance.
- Boundary between generic repository operations and project-specific policy.
- Whether routine work uses the same lifecycle record with a shorter route or a distinct operation profile.
