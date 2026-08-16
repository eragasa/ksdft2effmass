# Development harness

## Responsibility

The development harness is owned by `ksdft2effmass.harness`. Its authority is limited to:

- repository changes;
- software architecture;
- implementation;
- software verification;
- repository documentation;
- development review; and
- development lifecycle state.

Its conformance scope cuts across the repository, including workflow, calculator, scientific-domain, test, fixture, documentation, and harness paths. This cross-cutting scope does not transfer ownership of domain meaning to the harness or create runtime imports from scientific packages back to the development control plane.

## Core records

`HarnessTask` is an immutable requested development work definition. It records scope, preconditions, completion criteria, exclusions, and review requirements but grants no authority. `DevelopmentTaskSelection` is repository-derived requested/selected work state and keeps automatic successor behavior explicit; it is neither authority nor permission.

Neither object contains scientific colored-Petri-net markings, calculator requests, numerical observations, scientific findings, or parameter selections.

## Development lifecycle

A development operation moves through planned, active, implementation, software verification, review, and completed states according to policy. Protected or human-owned decisions remain explicit external inputs, but no stage is manufactured merely to add ceremony. The single immutable `DevelopmentDecision` model has unresolved and resolved variants/revisions and covers human-owned development architecture, dependencies, scope, protected repository operations, review, and acceptance. It preserves exact request/question/options/scope, verbatim response, normalized declared outcome when unambiguous, source/authority identity, and applicable predecessor/supersession. Ambiguous, unmatched, or conflicting responses remain unresolved; a pending decision blocks only its declared transition and scope. See [human decisions](../../human-decisions.md). Routine deterministic corrections may use a shorter route.

The development harness may:

- observe an explicit repository root, starting revision, candidate revision, exact selection revision, and exact Task revision;
- validate operation-specific repository preconditions;
- reconstruct and verify a candidate-independent `DevelopmentAuthorityContext`, then use `DevelopmentOperationAuthorizer` to return an exact authorization result for those revisions, the operation, and permitted paths;
- enforce the resulting scope of explicitly authorized source and documentation changes;
- run repository-wide [development conformance](conformance.md) and applicable software-verification checks;
- calculate mechanical promotion eligibility without manufacturing human authority;
- project development control state through the deterministic [compiler architecture](compiler-architecture.md); and
- retain independently authorized development review and acceptance records.

It may not execute a scientific `Workflow`, advance a `WorkflowRun`, classify a calculator result scientifically, or record a `ScientificDisposition`.

## Package boundary

`ksdft2effmass.harness` owns development-harness contracts and composition. Project scientific specifications and scientific workflow state remain outside the harness package. Harness operations receive explicit roots and inputs; they perform no ambient repository discovery.

A project specializes development conformance with an explicit immutable policy and validator composition. It does not subclass a nominal base conformance architecture and override inherited rules. A future ProjectKoios extraction may receive only generic behavior demonstrated by the local implementation; concrete `ksdft2effmass` policy remains project-owned.

Submodule and wire-format details may be refined while preserving this package boundary.

## Unresolved issues

- Exact public fields of `HarnessTask` and `DevelopmentTaskSelection`.
- Closed lifecycle vocabulary and permitted transition rules.
- Exact field and wire representation of `DevelopmentDecision` variants/revisions.
- Boundary between generic repository operations and project-specific policy.
- Exact local conformance-policy and profile contracts before any ProjectKoios extraction.
- Whether routine work uses the same lifecycle record with a shorter route or a distinct operation profile.

## Aggregate and authority topology

Authoritative repository sources compile independently of authority to one complete immutable `HarnessState`, which lossless revisioned persistence may reconstruct but not supersede. Unrepresentable normalization returns no state; representable cross-record defects remain available for validation. Protected development authority is resolved separately as `DevelopmentAuthorityLedger` through explicit `DevelopmentAuthorityContextResolver`, `DevelopmentAuthorityContext`, and `DevelopmentTrustConfiguration`, and exact operation matching belongs to `DevelopmentOperationAuthorizer`. Compilation and validation never select authority from ambient or candidate-controlled state. A `HarnessTask`, `DevelopmentTaskSelection`, candidate decision, candidate artifact, validation result, or target operation cannot authorize itself.
