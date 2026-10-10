# M2 calculator mathematics

Projection, attack, and hopping-convolution equations are
`EQ-M2-PROJECTION-001`, `EQ-M2-ATTACK-002`, and
`EQ-M2-HOPPING-CONVOLUTION-003` in [the M2 scientific page](../../../../scientific.md).

`_global_rotation` takes the SVD/polar factor of the aggregate cross-covariance and
therefore chooses one unitary for all $k$. `_frame_defect` measures represented frame
difference and is not a projector invariant. `_operator_defect` compares matrices only
inside the identified common rank-two frame. `_rotation_recovery_defect` compares
pointwise recovered unitaries with the constructed attack family.

These norms remain separate because they answer different invariant and represented
questions.
