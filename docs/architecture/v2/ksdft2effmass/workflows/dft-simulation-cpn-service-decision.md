# DFT simulation CPN service decision

## Status

Selected for bounded internal implementation on 2026-09-02. The human selected
option B after review of the paired Quantum ESPRESSO 7.5 and ABINIT 10.8.3
silicon SCF-to-bands observations.

This decision authorizes no scientific executable invocation, dependency change,
external computation, retry, scientific-setting change, numerical comparison,
validation, or release. The resulting Python surfaces remain private and
revisable; this page does not accept a stable public API or wire format.

## Context

The retained paired tutorial exposes one shared logical dependency:

```text
SCF input -> self-consistent native state -> fixed-density-bands input -> bands result
```

Its native realizations differ. QE used separate `pw.x` SCF and bands processes,
then a `bands.x` postprocessor. ABINIT represented SCF and bands as two datasets
inside one process. Both realizations produce an explicit native density role,
but a process, dataset, native file, logical scientific stage, and CPN transition
are not interchangeable concepts.

The existing generic colored-Petri-net kernel is immutable and effect-free. The
Workflow adapter owns mapping between workflow values and generic CPN values;
the CPN kernel owns no Task execution, calculator policy, persistence, scheduling,
or scientific acceptance. The first cross-backend slice must preserve those
boundaries rather than introducing a calculator registry or moving effects into
the net.

Current retained results are sufficient to exercise logical replay and
fail-closed incompatibility reporting. They are insufficient for numerical
QE--ABINIT comparison because the pseudopotentials, cutoffs, lattice constants,
path discretizations, coordinate conventions, energy alignment, and convergence
semantics are not aligned. The complete spectra also remain external to the
committed compact observations.

## Alternatives considered

### Option A: collect more workflow evidence before implementation

Continue executing targeted tutorials and defer all simulation types, CPN
composition, normalization, and comparison code. This minimizes early code but
leaves existing concrete findings unexercised as software contracts and delays
feedback on object ownership.

### Option B: implement one thin internal vertical slice

Introduce closed calculator-specific SCF and fixed-density-bands input/output
unions, a narrow injected `DftCalculator` execution port, effect-free Workflow-
owned CPN replay of already-existing results, backend-specific retained-result
adaptation, and specification-owned fail-closed comparison. Exercise the slice
against the current paired observations before adding execution services.

### Option C: build a durable Airflow-like CPN service now

Introduce durable scheduling, persistence, remote workers, retries,
cancellation, service APIs, and deployment contracts before the scientific
operation and result boundaries have survived multiple workflows. This offers
early operational breadth but would stabilize speculative contracts and
duplicate decisions that the targeted slices are intended to discover.

## Decision

Select **option B**.

The first implementation is synchronous and effect-free. It imports retained
results and replays logical dependency state through the existing generic CPN
kernel. It does not invoke the `DftCalculator` protocol. Future effectful workflow
control may call an injected calculator only after the separately owned
workflow-control and executor-boundary authorization checks admit the exact
operation.

ABINIT's retained two-dataset invocation is imported as one native process
observation that supports two distinct logical result records. The prototype does
not fabricate a transition between effects that were atomic in the observed
native invocation. It does replay the dependency between the admitted logical SCF
result and admitted logical bands result. QE imports distinct process observations
for the two logical results. The same CPN topology therefore does not encode
process count.

## Ownership decomposition

| Surface | Ownership and role |
|---|---|
| Calculator-specific SCF and bands inputs | Immutable private calculator DataObjects; exact native input, pseudopotential, upstream-result, and native-state identities |
| Calculator-specific SCF and bands outputs | Immutable private calculator ResultObjects; input, process-observation, native-state, and represented-band-result identities only |
| `SimulationTypeInput` and `SimulationTypeOutput` | Closed private unions of concrete QE and ABINIT operation variants; no generic dictionary and no runtime registry |
| `DftCalculator[InputT, OutputT]` | Narrow private structural consumer port; protocol conformance grants no execution authority |
| SCF-to-bands CPN replay | Workflow-owned ActionObject using the existing effect-free generic CPN enabler, selector, and firer |
| Backend retained-result mapping | Concrete tutorial adapter; it preserves observed process fusion/separation and supplies typed values without fabricating execution lineage |
| `BandStructureObservation` | Periodic-owned immutable calculator-neutral represented observation after backend-specific normalization; missing complete arrays and missing alignment identities remain explicit |
| `BandComparisonSpecification` | Analysis-owned explicit system, path, band-count, grid, pseudopotential-alignment, energy-alignment, unit, and tolerance policy |
| `BandStructureComparator` | Analysis-owned cross-object ActionObject; compares only complete admitted observations and otherwise returns structured rejection |
| `BandStructureComparisonResult` | Analysis-owned immutable result separating logical workflow-shape compatibility from numerical-comparison admission and tolerance outcome |

The generic `ksdft2effmass.petrinet.colored` package remains calculator-neutral and
effect-free. The Workflow replay imports neither calculators nor concrete QE or
ABINIT integrations; it consumes already-adapted identity correlations. Calculator
records import only the generic Workflow context they structurally consume. Tutorial
adaptation may import both private calculator and workflow contracts because it is the
bounded composition consumer.

## Initial vertical slice

The internal slice has this flow:

```text
committed QE observation ----> QE typed logical results ----> QE CPN replay --+
                                                                            |
committed ABINIT observation -> ABINIT typed logical results -> ABINIT replay +
                                                                            |
backend normalization -> BandStructureObservation pair ----------------------+-->
explicit BandComparisonSpecification -> BandStructureComparator -> result
```

The retained pair must produce these exact high-level outcomes:

- both backends replay `dft.scf` followed by
  `dft.fixed-density-bands` through the same CPN definition;
- QE's logical stages retain distinct process-observation identities;
- ABINIT's logical stages retain one shared process-observation identity;
- the shared system, SCF-to-bands dependency, path topology, and eight-band role
  are structurally compatible; and
- numerical comparison is rejected with explicit findings rather than coerced
  values.

The current rejection includes different point counts and coordinate
conventions, no common comparison-grid identity, different lattice parameters
and cutoffs under zero prototype tolerances, no pseudopotential-alignment
identity, no energy-alignment identity, and no committed complete spectrum
arrays. The rejection is expected software behavior, not a failed scientific
validation.

## Consequences

The selected slice provides early executable feedback on type and ownership
boundaries without invoking scientific software. It keeps backend-native
continuation and process topology visible while giving Workflow control one
logical dependency model. It also makes unsupported numerical comparison a
first-class result.

The slice intentionally duplicates some concrete QE and ABINIT record shapes.
That duplication preserves variant-specific construction and prevents a
premature universal simulation envelope. Shared structure may be extracted only
after additional operations demonstrate a stable contract.

## Reusable stage-Task clarification

The human subsequently required SCF, NSCF, and DOS to be independent CPN
sub-Tasks for reuse. For this architecture, a CPN sub-Task means one
operation-specific, run-scoped `Task` instance selected and correlated by its own
CPN transition. It is not an anonymous stage inside a shell sequence and is not a
new primitive in the generic `petrinet.colored` package.

The DOS probe must therefore compose three reusable operation definitions:

```text
SCF Task --identified native-state result--> NSCF Task
NSCF Task --identified native-state result--> DOS Task
```

Each Task has its own exact input, activation, attempt, execution grant, isolated
workspace, process observation, immutable result, failure boundary, result ingress,
and CPN firing. The downstream Task consumes an admitted predecessor ResultObject
and an exact immutable native-state identity; it must not discover or mutate a
predecessor's working directory. A calculator integration may stage a copy of the
identified predecessor state into the downstream Task's private workspace.

Reuse means that other Workflows may instantiate the same SCF, NSCF, or DOS Task
definition with different exact inputs and predecessor results. It does not mean
that scientific settings, pseudopotentials, state files, or mutable `prefix` and
`outdir` directories are interchangeable. The Workflow is the genuine reusable
multi-step ActionObject; operation-specific DataObjects retain intrinsic fields,
operation-specific ResultObjects record outcomes, and cross-stage compatibility
remains an ActionObject or Workflow-control responsibility.

No public export is added from `ksdft2effmass.calculators`,
`ksdft2effmass.workflows`, `ksdft2effmass.periodic`, or
`ksdft2effmass.analysis`. The private
`ksdft2effmass.workflows._dft_scf_nscf_dos` slice now composes three distinct
run-scoped Task instances, stable operation-definition identities, explicit
Task-to-transition bindings, and read-only predecessor-result arcs. This is an
effect-free topology contract, not a calculator executor, dispatch, result ingress,
or scientific result. No schema, persistence
model, service endpoint, scheduler, asynchronous interface, plugin registry, or
automatic retry policy is selected.

## Required probes before service stabilization

Use further bounded vertical slices to test the contracts in this order:

1. SCF -> fixed-density bands with an actually aligned comparison grid and
   complete compact synthetic spectra, to exercise successful comparison without
   making a physical-validation claim;
2. SCF -> NSCF -> DOS, represented as three independent reusable CPN Task instances, to test additional operation variants, immutable native-state handoff, and normalization;
3. convergence fan-out/fan-in, to test collection and join semantics; and
4. QE -> Wannier90, to test multi-program native continuation and interface
   artifacts.

The first probe is implemented as a private numerical-verification case using two
complete `2 x 2` synthetic spectra on one explicit synthetic grid. Their exact
hand-derived maximum absolute difference is `0.25 Ha`; its bounded numerical result is
human-accepted and administratively closed. Passing establishes only the comparison
mechanics and inclusive synthetic tolerance boundary. It provides no physical
alignment or backend-agreement evidence. The second probe has its private reusable
three-Task CPN composition covered by software-verification evidence
`SV-DFT-SCF-NSCF-DOS-CPN-001`--`SV-DFT-SCF-NSCF-DOS-CPN-004`. Private QE NSCF
and DOS input/result variants are separately covered by
`SV-DFT-NSCF-DOS-001`--`SV-DFT-NSCF-DOS-006`. Checkpoint
`QE-SILICON-DOS-RUN-HC01` authorized one actual-data Workflow: all three independent
Task processes completed, exact immutable SCF-to-NSCF and NSCF-to-DOS state copies
were verified, and each admitted result received its own CPN firing. The compact
calculated observation retains a bounded finite DOS parse, but no general reusable DOS
normalization API or stable service contract is accepted. The final two probes remain
unimplemented.

Only after those probes should the project reconsider durable run persistence,
remote workers, scheduling, retries, cancellation, REST or other service APIs,
and stable public simulation contracts. Any protected execution still requires
its own exact preflight and authorization.
