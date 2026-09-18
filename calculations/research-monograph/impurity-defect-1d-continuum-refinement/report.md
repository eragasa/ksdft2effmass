# Separated continuum refinement for the synthetic one-dimensional defect

## Abstract

A controlled refinement separates continuum discretization, finite domain, periodic lattice images, represented lattice scale, and defect-profile width for the accepted scalar one-dimensional parent. Continuum-mesh, continuum-domain, and lattice-supercell support axes pass their frozen criteria. At fixed physical profile, the scaled lattice agrees persistently with the parabolic comparator from $a=0.5a_{\mathrm{ref}}$ through the finest tested spacing $a=0.125a_{\mathrm{ref}}$. At the original spacing $a=a_{\mathrm{ref}}$, neither fixed-integrated nor fixed-peak Gaussian width defines a crossover: a compressed parent-dispersion residual remains $3.78\times10^{-3}E_G$, above the frozen $10^{-3}E_G$ criterion, even when lowest-state spectral and projector errors become small. This is a bounded synthetic numerical-verification result, not an asymptotic theorem or material validation.

## Question

The accepted defect-1D benchmark showed improving lattice/parabolic agreement as Gaussian profiles broadened, but used one finite band-limited grid and explicitly declined a continuum conclusion. The present exercise asks which part of that trend survives when numerical mesh, domain, image, lattice-scale, and profile-family effects are controlled independently.

## Methods

The accepted isolated-band hopping coefficients define the lattice dispersion $E_{\mathrm{lat}}(k)$, lower edge $E_0$, and parabolic coefficient $\alpha=0.6519378386943853E_Ga_{\mathrm{ref}}^2$. At physical lattice spacing $a$, the scaled represented parent is

$$
E_a(q)=E_0+\frac{E_{\mathrm{lat}}(aq)-E_0}{a^2},
$$

while the comparator is $E_0+\alpha q^2$. This scaling keeps the physical domain and Gaussian profile fixed while shrinking the represented lattice period.

The continuum route uses analytical Fourier coefficients of the periodized Gaussian. The lattice route samples the same declared profile on lattice sites. Fixed-integrated magnitude $g=0.30E_Ga_{\mathrm{ref}}$ and fixed-peak magnitude $0.12E_G$ are never combined into one sequence.

Comparison uses binding, below-edge count, lowest-state projector defect, low-momentum compressed operator residual, low/high cross residual, and outer-Brillouin weight. `protocol.md` retains the exact axes and frozen thresholds.

## Numerical support axes

All three supporting axes pass:

- The final continuum-mesh binding change between 192 and 256 modes is $5.55\times10^{-17}E_G$; the corresponding projector difference is at the floating-point floor.
- The final continuum-domain binding change between $L=96a_{\mathrm{ref}}$ and $128a_{\mathrm{ref}}$ is $5.27\times10^{-16}E_G$, with largest-domain boundary probability $2.65\times10^{-30}$.
- The final lattice-supercell binding change between 96 and 128 cells is $2.78\times10^{-17}E_G$, with largest-supercell boundary probability $3.31\times10^{-28}$.

These controls show that the subsequent discrepancies are not explained by the frozen mesh, domain, or periodic-image tolerances.

## Fixed-profile lattice-scale result

At $a=a_{\mathrm{ref}}$, the fixed-integrated $\sigma=2a_{\mathrm{ref}}$ control fails five of six comparison criteria: relative binding error $3.43\times10^{-3}$, projector defect $2.25\times10^{-2}$, compressed residual $3.78\times10^{-3}E_G$, Brillouin-edge weight $7.77\times10^{-3}$, and below-edge counts 5 versus 4. The cross residual alone passes.

At $a=0.5a_{\mathrm{ref}}$, all criteria pass: relative binding error $7.68\times10^{-4}$, projector defect $4.52\times10^{-3}$, compressed residual $8.68\times10^{-4}E_G$, cross residual below $4.9\times10^{-18}E_G$, Brillouin-edge weight $5.18\times10^{-7}$, and equal count 4. All criteria continue to pass at $a=0.25a_{\mathrm{ref}}$ and $0.125a_{\mathrm{ref}}$. The finest relative binding error is $4.67\times10^{-5}$ and the finest projector defect is $2.69\times10^{-4}$.

Thus the frozen sequence has a persistent bounded lattice-scale pass from $a=0.5a_{\mathrm{ref}}$. This is evidence for the declared finite scaling sequence, not proof of an $a\to0$ theorem.

## Width families and the negative crossover result

For the fixed-integrated family at the original lattice spacing, spectral and state metrics improve with width. At $\sigma=12a_{\mathrm{ref}}$, the relative binding error is $8.63\times10^{-5}$, the projector defect is $1.21\times10^{-3}$, the Brillouin-edge weight is $1.34\times10^{-19}$, and both representations have 11 below-edge states. Nevertheless, the compressed operator residual remains $3.78\times10^{-3}E_G$ for every sufficiently broad profile because it contains the unchanged parent-dispersion discrepancy on the fixed physical low-momentum sector. It therefore fails the $10^{-3}E_G$ rule.

The fixed-peak family also has no crossover. At $\sigma=12a_{\mathrm{ref}}$, binding, projector, and Brillouin-edge criteria pass, but the compressed parent residual still fails and the below-edge counts are 41 and 37. Broadening a fixed-peak well increases its integrated strength and number of shallow levels; it is not the same limiting family as fixed-integrated broadening.

The retained conclusion is consequently **no profile-defined continuum crossover over the tested width domain**, despite a successful fixed-profile lattice-scale sequence. This is the intended distinction that the earlier fixed-grid scan could not make.

## Independent verification

The verifier does not import the runner. It reconstructs the lattice operator through site-space hopping assembly and a separate Fourier transformation, reconstructs the continuum matrix entry by entry, and repeats every eigensolve, projector comparison, operator partition, criterion, boundary decision, and quantized content digest. Independent verification passes.

## Literature relationship and limitations

Koster--Slater finite-rank impurity theory motivates host-resolvent treatment; band-edge homogenization literature motivates weak slowly varying envelope limits; discrete-to-continuum results motivate explicit changing-space control; finite-volume literature motivates a separate image axis; and semiconductor effective-mass literature motivates retaining the central-cell boundary. These precedents do not establish that this finite synthetic parent satisfies a published theorem or represents silicon.

Only one scalar represented parent, one parabolic expansion, finite sequences, and lowest-state projectors are tested. No material calculation, DFT, production Wannierization, infinite-volume theorem, scientific validation, transferability, or uncertainty quantification is claimed.
