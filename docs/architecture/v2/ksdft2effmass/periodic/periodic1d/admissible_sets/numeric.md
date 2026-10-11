# M3 numerical contract

## Parameter domain

The parameter domain is the closed rectangle
`energy_shift_ratio_bounds × splitting_scale_bounds`. Parameters are exact
built-in-float pairs `(energy_shift_ratio, splitting_scale)`; Boolean components,
numeric strings, infinities, and NaNs are rejected. The splitting bounds remain
strictly positive. The frozen finite inventory is instead the nine declared global
alignment angles.

## Mesh roles

M3 reuses the M2 training coordinates and builds a disjoint staggered evaluation mesh
with offset $1/(N+1)$. `evaluation_mesh_size` is an integer of at least three.
Evaluation objects are labeled by one of three exact roles:
`compatible-common-witness`, `separated-spectral-boundary`, or
`separated-operator-boundary`.

## Quadratic reconstruction

The producer derives exact two-dimensional squared-loss coefficients from the frozen
constructed geometry. `Periodic1DQuadraticLoss` requires:

- center length two with finite built-in floats;
- a finite symmetric positive-definite $2\times2$ matrix;
- nonnegative finite minimum squared loss; and
- nonnegative finite correlation defect.

The verifier independently reconstructs centers, both off-diagonal entries, curvature,
minima, sampled values, and correlations. `quadratic_absolute_tolerance` must be
strictly positive in the retained standalone contract.

## Separation lower bound

The certificate uses only the splitting-scale axis. It subtracts the largest feasible
operator-ellipse splitting coordinate from the smallest spectral-ellipse splitting
coordinate. This axis gap lower-bounds Euclidean set separation only after verifying
that both threshold ellipses are real, positive-curvature, symmetric, and unclipped by
the declared domain. No arbitrary-direction optimization is performed.
`separation_resolution` is dimensionless in normalized parameter-space Euclidean units.

## Norm and unit conventions

- spectral and operator losses are dimensionless after division by the M2 parent energy
  scale;
- parameter-space separation is dimensionless Euclidean distance;
- locality blocks and omitted-block norms retain the M2 energy unit; and
- all candidate frames operate on the identified rank-two retained space.

## Tolerances and determinism

| Control | Contract |
|---|---|
| `quadratic_absolute_tolerance` | finite, strictly positive built-in `float` for analytic/sample correlation |
| `verification_absolute_tolerance` | finite, strictly positive built-in `float` for final reconstructed maximum defect |
| `separation_resolution` | finite nonnegative built-in `float`; not an uncertainty bound |

Canonical JSON forbids nonfinite values. The finite angle loop and analytic
quadratics are deterministic under the retained binary64 stack.

## Numerical limitations

The axis-separation construction and quadratics apply only to the frozen continuous
two-parameter rectangle and finite angle inventory. No clipped-set certificate,
arbitrary-unitary optimization, probabilistic calibration, or material extrapolation is
provided.
