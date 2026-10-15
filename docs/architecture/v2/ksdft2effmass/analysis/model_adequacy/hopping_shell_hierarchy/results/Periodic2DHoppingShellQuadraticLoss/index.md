# `Periodic2DHoppingShellQuadraticLoss`

## Purpose and status

Prospective immutable DataObject representing one squared channel loss on one active
HSH-1 shell slice. It is not implemented or supported.

## Public contract

Planned `squared_loss(maximal_energy_coefficients)` checks the maximal-space length and
inactive-zero rule, extracts active energy coefficients in canonical order, divides by
the retained positive energy scale, and delegates the resulting dimensionless ratios to
one `DimensionlessPositiveDefiniteQuadraticLoss`. The shared primitive exposes immutable
completed-square state, `squared_loss`, and `rms_loss`; HSH supplies no implicit unit
conversion or normalization.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellQuadraticLoss`.

## State and identity

Identity includes class shell, HSH channel (`spectral` or `operator`), energy unit,
positive energy scale, strictly ordered active maximal-space indices, inactive-zero
tolerance, reconstruction/correlation defects, and one
`DimensionlessPositiveDefiniteQuadraticLoss`. The primitive's center and matrix ordering
follow the wrapper's active-index tuple.

## Invariants and failure behavior

The wrapper requires unique increasing nonnegative active indices, an exact channel and
shell identity, an exact supported energy unit, finite strictly positive energy scale,
finite nonnegative inactive-zero tolerance, nonnegative reconstruction/correlation
defects, and a primitive dimension matching the active-index count. It rejects wrong-
length maximal vectors and nonzero inactive entries outside the frozen tolerance. The
shared primitive owns strict finite dimensionless center/matrix/minimum typing, symmetry,
positive definiteness, and direct canonical-coordinate evaluation.

## Dependencies and collaborators

The calculator constructs the HSH wrapper and shared primitive from direct loss
formulas. The verifier may read the primitive's immutable center, matrix, and minimum as
claimed data, but it must not call the primitive constructor, `squared_loss`, or
`rms_loss`; it independently validates the premises and reconstructs direct/quadratic
values. Class results correlate the wrapper with shell masks and channel minima. HSH
does not move channel, energy unit/scale, active-index, weight, box, metric, defect, or
certificate policy into the lower-level primitive.

## Data and action flow

Direct design matrices produce a dimensionless completed-square primitive. The HSH
wrapper binds it to the energy scale and active maximal-space embedding and serves as the
proof/evaluation object for feasibility, witness, certificate, and verifier checks.

## Serialization and compatibility

HSH schema v1 nests or inlines the primitive's dimensionless matrix, center, and minimum
together with the wrapper's energy unit/scale, active indices, channel, shell, inactive-
zero tolerance, and defects in canonical order. The HSH decoder reconstructs both types
and reruns all invariants; it does not define a universal primitive wire identity.

## Scientific and numerical boundary

The object represents the frozen finite weighted loss only. Positive definiteness is a
finite-design premise, not a physical convexity claim. See
[scientific](../../scientific.md).

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/results.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.results.Periodic2DHoppingShellQuadraticLoss` | Active-slice quadratic proof object |
| same | Method | `...Periodic2DHoppingShellQuadraticLoss.squared_loss` | Validate maximal embedding and delegate active-coordinate evaluation |

## Test mapping

Planned tests cover direct-loss agreement, both cross terms, symmetry, curvature,
active-index mapping, Boolean rejection, wrong dimensions, and inactive-coordinate
attacks. No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license. Mathematical representation derives
from the affine finite Fourier model in the HSH-1 protocol.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | DataObject absent | None |
| Numerical verification | Not evaluated | No direct-loss reconstruction | None |
| Scientific validation | Not evaluated | Synthetic loss | None |
| Uncertainty quantification | Not applicable | Loss is not an uncertainty | None |
| Human acceptance | Not evaluated | No frozen object | None |

## Limitations and deviations

The wrapper does not own coefficient-box clipping, channel thresholds, metric distance,
or certificates; those remain with the calculator, class result, and verifier. The
shared primitive owns no shell, channel, active-index, energy-scale, weight, box, metric,
certificate, or reconstruction-defect semantics.
