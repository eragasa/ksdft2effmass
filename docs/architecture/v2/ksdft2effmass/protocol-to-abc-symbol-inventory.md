# Protocol-to-ABC symbol inventory

## Status and use

**Authoritative implementation inventory; coordinated source changes are implemented and locally software-verified.**

This inventory expands the 13-row
[contract crosswalk](protocol-to-abc-migration.md) into concrete declarations, exports,
implementations, test doubles, consumers, and target actions. Paths are authoritative;
line numbers in review reports are inspection aids and may move during implementation.
No unlisted structural implementation may remain accepted after migration.

## `PlaneWaveCalculator` → `AbstractPlaneWaveCalculator`

| Kind | Exact symbols or paths | Target action |
|---|---|---|
| Declaration | `python/src/ksdft2effmass/calculators/dft/pw/calculator.py:AbstractPlaneWaveCalculator` | Implemented as the nominal generic ABC with abstract `execute`. |
| Export | `python/src/ksdft2effmass/calculators/dft/pw/__init__.py` | Export only `AbstractPlaneWaveCalculator`; remove the retired name. |
| Production consumers | Four calculator fields/checks in `integration/quantum_espresso/tasks.py`; calculator field/check in `integration/quantum_espresso/simulation.py` | Remove the Task fields, constructor parameters, checks, and direct invocation under the accepted simulation route. Change only the retained `QuantumEspressoSimulation` reference nominally; do not infer calculator membership from an executor method name. |
| Production implementers | No maintained concrete source class has the exact generic calculator signature. `LocalQuantumEspressoExecutor.execute(SimulationDispatchEffectRequest)` is incompatible and is explicitly excluded. | Do not add the calculator ABC to `LocalQuantumEspressoExecutor`. |
| Retained positive test doubles | `_FixturePlaneWaveCalculator` in `calculators/test__PlaneWaveCalculator.py`; local `Calculator` classes in `integration/quantum_espresso/test__QuantumEspressoSimulation.py` | Inherit `AbstractPlaneWaveCalculator` explicitly because these tests continue to exercise the retained calculator boundary. |
| Removed/reworked Task-local fixtures | Local `PwCalculator`, `BandsCalculator`, `Calculator`, and `WrongCalculator` classes in `integration/quantum_espresso/test__quantum_espresso_task_contracts.py` | Do **not** migrate these obsolete direct-Task fixtures to the ABC. Rework constructor evidence around definition/input ownership; move relevant dispatch/result-shape and correlation behavior to engine/effect-route evidence; remove direct Task-delegation cases. `WrongCalculator` is currently a wrong-return-value fixture, not a nominal-membership negative. |
| Nominal negative fixture | Add a separate method-matching non-inheriting lookalike in `calculators/test__PlaneWaveCalculator.py`. | Assert rejection specifically because nominal inheritance is absent, independently of wrong-result behavior. |
| Public/evidence tests | `calculators/test__calculator_public_api.py`, `calculators/test__PlaneWaveCalculator.py`, QE Task and Simulation tests | Assert new export, retained nominal acceptance, distinct lookalike rejection, retired-name absence, and absence of direct calculator execution from QE Tasks. |

## Operator representation ABCs

| Current → target | Declaration/export | Nominal production implementation | Consumers and tests | Target action |
|---|---|---|---|---|
| `UniformGrid1DRepresentation` → `AbstractUniformGrid1DRepresentation` | `operators/finite_differences.py`; `operators/__init__.py` | `analysis/model_systems/cartesian_grids.py:UniformCartesianGrid1D` | `SecondOrderCentralDifferenceLaplacian1D`; `operators/test__UniformGrid1DRepresentation.py` | Add explicit inheritance; replace structural checks and public import; add a non-inheriting lookalike rejection case. |
| `DirichletBoundaryConditionRepresentation` → `AbstractDirichletBoundaryConditionRepresentation` | `operators/finite_differences.py`; `operators/__init__.py` | `analysis/model_systems/boundary_conditions.py:DirichletBoundaryCondition` | `SecondOrderCentralDifferenceLaplacian1D`; `operators/test__DirichletBoundaryConditionRepresentation.py` | Add explicit inheritance; replace checks/import; reject lookalikes. |
| `DirichletIntervalRepresentation` → `AbstractDirichletIntervalRepresentation` | `operators/finite_differences.py`; `operators/__init__.py` | `analysis/model_systems/intervals.py:DirichletInterval` | `SecondOrderCentralDifferenceLaplacian1D`, `SchrodingerKineticEnergy1D`, `SampledPotential1D`, and `FiniteDifferenceHamiltonian1D`; `operators/test__DirichletIntervalRepresentation.py` | Add explicit inheritance; replace checks/import; reject lookalikes. |

The concrete analysis modules may import the ABC definitions from
`operators.finite_differences`; that module imports operator-owned quantities and no
analysis package. This is a new module-level import for `intervals.py`, not a claim
that every affected module already imports the ABC owner.

## `AtomicRevisionStore` → `AbstractAtomicRevisionStore`

| Kind | Exact symbols or paths | Target action |
|---|---|---|
| Declaration/export | `persistence/store.py:AtomicRevisionStore`; `persistence/__init__.py` | Rename/export nominal ABC only; make `read` and `commit` abstract. |
| Production implementation | `persistence/sqlite.py:SQLiteAtomicRevisionStore` | Inherit explicitly. |
| Production consumer | `workflows/persistence.py:WorkflowRunAtomicRepository.store` and constructor check | Annotate/check `AbstractAtomicRevisionStore`. |
| Positive test doubles | `CompleteStore` in `persistence/test__store_contract.py`; `CountingStore` in `workflows/persistence/test__WorkflowRunAtomicRepository__nested_history.py`; `Store` in `test__WorkflowRunAtomicRepository.py` | Inherit explicitly. |
| Negative test double | `ReadOnlyStore` in `persistence/test__store_contract.py` | Remain non-nominal and be rejected. |
| Evidence | `persistence/test__SQLiteAtomicRevisionStore.py`, `test__store_contract.py`, and the two Workflow repository modules above | Replace structural-conformance assertions with nominal acceptance/lookalike rejection and retired-name absence. |

## Dispatch ABCs

### `SimulationDispatchEntryCommitter` → `AbstractSimulationDispatchEntryCommitter`

- Declaration: `workflows/control/dispatch.py`.
- Exports: `workflows/control/__init__.py` and `workflows/__init__.py`.
- Production implementation: `WorkflowRunDispatchEntryCommitter`.
- Production consumer: `SimulationDispatchAdapter.entry_committer` and its constructor
  check.
- Positive test double: `RecordingSimulationDispatchEntryCommitter` in
  `workflows/control/resources/scenarios.py`.
- Evidence/public API: Workflow control scenario and dispatch-adapter tests,
  `workflows/control/test__public_api.py`, and `workflows/runs/test__public_api.py`.
- Target action: explicit inheritance, abstract `execute(SimulationDispatchRequest)`,
  nominal check, new export only, and lookalike rejection.

### `SimulationDispatchEffect` → `AbstractSimulationDispatchEffect`

- Declaration: `workflows/control/dispatch.py`.
- Exports: `workflows/control/__init__.py` and `workflows/__init__.py`.
- Production implementation: `integration/quantum_espresso/executor.py:LocalQuantumEspressoExecutor`.
- Production consumers: `SimulationDispatchAdapter.effect` and
  `integration/quantum_espresso/simulation.py:QuantumEspressoSimulation.executor`.
- Positive test doubles: `RecordingSimulationDispatchEffect` in
  `workflows/control/resources/scenarios.py` and local `NonInvokedEffect` in
  `integration/quantum_espresso/test__QuantumEspressoSimulation.py`.
- Evidence/public API: `workflows/control/test__SimulationDispatchEffect.py`, dispatch
  adapter tests, `integration/quantum_espresso/test__LocalQuantumEspressoExecutor.py`,
  QE Simulation tests, and both Workflow public-API modules.
- Target action: explicit inheritance, abstract `executor_identity` and `execute`,
  nominal checks, retired-name absence, and no generic dispatch-effect parent.

## `ResultObject` → `AbstractResultObject`

### Declaration, export, and production implementations

- Declaration: `workflows/model.py:ResultObject`.
- Export: `workflows/__init__.py`.
- Exact maintained production implementations:
  - `workflows/runs/records.py:ScientificDecisionResolution`;
  - `workflows/observations.py:NormalizedObservationSet`;
  - `integration/quantum_espresso/contracts.py:QuantumEspressoPwResult`;
  - `integration/quantum_espresso/contracts.py:QuantumEspressoBandsResult`;
  - `integration/quantum_espresso/observation.py:QuantumEspressoExtractedObservationResult`;
  - `analysis/qoi.py:ScalarQuantityOfInterestValue`; and
  - `analysis/qoi.py:ScalarQuantityOfInterestEvaluationFailure`.

Each inherits explicitly. No other production class is added merely because its name
contains `Result`.

### Production consumers

The exact Workflow boundaries are:

- `workflows/model.py`: `TaskInputBinding` and current Task return annotations;
- `workflows/engine.py`: current return/result checks, replaced by
  `TaskExecutionResults` and nominal members;
- `workflows/observations.py`: observation-source/result assembly;
- `workflows/persistence.py`: decode values, serializer inputs, run values, and source
  codec;
- `workflows/runs/records.py`: result production and invocation outcomes;
- `integration/quantum_espresso/tasks.py`: current Task returns;
- `integration/quantum_espresso/result_values.py`, `analysis/result_values.py`, and
  `application/result_values.py`: codec inputs and exact supported branches; and
- `integration/quantum_espresso/executor.py` and `observation.py`: returned/adapted
  exact results.

### Maintained test-only result implementations

The following positive synthetic result classes inherit `AbstractResultObject`:

- `workflows/test__WorkflowEngine.py:SyntheticResult`;
- `workflows/_cpn_adapter_fixtures.py:SyntheticResult`;
- `workflows/persistence/test__WorkflowResultValueDecodeResult.py:SyntheticResult`;
- `workflows/model/test__TaskInputBinding.py:ConcreteResult` cases;
- `workflows/model/test__TaskActivation.py:ConcreteResult`;
- `workflows/model/test__ResultObject.py:ConcreteResult`;
- `workflows/control/resources/scenarios.py:SyntheticControlResult`;
- `workflows/runs/records/test__TaskInvocationOutcome.py:_SyntheticResult`;
- `workflows/runs/aggregate/test__WorkflowRun.py:_SyntheticResult`; and
- `workflows/runs/replay/test__WorkflowRunReplayer.py:_SyntheticResult`.

The local `IdentityOnly` classes in the analysis, application, Workflow, and QE codec
tests become explicit test-only `AbstractResultObject` subclasses when the test intends
an unsupported-but-valid nominal result. Separate new lookalike cases remain
non-nominal and must raise `TypeError`; this preserves the distinction between nominal
result membership and codec support.

Public/export evidence is owned by `workflows/runs/test__public_api.py` and affected
Workflow model, engine, run, persistence, QE, analysis, and application codec modules.

## Observation ABCs

| Current → target | Production implementations | Consumers/test doubles | Target action |
|---|---|---|---|
| `ObservationCorrelationIdentity` → `AbstractObservationCorrelationIdentity` | `QuantumEspressoParsedDocumentIdentity`, `QuantumEspressoXsdParserIdentity`, `QuantumEspressoObservationNormalizationPolicyIdentity` in `integration/quantum_espresso/observation.py` | `workflows/observations.py`; QE observation adapter/codec; observation assembler tests | Explicit inheritance for all three identities; nominal annotations and checks; retired export absent. |
| `ObservationNormalizationPolicySource` → `AbstractObservationNormalizationPolicySource` | `QuantumEspressoObservationNormalizationPolicy` | `NormalizedObservationSource.normalization_policy`; assembler and QE adapter/codec tests; local `SyntheticMalformedNormalizationPolicy` negative fixture | Production policy inherits. The malformed fixture either inherits with a narrow intentional type violation when policy-shape validation is under test or remains non-nominal when membership rejection is under test; the two claims must be separate. |
| `NormalizedObservationSource` → `AbstractNormalizedObservationSource` | `QuantumEspressoExtractedObservationResult` | `NormalizedObservationAssembler`; persistence source codec; `SyntheticNormalizedObservationSource` in `workflows/test__NormalizedObservationAssembler.py` | ABC extends `AbstractResultObject`; production and positive synthetic source inherit explicitly; all twelve source properties remain unchanged. |

All three retired names are exported only through `workflows/__init__.py`; only the
three target names remain. Public-import evidence is in
`workflows/runs/test__public_api.py` and the observation assembler's explicit import
checks.

## `WorkflowResultValueCodec` → `AbstractWorkflowResultValueCodec`

| Kind | Exact symbols or paths | Target action |
|---|---|---|
| Declaration/export | `workflows/persistence.py`; `workflows/__init__.py` | Rename/export nominal ABC only; abstract `encode` and `decode`. |
| Production implementations | `workflows/persistence.py:WorkflowResultValueSerializer`; `integration/quantum_espresso/result_values.py:QuantumEspressoResultValueSerializer`; `analysis/result_values.py:QuantityOfInterestResultValueSerializer`; `application/result_values.py:ApplicationResultValueSerializer` | Inherit explicitly; retain exact bytes and branches. |
| Production consumers | `WorkflowRunSerializer.result_codec`; `WorkflowResultValueSerializer.source_codec`; application composition | Use nominal annotations/checks. |
| Positive test doubles | `FailureCodec`, `AgreementCodec`, `WrongResultCodec`, and `RecursionCodec` in `workflows/persistence/test__WorkflowRunSerializer__codec_failures.py`; `FaultCodec` in `test__WorkflowRunSerializer.py` | Inherit explicitly. Names describe represented behavior, not invalid membership. |
| Evidence | Workflow, QE, analysis, and application result-value serializer tests plus Workflow public API | Assert nominal membership, bytes unchanged, unsupported nominal result handling, lookalike rejection, and retired-name absence. |

## `WorkflowRunRepository` → `AbstractWorkflowRunRepository`

- Declaration: `workflows/persistence.py`.
- Export: `workflows/__init__.py`.
- Production implementation: `WorkflowRunAtomicRepository`.
- Production consumer: `WorkflowRunDispatchEntryCommitter.repository` and constructor
  check.
- Positive test double: `EntryRepositoryProbe` in
  `workflows/control/resources/entry_ports.py`.
- Evidence: `workflows/persistence/test__WorkflowRunAtomicRepository.py`, nested-history
  tests, dispatch-entry tests, and Workflow public API.
- Target action: explicit inheritance, abstract `load`, `commit`, and `load_claim`,
  nominal checks, structural-lookalike rejection, and retired-name absence.

## Exact current symbol-use audit

The following list records every current non-declaration Python file in which the
retired symbol occurs as an AST name or attribute, rather than only in prose. The
implementation run must rename or remove each use. Structural implementers that do not
currently name their Protocol are listed in the sections above and must gain explicit
inheritance.

| Retired symbol | Maintained source direct uses | Test direct uses |
|---|---|---|
| `PlaneWaveCalculator` | `integration/quantum_espresso/simulation.py`; `integration/quantum_espresso/tasks.py` | `calculators/test__PlaneWaveCalculator.py`; `integration/quantum_espresso/test__QuantumEspressoSimulation.py` |
| `UniformGrid1DRepresentation` | `operators/finite_differences.py` | `operators/test__UniformGrid1DRepresentation.py` |
| `DirichletBoundaryConditionRepresentation` | `operators/finite_differences.py` | `operators/test__DirichletBoundaryConditionRepresentation.py` |
| `DirichletIntervalRepresentation` | `operators/finite_differences.py` | `operators/test__DirichletIntervalRepresentation.py` |
| `AtomicRevisionStore` | `workflows/persistence.py` | `persistence/test__SQLiteAtomicRevisionStore.py`; `persistence/test__store_contract.py`; `workflows/persistence/test__WorkflowRunAtomicRepository.py`; `test__WorkflowRunAtomicRepository__nested_history.py` |
| `SimulationDispatchEntryCommitter` | `workflows/control/dispatch.py` | No direct name use; the structural recording double above must gain nominal inheritance. |
| `SimulationDispatchEffect` | `integration/quantum_espresso/simulation.py`; `workflows/control/dispatch.py` | `integration/quantum_espresso/test__LocalQuantumEspressoExecutor.py`; `test__QuantumEspressoSimulation.py`; `workflows/control/test__SimulationDispatchEffect.py` |
| `ResultObject` | `analysis/result_values.py`; `application/result_values.py`; `integration/quantum_espresso/result_values.py`; `integration/quantum_espresso/tasks.py`; `workflows/engine.py`; `workflows/model.py`; `workflows/observations.py`; `workflows/persistence.py`; `workflows/runs/records.py` | `integration/quantum_espresso/test__QuantumEspressoObservationAdapter.py`; `test__quantum_espresso_execution_contract.py`; `workflows/model/test__AbstractScientificTask.py`; `test__AbstractSimulationTask.py`; `test__AbstractTask.py`; `test__NestedWorkflowTask.py`; `test__ResultObject.py`; `test__WorkflowExecutionPlan.py`; `test__WorkflowTaskBinding.py`; `workflows/persistence/test__WorkflowRunSerializer.py`; `test__WorkflowRunSerializer__codec_failures.py`; `test__WorkflowRunSerializer__results.py`; `workflows/test__NormalizedObservationAssembler.py`; `test__WorkflowEngine.py` |
| `ObservationCorrelationIdentity` | `workflows/observations.py` | `workflows/test__NormalizedObservationAssembler.py` |
| `ObservationNormalizationPolicySource` | `workflows/observations.py` | `workflows/test__NormalizedObservationAssembler.py` |
| `NormalizedObservationSource` | `workflows/observations.py`; `workflows/persistence.py` | `workflows/test__NormalizedObservationAssembler.py` |
| `WorkflowResultValueCodec` | `workflows/persistence.py` | `analysis/test__QuantityOfInterestResultValueSerializer.py`; `application/test__ApplicationResultValueSerializer.py`; `integration/quantum_espresso/test__QuantumEspressoResultValueSerializer.py`; `workflows/persistence/test__WorkflowResultValueSerializer.py` |
| `WorkflowRunRepository` | `workflows/control/dispatch.py` | `workflows/persistence/test__WorkflowRunAtomicRepository.py` |

All paths in this table are relative to `python/src/ksdft2effmass/` or
`python/tests/software_verification/ksdft2effmass/` as applicable. Public re-export
uses are separately exhaustive in the next table because import aliases and `__all__`
strings are not ordinary AST name expressions.

## Export replacement matrix

| Owning public module | Retired exports | Target exports |
|---|---|---|
| `ksdft2effmass.calculators.dft.pw` | `PlaneWaveCalculator` | `AbstractPlaneWaveCalculator` |
| `ksdft2effmass.operators` | `UniformGrid1DRepresentation`, `DirichletBoundaryConditionRepresentation`, `DirichletIntervalRepresentation` | Corresponding three `Abstract...` names |
| `ksdft2effmass.persistence` | `AtomicRevisionStore` | `AbstractAtomicRevisionStore` |
| `ksdft2effmass.workflows.control` | `SimulationDispatchEntryCommitter`, `SimulationDispatchEffect` | Corresponding two `Abstract...` names |
| `ksdft2effmass.workflows` | Both dispatch names plus `ResultObject`, three observation names, `WorkflowResultValueCodec`, and `WorkflowRunRepository` | Corresponding eight `Abstract...` names |

Implementation is incomplete if any retired name remains importable, in `__all__`, in
public documentation, or accepted as a compatibility alias.

## Pre-implementation audit commands

Before mutation, rerun exact symbol searches for every retired name across
`python/src`, `python/tests`, and Sphinx API pages. After mutation, require:

- no `typing.Protocol` or `runtime_checkable` import left solely for these contracts;
- no retired export or annotation;
- every positive symbol above inheriting the exact ABC;
- every negative lookalike remaining non-nominal and rejected; and
- no newly discovered positive structural implementation absent from this inventory.
