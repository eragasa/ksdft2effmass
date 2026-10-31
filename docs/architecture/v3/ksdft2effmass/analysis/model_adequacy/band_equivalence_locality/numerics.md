# Numerical contract

## Spaces and dimensions

A case has spatial dimension $d\in\{2,3\}$, a four-dimensional synthetic parent fiber,
and a retained rank-two spectral subspace. These three quantities are distinct. The
parent field acts on $\mathbb C^4$ at each reduced reciprocal coordinate; represented
reference and comparison fields act on identified $\mathbb C^2$ retained coordinates.

Parent and retained matrices are never subtracted across unequal spaces. The retained
frame and the declared gauge transformation supply the coordinate maps before any
represented-Hamiltonian comparison.

## Geometry and reciprocal coordinates

The case records a direct-lattice primitive basis with primitive vectors stored as
columns. Positive integral bonds define the parent and gauge orbit. `DirectLatticeMetric`
maps integer displacements to physical metric lengths; KSD's positive shell scale then
defines complete metric-shell membership. Basis offsets are explicit for the
non-Bravais-inspired cases.

Construction and evaluation are tensor-product uniform meshes in reduced reciprocal
coordinates. The construction size is even. Evaluation has its own size and fractional
shift, so it is not silently identified with the construction mesh. The direct square
and triangular/honeycomb requests use construction size 16 and evaluation size 33. The
direct simple-cubic and FCC/diamond requests use construction size 8 and evaluation
size 17. All four use a shift of $1/3$ of one evaluation step.

## Parent and gauge families

The parent is a Hermitian four-state synthetic field selected from:

- directed-axis hopping;
- Hermitian Bravais-bond hopping; or
- a bipartite-inspired two-sublattice law.

The parent scale lies in $[0,1]$. The retained space consists of the lowest two ordered
eigenstates, followed by deterministic seed projection and frame closure. Neighbor
transport reports singular values, rank cutoffs, Procrustes residuals, unitarity defects,
closure, and applicable plaquette quantities. Rank-deficient links make closure and
plaquette quantities inapplicable with an explicit stable reason.

The comparison field applies a smooth $SO(2)$ rotation. `axis-maximum` and `bond-rms` are
different amplitude conventions and are recorded explicitly. A known gauge relation
establishes sampled spectral equivalence of the complete represented fields; it does not
establish equal Fourier locality after support restriction.

## Fourier and support conventions

The calculation uses complete centered multidimensional finite Fourier transforms on the
construction mesh. It reports reconstruction, Parseval, and twisted-Nyquist diagnostics
before converting to an ordinary conjugate-paired hopping inventory. Nyquist power is a
separate conversion channel rather than hidden inside ordinary support error.

Truncation iterates complete shells under the declared direct-lattice metric and shell
scale. PhysKit first computes the raw squared Frobenius power of every typed hopping
block. KSD then assigns the block to its declared metric shell and divides by the retained
rank $r=2$. Thus the power recorded exactly on shell $s$ is

$$
P_s = \frac{1}{r}\sum_{R:\,\operatorname{shell}(R)=s}\lVert H_R\rVert_F^2,
$$

while omitted power sums the same normalized block powers over shells strictly beyond
$s$. The current synthetic models are explicitly unitless; scalar conversion rejects a
physical-unit model rather than dropping squared-energy units. A shell result records the
complete retained block count, reference and comparison shell power, omitted power, and
both Hamiltonian and ordered-band consequences. Shells are compared only within one
declared finite inventory. The shared real-space-support selector returns the minimum
admitted support satisfying each tolerance and makes no unstated monotonicity
assumption. Historical records retain their existing first-passing field names.

## Separated error channels

For each reference/comparison route, the calculation distinguishes:

1. complete finite Fourier reconstruction;
2. evaluation-mesh interpolation;
3. cyclic-to-ordinary Nyquist conversion;
4. deliberate metric-shell truncation; and
5. total comparison with the direct represented field.

`ErrorChannels` retains the rank-normalized matrix-Frobenius maximum error and
rank-normalized matrix-Frobenius root-mean-square error separately from the ordered-
eigenvalue maximum-absolute error and ordered-eigenvalue root-mean-square error. These
functionals are evaluated independently for the reference and comparison model routes.
The shared truncation API groups the first pair in
`RankNormalizedMatrixFrobeniusErrors` and the second pair in
`OrderedEigenvalueErrors`; `RealSpaceSupportTruncationErrors` composes the two values.
A pointwise decomposition does not authorize adding
separately maximized interpolation, truncation, and total norms. Parent, frame,
transport, gauge-covariance, Parseval, and support diagnostics also remain distinct.

## Threshold and resolution semantics

Band tolerances are a finite, unique, decreasing request inventory. For each error
functional and model role, the selected shell support is the minimum member of the
strictly nested admitted sequence satisfying the declared tolerance. Absence of a
satisfying support remains unresolved. The amplitude-resolution ladder is a declared
doubling inventory and reports direct midpoint interpolation defects. An unfrozen draft
tolerance must not be presented as acceptance.

All four direct requests sample parent scales $0$ and $1$ and band tolerances $10^{-3}$
and $10^{-5}$. The axis-maximum square and simple-cubic requests sample amplitudes $0$,
$\pi/8$, and $\pi/4$. The bond-RMS triangular/honeycomb request defines
$A_2=\pi/(4\sqrt{6})$, while the bond-RMS FCC/diamond request defines
$A_3=\pi/(4\sqrt{12})$; each samples $0$, half its maximum, and its maximum. The square,
triangular/honeycomb, simple-cubic, and FCC/diamond requests include complete shells
through caps 25, 21, 9, and 7, respectively. These are inputs to bounded synthetic
calculations, not transferable material thresholds.

## Independent comparison controls

The exact-byte verifier independently reconstructs stored identity, parent, band,
Nyquist, shell, omitted, and total-omitted power checks. Its current absolute controls
are $5\times10^{-11}$ for stored identity and independent shell-power comparisons, and
$5\times10^{-14}$ for independent parent and band comparisons. Passing these checks
establishes bounded binary64 agreement for the declared finite case only. It does not
establish continuum convergence, uncertainty, or scientific validation.
