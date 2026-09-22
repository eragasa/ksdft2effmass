# Protocol: two-dimensional separable-to-coupled periodic reduction

## Evidence status

This protocol defines an **illustrative numerical-verification experiment** for a
synthetic spinless scalar Hamiltonian. Passing it does not establish scientific
validation, material transferability, uncertainty quantification, production
Wannier localization, or adequacy for silicon.

## Represented parent

The dimensionless lattice convention is

$$
a=2\pi,\qquad G=1,\qquad E_G=\frac{\hbar^2G^2}{2m}=1,
$$

with first Brillouin zone $-1/2\leq k_x,k_y<1/2$ and

$$
H=-\nabla^2+\lambda_x\cos x+\lambda_y\cos y
 +\lambda_{xy}\cos x\cos y.
$$

Every represented operator uses this geometry, energy zero, unit convention,
spinless scalar convention, and Bloch momentum. Plane-wave ordering is $p$
outer and $q$ inner, both increasing. Finite-difference ordering is $x$ outer
and $y$ inner. Matrix subtraction is performed only after explicit discrete
Bloch--Fourier transport to the common ordered low-mode basis.

The isotropic parent has $\lambda_x=\lambda_y=0.5$. Nonseparability is varied
through the frozen sequence $\lambda_{xy}=0,0.05,0.15,0.30$. A separate
anisotropic control uses $(\lambda_x,\lambda_y,\lambda_{xy})=(0.3,0.7,0)$ so
that anisotropy is not conflated with nonseparability.

## Numerical representations

### Plane waves

The plane-wave basis contains $(p,q)\in[-P,P]^2$. Cutoffs
$P=1,2,3,4$ are compared with $P=5$ at four declared momenta for the lowest
four bands. The coupled parent comparison uses $\lambda_{xy}=0.15$.

### Finite differences

An independently assembled centered second-order Bloch finite-difference
operator uses $N=9,13,17,25$ points per direction. Spectra are compared with
the $P=5$ parent. The represented matrix is also transported to the common
$|p|,|q|\leq1$ sector before a Frobenius residual is formed.

The finite-difference matrix and plane-wave matrix have different dimensions;
they are never directly subtracted.

## Exact separable controls

At $\lambda_{xy}=0$, the two-dimensional plane-wave matrix must equal

$$
H_x(k_x)\otimes I+I\otimes H_y(k_y)
$$

under the declared ordering. Its complete represented spectrum must equal the
sorted pairwise sums of the one-dimensional spectra. At $\Gamma$, the
$E_0+E_1$ cluster is rank two. Its complete projector is compared with the
product-space projector. A fixed Hadamard rotation supplies a controlled case
where individual-vector overlaps are $1/\sqrt2$ although the projector is
unchanged.

## Reciprocal mesh, topology, and gauge diagnostics

The lowest isolated band is evaluated on a complete $15\times15$ uniform mesh.
Across a reciprocal boundary, neighbor overlaps use explicit plane-wave index
sewing. The retained diagnostics are:

- minimum nearest-neighbor overlap magnitude;
- Wilson-loop phases in both reciprocal directions;
- elementary plaquette phases;
- the summed lattice Chern diagnostic; and
- invariance under a deterministic momentum-dependent phase attack.

The structured stops are:

- `PERIODIC_2D.SUBSPACE_OVERLAP_TOO_SMALL` when the minimum overlap falls below
  `0.85`;
- `PERIODIC_2D.CHERN_NOT_QUANTIZED` when the Chern integer defect exceeds
  `1e-10`; and
- `PERIODIC_2D.REPRESENTATION_MISMATCH` before operator arithmetic when units,
  geometry, basis order, energy zero, spin convention, or Bloch momentum do not
  agree.

The scalar real-potential family is expected to be topologically trivial. This
is a verified control, not a test of a nontrivial Chern band.

## Wannier Hamiltonian and shell hierarchy

For the lowest isolated band, scalar represented hoppings are the complete
$15\times15$ inverse discrete transform

$$
t_{r_xr_y}=\frac{1}{N_k}\sum_{\mathbf k}
 e^{-i2\pi(k_xr_x+k_yr_y)}E_0(\mathbf k),
$$

with centered representatives $r_x,r_y=-7,\ldots,7$. The frozen shell hierarchy
retains $r_x^2+r_y^2\leq s$ for

$$
s=0,1,2,4,8,18,50,98.
$$

Each shell is a complete square-lattice point-group orbit. Report omitted-block
norm, transform-mesh RMS and maximum error, $31\times31$ withheld-mesh RMS and
maximum error, and the Parseval residual separately.

The mediated route truncates the complete transform. The direct route solves an
equal-weight least-squares problem on the same complete mesh using exactly the
same Fourier columns. Agreement is expected only for this matched objective.
The full shell reconstructs the transform mesh, but its withheld error remains
a reciprocal-mesh interpolation error and is not a hopping-truncation error.

## Effective-mass and symmetry controls

A fixed centered Hessian stencil with step $0.002G$ gives the lowest-band mass
tensor at $\Gamma$. In these units the inverse mass relative to the bare inverse
mass is one half of the energy Hessian. The isotropic family should have equal
principal masses and negligible mixed curvature. The anisotropic control should
retain time reversal and reflections while breaking fourfold rotation and
splitting the two principal masses.

## Composite-band extension

The human-requested composite comparison freezes the lowest three bands at
$\lambda_{xy}=0.15$, where their sampled minimum exterior gap is
$3.48\times10^{-2}E_G$. A $k$-dependent set of centered Gaussian $s$, $p_x$,
and $p_y$ trials is projected into this rank-three subspace and symmetrically
orthonormalized. For $A=L\Sigma R^\dagger$, the projected frame uses the polar
factor $LR^\dagger=A(A^\dagger A)^{-1/2}$. A provisional implementation that
formed $AA^{-1}$ and therefore returned the raw eigengauge was deterministically
corrected before acceptance; `composite-projected-gauge-correction.md` retains
the disposition. Projection singular values and sewn-neighbor singular values
must remain above 0.75; otherwise the calculation stops with
`PERIODIC_2D.COMPOSITE_PROJECTION_RANK_LOSS` or
`PERIODIC_2D.COMPOSITE_NEIGHBOR_RANK_LOSS`.

Non-Abelian polar links define determinant plaquette phases and rank-three
Wilson spectra. A deterministic rapidly varying $O(3)$ gauge attack preserves
the subspace and spectra while changing individual frame coordinates. Chern and
Wilson eigenphase sets are compared invariantly, including optimal phase-set
assignment at branch cuts.

Both gauges are transformed into matrix-valued hopping blocks over the same
frozen shell hierarchy. Full-mesh reconstruction, block Hermiticity, Parseval
residuals, and matched direct-versus-mediated matrix coefficients are checked.
A $128\times128$ Fourier grid on the 15-cell Born--von Karman supercell provides
finite-supercell density centers, spreads, and content identities for each
orbital. These spreads are localization diagnostics, not an infinite-mesh
theorem.

The direct composite result does not substitute for the requested Wannier90
comparison. `wannier90-preflight.md` froze the independent interface and
resource envelope for the first protected attempt.

## Wannier90 failure and correction boundary

The attempt authorized at `RM-PERIODIC-2D-WANNIER90-EXECUTION-HC02` stopped in
preprocessing with `kmesh_get: something wrong, found too many nearest
neighbours`. It exited before producing `.nnkp`; therefore `.mmn` generation
and localization were not started. The failure is retained rather than treated
as localization evidence.

The mismatch is between a $15\times15\times1$ mesh and the auxiliary unit cubic
embedding: the inactive reciprocal increment is 15 times the active increments,
forcing the three-dimensional completeness search through too many shorter
in-plane shells. `wannier90-retry-preflight.md` freezes a one-line correction
that changes only the inactive direct-lattice length from 1 to 15. The human
authorized that exact correction at
`RM-PERIODIC-2D-WANNIER90-EMBEDDING-RETRY-HC04`.

The corrected preprocessing produces six axial neighbors. Localization then
converges under the frozen criterion. Native centers and spreads are restricted
to the active plane; the auxiliary transverse contribution remains separately
zero. The external $U$ matrices and `_hr.dat` blocks are independently parsed.
The comparison reconstructs subspace projectors, raw and aligned represented
operators, bounded translation-plus-constant alignment, hopping-shell tails,
and Fourier reconstruction. The limited `_hr.dat` decimal precision remains a
serialization error distinct from gauge and truncation errors.

The later authorization `RM-PERIODIC-2D-NONDFT-STUDY-HC06` adds six serial,
one-attempt cases around $(P,N,c)=(3,15,15)$: $N=11,19$, $P=2,4$, and
$c=12,18$. Mesh cases keep $c=N$; embedding cases preserve every active-plane
input. Each stage is limited to five minutes and 512 MiB, each case to 50 MiB,
and no retry or replacement case is allowed. Native Berry-link spread, common
finite-supercell spread, center sets, represented operators, hopping tails,
serialization error, runtime, and resource use remain separate. The study
records sensitivity rather than requiring monotone convergence.

## Three topological models

The human-selected combined Option E treats three models as distinct controlled
experiments. They share a diagnostic algorithm but not a represented state
space, Hamiltonian, energy scale, or approximation error:

1. the two-state Qi--Wu--Zhang square-lattice model at masses $m=-1$ and $m=3$;
2. the three-state flux-$1/3$ Hofstadter magnetic-cell model at superlattice
   amplitudes $\Delta=0$ and $\Delta=4$; and
3. the two-state periodic-gauge Haldane model at sublattice masses $M=0$ and
   $M=1$, with $t_1=1$, $t_2=0.15$, and $\phi=\pi/2$.

The first parameter in each pair is topological and the second is a declared
trivial control. Each is evaluated on odd meshes $N=21,31,51,81$. Normalized
neighbor links give oriented plaquette Chern sums and horizontal Wilson phases.
The chosen orientation has Wilson winding $w=-C$. A periodic phase attack must
leave both invariants unchanged, and reciprocal-seam projectors must agree.

The primary calculation fails closed with:

- `TOPOLOGICAL.NEIGHBOR_OVERLAP_TOO_SMALL`;
- `TOPOLOGICAL.GAP_CLOSED`;
- `TOPOLOGICAL.CHERN_NOT_QUANTIZED`;
- `TOPOLOGICAL.GAUGE_INVARIANCE_FAILED`; or
- `TOPOLOGICAL.OBSTRUCTION_MISMATCH`.

A nonzero Chern integer and matching nonzero Wilson winding are retained as the
numerical obstruction diagnostic. This does not turn any model into a phase of
the scalar continuum parent, combine their errors, or numerically prove the
general obstruction theorem.

A separate $51^2$ parameter sweep samples QWZ mass $[-3,3]$, Hofstadter
superlattice amplitude $[0,12]$, and Haldane mass $[-1.2,1.2]$. It compares
QWZ and Haldane sectors with their analytic boundaries and uses Hofstadter only
as a numerical continuation. A separate projector-Bargmann verifier
reconstructs every sampled gap and Chern sum.

## Independent verification

`verify_result.py`, `verify_composite.py`, and `verify_topological.py` do not
import their runners. `verify_wannier90_execution.py` separately checks the
first external failure identities and confirms that no later stage ran.
`verify_wannier90_balanced.py` independently reconstructs the corrected parent,
projected gauge through a Hermitian inverse square root, external gauge,
hoppings, alignment search, native spread, and common-grid finite-supercell
spread. Its portable mode uses the compact extracted arrays retained in the
result; its native mode additionally checks the external file identities,
formats, and logs. Together the verifiers independently
reconstruct or verify:

- plane-wave and finite-difference matrices;
- low-band refinement records and common-basis transport;
- Kronecker sums, product spectra, and degeneracy projectors;
- all retained lowest-band mesh energies and isolation gaps;
- reciprocal-boundary sewing and the Chern sum;
- hopping coefficients, shell residuals, Parseval identities, and direct fits;
- withheld-mesh errors; and
- isotropic and anisotropic mass tensors;
- the rank-three trial projection, exterior gap, and subspace projectors;
- non-Abelian sewn links, determinant Chern sum, and Wilson spectra;
- smooth and attacked matrix-valued hoppings and shell residuals; and
- finite-supercell orbital centers, spreads, and density identities;
- all three topological Bloch matrices, spectra, and seam projectors; and
- Chern sums and Wilson loops by projector Bargmann products rather than the
  topological runner's normalized eigenvector links; and
- first-attempt Wannier90 input/log identities, exit status, resource facts,
  and absence of every post-preprocessing output; and
- corrected Wannier90 convergence, native and common-estimator active-plane
  localization, represented operators, bounded alignment residual, and hopping
  tails;
- all six non-DFT Wannier90 cases in portable mode and, locally, their external
  execution identities and resource records; and
- every topological phase-sweep sample through projector Bargmann loops.

Acceptance requires monotonically decreasing parent-refinement errors; final
plane-wave error below $10^{-9}E_G$; separable matrix defect below
$10^{-13}E_G$; separable spectral defect below $10^{-12}E_G$; rank-two
projector defect below $2\times10^{-13}$; symmetry residuals below
$5\times10^{-13}E_G$ where the symmetry is expected; topology and overlap
stops remaining clear; full-mesh reconstruction below $2\times10^{-13}E_G$;
and independently reconstructed energies and hoppings within $2\times10^{-14}$.
These are software and numerical-verification criteria, not scientific
acceptance criteria.

## Explicit limitations

The bounded Wannier90 study addresses one isolated synthetic rank-three
subspace and one frozen trial family. Its auxiliary transverse embedding is not
a physical third direction, and only active-plane centers and spreads are
interpreted. The nonmonotone mesh and cutoff records do not establish a
converged localization limit, and the $c=18$ result demonstrates that the
selected localization basin is not embedding independent. No retries or
additional initializations were used to select a preferred basin. The three
Chern benchmarks are separate model operators, not phases of the scalar parent.
The exercise does not address a two-dimensional material, DFT, silicon,
interacting topology, scientific validation, transferability, or uncertainty
propagation.
