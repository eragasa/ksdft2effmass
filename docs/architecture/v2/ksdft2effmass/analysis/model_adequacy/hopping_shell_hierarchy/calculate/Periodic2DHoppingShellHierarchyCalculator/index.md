# `Periodic2DHoppingShellHierarchyCalculator`

## Purpose and status

Prospective stateless ActionObject for HSH-1. It is not implemented or supported.

## Public contract

`execute(definition)` maps one exact
`Periodic2DHoppingShellHierarchyDefinition` to one
`Periodic2DHoppingShellHierarchyResult`. The method has no file-system, external-
calculator, scheduler, network, or mutable-global side effects.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellHierarchyCalculator`.

## State and identity

The calculator has no maintained instance state. Algorithm identity and dependency
versions belong to result provenance; all scientific controls belong to the definition.

## Invariants and failure behavior

The action returns only a fully correlated result. Invalid top-level source projection,
orbit inventory, definition, or nesting raises a stable execution failure. A named
class-local quadratic or certificate premise failure may be retained as
`invalid-premise`, with no distance or hierarchy claim. Valid but inconclusive nonempty
geometry emits `unresolved-nonempty`.

## Dependencies and collaborators

The calculator consumes `definition`, constructs HSH objects from `results`, composes
exact-pinned
`projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss`, and may
use `periodic2d` parent/model primitives plus public PhysKit and Optimization Actions.
The definition selects and retains dense/sparse quadratic backend use. The calculator
neither calls the result verifier nor delegates semantic validation to serialization.
Existing M4/M5 scaffolds are not collaborators.

## Data and action flow

See [implementation](../../implementation.md) for the twelve-stage producer flow and
[schematic](../../schematic.md) for the training/withheld barrier.

## Serialization and compatibility

The ActionObject returns typed results only. It does not know output paths or manifests.
Algorithm changes that can alter proof objects or dispositions require a versioned
schema/provenance change and renewed freeze.

## Scientific and numerical boundary

The action evaluates one finite synthetic hierarchy. An optimizer supplies candidates;
compatibility and separation require reconstructed proof objects. No material or
infinite-lattice claim follows.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/calculate.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.calculate.Periodic2DHoppingShellHierarchyCalculator` | Pure producer ActionObject |
| same | Method | `...Periodic2DHoppingShellHierarchyCalculator.execute` | Definition-to-result transformation |

## Test mapping

Planned software/numerical class:
`TestPeriodic2DHoppingShellHierarchyCalculator`. Intended tests cover source projection,
orbits, quadratics, bounded minima, empty sets, witnesses, feasible pairs, support
certificates, nesting, hierarchy resolution, and withheld role separation. No test
exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | ActionObject absent | None |
| Numerical verification | Not evaluated | No execution or oracle | None |
| Scientific validation | Not evaluated | Synthetic parent | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | None |
| Human acceptance | Not evaluated | No accepted run | None |

## Limitations and deviations

The public semantic stage-Action split, convex solver, and interval backend are
unresolved. They must be selected explicitly before HSH source implementation; the
aggregate calculator cannot hide scientific formulas in private workflow helpers.

## Detail navigation

- [Implementation plan](../../implementation.md)
- [Scientific model](../../scientific.md)
- [Numerical contract](../../numeric.md)
- [Testing plan](../../testing.md)
