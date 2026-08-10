back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 01: Shared Foundation

## Objective

Define the physical scope, numerical conventions, persistent data structures, validation metrics, and regression tests used by every downstream calculation.

## Task Registry

| Task                                               | Description                                                           | Prerequisites          | Output                      | Initial state |
| -------------------------------------------------- | --------------------------------------------------------------------- | ---------------------- | --------------------------- | ------------- |
| [[ksdft2Effmass.computational.01.01.01\|01.01.01]] | Freeze the physical reference specification                           | None                   | `PhysicalSpecification-v1`  | Passed        |
| [[ksdft2Effmass.computational.01.01.02\|01.01.02]] | Freeze numerical conventions and software stack                       | `01.01.01`             | `NumericalSpecification-v1` | Passed        |
| [[ksdft2Effmass.computational.01.02.01\|01.02.01]] | Implement the operator-record schema                                  | `01.01.01`             | Tested `OperatorRecord`     | Passed        |
| [[ksdft2Effmass.computational.01.02.02\|01.02.02]] | Implement run manifests and provenance capture                        | `01.01.02`             | Tested `RunManifest`        | Ready         |
| [[ksdft2Effmass.computational.01.03.01\|01.03.01]] | Implement common operator, subspace, spectral, and observable metrics | `01.02.01`             | Metrics library             | Ready         |
| [[ksdft2Effmass.computational.01.03.02\|01.03.02]] | Construct composed synthetic scientific workflow benchmarks          | `01.02.01`, `01.03.01` | Passing G01b regression suite | Blocked     |

## Work Packages

### `01.01`: Reference conventions

This package fixes the physical and numerical meaning of every parent calculation. It must distinguish physical choices from discretization choices.

### `01.02`: Persistent computational objects

This package defines how operators, bases, geometries, energy references, projectors, gauges, and provenance are stored.

### `01.03`: Validation infrastructure

This package implements the metrics in [[ksdft2Effmass.08]] and verifies them against controlled matrices with known answers.

## Prospective supersession of historical gate `G01`

The original unsplit `G01` definition and its evidence are retained as historical
records. Human architecture approval on 2026-08-03 prospectively supersedes that
gate with two noncircular gates.

### `G01a`: computational foundation

The `G01a` accepted marking exists only when the frozen specifications, accepted operator-record foundation, run manifests and artifact identities, common metrics needed by early calculations, backend-neutral Kohn–Sham contracts, QE mechanical rendering/parsing, semantic mapping, and synthetic command-execution infrastructure have each completed their own implementation, tests, documentation, independent review, parent verification, and human acceptance. The bounded control-plane Tasks A–F in
`harness/tasks/backend-neutral-kohn-sham-qe-architecture.json` provide the prospective
implementation sequence. Synthetic fixtures do not authorize a real QE run.

### `G01b`: composed synthetic scientific workflows

The `G01b` accepted marking exists only after the accepted operator-record foundation and required metrics support composed synthetic workflows that:

1. construct related finite-dimensional Hamiltonians;
2. perform an explicitly approved basis/state-space alignment;
3. form represented differences only after compatibility/alignment;
4. compute the prescribed error vector;
5. exercise composed reduction paths; and
6. reproduce the workflow from accepted manifests.

Task `01.03.02` contributes to `G01b`, not `G01a`. G02 depends on `G01a` and does
not wait for basis or gauge alignment. Alignment and later composed synthetic
end-to-end evidence may proceed after their own prerequisites and do not form a
prerequisite cycle with `G01a`. Static prerequisites are only a planning projection; the future workflow state is a multiset marking with explicit evidence, failure, retry, and blocked tokens.

## Parallelization

After `01.01.01`, the operator schema and numerical specification can be
developed in parallel. Metric implementation begins as soon as the operator
schema stabilizes. After Task A is accepted, the bounded provenance and QE
mechanical-I/O tasks may follow their recorded independent prerequisites; no
approval automatically launches them.
