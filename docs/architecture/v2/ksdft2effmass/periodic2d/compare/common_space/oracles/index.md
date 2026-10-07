# Row-036 numerical-oracle dossiers

## Purpose and status

These pages document the three claim-bearing analytic oracles consumed by the bounded
`Periodic2DCommonSpaceOperatorComparator` numerical tests. Each oracle remains a
**Candidate** under the repository
[numerical-oracle qualification standard](../../../../../documentation/numerical-oracle-qualification.md).
No machine-readable v1 record, independent qualification-test owner, technical
disposition, or acceptance-gate result exists yet.

The dossiers are deliberately separate because the claims are different:

1. sampling-map orthogonality concerns basis-column inner products;
2. centered-difference dispersion concerns the grid kinetic stencil on one sampled
   Bloch mode; and
3. resolved cosine Fourier transfer concerns pointwise potential sampling and the
   absence of transfer aliasing in one bounded cutoff/grid domain.

A derivation of one claim may use the same finite Fourier identity as another, but that
does not merge their validity domains, comparators, tolerances, or exclusions.

## Candidate inventory

| Candidate oracle ID | Bounded claim | Current consumer | Technical status |
|---|---|---|---|
| [`periodic2d.common-space.dft-orthogonality.v1`](dft-orthogonality-v1.md) | Normalized period-$2\pi$ sampled plane-wave columns are orthonormal when their reciprocal indices are distinct modulo $N$; the square $M=2,N=5$ map is unitary | Square-map equality-boundary test | Candidate; consumer provisional |
| [`periodic2d.common-space.centered-difference-dispersion.v1`](centered-difference-dispersion-v1.md) | The directed-seam centered negative Laplacian has the declared discrete Bloch-mode eigenvalue in the fixed free/cosine test cases | Free and cosine comparator tests | Candidate; consumers provisional |
| [`periodic2d.common-space.resolved-cosine-fourier-transfer.v1`](resolved-cosine-fourier-transfer-v1.md) | For the declared $M=1,N=7$ cosine case, compressed sampled potential blocks equal the parent Fourier coefficients without unintended retained-transfer aliasing | Cosine comparator test | Candidate; consumer provisional |

## Shared representation boundary

All three candidates concern the same dimensionless spinless scalar period-$2\pi$
parent and one exact Bloch fiber. The plane-wave basis is ordered with $p$ outer and
$q$ inner; the Euclidean coordinate-site basis is ordered with $x$ outer and $y$ inner.
The sampling map goes from plane-wave coefficients to grid samples. The model energy
unit is dimensionless reciprocal kinetic energy and the energy zero is parent-owned.
No frame, retained physical subspace, downfolding, material identity, or external
calculation provenance is involved.

The shared use of complex128/NumPy arithmetic is an explicit numerical dependency, not
scientific authority. Each dossier narrows this boundary further.

## Planned qualification ownership

The candidate implementation will use explicit artifact-owned test modules and bounded
resource files beside the current numerical consumers. It will not introduce a generic
oracle engine, factory, plugin, registry, discovery mechanism, or production evaluator.
Qualification tests will not import or invoke
`Periodic2DCommonSpaceOperatorComparator` or copy its private sampling-map kernel.

The three candidates will receive separate record identities even if one artifact-owned
qualification module checks their related finite-Fourier derivations. A qualification
record and test pass will not by themselves make the candidate `Qualified`; the later
reviewed-revision disposition and acceptance gate remain required.

## Evidence status

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Not applicable | These dossiers describe expected numerical relations rather than a production software contract | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Numerical verification | Not evaluated | Three candidate analytic oracles are documented, but qualification and acceptance are not implemented | Linked dossiers and provisional consumers | Candidate-specific, not yet accepted | complex128/binary64 | Fixed domains in each dossier | Not applicable |
| Scientific validation | Not evaluated | No material, experimental, or converged physical reference | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model or propagation | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Technical qualification and scientific acceptance remain separate | Future decision record | Not applicable | Not applicable | Candidate oracle adoption | Named human authority required |

## Navigation

- [Common-space module](../index.md)
- [Comparator verification strategy](../Periodic2DCommonSpaceOperatorComparator/implementation/testing/index.md)
- [Comparator mathematics](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
- [Project oracle-qualification standard](../../../../../documentation/numerical-oracle-qualification.md)
