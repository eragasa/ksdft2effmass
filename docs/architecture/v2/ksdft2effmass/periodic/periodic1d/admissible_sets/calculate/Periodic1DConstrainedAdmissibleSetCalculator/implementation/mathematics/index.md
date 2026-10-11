# M3 calculator mathematics

Candidate, loss, quadratic, admissible-set, and separation equations are
`EQ-M3-CANDIDATE-001` through `EQ-M3-SEPARATION-005` in
[the M3 scientific page](../../../../scientific.md).

`_quadratic` forms $Q=X^TX/(NE_G^2)$ and the corresponding linear/constant terms from
the finite feature representation, solves for the center, and retains the minimum;
`Periodic1DQuadraticLoss` then requires exact symmetry and positive curvature.
`_axis_extreme` evaluates a splitting-axis threshold-ellipse boundary.
`_domain_minimum_squared_loss` handles the declared box. The separated-case axis lower
bound is valid only after verifying real positive radii and no domain clipping.

All loss values are normalized and dimensionless; locality remains energy-valued and is
not merged into the admissible metric.
