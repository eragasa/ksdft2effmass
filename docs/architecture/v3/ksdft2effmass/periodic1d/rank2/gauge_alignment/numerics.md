# Rank-two gauge-alignment numerical contract

For attacked frames $A_j$ and reference frames $B_j$, the pointwise capability solves

$$
\min_{U_j\in U(2)} \lVert A_j U_j-B_j\rVert_F
$$

at each construction point. The request requires both paths to have rank two, the same
ordered reciprocal mesh, the same ambient dimension, and the same endpoint sewing map.
The aggregate capability
reshapes the complete frame inventories into one stacked problem and solves for a single
$U_{\mathrm{global}}\in U(2)$. Both use the caller-declared absolute and relative rank
cutoffs and validation absolute tolerance through Project Koios Optimization.

The retained analysis requires the pointwise and globally aligned paths to preserve the
same rank, mesh, ambient dimension, and sewing map, and requires exactly one pointwise
$U(2)$ matrix per reciprocal sample. These are structural correlation checks, not scientific
acceptance thresholds.

Rank deficiency remains fail-closed through the solver's unique-transformation
requirement. The result retains the minimum cross singular values and applied cutoff
values without converting them into scientific acceptance claims.
