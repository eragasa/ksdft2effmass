# Isotropic 2-D implementation architecture

## Planned package

Concrete HSH composition will use the Architecture v3 calculation lifecycle, while
reusable behavior lives with reviewed installed source owners.

- Maintained calculation root: `calculations/periodic2d/rank1/hopping-shell-hierarchy/`.
- Architecture: `docs/architecture/v2/experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/`.
- Task: `docs/tasks/dev/experiments/isotropic2d/`.
- The design root currently contains the maintained protocol, exact orbit/support inventory, and [pre-canonical execution-structure donor](../../../../../../../calculations/periodic2d/rank1/hopping-shell-hierarchy/execution-structure.md).
- Source is not implemented. Its cohesive installed owner and concrete types must be selected before implementation; the calculation root will not host a second installable `src/` package.

## Planned responsibilities

The future package follows the maintained periodic-1D experiment execution graph.

- `definition.py` owns `HoppingShellHierarchyDefinition` and every outcome-relevant scientific control.
- `experiment.py` owns the in-process `HoppingShellHierarchyExperiment.execute(definition)` Action without file I/O.
- `results.py` owns immutable parent, class, hierarchy, evidence, and disposition records.
- `verify.py` owns `HoppingShellHierarchyResultVerifier`, which reconstructs decisive mathematics without calling or importing the producer Action.
- `serialization.py` owns strict canonical input, result, and verification wire mechanics without scientific behavior.
- Calculation entry points remain thin effect adapters around these typed objects and live in the maintained calculation root; reusable behavior remains in installed owner source.

## Dependency ownership

The experiment composes reviewed owners without duplicating their generic behavior.

- PhysKit owns reusable lattice, hopping, Bloch, unit, and supplied-operation diagnostic semantics.
- Numerics owns reusable finite Fourier arithmetic, finite-operation orbit enumeration, and conservative arithmetic through reviewed contracts.
- Optimization owns unit-free quadratic minimization, feasibility, support, and strict-separation mathematics through capability-specific reviewed contracts; arbitrary-dimensional closed-box quadratic minimization is reviewed and bound, while feasibility and strict-separation capabilities remain open.
- The experiment consumes matching owner contracts directly and does not add a pass-through solver facade.
- The experiment owns the exact square-symmetry operation/domain/order binding, channel construction, thresholds, hierarchy policy, evidence, and interpretation.

## Architecture migration

The legacy installed-package design bundle remains a source of reviewed requirements but
must not be implemented at its old path.

- Reconcile every legacy class with experiment ownership.
- Create mirrored module architecture only when a source module is selected.
- Create detailed `ClassName` science and numerics pages at the implementing class.
- Remove or supersede false public-package mappings only after all inbound links are migrated.

## Verification and evidence

No implementation or retained evidence currently exists.

- Direct tests must cover symmetry, ordering, quadratics, certificates, schemas, and role isolation.
- Independent tests must use analytic or higher-precision oracles where applicable.
- Passing tests will establish bounded software behavior only.
- Retained execution remains separately gated.
