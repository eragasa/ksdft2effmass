# Repository-wide Protocol-to-ABC migration

## Status

**Accepted repository-wide direction; class contracts and source implementation remain pending.**

The human decision requires maintained Python source to contain no
`typing.Protocol` classes. Every current structural Protocol becomes a nominal ABC in
its owning package. Target names use the `Abstract...` prefix, concrete implementations
inherit explicitly, and retired Protocol names receive no compatibility aliases.

This is a software-contract migration. It authorizes no external calculation, replay,
persistence mutation, scientific acceptance, release, or publication.

## Complete current-to-target crosswalk

| Current Protocol | Target nominal ABC | Owner | Primary nominal implementations or consumers |
|---|---|---|---|
| `PlaneWaveCalculator` | `AbstractPlaneWaveCalculator` | `calculators.dft.pw` | Retained calculator implementations and test doubles inherit explicitly. QE Task-local calculator fields and direct-delegation fixtures are removed rather than migrated; only `QuantumEspressoSimulation` receives mechanical nominal-reference changes. `LocalQuantumEspressoExecutor` is not admitted through this ABC because its authority-bearing `execute` signature belongs to the dispatch-effect route. |
| `UniformGrid1DRepresentation` | `AbstractUniformGrid1DRepresentation` | `operators.finite_differences` | `analysis.model_systems.UniformCartesianGrid1D` |
| `DirichletBoundaryConditionRepresentation` | `AbstractDirichletBoundaryConditionRepresentation` | `operators.finite_differences` | `analysis.model_systems.DirichletBoundaryCondition` |
| `DirichletIntervalRepresentation` | `AbstractDirichletIntervalRepresentation` | `operators.finite_differences` | `analysis.model_systems.DirichletInterval` |
| `AtomicRevisionStore` | `AbstractAtomicRevisionStore` | `persistence.store` | `SQLiteAtomicRevisionStore` |
| `SimulationDispatchEntryCommitter` | `AbstractSimulationDispatchEntryCommitter` | `workflows.control.dispatch` | `WorkflowRunDispatchEntryCommitter` |
| `SimulationDispatchEffect` | `AbstractSimulationDispatchEffect` | `workflows.control.dispatch` | `LocalQuantumEspressoExecutor` and explicit test effects |
| `ResultObject` | `AbstractResultObject` | `workflows` | The closed maintained Workflow result set listed below |
| `ObservationCorrelationIdentity` | `AbstractObservationCorrelationIdentity` | `workflows.observations` | QE parsed-document, parser, and normalization-policy identity classes plus explicit test identities |
| `ObservationNormalizationPolicySource` | `AbstractObservationNormalizationPolicySource` | `workflows.observations` | `QuantumEspressoObservationNormalizationPolicy` plus explicit test policies |
| `NormalizedObservationSource` | `AbstractNormalizedObservationSource` | `workflows.observations` | `QuantumEspressoExtractedObservationResult` plus explicit test sources |
| `WorkflowResultValueCodec` | `AbstractWorkflowResultValueCodec` | `workflows.persistence` | `WorkflowResultValueSerializer`, `QuantumEspressoResultValueSerializer`, `QuantityOfInterestResultValueSerializer`, and `ApplicationResultValueSerializer` |
| `WorkflowRunRepository` | `AbstractWorkflowRunRepository` | `workflows.persistence` | `WorkflowRunAtomicRepository` |

The exhaustive [symbol inventory](protocol-to-abc-symbol-inventory.md) records every
maintained declaration, export, production implementation, positive and negative test
double, boundary consumer, and target action known at this gate.

The target does not add registries, factories, virtual subclass registration,
`__subclasshook__` structural fallback, or compatibility aliases. An object with
matching attribute names but no nominal inheritance is rejected.

## Closed `AbstractResultObject` migration set

Nominal conversion must not make every class whose name ends in `Result` a Workflow
result. The maintained objects that currently cross the exact Workflow result boundary
and therefore inherit `AbstractResultObject` are:

- `ScientificDecisionResolution`;
- `NormalizedObservationSet`;
- `QuantumEspressoPwResult`;
- `QuantumEspressoBandsResult`;
- `QuantumEspressoExtractedObservationResult`;
- `ScalarQuantityOfInterestValue`; and
- `ScalarQuantityOfInterestEvaluationFailure`.

Test-only concrete result classes inherit the ABC explicitly. Other scientific,
numerical, verification, campaign, and serializer result records remain owned by their
existing domains unless an actual Workflow result route separately admits them. The
migration adds no identity merely because a class name contains `Result`.

`AbstractNormalizedObservationSource` inherits `AbstractResultObject`, so
`QuantumEspressoExtractedObservationResult` has one nominal route rather than parallel
structural checks.

## Concrete dependency changes

### Calculator and Quantum ESPRESSO integration

`AbstractPlaneWaveCalculator[InputT, OutputT]` preserves the current generic calculator
signature and grants no Workflow authority. It is not the external-effect port.
Authority-bearing local process invocation remains exclusively
`AbstractSimulationDispatchEffect.execute(SimulationDispatchEffectRequest)`.

The coordinated Workflow migration removes calculator invocation from the four QE
simulation Tasks. Existing QE Workflow implementations outside this migration are not
redesigned. `QuantumEspressoSimulation` receives only mechanical nominal-ABC reference
changes in this scope. The incompatible method signatures mean
`LocalQuantumEspressoExecutor` must not be treated as an
`AbstractPlaneWaveCalculator` merely because runtime Protocol inspection previously saw
an `execute` attribute.

### Operator representations

The three analysis-owned model-system records inherit the operator-owned ABCs
nominally. This preserves the existing direction from analysis to operators; affected
analysis modules add the required operator-owned ABC imports without any reverse
operator-to-analysis import. Operator constructors replace
runtime structural checks with nominal checks. The migration adds no numerical method,
grid convention, boundary convention, or convergence claim.

### Shared and Workflow persistence

`SQLiteAtomicRevisionStore` inherits `AbstractAtomicRevisionStore`.
`WorkflowRunAtomicRepository` inherits `AbstractWorkflowRunRepository` and continues
to compose the shared store; no domain-specific SQLite subclass is introduced.
`WorkflowRunDispatchEntryCommitter` inherits
`AbstractSimulationDispatchEntryCommitter`.

All four maintained result-value serializers inherit
`AbstractWorkflowResultValueCodec`. Their exact supported branches, bytes, versions,
and closed failures remain unchanged.

### Observation adaptation

The QE-owned nominal identity, policy, and extracted-result classes explicitly inherit
the applicable Workflow observation ABCs. Workflow still owns only the neutral
read-only boundary; QE retains native parsing, policy meaning, and source provenance.
Nominal inheritance establishes software membership only, not provenance authenticity
or scientific validity.

## Public API changes

Every current Protocol export is removed and replaced by its target `Abstract...`
export at the same owning package boundary. Tests and documentation use only the new
names. Importability of a retired name is a migration failure; no alias or deprecation
shim is retained.

`typing.Protocol` and `typing.runtime_checkable` imports disappear when no other local
contract needs them. Runtime checks use the nominal ABC. Static typing must show every
maintained implementation inheriting its exact ABC.

## Affected evidence owners

The coordinated implementation updates at least these maintained evidence surfaces:

- `python/tests/software_verification/ksdft2effmass/calculators/test__PlaneWaveCalculator.py` and calculator public-API tests;
- the three operator representation test modules and their ownership resource;
- `persistence/test__SQLiteAtomicRevisionStore.py` and `test__store_contract.py`;
- Workflow model, observation, control, persistence, public-API, and engine tests;
- QE Task, Simulation, executor, observation-adapter, result-codec, execution-contract,
  and dependency-direction tests;
- analysis and application result-codec tests; and
- all local synthetic implementations currently accepted structurally.

Tests that currently assert conformance without inheritance are inverted: missing
nominal inheritance must fail, while exact nominal subclasses must pass. Negative tests
must not widen production annotations or reintroduce structural fallback.

## Coordinated implementation order

1. Add all target ABCs and remove Protocol decorators/imports.
2. Migrate concrete identities, records, adapters, repositories, serializers, stores,
   representations, and retained positive test doubles to nominal inheritance; remove
   obsolete structural fixtures rather than granting them nominal membership.
3. Apply the accepted Workflow Task, result, plan, binding, and engine migration,
   including the definition-only QE simulation Task changes.
4. Update `QuantumEspressoSimulation` references mechanically without designing a QE
   Workflow.
5. Replace public exports, annotations, documentation, and tests; retain no aliases.
6. Run a source-wide `Protocol` absence check, strict typing, Ruff, formatting, focused
   suites, broader Workflow/QE/persistence/operator/calculator suites, public-API
   checks, strict Sphinx, and `git diff --check`.

## Required evidence

Before the architecture gate can close, class-owned contracts and schematics must exist
for every target ABC, all owning architecture pages must use nominal terminology, and
an independent review must find no unresolved target contradiction.

Before source implementation can close, evidence must establish:

- zero maintained `typing.Protocol` declarations or imports;
- exact nominal acceptance and structural-lookalike rejection for every ABC;
- complete concrete-implementation inheritance and retired-name absence;
- unchanged serializer bytes and persistence payloads;
- unchanged scientific and numerical values;
- no import cycle introduced by nominal bases;
- simulation effects remain behind the authority-bearing request route; and
- the accepted Workflow route, result, plan, binding, and engine invariants hold.

These checks establish software conformance only. They do not establish numerical
verification, scientific validation, uncertainty quantification, execution authority,
or human acceptance.
