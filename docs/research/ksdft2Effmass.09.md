back_to: [[ksdft2Effmass.00]]
# Continuum Reduction and the Atomistic-to-Continuum Crossover
## Scope
This section defines the reduction from a validated lattice Hamiltonian and impurity operator to a continuum envelope-function model. The objective is to determine the spatial, spectral, and energetic domain in which the atomistic impurity operator may be replaced by the screened potentials used in semiconductor effective-mass theory.

For dopant $d\in\mathcal{D}=\{\mathrm{P},\mathrm{B}\}$, the principal quantity is the crossover radius
$$
r_{c,d},
$$
defined as the smallest distance beyond which the continuum impurity representation satisfies prespecified operator and physical error tolerances.

## Scale Separation
Let $a$ be a characteristic silicon lattice spacing and let $L_d$ be the characteristic spatial extent of the impurity-bound envelope. Define
$$
\eta_d
=
\frac{a}{L_d}.
$$
The continuum approximation requires
$$
\eta_d
\ll
1,
$$
so that the envelope varies slowly over the length scale of a unit cell. This condition is necessary but not sufficient: short-range intervalley, interband, and central-cell effects may remain important even when the overall state is spatially extended.

## Host Band Extrema
Let $\mathcal{V}$ index the host-band extrema retained in the continuum description. For each $\nu\in\mathcal{V}$, let $\mathbf{k}_{\nu}$ be the corresponding extremal wavevector and let $E_{\nu}$ be the band-edge energy.

Near a nondegenerate extremum, the host band is expanded as
$$
E_{\nu}(\mathbf{k}_{\nu}+\mathbf{q})
\approx
E_{\nu}
+
\frac{\hbar^2}{2}
\mathbf{q}^{\mathsf{T}}
\mathbf{m}_{\nu}^{*-1}
\mathbf{q},
$$
where $\mathbf{q}$ is a small displacement from $\mathbf{k}_{\nu}$ and $\mathbf{m}_{\nu}^{*}$ is the effective-mass tensor.

Its inverse is defined by
$$
\left[
\mathbf{m}_{\nu}^{*-1}
\right]_{ij}
=
\frac{1}{\hbar^2}
\left.
\frac{\partial^2E_{\nu}(\mathbf{k})}
{\partial k_i\partial k_j}
\right|_{\mathbf{k}=\mathbf{k}_{\nu}},
$$
where $i,j\in\{x,y,z\}$ label Cartesian components.

Degenerate band edges require a multiband expansion rather than independent scalar effective masses. This distinction is especially important for valence-band acceptor states.

## Envelope-Function Expansion
Let $u_{\nu}(\mathbf{r})e^{i\mathbf{k}_{\nu}\cdot\mathbf{r}}$ denote the Bloch factor associated with extremum $\nu$. The continuum wavefunction is written as
$$
\Psi(\mathbf{r})
=
\sum_{\nu\in\mathcal{V}}
F_{\nu}(\mathbf{r})
u_{\nu}(\mathbf{r})
e^{i\mathbf{k}_{\nu}\cdot\mathbf{r}},
$$
where $F_{\nu}(\mathbf{r})$ is the slowly varying envelope associated with channel $\nu$.

Collect the envelopes into
$$
\mathbf{F}(\mathbf{r})
=
\left(
F_1(\mathbf{r}),
\ldots,
F_{N_{\mathcal{V}}}(\mathbf{r})
\right)^{\mathsf{T}},
$$
where $N_{\mathcal{V}}$ is the number of retained valleys or band-edge channels and the superscript $\mathsf{T}$ denotes transpose.

## Multichannel Effective-Mass Operator
The continuum Hamiltonian acts on
$$
\mathcal{H}_{\mathrm{cont}}
=
L^2(\Omega)
\otimes
\mathbb{C}^{N_{\mathcal{V}}},
$$
where $\Omega\subset\mathbb{R}^3$ is the continuum simulation domain, $L^2(\Omega)$ is the space of square-integrable envelopes, and $\mathbb{C}^{N_{\mathcal{V}}}$ carries the valley or band-edge channel index.

A general multichannel effective-mass Hamiltonian has matrix elements
$$
\boxed{
\left[
\hat{H}_{\mathrm{cont},d}
\right]_{\nu\nu'}
=
\delta_{\nu\nu'}
\left[
E_{\nu}
-
\frac{\hbar^2}{2}
\boldsymbol{\nabla}
\cdot
\mathbf{m}_{\nu}^{*-1}
\boldsymbol{\nabla}
\right]
+
V_{\nu\nu',d}(\mathbf{r})
}.
$$
Here, $\boldsymbol{\nabla}$ is the spatial gradient, $\delta_{\nu\nu'}$ is the Kronecker delta, and $V_{\nu\nu',d}(\mathbf{r})$ is the impurity potential matrix in channel space. Diagonal elements describe intravalley or intraband scattering; off-diagonal elements describe intervalley or interband coupling.

The continuum eigenproblem is
$$
\hat{H}_{\mathrm{cont},d}
\mathbf{F}_{\ell,d}
=
E_{\ell,d}^{\mathrm{cont}}
\mathbf{F}_{\ell,d},
$$
where $\mathbf{F}_{\ell,d}$ is the multicomponent envelope of state $\ell$ and $E_{\ell,d}^{\mathrm{cont}}$ is its energy.

## Projection of the Atomistic Impurity Operator
Let
$$
\Delta\hat{H}_{\mathrm{ref},d}
$$
be the atomistic impurity operator obtained from [[ksdft2Effmass.06]]. Its matrix elements between host Bloch states near band extrema are
$$
\mathcal{V}_{\nu\nu',d}
\left(
\mathbf{q},
\mathbf{q}'
\right)
=
\left\langle
\psi_{\nu,\mathbf{k}_{\nu}+\mathbf{q}}
\middle|
\Delta\hat{H}_{\mathrm{ref},d}
\middle|
\psi_{\nu',\mathbf{k}_{\nu'}+\mathbf{q}'}
\right\rangle.
$$
The vectors $\mathbf{q}$ and $\mathbf{q}'$ are small wavevector displacements from the retained extrema. The kernel $\mathcal{V}_{\nu\nu',d}(\mathbf{q},\mathbf{q}')$ is the impurity operator restricted to the low-energy channel space.

A local continuum potential assumes that this kernel can be approximated by a function of momentum transfer:
$$
\mathcal{V}_{\nu\nu',d}
\left(
\mathbf{q},
\mathbf{q}'
\right)
\approx
\widetilde{V}_{\nu\nu',d}
\left(
\mathbf{q}-\mathbf{q}'
\right),
$$
where $\widetilde{V}_{\nu\nu',d}$ is the Fourier transform of $V_{\nu\nu',d}(\mathbf{r})$. Failure of this approximation indicates nonlocal operator structure that cannot be represented by a multiplicative continuum potential.

## Screened Coulomb and Central-Cell Terms
Let $q_e=-e$ be the electron charge, $Q_d$ the effective charge of the ionized impurity, and $\varepsilon_{\mathrm{Si}}$ the static relative dielectric constant of silicon. The screened Coulomb interaction energy is
$$
V_{\mathrm{C},d}(r)
=
\frac{
q_eQ_d
}{
4\pi\varepsilon_0\varepsilon_{\mathrm{Si}}r
},
$$
where $r=\lvert\mathbf{r}-\mathbf{r}_d\rvert$ is the distance from the dopant position $\mathbf{r}_d$.

The continuum impurity potential is written as
$$
V_{\nu\nu',d}(\mathbf{r})
=
\delta_{\nu\nu'}
V_{\mathrm{C},d}(r)
+
V_{\mathrm{cc},\nu\nu',d}(\mathbf{r}),
$$
where $V_{\mathrm{cc},\nu\nu',d}$ is the central-cell correction. This correction contains the short-range scalar deviation from screened Coulomb behavior and any intervalley or interband coupling retained in the continuum model.

The central-cell term is not assumed a priori to be a single fitted scalar. Its required channel and spatial structure must be inferred from the atomistic residual and validated against bound-state observables.

## Material-Specific Channel Structure
For phosphorus donors in silicon, the conduction-band description must account for the six equivalent valleys and their anisotropic longitudinal and transverse masses. Short-range impurity terms may couple these valleys and produce valley-orbit splittings.

For boron acceptors, the valence-band edge is degenerate and includes heavy-hole, light-hole, and spin-orbit structure. A scalar single-band effective-mass model is therefore not the natural starting point. The required multiband channel space must be specified before the acceptor continuum reduction is evaluated.

The donor and acceptor reductions may share the same operator framework while requiring different continuum state spaces.

## Continuum Representation in the Wannier Space
To compare the continuum and atomistic operators, define an embedding
$$
\hat{J}
:
\mathcal{H}_{\mathrm{cont}}
\rightarrow
\mathcal{H}_{\mathrm{W}}^{(P)}
$$
from continuum envelopes to the retained atomistic Wannier space. The embedded continuum impurity operator is
$$
\Delta\hat{H}_{\mathrm{cont},d}^{(\mathrm{W})}
=
\hat{J}
\Delta\hat{H}_{\mathrm{cont},d}
\hat{J}^\dagger.
$$
The embedding is taken to be isometric on the retained continuum space,
$$
\hat{J}^\dagger
\hat{J}
=
\hat{I}_{\mathrm{cont}},
$$
where $\hat{I}_{\mathrm{cont}}$ is the identity operator on $\mathcal{H}_{\mathrm{cont}}$. The superscript $(\mathrm{W})$ indicates that the continuum operator has been represented on the atomistic comparison space. The embedding must specify how envelope channels are reconstructed from the retained Bloch or Wannier basis.

Without this embedding, a norm of the difference between a continuum differential operator and an atomistic matrix is not mathematically defined.

## Exterior Projectors
Let $\lvert w_{a,d}\rangle$ be the aligned Wannier orbitals with centers $\overline{\mathbf{r}}_{a,d}$. Define the projector onto orbitals outside radius $r$ by
$$
\hat{P}_{>r,d}
=
\sum_{
a:
\left|
\overline{\mathbf{r}}_{a,d}
-
\mathbf{r}_d
\right|
\geq r
}
\lvert w_{a,d}\rangle
\langle w_{a,d}\rvert.
$$
The complementary interior projector is
$$
\hat{P}_{<r,d}
=
\hat{I}
-
\hat{P}_{>r,d},
$$
where $\hat{I}$ is the identity on the atomistic comparison space.

## Exterior Continuum Error
Define the embedded continuum residual operator by
$$
\hat{E}_{\mathrm{cont},d}
=
\Delta\hat{H}_{\mathrm{cont},d}^{(\mathrm{W})}
-
\Delta\hat{H}_{\mathrm{ref},d}.
$$
The relative exterior operator error is
$$
\boxed{
\varepsilon_{\mathrm{out},d}(r)
=
\frac{
\left\|
\hat{P}_{>r,d}
\hat{E}_{\mathrm{cont},d}
\hat{P}_{>r,d}
\right\|
}{
\left\|
\hat{P}_{>r,d}
\Delta\hat{H}_{\mathrm{ref},d}
\hat{P}_{>r,d}
\right\|
}
}.
$$
The norm must be specified and evaluated only where the denominator is nonzero.

The coupling error across the radius is
$$
\varepsilon_{\mathrm{cross},d}(r)
=
\frac{
\left\|
\hat{P}_{>r,d}
\hat{E}_{\mathrm{cont},d}
\hat{P}_{<r,d}
\right\|
}{
\left\|
\Delta\hat{H}_{\mathrm{ref},d}
\right\|
}.
$$
This quantity measures continuum error in matrix elements that couple the exterior and central-cell regions.

## Crossover Radius
Let $\tau_{\mathrm{out},d}$ and $\tau_{\mathrm{cross},d}$ be the prescribed tolerances for the exterior and cross-region errors. Define
$$
\boxed{
r_{c,d}
=
\inf
\left\{
r\geq0
:
\begin{aligned}
\varepsilon_{\mathrm{out},d}(r')
&\leq
\tau_{\mathrm{out},d},
\\
\varepsilon_{\mathrm{cross},d}(r')
&\leq
\tau_{\mathrm{cross},d}
\end{aligned}
\quad
\text{for every }r'\geq r
\right\}
}.
$$
The symbol $\inf$ denotes the infimum of the admissible radii. Requiring the inequalities for every $r'\geq r$ prevents a nonmonotonic error profile from producing an artificially small crossover radius.

If no radius satisfies both inequalities, the admissible set is empty and the crossover radius is reported as $r_{c,d}=+\infty$ for the selected continuum model and tolerances.

The value of $r_{c,d}$ depends on the continuum model class, operator norm, orbital-center convention, embedding $\hat{J}$, and selected tolerances. These choices must accompany every reported crossover radius.

## Bound-State Validation
The continuum model must reproduce more than the exterior operator profile. For each target bound state, compare:

1. the binding energy and level splittings;
2. the continuum envelope with the coarse-grained atomistic state;
3. valley or band-channel populations;
4. spatial moments and localization radii;
5. state or subspace fidelity after embedding through $\hat{J}$.

If $\hat{\Pi}_{\mathrm{ref},d}$ is the atomistic target projector and $\hat{\Pi}_{\mathrm{cont},d}^{(\mathrm{W})}$ is the embedded continuum target projector, the subspace fidelity is
$$
F_{\mathrm{cont},d}
=
\frac{1}{r_d}
\operatorname{Tr}
\left(
\hat{\Pi}_{\mathrm{ref},d}
\hat{\Pi}_{\mathrm{cont},d}^{(\mathrm{W})}
\right),
$$
where $r_d$ is the target-subspace dimension.

## Numerical Continuum Problem
Choose a bounded computational domain $\Omega_L$ with characteristic size $L$. For a localized impurity state, impose either homogeneous Dirichlet boundary conditions,
$$
\mathbf{F}(\mathbf{r})
=
\mathbf{0},
\qquad
\mathbf{r}\in\partial\Omega_L,
$$
or another stated boundary condition that approximates decay at infinity. Here, $\partial\Omega_L$ is the boundary of the domain.

The continuum Hamiltonian is then discretized by finite differences, finite elements, spectral methods, or another convergent scheme. The grid spacing, domain size, boundary conditions, and treatment of the Coulomb singularity must be converged against the target binding energies and wavefunctions.

Discretization error belongs to the continuum solver and must be separated from the physical lattice-to-continuum reduction error.

## Domain of Validity
The final continuum claim must specify:

1. the energy window around the retained band extrema;
2. the valley or band-channel space;
3. the spatial region $r\geq r_{c,d}$;
4. the bound states and observables tested;
5. the operator and physical error tolerances;
6. the supercell, embedding, and discretization convergence conditions.

The continuum model is not asserted to reproduce all atomistic information. It is accepted only for the specified low-energy states, spatial scales, and observables.

## Role in the Reduction Program
The completed reduction is
$$
\boxed{
\Delta\mathbf{H}_{\mathrm{W},d}
\longrightarrow
\Delta\mathbf{H}_{\mathrm{red},d}
\longrightarrow
\hat{H}_{\mathrm{cont},d}
},
$$
with the validity statement
$$
r
\geq
r_{c,d},
\qquad
\boldsymbol{\varepsilon}_{\mathrm{cont},d}
\leq
\boldsymbol{\tau}_d.
$$
Here, $\boldsymbol{\varepsilon}_{\mathrm{cont},d}$ collects the required operator, binding-energy, subspace, and observable errors, while $\boldsymbol{\tau}_d$ contains their tolerances.

For each dopant, the final result is not merely a fitted potential. It is a continuum Hamiltonian accompanied by a state space, embedding, central-cell structure, crossover radius, target observables, and quantified error domain.

## References
[1] W. Kohn and J. M. Luttinger, "Theory of donor states in silicon," *Phys. Rev.*, vol. 98, pp. 915-922, 1955, doi: 10.1103/PhysRev.98.915.

[2] A. Baldereschi and N. O. Lipari, "Spherical model of shallow acceptor states in semiconductors," *Phys. Rev. B*, vol. 8, pp. 2697-2709, 1973, doi: 10.1103/PhysRevB.8.2697.

[3] C. J. Wellard and L. C. L. Hollenberg, "Donor electron wave functions for phosphorus in silicon: Beyond effective-mass theory," *Phys. Rev. B*, vol. 72, Art. no. 085202, 2005, doi: 10.1103/PhysRevB.72.085202.