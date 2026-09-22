# Appendix G isolated-band, stress, and direct composite protocol

## Evidence boundary

This protocol governs **calculated illustrative numerical experiments** for the
one-dimensional cosine parent. It covers the isolated-band, adversarial, direct
composite, and separately authorized bounded Wannier90 slices of Appendix G. It
is not semiconductor validation. Initial Wannier90 slices failed their frozen
iteration limits; a final preconditioned slice satisfied the unchanged declared
localization convergence rule for both retained pairs.

## Parent and representations

The frozen convention is $a=2\pi$, $G=1$, $E_G=1$, and
$V(x)/E_G=0.5\cos x$. Plane-wave fibers use reciprocal indices
$n=-P,\ldots,P$. The independent cell-grid representation uses an $N$-point
periodic grid and conjugate Bloch boundary phases. The following errors remain
separate:

1. plane-wave cutoff error against $P=15$;
2. finite-difference error against the same plane-wave reference;
3. a transported low-mode operator error for $|n|\leq3$;
4. exact inversion and $V_0\leftrightarrow -V_0$ translation checks; and
5. Mathieu characteristic-value comparisons at the zone center and boundary.

The refinement sequences are $P=3,5,7,9,11$ and
$N=31,63,127,255$. Agreement between the two finite representations is not used
as its own convergence oracle.

## Isolated-band map and localization

The lowest plane-wave band is evaluated on a complete 64-point uniform
reciprocal mesh. Neighboring eigenvectors are parallel transported by making
each overlap real and nonnegative. Reciprocal closure uses the explicit
$k\mapsto k+G$ reciprocal-index sewing. The closure holonomy is distributed
uniformly to produce a periodic gauge.

The Born--von Karman inverse transform is evaluated on 32 points per cell over
64 cells. The result retains the quadrature norm, center modulo the lattice,
spread, sample count, and SHA-256 identity of the canonical binary64 density,
not a dense profile array.

## Hopping and reduction

For centered Born--von Karman representatives $r=-32,\ldots,31$,

$$
t_r=\frac1{N_k}\sum_k e^{-ikra}E(k).
$$

The complete inverse transform must reconstruct the represented mesh band.
Finite-range models retain $|r|\leq r_c$ for
$r_c=0,1,2,3,4,6,8$. Every range records:

- omitted hopping norm;
- training and independent withheld-mesh errors;
- Parseval residual;
- direct-versus-mediated coefficient and band defects;
- bandwidth error; and
- zone-center curvature.

The direct route uses equal-weight least squares on the same complete uniform
mesh and same unconstrained Fourier class. Under these conditions it should
agree with truncating the complete discrete hopping transform. This algebraic
agreement is verified separately from model adequacy.

## Adversarial stress extension

The stress input separately challenges the assumptions of the nominal
construction. It sweeps $V_0/E_G=0,0.02,0.1,0.5,1,2,4$; compares the first eight
parent bands; samples band indices $0,1,2,3,5,7$ on reciprocal meshes of
8, 16, 32, 64, and 128 points; and uses a $P=21$ plane-wave reference. A zero or
sub-threshold adjacent gap is recorded as a failure of scalar isolated-band
applicability, not as a numerical failure to be hidden.

Potential-shape cases include the baseline cosine, a translated cosine, a
constant energy shift, a second cosine harmonic, an inversion-breaking sine
harmonic, and a three-cosine-harmonic shape. Translation is required to preserve
the spectrum, the energy shift is required to affect only the energy reference,
and every real scalar potential is required to preserve spinless
time-reversal energy symmetry. No assumption is made that additional harmonics
preserve band gaps, localization, or finite-range accuracy.

A deterministic phase attack checks projector and parallel-transport gauge
covariance. Route-equivalence attacks replace equal reciprocal weights or
restrict the training region while retaining the same nominal hopping range.
These attacks are expected to break the ideal direct-versus-mediated equality;
their purpose is to identify the equality's assumptions rather than force a
pass under changed mathematics.

## Direct composite-band extension

The composite calculation retains the contiguous pairs 0--1 and 2--3 from the
same $V_0/E_G=0.5$, $P=15$ parent on a 128-point half-open reciprocal mesh. The
first pair is a well-conditioned baseline; the second is a higher-band stress
case. Each retained pair must remain separated from excluded bands by more than
$10^{-8}E_G$. Neighboring and sewn overlap singular values are retained rather
than inferring compatibility from energy ordering.

A direct polar-transport frame is closed by distributing the unitary closure
over the reciprocal mesh. The calculation retains the Wilson-loop eigenphases,
then applies a smooth controlled momentum-dependent $U(2)$ transformation.
Projectors, Wilson-phase sets, and represented eigenvalues must remain
invariant; pointwise unitary alignment must recover the reference frame and
operator.

The represented $2\times2$ Hamiltonians are Fourier transformed into centered
block hoppings. Complete blocks must reconstruct the reciprocal operator and
satisfy $T_{-R}=T_R^\dagger$. Finite-range errors are compared in the smooth
polar frame and in a deliberately rough periodic gauge. The rough-gauge attack
is expected to preserve exact pointwise spectra while degrading block locality
and truncated-model accuracy.

At $r_c=4a$, an equal-weight direct matrix Fourier fit uses the same complete
uniform mesh and model class as mediated block truncation. Their coefficients
and represented training operators must agree to numerical precision. This
control does not imply gauge-independent truncation.

## Acceptance boundary

The nominal verifier checks source identities, independent Mathieu values,
symmetry, refinement behavior, the complete Fourier reconstruction, Parseval
identity, direct-versus-mediated agreement, withheld errors, and localization
normalization. The stress verifier independently checks the free-limit gap
closure, eight-band convergence, higher-band coverage, potential covariance
controls, gauge covariance, complete hopping reconstruction, and both the ideal
route control and deliberately broken route assumptions. The composite verifier
additionally checks external subspace gaps, overlap conditioning, gauge and
Wilson covariance, alignment recovery, retained operator and hopping identities,
block Hermiticity, smooth-gauge range convergence, rough-gauge locality loss,
and direct-versus-mediated matrix agreement. Passing establishes numerical
verification for the declared nominal, adversarial, and direct composite
calculations only. The failed preprocessing, nonconverged 500-iteration runs,
nonconverged low-pair 5000-iteration run, and converged preconditioned runs remain
distinct records. The final runs satisfied the unchanged spread convergence rule
at iterations 69 and 4176 and establish a converged localization comparison for
the fixed synthetic interface. They do not establish material validation,
transferability to silicon, or uncertainty quantification.
