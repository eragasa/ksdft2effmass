# Numerical contract

The current flat parent uses the dimensionless represented Hamiltonian

```math
H_0=\operatorname{diag}(1,-1)
```

and the real gauge attack

```math
U_a(q)=R(a\sin 2\pi q),\qquad
H_a(q)=U_a(q)^{\mathsf T}H_0U_a(q),\qquad 0\le a\le\pi/4.
```

`Periodic1DRank2SinusoidalGaugeRotation(a)` defines the matrix-valued field
`U_a`; it does not retain a sampled matrix inventory. Generic `GaugeAttack`
evaluates that field on the declared coordinates, checks the resulting matrices for
unitarity using the producer tolerance, and applies `U_a^\dagger H U_a` to the aligned
represented-operator inventory.

The construction mesh is centered, uniform, half open, and even. The evaluation mesh is
a prospectively declared exact rational shift and must be disjoint from the construction
mesh. The finite transform retains all centered cyclic representatives. Conversion to an
ordinary-lattice model removes only the negative-Nyquist representative and reports its
normalized squared Frobenius power.

The restricted global real rotation maximizes the finite harmonic correlation. The
nonnegative optimal splitting scale is the positive part of that correlation. The
operator-only and exact-spectrum joint thresholds remain separate. The continuum
`J_0(2a)` value is an analytic comparator; its discrepancy from the finite correlation
is reported and it does not replace the finite value.

For each ordinary cutoff, the implementation separately reports omitted-block L2 norm,
truncation-only Hamiltonian/spectral errors, and total errors relative to direct attacked
values on the disjoint mesh. Matrix errors use the maximum Frobenius norm normalized by
`\sqrt{2}`; spectral errors use maximum sorted-eigenvalue discrepancy. These channels
are not asserted to be additive.

## Embedded-subspace/rank2 parent core

The nonflat control constructs the protocol's fixed four-by-four finite-range parent in
its declared ambient basis and normalizes every energy by `E_ref`. The lowest two
sampled eigenvectors define the retained subspace only after the sampled external gap
passes its explicit lower bound. PhysKit then transports that frame around the centered
finite route with the identity endpoint sewing, explicit principal phase branch, and
explicit Optimization tolerance. Backend failure, numerical rank failure, and failure of
the stricter scientific singular-value threshold produce distinct closed result variants
and no representation-orbit points.

After qualification, the analyzer represents the parent in the transported rank-two
frame, applies the same retained-space sinusoidal real rotations, and separately reports
pointwise sorted-band defect, finite restricted harmonic correlation, operator-only and
joint thresholds, minimum-loss reconstruction defect, reference/comparison nonzero
hopping power, and reference/comparison Parseval defects. Harmonic controls configure the
producer maximizer internally. Fourier coordinate admission uses the producer's frame
numerical tolerance, not verification policy. Correlation bounding corrects only
binary64 overshoot beyond the mathematical interval, while the exactly zero attack uses
its exact identity-model consequence. The cyclic Nyquist class stays in this core
inventory; no ordinary-lattice truncation is implied.

Independent verification reconstructs the same installed mathematical problem without
the producer actions. It diagonalizes the explicit parent matrices, forms each polar
right action from the eigendecomposition of the cross-Gram matrix rather than the
production SVD path, reconstructs the endpoint matrix function from an independent
unitary eigendecomposition, and evaluates Fourier blocks with explicit finite sums.  At
exactly zero attack amplitude, the independent route separately applies the mathematical
identity $A_0=H$, so the normalized correlation is exactly one and both threshold
formulas are exactly zero rather than square roots of accumulated roundoff.
Qualification variants and inventories compare exactly; binary64 scalar, phase,
harmonic, and hopping discrepancies use a fixed installed absolute verification policy.
Canonical admission rejects a retained value that claims another policy. A passing
comparison establishes agreement of these two software routes on the admitted finite
subject, not mesh convergence or physical-model validation.

## Embedded rank-two ordinary truncation

The truncation request holds the qualified parent mesh and amplitudes fixed, requires a
unique increasing inventory of ordinary cutoffs strictly below the negative-Nyquist
index, and requires at least `2*N+1` shifted evaluation points. The evaluation coordinates
are

```math
q_j=-\frac12+\frac{j+1/(N+1)}{M},\qquad j=0,\ldots,M-1,
```

and their minimum periodic separation from the construction mesh is retained. The finite
cyclic transform removes only representative `-N/2`; its squared Frobenius norm divided
by retained rank two is retained as conversion power. Ordinary omitted power is the sum
of the same normalized block powers outside `|R| <= R_c`; total omitted power adds the
conversion power without claiming an off-node Nyquist interpolation.

Reference and attacked ordinary fields are evaluated on the shifted mesh. The direct
attacked comparator applies the declared gauge rotation to the complete reference
ordinary field at those evaluation coordinates. Interpolation, truncation-only, and
total differences therefore remain distinct. Hamiltonian maximum and RMS errors use
rank-normalized Frobenius norms. Spectral maximum and RMS errors are calculated directly
from independently diagonalized sorted eigenvalues; they are not copied from or replaced
by Hamiltonian bounds. The independent route repeats these finite sums and maxima without
production Fourier, interpolation, conversion, or truncation actions.

## Nested momentum refinement

The installed momentum-refinement request requires at least two centered meshes related
by exact doubling, with the first mesh equal to the embedded request template. Every
other scientific and numerical control is unchanged. Each mesh runs the complete
single-mesh qualification and locality analysis. If any mesh is unqualified, the closed
qualification-stopped variant retains all mesh outcomes and performs no adjacent-mesh
stability comparison.

For qualified meshes, each adjacent pair reports maximum changes in parent diagnostics,
restricted correlation, operator thresholds, nonzero hopping weights, shared cyclic
hopping powers, and maximizing angles. It separately retains fine-mesh band,
reconstruction, and Parseval residuals and exact stability of the harmonic maximizing
angle disposition. Shared parent eigenvalues and spectral projectors are compared only
at the coarse points embedded exactly in the doubled mesh. Convergence requires the
declared number of final adjacent refinements to pass every separate threshold; failure
to do so is unresolved, not a qualification failure.

The independent route rebuilds mesh requests from primitive fields, reconstructs every
single-mesh result without production factories, diagonalizes explicit parent matrices
at shared points, and repeats the adjacent comparisons. The installed comparison is
currently in-memory and deliberately does not define refinement artifact bytes.

## Adaptive amplitude refinement

At one fixed momentum mesh, the adaptive request starts from a unique increasing
amplitude inventory spanning exactly `0` through `pi/4`. Each level directly evaluates
every interval midpoint and compares five separately retained quantities with their
linear interpolants: restricted correlation, operator threshold, joint threshold,
nonzero hopping weight, and every shared cyclic hopping power. Only failing intervals
receive their midpoint as a node for the next level.

A midpoint-stable level is not accepted immediately. Two disjoint quarter points per
interval are directly evaluated against the same frozen nodes. Failing quarter points
become the next nodes; passing all quarter points yields the closed converged variant.
Parent qualification failure, exhaustion of the level cap, and exhaustion of the unique
sample cap are distinct closed outcomes. Refinement classification uses only the
declared amplitude thresholds; the installed independent-comparison tolerance is not a
producer margin or scientific input.

The independent route constructs every amplitude-specific embedded request directly from
primitive fields, uses the independent parent/transport/Fourier reconstruction, and
repeats midpoint selection, quarter-point validation, and cap decisions. This comparison
is in memory and does not define canonical refinement artifact bytes.
