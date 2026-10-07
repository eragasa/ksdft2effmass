# `ksdft2effmass.periodic2d.compare.common_space`

## Purpose and status

This implemented module owns `PERIODIC-XWALK-036`: explicit directional alignment and
threshold-free disagreement between the dimensionless cosine Hamiltonian's finite
plane-wave and finite-difference representations.

## Public contract inventory

| Symbol | Role | Supported route |
|---|---|---|
| `Periodic2DCommonSpaceComparisonRequest` | Immutable comparison RequestObject | `ksdft2effmass.periodic2d` and `ksdft2effmass.periodic2d.compare` |
| `Periodic2DCommonSpaceComparisonResult` | Immutable comparison ResultObject | `ksdft2effmass.periodic2d` and `ksdft2effmass.periodic2d.compare` |
| `Periodic2DCommonSpaceOperatorComparator` | Stateless comparison ActionObject | `ksdft2effmass.periodic2d` and `ksdft2effmass.periodic2d.compare` |

## Represented objects and state spaces

The source finite-difference matrix acts on the Euclidean coordinate-site space
`C**(N**2)` in `x_outer_y_inner` order. The plane-wave matrix acts on
`C**((2*M+1)**2)` in `p_outer_q_inner` order. The map `T` sends ordered plane-wave
coefficients to grid samples. It is proper rectangular when `N>2*M+1` and square
unitary at the allowed equality boundary. The transported matrix and signed difference
act in the plane-wave common space; the Result is comparison evidence, not another
represented operator.

## Invariants, units, conventions, and failure behavior

The request requires the exact cosine adapter result types, equal configured parent and
Bloch momentum, a nonempty identity, and `2*M+1 <= N`. Exact adapters fix period
`2*pi`, scalar spin, dimensionless energy and zero, basis normalization, order, and seam
orientation.

The Result requires immutable unitless complex128 matrices of directional shapes,
validates `H_fd_tilde = T.conj().T @ H_fd @ T`, validates
`Delta_H = H_fd_tilde - H_pw`, and recomputes all diagnostics. Wrong types raise
`TypeError`; incompatible identities, shapes, units, or algebra raise `ValueError`;
unrepresentable finite arithmetic raises `OverflowError`. Dense allocation may raise
`MemoryError`.

No diagnostic is compared with a pass/fail tolerance.

## Dependency and neighboring-owner rules

The module composes quantity records from `ksdft2effmass.operators` and exact adapter
results from `periodic2d.model.toy_models`. It must not own lattice primitives,
represented-matrix assembly, eigensolves, retained spaces, convergence assessment,
serialization, or campaign execution.

## Class navigation

- [`Periodic2DCommonSpaceComparisonRequest`](Periodic2DCommonSpaceComparisonRequest/index.md)
- [`Periodic2DCommonSpaceComparisonResult`](Periodic2DCommonSpaceComparisonResult/index.md)
- [`Periodic2DCommonSpaceOperatorComparator`](Periodic2DCommonSpaceOperatorComparator/index.md)

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Module | `ksdft2effmass.periodic2d.compare.common_space` | Compatibility, transport, comparison, and intrinsic Result algebra |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonRequest.py` | `TestPeriodic2DCommonSpaceComparisonRequest` | Software verification | Parent/fiber/alias prerequisites |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonResult.py` | `TestPeriodic2DCommonSpaceComparisonResult` | Software verification | Directional shapes, immutability, transport, subtraction, and diagnostics |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator__execute.py` | `TestPeriodic2DCommonSpaceOperatorComparatorExecute` | Software verification | Fail-closed transport range behavior |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator.py` | `TestPeriodic2DCommonSpaceOperatorComparator` | Numerical verification | Independent finite-grid dispersion oracle |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/common_space.rst` | `ksdft2effmass.periodic2d` | Canonical API, equations, evidence, references, and limitations |
| `doc/sphinx/concepts/periodic2d-controlled-reduction.rst` | Conceptual workflow | Common-space placement within controlled reduction |

## Provenance

Original local work under the repository license. Authoritative mathematics and claim
boundaries are in
`specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Exact contract and mutation evidence | Mapped software modules | Exact equality and exception matching | Python/NumPy | Declared synthetic fixtures | Not applicable |
| Numerical verification | Supported | Two-sided square-map unitarity and independent discrete-dispersion equations | Mapped numerical module | Absolute `4e-15`/`6e-15` | complex128/binary64 | `M=2,N=5` boundary plus small free/cosine cases | Not applicable |
| Scientific validation | Not evaluated | No physical adequacy protocol | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Separate decision required | Decision record when available | Not applicable | Not applicable | Row 036 | Named human authority required |

## Limitations and deviations

The sampling map is dense and specialized to one exact adapter family. Manual Result
construction can establish intrinsic algebra but cannot establish that the Action ran.
The module does not supply sparse transport, arbitrary lattice geometry, convergence,
or scientific acceptance.
