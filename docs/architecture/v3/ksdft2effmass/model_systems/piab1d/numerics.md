# Numerical contract

## Finite representation

The successor uses the PhysKit full-grid homogeneous-Dirichlet convention. For
`N` interior degrees of freedom and box length `L`, the spacing is

$$
\Delta x = \frac{L}{N+1}.
$$

With `ℏ = m = 1`, the represented kinetic Hamiltonian has diagonal entries
`1 / Δx²` and nearest-neighbor entries `-1 / (2 Δx²)`. The finite matrix represents
the centered second-order discretization. It is not the continuum differential
operator.

The analytical continuum energies are

$$
E_n = \frac{n^2\pi^2}{2L^2},
$$

and the closed-form finite-difference energies are

$$
E_{n,N} = \frac{2}{\Delta x^2}
\sin^2\!\left(\frac{n\pi}{2(N+1)}\right).
$$

Every stored PIAB1D quantity uses the declared nondimensional unit. Constructors reject
dimensioned values, Boolean numeric inputs, numeric strings, nonfinite values, and
inconsistent shapes.

## Reduction

For the retained orthonormal basis `Φ_M`, the reduction map is `Φ_Mᵀ`, the embedding
map is `Φ_M`, and the projector is `P_M = Φ_M Φ_Mᵀ`. The reduced Hamiltonian is

$$
H_M = \Phi_M^{\mathsf T} H \Phi_M.
$$

The result keeps consistent compression, unmatched compression, boundary realization,
and discarded-sector quantities distinct. It never subtracts operators before their
state spaces and coordinate conventions agree.

## Grid sweep

`Piab1dGridSweepDefinition` stores strictly increasing interior dimensions and strictly
increasing positive fixed modes. The retained dimension exists on every grid. Stored
spacing values equal `L / (N + 1)` for each declared dimension.

Each represented spectrum contributes all modes `1, …, N` exactly once. Flattened
arrays use explicit offsets and mode-number inventories. Fixed-mode convergence uses
only grids on which the mode exists. Adjacent observed orders use

$$
p_i = \frac{\log(e_i/e_{i+1})}{\log(\Delta x_i/\Delta x_{i+1})}.
$$

## Residual norms

Residual studies use the canonical PhysKit Frobenius, spectral, and maximum-absolute-
entry norms in that order. Raw observations carry the nondimensional energy unit.
Normalized observations are unitless and use the same-grid Hamiltonian norm as their
denominator. A normalized value does not establish convergence between changing finite
spaces.

## Finite algebraic diagnostics

The grid-indexed diagnostic family stores:

- discrete-spectrum discrepancy;
- spectral-reconstruction discrepancy;
- projector-idempotency discrepancy;
- retained-coordinate discrepancy;
- retained-embedding discrepancy; and
- spectral leakage.

Energy-valued discrepancies use the nondimensional energy unit. Projector idempotency
is unitless. Every vector contains one value per declared grid and contains only finite
nonnegative values.

## Kinetic-potential decomposition

For retained Hamiltonian `H_M` and declared real-symmetric shift `Δ`, the operation
stores

$$
T_{physical}=H_M,\qquad V_{physical}=0,
$$

and

$$
T_{alternative}=H_M-\Delta,\qquad V_{alternative}=\Delta.
$$

Both pairs reconstruct the same finite Hamiltonian. The model-class projections use
this fixed order:

1. scalar;
2. diagonal;
3. tridiagonal; and
4. unrestricted real symmetric.

Each fit stores the projected matrix, unexplained residual, and canonical Frobenius
norm. The unrestricted class has zero residual by construction. The alternative split
is illustrative and carries no physical assignment.

## Verification tolerances

Comparison tolerances belong to verification observations. Configuration and options
contain only physical declarations and algorithmic choices. Scale-aware comparisons
use independently reconstructed references and explicit absolute tolerances. A passing
comparison establishes agreement for the declared finite calculation only.
