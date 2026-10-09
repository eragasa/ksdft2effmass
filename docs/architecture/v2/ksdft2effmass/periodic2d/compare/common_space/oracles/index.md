# Row-036 numerical-oracle dossiers

## Purpose and status

These pages document the three claim-bearing analytic oracles consumed by the bounded
`Periodic2DCommonSpaceOperatorComparator` numerical tests. Each oracle has a proposed
genesis `QUALIFIED` disposition under the repository
[numerical-oracle qualification standard](../../../../../documentation/numerical-oracle-qualification.md).
Machine-readable v1 records, local schemas, an artifact-owned independent
qualification-test module, exact consumer bindings, and reviewed-revision dispositions
are implemented in test infrastructure. Qualification and consumer-evidence status are
effective only if the exact disposition-and-status proposal commit passes its acceptance
gate.

The dossiers are deliberately separate because the claims are different:

1. sampling-map orthogonality concerns basis-column inner products;
2. centered-difference dispersion concerns the grid kinetic stencil on one sampled
   Bloch mode; and
3. resolved cosine Fourier transfer concerns pointwise potential sampling and the
   absence of transfer aliasing in one bounded cutoff/grid domain.

A derivation of one claim may use the same finite Fourier identity as another, but that
does not merge their validity domains, comparators, tolerances, or exclusions.

## Qualified inventory

| Oracle ID | Bounded claim | Current consumer | Technical status |
|---|---|---|---|
| [`periodic2d.common-space.dft-orthogonality.v1`](dft-orthogonality-v1.md) | Normalized period-$2\pi$ sampled plane-wave columns are orthonormal in the fixed $M=2,N=5$, $M=1,N=5$, and $M=1,N=7$ domains; only the square map is two-sided unitary | Square-map equality-boundary test plus free/cosine isometry diagnostics | Qualified after exact proposal acceptance |
| [`periodic2d.common-space.centered-difference-dispersion.v1`](centered-difference-dispersion-v1.md) | The directed-seam centered negative Laplacian has the declared discrete Bloch-mode eigenvalue in the fixed free/cosine test cases | Free and cosine comparator tests | Qualified after exact proposal acceptance |
| [`periodic2d.common-space.resolved-cosine-fourier-transfer.v1`](resolved-cosine-fourier-transfer-v1.md) | For the declared $M=1,N=7$ cosine case, compressed sampled potential blocks equal the parent Fourier coefficients without unintended retained-transfer aliasing | Cosine comparator test | Qualified after exact proposal acceptance |

## Shared representation boundary

All three qualified oracles concern the same dimensionless spinless scalar period-$2\pi$
parent and one exact Bloch fiber. The plane-wave basis is ordered with $p$ outer and
$q$ inner; the Euclidean coordinate-site basis is ordered with $x$ outer and $y$ inner.
The sampling map goes from plane-wave coefficients to grid samples. The model energy
unit is dimensionless reciprocal kinetic energy and the energy zero is parent-owned.
No frame, retained physical subspace, downfolding, material identity, or external
calculation provenance is involved.

The shared use of complex128/NumPy arithmetic is an explicit numerical dependency, not
scientific authority. Each dossier narrows this boundary further.

## Implemented qualification ownership

The qualification implementation uses explicit artifact-owned test modules and the bounded
resource files below. It introduces no generic oracle engine, factory, plugin,
registry, discovery mechanism, or production evaluator.

| Resource | Ownership |
|---|---|
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/resources/oracle-qualification-record-v1.schema.json` | Local Draft 2020-12 schema with a non-network `urn:ksdft2effmass:...` identifier |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/resources/*.oracle.json` | Three separately versioned semantic records |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/resources/oracle-qualification-disposition-ledger-v1.schema.json` | Append-only lifecycle schema |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/resources/oracle-qualification-dispositions-v1.json` | Three append-only genesis `QUALIFIED` decisions bound to reviewed revision `f37e5d722f8c9007d8ea55c06e808c9c73bf775d` |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_qualification.py` | Independent artifact-owned finite-algebra evidence |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_records.py` | Bounded schema, path, node, independence, lifecycle-structure, record-digest, and reviewed-revision validation for candidate and disposition states |

The qualification test does not import or invoke
`Periodic2DCommonSpaceOperatorComparator`, production model constructors, or private
production kernels. The structural test names exactly three record paths and performs
no ambient discovery. A qualification-record and test pass do not by themselves make an
oracle `QUALIFIED`; the recorded reviewed-revision disposition becomes effective only
through the exact proposal acceptance gate.

## Candidate gate

Run the bounded candidate gate from `python/`:

```bash
uv run --frozen pytest -q \
  tests/software_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_records.py \
  tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_qualification.py \
  tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator.py
```

At the candidate revision, the gate requires the disposition ledger to remain empty.
The shared structural validator also accepts later schema-valid disposition chains and
checks their record digests and review-revision bindings. Freezing that validator in the
candidate revision lets the proposal alter only the ledger and status documentation.
The command above verifies candidate implementation only and cannot by itself serve as
the later acceptance gate.

## Evidence status

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Not applicable | These dossiers describe expected numerical relations rather than a production software contract | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Numerical verification | Supported after exact proposal acceptance | Three reviewed-revision genesis `QUALIFIED` dispositions bind the fixed records, qualification tests, and consumers | Linked dossiers, machine-readable records, qualification tests, disposition ledger, and consumers | Dossier-specific absolute tolerances | complex128/binary64 | Fixed domains in each dossier | Not applicable |
| Scientific validation | Not evaluated | No material, experimental, or converged physical reference | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model or propagation | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Technical qualification and scientific acceptance remain separate | Separate scientific decision record if ever created | Not applicable | Not applicable | Qualified-oracle use | Named human authority required |

## Navigation

- [Common-space module](../index.md)
- [Comparator verification strategy](../Periodic2DCommonSpaceOperatorComparator/implementation/testing/index.md)
- [Comparator mathematics](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
- [Project oracle-qualification standard](../../../../../documentation/numerical-oracle-qualification.md)
