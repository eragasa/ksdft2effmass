back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 01: Shared Foundation

## Objective

Define the physical scope, numerical conventions, persistent data structures, validation metrics, and regression tests used by every downstream calculation.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.01.01.01|01.01.01]] | Freeze the physical reference specification | None | `PhysicalSpecification-v1` | Ready |
| [[ksdft2Effmass.computational.01.01.02|01.01.02]] | Freeze numerical conventions and software stack | `01.01.01` | `NumericalSpecification-v1` | Blocked |
| [[ksdft2Effmass.computational.01.02.01|01.02.01]] | Implement the operator-record schema | `01.01.01` | Tested `OperatorRecord` | Blocked |
| [[ksdft2Effmass.computational.01.02.02|01.02.02]] | Implement run manifests and provenance capture | `01.01.02` | Tested `RunManifest` | Blocked |
| [[ksdft2Effmass.computational.01.03.01|01.03.01]] | Implement common operator, subspace, spectral, and observable metrics | `01.02.01` | Metrics library | Blocked |
| [[ksdft2Effmass.computational.01.03.02|01.03.02]] | Construct synthetic regression benchmarks | `01.02.01`, `01.03.01` | Passing regression suite | Blocked |

## Work Packages

### `01.01`: Reference conventions

This package fixes the physical and numerical meaning of every parent calculation. It must distinguish physical choices from discretization choices.

### `01.02`: Persistent computational objects

This package defines how operators, bases, geometries, energy references, projectors, gauges, and provenance are stored.

### `01.03`: Validation infrastructure

This package implements the metrics in [[ksdft2Effmass.08]] and verifies them against controlled matrices with known answers.

## Completion Gate `G01`

Stage `01` passes only when all six tasks pass and a complete synthetic workflow can:

1. construct two related finite-dimensional Hamiltonians;
2. align them on a common state space;
3. form an operator difference;
4. compute the prescribed error vector;
5. reproduce the calculation from stored manifests.

## Parallelization

After `01.01.01`, the operator schema and numerical specification can be developed in parallel. Metric implementation begins as soon as the operator schema stabilizes.
