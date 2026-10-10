# `ksdft2effmass.periodic1d.admissible_sets`

## Purpose and status

This package owns M3, the implemented constrained admissible-set study. M3 composes one
rank-two M2 baseline, uses a continuous rectangle of normalized energy-shift and
splitting-scale parameters, and restricts alignment to nine global real rotations. It
retains one compatible case with an explicit common witness and one separated case with
a certified analytic lower bound.

## Public contract

| Module | Public responsibility |
|---|---|
| [`definition`](definition/index.md) | Composed M2 baseline, continuous bounded parameter domain, finite angles, thresholds, and evaluation coordinates |
| [`calculate`](calculate/index.md) | Deterministic loss, witness, and separation-certificate producer |
| [`results`](results/index.md) | Quadratic proof objects, per-case outcomes, and dispositions |
| [`serialization`](serialization/index.md) | Canonical M3 schema-v1 JSON encoding |
| [`verify`](verify/index.md) | Independent reconstruction of losses, roles, quadratics, and certificates |

Cross-cutting documentation:

- [scientific boundary](scientific.md);
- [calculation schematic](schematic.md);
- [numerical contract](numeric.md);
- [implementation mapping](implementation.md); and
- [testing and evidence](testing.md).

## Ownership boundary

M3 owns the finite global-rotation family, normalized component metric, training and
staggered-evaluation roles, compatible-witness disposition, certified-separation
disposition, and correlation of analytic quadratics to sampled losses. It does not own
a general nonconvex gauge search, physical uncertainty model, or universal acceptance
threshold.

## Dependency rules

M3 must compose an exact `Periodic1DMultibandAlignmentCalculationDefinition` with
retained rank two. It must not subclass M2. Evaluation data cannot alter M2 frames, M3
thresholds, witnesses, certificates, parameter ranges, or dispositions. The verifier
must reconstruct decisive premises rather than trust serialized quadratics.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/admissible_sets/__init__.py` | Package | `ksdft2effmass.periodic1d.admissible_sets` | Public exports |
| `.../definition.py` | Module | `...admissible_sets.definition` | Frozen M3 controls |
| `.../calculate.py` | Module | `...admissible_sets.calculate` | Producer Action |
| `.../results.py` | Module | `...admissible_sets.results` | Proof and result objects |
| `.../serialization.py` | Module | `...admissible_sets.serialization` | Wire format |
| `.../verify.py` | Module | `...admissible_sets.verify` | Independent reconstruction |

## Test and Sphinx mapping

Direct test owners are:

- `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetCalculator.py`; and
- `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetThresholdSensitivity.py` for the separate post-hoc sensitivity projection.

The user-facing page is
`doc/sphinx/api/ksdft2effmass/periodic1d/admissible_sets.rst`.

## Provenance

Original local work under the repository license. The confirmatory retained package is
`calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/`. The distinct
post-hoc package is
`calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/`.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Supported | Strict definitions/results, deterministic encoding, adversarial tests | M3 API and retained input |
| Numerical verification | Supported | Independent loss/quadratic/certificate reconstruction | Nine-angle two-parameter family |
| Scientific validation | Not evaluated | No material comparator | None |
| Uncertainty quantification | Not evaluated | Thresholds are pedagogical controls | None |
| Human acceptance | Not applicable | No acceptance decision encoded | None |

## Limitations and deviations

The certificate applies only to the frozen Euclidean two-parameter domain, nine global
rotations, declared thresholds, and unclipped quadratic ellipses. Failed witness search
alone never proves incompatibility; only the retained analytic lower bound supports the
separated disposition. The threshold-sensitivity chart is post hoc and is not a
universal phase diagram.
