# `ksdft2effmass.periodic1d.isolated_band`

## Purpose and status

This package owns M1, the implemented one-dimensional isolated-band controlled
calculation. M1 constructs parent spectra from a finite Fourier potential, extracts one
selected scalar band on a uniform reciprocal mesh, performs the complete discrete
Fourier transform, studies declared finite hopping ranges, and retains independent
training and staggered-evaluation diagnostics.

The word “isolated” is the route name. M1 does not independently prove a physical
external gap or localization theorem.

## Public contract

| Module | Public responsibility |
|---|---|
| [`definition`](definition/index.md) | Immutable model, sampling, range, unit, and tolerance controls |
| [`calculate`](calculate/index.md) | Deterministic in-process producer Action |
| [`results`](results/index.md) | Immutable convergence, range, and aggregate results |
| [`serialization`](serialization/index.md) | Canonical schema-v1 UTF-8 JSON encoding |
| [`verify`](verify/index.md) | Independent numerical reconstruction |

Scientific meaning, numerical details, and evidence are separated into:

- [scientific boundary](scientific.md);
- [calculation schematic](schematic.md);
- [numerical contract](numeric.md);
- [implementation mapping](implementation.md); and
- [testing and evidence](testing.md).

## Ownership boundary

M1 owns the finite protocol and its result correlations. It composes, rather than
reimplements, plane-wave and finite-difference parent constructors, Fourier/hopping
transforms, truncation, least-squares fitting, Hermiticity, Parseval, and band-shape
diagnostics. It owns no Wannier gauge, material acceptance policy, or external
execution.

## Dependency rules

`calculate` may depend on maintained `analysis`, `operators`, and `solid_state`
Actions. `verify` may reconstruct with lower-level numerical constructors but must not
invoke `Periodic1DIsolatedBandCalculator` or read the producer's retained output.
`serialization` owns wire mechanics only.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/isolated_band/__init__.py` | Package | `ksdft2effmass.periodic1d.isolated_band` | Public exports |
| `python/src/ksdft2effmass/periodic1d/isolated_band/definition.py` | Module | `...isolated_band.definition` | Frozen definition |
| `python/src/ksdft2effmass/periodic1d/isolated_band/calculate.py` | Module | `...isolated_band.calculate` | Producer Action |
| `python/src/ksdft2effmass/periodic1d/isolated_band/results.py` | Module | `...isolated_band.results` | Result records |
| `python/src/ksdft2effmass/periodic1d/isolated_band/serialization.py` | Module | `...isolated_band.serialization` | Schema-v1 serializer |
| `python/src/ksdft2effmass/periodic1d/isolated_band/verify.py` | Module | `...isolated_band.verify` | Independent verifier |

## Test and Sphinx mapping

The direct test owner is
`python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DIsolatedBandCalculator.py::TestPeriodic1DIsolatedBandCalculator`.
The user-facing API page is
`doc/sphinx/api/ksdft2effmass/periodic1d/isolated_band.rst`.

## Provenance

Original local work under the repository license. The retained M1 package is
`calculations/ICMSEP2026/conference/paper_1/isolated-band/`.

## Evidence

| Evidence kind | Status | Evidence or reason | Comparator/tolerance | Validity domain |
|---|---|---|---|---|
| Software verification | Supported | Typed construction, strict inputs, deterministic schema, tamper tests | Exact identities and declared tolerances | M1 API and retained input |
| Numerical verification | Supported | Independent spectra/Fourier/range reconstruction | Retained maximum defects below `1e-12` | Frozen finite synthetic model |
| Scientific validation | Not evaluated | No material reference | Not applicable | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | None |
| Human acceptance | Not applicable | No acceptance decision encoded | Not applicable | None |

## Limitations and deviations

M1 uses one finite parent model, declared finite meshes, and one selected scalar band.
Passing tests establishes software and bounded numerical behavior only. The standalone
verifier shares numerical libraries and conventions with the producer.
