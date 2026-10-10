# Supplementary Appendix S2: M1 Isolated-Band Calculation

## S2.1 Role and frozen scope

M1 is the planning identifier for the prospectively frozen, controlled
one-dimensional lowest-band calculation used in the main paper. Its retained
calculation identity is
`icmsep2026.paper1.periodic1d.isolated-band.v1`.

The calculation is synthetic numerical-verification evidence. It evaluates a finite
parent representation, extracts the lowest scalar band, performs a complete
reciprocal-to-hopping transform, constructs finite-range reductions, compares matched
routes, and evaluates disjoint withheld points. The retained schema contains no
band-gap result and does not by itself establish that this lowest band is isolated; a
sampled-gap or stronger isolation argument is a separate prerequisite channel. The
historical identity is not reinterpreted as such evidence. The calculation contains no
material parameters or external electronic-structure execution.

The dimensionless parent is

$$
\widehat H(k)=-\frac{\mathrm d^2}{\mathrm d x^2}+0.5\cos x,
\qquad a=2\pi,\quad G=1,\quad E_G=1.
\tag{S2.1}
$$

Reduced momentum $k/G$ lies in $[-1/2,1/2]$. The energy zero is fixed by the model; no
post-calculation energy shift is fitted.

| Control | Frozen value |
|---|---|
| Plane-wave cutoffs | $3,5,7,9,11$ |
| Finite represented reference cutoff | $15$ |
| Production plane-wave cutoff | $11$ |
| Finite-difference grids | $31,63,127,255$ points |
| Parent momenta | $-1/2,-1/4,0,1/4,1/2$ |
| Compared parent bands | lowest three ordered bands |
| Training mesh | 64-point centered half-open mesh |
| Hopping ranges | $0,1,2,3,4,6,8$ |
| Withheld mesh | 257-point staggered uniform mesh |
| Numerical-consistency tolerance | $10^{-12}$ |
| Coordinate tolerance | $10^{-14}$ |

The historical Mathieu values, common-low-mode comparison, weak-potential sweep, and
stress attacks are outside M1. Multiband alignment, nonidentity gauge families, Wannier
localization, topology, two-dimensional shells, material validation, and uncertainty
quantification are also outside its frozen scope.

## S2.2 Parent-representation diagnostics

At each frozen momentum, the lowest three eigenvalues were compared with the cutoff-15
plane-wave representation. This cutoff is the declared finite reference for M1, not an
exact continuum spectrum.

| Cutoff $P$ | Maximum discrepancy ($E_G$) |
|---:|---:|
| 3 | $1.2107868154753731\times10^{-5}$ |
| 5 | $5.311306949806749\times10^{-13}$ |
| 7 | $6.483702463810914\times10^{-14}$ |
| 9 | $8.038014698286133\times10^{-14}$ |
| 11 | $8.448797217397441\times10^{-14}$ |

The cutoff-7 through cutoff-11 discrepancies fluctuate at the represented binary64
scale, so this sequence is not interpreted as a monotone continuum error estimate. The
independently assembled centered finite-difference channel produced:

| Grid points | Maximum discrepancy ($E_G$) |
|---:|---:|
| 31 | $1.75327419749558\times10^{-2}$ |
| 63 | $4.2534045602447\times10^{-3}$ |
| 127 | $1.0471636947908536\times10^{-3}$ |
| 255 | $2.597716946719508\times10^{-4}$ |

The observed decrease is the finite-grid refinement diagnostic. M1 does not convert it
into a continuum convergence certificate.

## S2.3 Training and withheld roles

The 64-point training mesh supplies the complete discrete Fourier transform and the
equal-weight direct fits. For training extent $N=64$ and withheld extent $M=257$,
withheld coordinate $i$ is

$$
\frac{k_i}{G}=-\frac12+\frac{i+1/(N+1)}{M},
\qquad i=0,\ldots,M-1.
\tag{S2.2}
$$

The retained verifier confirms that the training and withheld coordinates are
disjoint. Withheld values enter evaluation only; they do not alter coefficients,
ranges, tolerances, or figure selection.

The complete scalar hopping coefficients are

$$
t_R=\frac{1}{N}\sum_{j=0}^{N-1}e^{-2\pi iRk_j/G}E(k_j).
\tag{S2.3}
$$

For the centered half-open mesh $k_j/G=-1/2+j/N$, the Fourier columns obey

$$
\frac{1}{N}\sum_{j=0}^{N-1}e^{2\pi i(S-R)k_j/G}
=(-1)^{S-R}\delta_{R,S\ (\mathrm{mod}\ N)}.
$$

Thus distinct retained representatives modulo $N$ are orthogonal; the centered origin
contributes the factor $(-1)^{S-R}$. Their inverse transform reconstructs the training
samples with maximum absolute error $4.166137705498387\times10^{-17}E_G$. The maximum
modular Hermiticity defect is $2.0907097393389345\times10^{-18}E_G$.

For each range $R_{\max}$, the mediated route truncates the complete coefficients to
$|R|\leq R_{\max}$. The direct route fits those same representatives by equal-weight
complex least squares on the same training mesh.

| $R_{\max}$ | Training maximum ($E_G$) | Withheld maximum ($E_G$) | Omitted-block norm ($E_G$) |
|---:|---:|---:|---:|
| 0 | $4.6235761235\times10^{-2}$ | $4.6235757038\times10^{-2}$ | $3.0304371874\times10^{-2}$ |
| 1 | $3.4907261092\times10^{-3}$ | $3.4907249362\times10^{-3}$ | $2.1876792983\times10^{-3}$ |
| 2 | $4.1809353421\times10^{-4}$ | $4.1809323067\times10^{-4}$ | $2.5574448521\times10^{-4}$ |
| 3 | $6.0054872741\times10^{-5}$ | $6.0054797140\times10^{-5}$ | $3.6185634797\times10^{-5}$ |
| 4 | $9.5136496848\times10^{-6}$ | $9.5136312847\times10^{-6}$ | $5.6738480443\times10^{-6}$ |
| 6 | $2.8158443985\times10^{-7}$ | $2.8158339337\times10^{-7}$ | $1.6575039069\times10^{-7}$ |
| 8 | $9.4653549651\times10^{-9}$ | $9.4652957590\times10^{-9}$ | $5.5272060152\times10^{-9}$ |

| $R_{\max}$ | Direct-versus-mediated coefficient defect ($E_G$) |
|---:|---:|
| 0 | $4.1633363423\times10^{-17}$ |
| 1 | $3.4428416195\times10^{-17}$ |
| 2 | $5.9106172771\times10^{-17}$ |
| 3 | $7.3812041610\times10^{-17}$ |
| 4 | $6.0865104451\times10^{-17}$ |
| 6 | $4.7557874187\times10^{-17}$ |
| 8 | $6.4715834978\times10^{-17}$ |

Across the frozen sequence, the largest direct-versus-mediated coefficient defect is
$7.38120416098117\times10^{-17}E_G$, and the largest sampled maximum route defect is
$1.564917933602745\times10^{-16}E_G$. The largest Parseval residual is
$6.938893903907228\times10^{-18}E_G^2$, and the largest imaginary band-shape residual
is $9.479926314907974\times10^{-16}E_G$. These are matched-route and
numerical-consistency diagnostics. M1 defines no preferred hopping range or scientific
acceptance threshold.

## S2.4 Independent reconstruction and provenance

The retained verifier strictly decodes the frozen input and result documents and
imports neither the producer entry point nor the maintained `ksdft2effmass`
calculation implementation. It independently rebuilds parent matrices, spectra,
Fourier coefficients, truncations, least-squares fits, route defects, Hermiticity,
Parseval quantities, and band-shape diagnostics. It nevertheless shares NumPy, SciPy,
eigensolver semantics, model conventions, and the runtime environment with the
producer; it is an independent finite-protocol reconstruction, not an independent
physical or continuum oracle.

| Reconstructed channel | Maximum absolute defect |
|---|---:|
| Spectral | $0$ |
| Hopping | $4.781392881215698\times10^{-17}$ |
| Diagnostic | $2.731148640577885\times10^{-14}$ |

All are below the frozen $10^{-12}$ verification tolerance. The result and verification
wire identities are:

- `ksdft2effmass.periodic1d.isolated-band-calculation-result.v1`;
- `ksdft2effmass.periodic1d.isolated-band-calculation-verification.v1`.

The protocol-freeze record contains the hashes of `input.json` and `protocol.md`
recorded before confirmatory execution. The retained package further binds the result,
verification, scripts, software record, source manifest, figure data, and figure
through `SHA256SUMS`. These digests test byte identity relative to the retained
manifests; by themselves they do not supply an external trusted timestamp or prove
chronology. The source manifest records the calculation snapshot and is not a claim
that a later evolving worktree has identical hashes. The calculation used local
in-process Python software only; it invoked no external electronic-structure
calculator, scheduler, remote resource, or material dataset.
