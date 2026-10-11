# `ksdft2effmass.periodic1d.multiband_alignment`

## Purpose and status

This package owns M2, the implemented rank-two multiband alignment and locality
calculation. M2 separates invariant spectral/projector comparisons from represented
matrix comparisons that require a frame. It further separates exact pointwise
Procrustes recovery from a finite one-global-unitary family.

## Public contract

| Module | Public responsibility |
|---|---|
| [`definition`](definition/index.md) | Immutable parent, attack, frame, range, mesh, and tolerance controls |
| [`calculate`](calculate/index.md) | Deterministic frame/alignment/locality producer Action |
| [`results`](results/index.md) | Immutable diagnostics, range channels, and aggregate result |
| [`serialization`](serialization/index.md) | Canonical M2 schema-v1 JSON encoding |
| [`verify`](verify/index.md) | Independent reconstruction of frames, transforms, and diagnostics |

Cross-cutting documentation:

- [scientific boundary](scientific.md);
- [calculation schematic](schematic.md);
- [numerical contract](numeric.md);
- [implementation mapping](implementation.md); and
- [testing and evidence](testing.md).

## Ownership boundary

M2 owns the frozen rank-two attack family, frame-channel distinctions, global alignment
constraint, gauge-resolved hopping transforms, locality ranges, and training/evaluation
roles. Lower-level frame transport, Procrustes alignment, Fourier transformation, and
hopping interpolation remain with their reusable domain owners.

M2 does not own a general momentum-dependent gauge optimizer, material validation,
Wannier90 execution, or scientific acceptance.

## Dependency rules

The calculation may compose `solid_state` frame and hopping Actions. The verifier must
not invoke the producer. The serializer must not derive scientific values. M3 may
compose an exact M2 definition/result; M2 must not depend on M3.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/__init__.py` | Package | `ksdft2effmass.periodic1d.multiband_alignment` | Public exports |
| `.../definition.py` | Module | `...multiband_alignment.definition` | Frozen M2 definition |
| `.../calculate.py` | Module | `...multiband_alignment.calculate` | Producer Action |
| `.../results.py` | Module | `...multiband_alignment.results` | Result objects |
| `.../serialization.py` | Module | `...multiband_alignment.serialization` | Wire format |
| `.../verify.py` | Module | `...multiband_alignment.verify` | Independent reconstruction |

## Test and Sphinx mapping

The direct test owner is
`python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DMultibandAlignmentCalculator.py::TestPeriodic1DMultibandAlignmentCalculator`.
The user-facing page is
`doc/sphinx/api/ksdft2effmass/periodic1d/multiband_alignment.rst`.

## Provenance

Original local work under the repository license. The retained package is
`calculations/ICMSEP2026/conference/paper_1/multiband-alignment/`.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Supported | Typed construction, deterministic encoding, strict tamper tests | M2 API and retained input |
| Numerical verification | Supported | Independent frame/operator/hopping reconstruction | Frozen finite rank-two protocol |
| Scientific validation | Not evaluated | Synthetic toy parent only | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | None |
| Human acceptance | Not applicable | No acceptance decision encoded | None |

## Limitations and deviations

The attack is constructed, the retained group has rank two, and the constrained family
contains one global unitary. Exact pointwise recovery is not evidence that a finite
one-global-unitary family preserves locality, and failure of that family is not proof
against arbitrary momentum-dependent alignment.
