# First-Principles Impurity-Operator Extraction

back_to: [[ksdft2Effmass.00]]
## Scope

This section defines the computational extraction of the atomistic one-particle perturbation produced by substitutional phosphorus or boron in silicon. The input consists of independently validated bulk and dopant Wannier Hamiltonians together with the state-space and energy alignments constructed in [[ksdft2Effmass.04]].

Let $\mathcal{D}=\{\mathrm{P},\mathrm{B}\}$ denote the dopant species. For each $d\in\mathcal{D}$, the target output is
the matrix representation of the projected dopant-induced operator in a common aligned Wannier basis, $\Delta\mathbf{H}_{\mathrm{W},d},$.

This object is not assumed to be a scalar potential. It may contain scalar onsite shifts, orbital-dependent onsite terms, changes in hybridization, modified hoppings, and other nonlocal matrix elements.

The extraction is performed at the aligned Wannier level and therefore does not depend on selecting a particular tight-binding fit. Its later use in a reduced lattice calculation does depend on the compatible bulk host Hamiltonian selected from the joint spectral-operator admissible set in [[ksdft2Effmass.05]].

## Matched Supercell Calculations

Let $\mathcal{L}_{\mathrm{sc}}$ denote the supercell lattice used for the doped calculation, and let $\mathrm{BZ}_{\mathrm{sc}}$ be its Brillouin zone. Two first-principles calculations are required:
$$
\hat{H}_{b,\mathrm{sc}}
\qquad\text{and}\qquad
\hat{H}_{d,\mathrm{sc}},
$$
where $\hat{H}_{b,\mathrm{sc}}$ is pristine silicon represented in the comparison supercell and $\hat{H}_{d,\mathrm{sc}}$ is the same supercell with one silicon atom replaced by dopant $d$.

The two calculations must use compatible lattice vectors, boundary conditions, exchange-correlation approximation, pseudopotential family, plane-wave cutoffs, Brillouin-zone sampling, and convergence tolerances. Structural conventions must also be stated: the bulk and doped cells may be compared at fixed host geometry or after a documented relaxation protocol.

Using the same supercell does not guarantee that the projected subspaces or Wannier gauges agree. It establishes only the common periodic geometry required for their comparison.

## Projected Wannier Operators
For $s\in\{b,d\}$, construct the projected Wannier Hamiltonian
$$
\mathbf{H}_{\mathrm{W},s}(\mathbf{R})
=
\frac{1}{N_k}
\sum_{\mathbf{k}\in\mathcal{K}_{\mathrm{sc}}}
e^{-i\mathbf{k}\cdot\mathbf{R}}
\mathbf{H}_s^{(P)}(\mathbf{k}),
$$
where $\mathcal{K}_{\mathrm{sc}}$ is the supercell Brillouin-zone mesh, $N_k$ is its number of wavevectors, and $\mathbf{R}\in\mathcal{L}_{\mathrm{sc}}$ is a supercell lattice vector.

The bulk and dopant Wannier constructions should use compatible target dimensions, initial orbital characters, outer windows, frozen windows, and localization criteria. Exact equality of all numerical settings is not mandatory if it degrades one construction, but every difference must be documented and its effect on the extracted operator tested.

## Common Orbital Indexing
Let
$$
a
=
\left(
\mathbf{R}_a,
\tau_a,
\mu_a
\right)
$$
be a composite Wannier-orbital index. Here, $\mathbf{R}_a$ is a supercell lattice vector, $\tau_a$ identifies a site within the supercell, and $\mu_a$ identifies the localized orbital associated with that site. Spin or another internal degree of freedom may be appended to $a$ when included explicitly.

The bulk and dopant bases must be assigned a common set of orbital labels. Away from the substitution site, this assignment follows the host lattice correspondence. Near the impurity, it must be validated through Wannier centers, orbital character, spatial overlap, and continuity from the pristine system.

## State-Space Identification

Assume that the retained bulk and dopant spaces have the same finite dimension and admit a validated unitary map
$$
\hat{U}_d
:
\mathcal{H}_{b,\mathrm{sc}}^{(P)}
\rightarrow
\mathcal{H}_{d,\mathrm{sc}}^{(P)}.
$$
Its matrix representation in the selected Wannier bases is $\mathbf{U}_d$. The matrix must satisfy
$$
\mathbf{U}_d^\dagger
\mathbf{U}_d
=
\mathbf{I}_b^{(P)},
\qquad
\mathbf{U}_d
\mathbf{U}_d^\dagger
=
\mathbf{I}_d^{(P)}
$$
within numerical tolerance. Here, $\mathbf{I}_b^{(P)}$ and $\mathbf{I}_d^{(P)}$ are the identity matrices on the retained bulk and dopant coordinate spaces, respectively. They have the same numerical form when the two spaces have the same dimension but represent identities on different labeled spaces.

The existence of an abstract unitary follows from equal dimensions. The physical identification does not. Its construction and diagnostics are those defined in [[ksdft2Effmass.04]].

## Energy Alignment

Let $E_{\mathrm{ref},s}$ be the energy reference selected for system $s$. The aligned Wannier matrix is
$$
\overline{\mathbf{H}}_{\mathrm{W},s}
=
\mathbf{H}_{\mathrm{W},s}
-
E_{\mathrm{ref},s}
\mathbf{I}.
$$
The same physical alignment convention must be applied to the bulk and dopant calculations. For a localized impurity in a sufficiently large supercell, a natural reference is the average electrostatic potential or another reproducible bulk-like quantity evaluated far from the dopant.

The alignment uncertainty must be estimated by changing the bulk-like sampling region and numerical procedure. A scalar alignment error contributes a multiple of the identity to the extracted impurity matrix.

## Impurity-Operator Definition

The aligned bulk matrix transported to dopant coordinates is
$$
\overline{\mathbf{H}}_{\mathrm{W},b\rightarrow d}
=
\mathbf{U}_d
\overline{\mathbf{H}}_{\mathrm{W},b}
\mathbf{U}_d^\dagger.
$$
The first-principles impurity perturbation is then
$$
\boxed{
\Delta\mathbf{H}_{\mathrm{W},d}
=
\overline{\mathbf{H}}_{\mathrm{W},d}
-
\overline{\mathbf{H}}_{\mathrm{W},b\rightarrow d}
}.
$$
Both matrices on the right-hand side act on the same aligned dopant coordinate space. If the bases have been aligned so that $\mathbf{U}_d=\mathbf{I}$, this reduces to
$$
\Delta\mathbf{H}_{\mathrm{W},d}
=
\overline{\mathbf{H}}_{\mathrm{W},d}
-
\overline{\mathbf{H}}_{\mathrm{W},b}.
$$

For composite indices $a$ and $b$, the matrix element
$$
\left[
\Delta\mathbf{H}_{\mathrm{W},d}
\right]_{ab}
$$
is the change in the one-particle coupling between the corresponding aligned Wannier orbitals caused by introducing dopant $d$.

## Real-Space Blocks

Using a cell-orbital representation, define
$$
\left[
\Delta\mathbf{H}_{\mathrm{W},d}(\mathbf{R})
\right]_{\alpha\beta}
=
\left\langle
w_{\alpha\mathbf{0},d}
\middle|
\Delta\hat{H}_d^{(P)}
\middle|
w_{\beta\mathbf{R},d}
\right\rangle.
$$
Here, $\alpha$ and $\beta$ label Wannier orbitals within a comparison supercell, while $\mathbf{R}$ labels the displacement between repeated supercells.

Hermiticity requires
$$
\Delta\mathbf{H}_{\mathrm{W},d}(-\mathbf{R})
=
\Delta\mathbf{H}_{\mathrm{W},d}(\mathbf{R})^\dagger.
$$
Violation of this relation beyond numerical tolerance indicates an indexing, alignment, or extraction error.

## Spatial Assignment of Matrix Elements

Let $\overline{\mathbf{r}}_{a,d}$ be the center of Wannier orbital $a$ and $\mathbf{r}_d$ the position of the substitutional dopant. Define the orbital distance from the impurity by
$$
\rho_{a,d}
=
\left|
\overline{\mathbf{r}}_{a,d}
-
\mathbf{r}_d
\right|.
$$
For an off-diagonal matrix element connecting orbitals $a$ and $b$, define the midpoint distance
$$
\rho_{ab,d}
=
\left|
\frac{
\overline{\mathbf{r}}_{a,d}
+
\overline{\mathbf{r}}_{b,d}
}{2}
-
\mathbf{r}_d
\right|.
$$
These distances permit onsite and hopping perturbations to be organized into radial shells around the impurity.

The midpoint assignment is a bookkeeping convention rather than a unique physical localization of a nonlocal operator. Alternative assignments must be tested if the inferred crossover behavior depends strongly on this choice.

## Periodic-Image Effects

A doped supercell represents a periodic array of impurities rather than a single isolated impurity. Let $L_{\mathrm{sc}}$ denote a characteristic linear size of the supercell. The extracted operator therefore depends on $L_{\mathrm{sc}}$:
$$
\Delta\mathbf{H}_{\mathrm{W},d}
=
\Delta\mathbf{H}_{\mathrm{W},d}^{(L_{\mathrm{sc}})}.
$$
The isolated-impurity operator is approached only if selected matrix elements, bound-state energies, and localization measures converge as $L_{\mathrm{sc}}$ increases.

Charged-supercell corrections, electrostatic boundary conventions, and compensating backgrounds must be treated consistently when the modeled charge state requires them. Their contribution must not be silently absorbed into the impurity operator.

## Extraction Diagnostics

The following residual tests are required.

The alignment residual is
$$
\varepsilon_{\mathrm{align},d}
=
\left\|
\mathbf{U}_d^\dagger\mathbf{U}_d
-
\mathbf{I}_b^{(P)}
\right\|.
$$
The Hermiticity residual is
$$
\varepsilon_{\mathrm{Herm},d}
=
\max_{\mathbf{R}}
\left\|
\Delta\mathbf{H}_{\mathrm{W},d}(-\mathbf{R})
-
\Delta\mathbf{H}_{\mathrm{W},d}(\mathbf{R})^\dagger
\right\|.
$$
The symbol $\|\cdot\|$ denotes a stated matrix norm. Both residuals should be consistent with the numerical precision of the Wannier and alignment procedures.

The extraction must also be repeated under controlled variations of energy alignment, Wannier windows, initial projections, and structural relaxation. The variation of $\Delta\mathbf{H}_{\mathrm{W},d}$ under these changes is part of the extraction uncertainty.

## Required Computational Outputs
For each $d\in\{\mathrm{P},\mathrm{B}\}$, the extraction stage must produce:

1. converged pristine and doped supercell calculations;
2. validated bulk and dopant Wannier Hamiltonians;
3. a documented orbital correspondence and alignment map;
4. an energy-alignment report;
5. the full matrix $\Delta\mathbf{H}_{\mathrm{W},d}(\mathbf{R})$ with orbital and position metadata;
6. radial profiles of onsite and hopping perturbation magnitudes;
7. supercell-size and Wannier-setting convergence studies;
8. the impurity-bound-state spectrum of the unreduced atomistic reference.

## Role in the Reduction Program
The construction established here is
$$
\boxed{
\left(
\overline{\mathbf{H}}_{\mathrm{W},b},
\overline{\mathbf{H}}_{\mathrm{W},d}
\right)
\xrightarrow{\mathbf{U}_d}
\Delta\mathbf{H}_{\mathrm{W},d}
}.
$$
The result is the atomistically resolved impurity operator against which all subsequent lattice and continuum impurity models are evaluated.

The decomposition of this operator into nested scalar, orbital, and nonlocal model classes is developed in [[ksdft2Effmass.07]].

## References
[1] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, "Maximally localized Wannier functions: Theory and applications," *Rev. Mod. Phys.*, vol. 84, pp. 1419-1475, 2012, doi: 10.1103/RevModPhys.84.1419.

[2] C. Freysoldt, B. Neugebauer, and C. G. Van de Walle, "First-principles calculations for point defects in solids," *Rev. Mod. Phys.*, vol. 86, pp. 253-305, 2014, doi: 10.1103/RevModPhys.86.253.