# Protocol: matched one-dimensional pristine–defect extraction

## Evidence class and scope

This protocol produces software and numerical-verification evidence from
synthetic finite operators. It checks whether a known impurity operator can be
recovered after exact primitive-to-supercell folding and declared changes of
coordinates and energy reference. It also separates periodic-image effects,
model-class residuals, and selected bound-state observables. It does not perform
scientific validation or uncertainty quantification.

The fixed parent records are:

- the accepted isolated lowest-band hopping record in
  `calculations/research-monograph/periodic-1d/result.json`; and
- the accepted smooth two-band `low_pair` hopping blocks in
  `calculations/research-monograph/periodic-1d/composite-result.json`, truncated
  to $|R|\leq 4$ cells.

Their exact SHA-256 identities are part of `input.json` and are checked before
execution.

## Represented spaces and folding

Let $h_R\in\mathbb C^{2\times2}$ be the retained two-orbital hopping block. The
primitive Bloch matrix is

$$
H(k)=\sum_{R=-4}^{4}e^{2\pi i kR}h_R,
$$

where $k$ is reduced momentum in reciprocal-lattice units. For an $N$-cell
supercell at reduced supercell momentum $K$, a hopping from site $n$ to
$n+R=qN+m$ receives the boundary phase $e^{2\pi iKNq}$. The folding map has
blocks

$$
F_{n\alpha,j\beta}=N^{-1/2}e^{2\pi i k_jn}\delta_{\alpha\beta},
\qquad
k_j=K+\frac{j}{N}\pmod{1}.
$$

The protocol checks map unitarity, the off-block norm of
$F^\dagger H_N(K)F$, its defect from $\bigoplus_jH(k_j)$, and the corresponding
eigenvalue defect for three $K$ values at $N=16$.

The canonical site–orbital ordering is site-major with the two retained
orbitals contiguous. Spinful controls use site–orbital–spin ordering with spin
fastest. Every represented operator also declares the state-space identity,
cell and internal dimensions, momentum, orderings, coordinate frame, energy
unit and reference, geometry, and retained subspace.

## Matched extraction and alignment

The pristine and defect Hamiltonians are constructed on the same supercell:

$$
H_{\mathrm{def}}=H_{\mathrm{pris}}+\Delta_{\mathrm{plant}}.
$$

The defect representation is then deliberately scrambled by the known unitary
$G$, which combines a three-cell cyclic translation, an orbital permutation,
an orbital rotation, orbital phases, a site-dependent phase, and, for spinors,
a global spin-frame
rotation. A scalar energy-reference shift $c=0.137E_G$ is added:

$$
\widetilde H_{\mathrm{def}}
 =G H_{\mathrm{def}}G^\dagger+cI.
$$

Direct subtraction against $H_{\mathrm{pris}}$ must stop because its ordering,
frame, and energy-reference metadata differ. The declared inverse maps give

$$
\Delta_{\mathrm{rec}}
 =G^\dagger(\widetilde H_{\mathrm{def}}-cI)G-H_{\mathrm{pris}}.
$$

Seven planted controls are retained at $N=16$: null, scalar onsite,
two-orbital onsite, range-one hopping, range-two hopping, collinear spin, and
general spin mixing. The compact nonzero planted blocks and canonical matrix
hashes are retained. The null case must recover zero. Every non-null case must
recover its independently reconstructed plant within the algebraic tolerance
$10^{-11}$.

A deliberately uncorrected extraction omits $cI$. Its exterior norm records how
a scalar-reference mismatch creates a false delocalized offset; it is not an
impurity diagnostic.

## Stopping controls

No residual is returned for the following incompatible comparisons:

1. unequal retained rank;
2. mismatched spin space;
3. incorrect supercell geometry;
4. lost site correspondence;
5. incompatible retained subspace; or
6. an unknown energy-reference relation.

Each case retains structured issue codes and a null residual.

## Frozen model-class hierarchy

The model hierarchy is fixed before observing the residuals. Spinless classes
are scalar onsite, full orbital onsite, range-one nonlocal, and range-two
nonlocal. Spinful classes are spin-independent onsite, collinear onsite, and
general spinor onsite. Orthogonal projection into each nested class is compared
with the planted operator in Frobenius norm. The first class below the frozen
algebraic tolerance is reported; no tolerance is changed to obtain agreement.

## Periodic-image sequence

A fixed-peak Gaussian orbital defect is repeated in supercells
$N=12,16,24,32,48$. Its width is $0.7a$, its scalar amplitude is
$-0.12E_G$, and its orbital block is frozen in `input.json`. For each size the
protocol reports:

- the core-restricted operator defect relative to $N=48$;
- exterior and core–exterior operator norms for a radius-$2a$ core;
- the lowest defect-band center and width over 65 supercell momenta;
- binding relative to the lower host-band edge;
- bound-state count at $K=0$; and
- inverse participation ratio, core probability, and RMS radius of the lowest
  state.

These metrics are separate; a narrow defect band is not by itself evidence that
the operator or wavefunction has converged.

## Lattice and parabolic comparisons

The accepted scalar hopping record defines an exact band-limited lattice parent
on an $N=128$ periodic grid. Its edge expansion is

$$
E(k)=E_0+\alpha k^2+O(k^4),\qquad
\alpha=-\frac12\sum_R(2\pi R)^2t_R.
$$

The comparator replaces the lattice dispersion by $E_0+\alpha k^2$ on the same
finite Fourier grid. Two Gaussian families are scanned over
$\sigma/a=0.5,1,2,4,8$: fixed peak and fixed continuum-normalization
parameter $g$. The actual discrete sum is retained; at the narrowest width it
differs from $g$ because the lattice quadrature is not a continuum integral.
Binding energy, below-edge eigenvalue count, wavefunction fidelity,
high-momentum weight,
and RMS radius are reported separately. Because the continuum comparator is
band-limited on one fixed grid, the scan can show a trend but does not establish
a converged continuum crossover.

## Operator-versus-observable controls

At the broad fixed-integrated profile, two exactly constructed perturbations
show why no single operator norm is an observable oracle:

- a rank-one perturbation confined to the highest excited eigenstate gives a
  large global operator residual but leaves the lowest bound state unchanged;
- a much smaller coupling between the lowest bound state and first unbound
  state produces a visible binding-energy change and state infidelity.

Global operator residual, binding error, bound-state count, and wavefunction
fidelity remain separately labeled.

## Independent verification and acceptance rules

`verify_result.py` does not import the runner. It independently reloads the
identified parents, rebuilds all maps and operators, reproduces every retained
numerical table and matrix digest, checks the stopping records, and rejects any
mismatch. Acceptance requires:

- source and provenance hashes to agree;
- folding and planted-recovery defects below $10^{-11}$;
- the null control to recover zero within that tolerance;
- every incompatible case to stop without a residual;
- independently reconstructed finite-size, smoothness, and metric-contrast
  values to agree with the retained record; and
- all retained checksums to pass.

Passing these rules verifies the documented synthetic calculation only.
