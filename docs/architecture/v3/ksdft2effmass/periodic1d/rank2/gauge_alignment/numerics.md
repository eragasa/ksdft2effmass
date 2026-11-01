# Rank-two gauge-alignment numerical contract

For attacked frames $A_j$ and reference frames $B_j$, the pointwise capability solves

$$
\min_{U_j\in U(2)} \lVert A_j U_j-B_j\rVert_F
$$

at each construction point. The aggregate capability reshapes the complete frame
inventories into one stacked problem and solves for a single $U_{\mathrm{global}}\in
U(2)$. Both use the caller-declared absolute and relative rank cutoffs and validation
absolute tolerance through Project Koios Optimization.

Rank deficiency remains fail-closed through the solver's unique-transformation
requirement. The result retains the minimum cross singular values and applied cutoff
values without converting them into scientific acceptance claims.
