# Alignment and Comparison of Projected Operators

back_to: [[ksdft2Effmass.00]]
## Scope

This section defines the comparison of the independently constructed bulk and dopant operators. The inputs are the projected operators from [[ksdft2Effmass.02]] and their localized Wannier representations from [[ksdft2Effmass.03]].

Let $\mathcal{D}=\{\mathrm{P},\mathrm{B}\}$ denote the dopant species considered in this work. For dopant $d\in\mathcal{D}$, the two systems are pristine bulk silicon, indexed by $s=b$, and silicon containing dopant $d$, indexed by $s=d$. The objective is to construct a dopant-induced operator difference that is defined on a common retained state space and is independent of arbitrary basis choices up to a stated covariance rule.

The same common-space principle is used in [[ksdft2Effmass.05]] to compare a parameterized tight-binding Hamiltonian with the bulk Wannier reference. The alignment maps are application-specific: bulk--dopant identification and Wannier-tight-binding identification must not be conflated.

## Comparison Problem

The projected bulk and dopant Hamiltonians act as
$$\begin{gather}
\hat{H}_b^{(P)}
:
\mathcal{H}_b^{(P)}
\rightarrow
\mathcal{H}_b^{(P)},
\\
\hat{H}_d^{(P)}
:
\mathcal{H}_d^{(P)}
\rightarrow
\mathcal{H}_d^{(P)}.
\end{gather}$$
The spaces $\mathcal{H}_b^{(P)}$ and $\mathcal{H}_d^{(P)}$ are constructed independently. Consequently, the formal expression
$$
\hat{H}_d^{(P)}
-
\hat{H}_b^{(P)}
$$
is not defined until the two operators have been placed on a common state space and assigned a common energy reference.

The required construction is
$$
\boxed{
\left(
\hat{H}_b^{(P)},
\hat{H}_d^{(P)}
\right)
\xrightarrow{\text{state-space identification}}
\left(
\hat{H}_{b\rightarrow d}^{(P)},
\hat{H}_d^{(P)}
\right)
\xrightarrow{\text{energy alignment}}
\Delta\hat{H}_d^{(P)}
}.
$$
The transported operator $\hat{H}_{b\rightarrow d}^{(P)}$ is the bulk Hamiltonian represented on the retained dopant space, while $\Delta\hat{H}_d^{(P)}$ is the resulting projected impurity perturbation.

## Common Comparison Geometry
Before state-space identification, the bulk and dopant calculations must be expressed using compatible periodic geometries. Let $\mathcal{L}_{\mathrm{c}}$ denote the common comparison lattice and $\mathrm{BZ}_{\mathrm{c}}$ its Brillouin zone. The subscript $\mathrm{c}$ denotes the comparison geometry.

For a doped-supercell calculation, the natural choice is to express both the pristine reference and the doped system in the same supercell lattice. A primitive-cell bulk calculation must then be repeated or folded into the supercell representation before its Bloch fibers can be compared with those of the doped system.

After this construction, both projected families are indexed by $\mathbf{k} \in \mathrm{BZ}_{\mathrm{c}}$.  Using a common Brillouin zone does not by itself identify the retained electronic states. It only establishes a common periodic coordinate structure on which a fiberwise comparison can be formulated.

## Rank Compatibility
Assume initially that the projected bulk and dopant fibers have the same constant dimension,
$$
\dim\mathcal{H}_{b,\mathbf{k}}^{(P)}
=
\dim\mathcal{H}_{d,\mathbf{k}}^{(P)}
=
M
$$
for every $\mathbf{k}\in\mathrm{BZ}_{\mathrm{c}}$. Here, $M$ is the common number of retained states per Bloch fiber.

Under this rank-matching condition, there exists at least one unitary isomorphism
$$
\hat{U}_d(\mathbf{k})
:
\mathcal{H}_{b,\mathbf{k}}^{(P)}
\rightarrow
\mathcal{H}_{d,\mathbf{k}}^{(P)}
$$
at each $\mathbf{k}$. It satisfies
$$\begin{align}
\hat{U}_d(\mathbf{k})^\dagger
\hat{U}_d(\mathbf{k})
=
\hat{I}_{b,\mathbf{k}}^{(P)},
\\
\hat{U}_d(\mathbf{k})
\hat{U}_d(\mathbf{k})^\dagger
=
\hat{I}_{d,\mathbf{k}}^{(P)},
\end{align}$$
where $\hat{I}_{b,\mathbf{k}}^{(P)}$ and $\hat{I}_{d,\mathbf{k}}^{(P)}$ are the identity operators on the retained bulk and dopant fibers.

Equality of dimensions guarantees the existence of some unitary isomorphism. It does not determine a unique physical identification. A suitable $\hat{U}_d(\mathbf{k})$ must additionally preserve the intended correspondence among orbitals, sites, symmetry sectors, and spatially localized states.

If the two projected fibers have different dimensions, no unitary isomorphism exists between them. The target subspaces must then be revised, or the comparison must be restricted to equal-dimensional matched subspaces with an explicit error assigned to the omitted directions.

## Global and Fiberwise Identification
A collection of pointwise maps $\hat{U}_d(\mathbf{k})$ defines a global identification only if it varies measurably, periodically, and with adequate regularity over $\mathrm{BZ}_{\mathrm{c}}$. Formally,
$$
\hat{U}_d
\cong
\int_{\mathrm{BZ}_{\mathrm{c}}}^{\oplus}
\hat{U}_d(\mathbf{k})
\,
\mathrm{d}\mathbf{k}.
$$
The operator $\hat{U}_d$ then maps the global retained bulk space to the global retained dopant space.

Equal rank at each $\mathbf{k}$ guarantees pointwise unitary maps but does not guarantee that a globally smooth and periodic choice exists. Such a choice additionally requires compatible Bloch-bundle topology. In the present silicon application, the practical construction will be performed through localized Wannier representations on a common supercell, but smoothness and continuity must still be verified numerically.

## Wannier-Orbital Correspondence
Let
$$
\left\{
\lvert w_{a,b}\rangle
\right\}_{a=1}^{M_{\mathrm{c}}},
\qquad
\left\{
\lvert w_{a,d}\rangle
\right\}_{a=1}^{M_{\mathrm{c}}}
$$
be orthonormal Wannier bases for the retained bulk and dopant spaces in a finite common supercell representation. The composite index $a$ specifies the lattice site, orbital label, and any retained internal degree of freedom. The integer $M_{\mathrm{c}}$ is the total number of retained Wannier orbitals in the comparison supercell.

If a physically justified one-to-one correspondence between these basis states has been established, define
$$
\hat{U}_d
=
\sum_{a=1}^{M_{\mathrm{c}}}
\lvert w_{a,d}\rangle
\langle w_{a,b}\rvert.
$$
Orthonormality of the two bases implies
$$
\hat{U}_d^\dagger\hat{U}_d
=
\hat{I}_b^{(P)},
\qquad
\hat{U}_d\hat{U}_d^\dagger
=
\hat{I}_d^{(P)}.
$$
The formula therefore defines a unitary isomorphism. Its physical validity, however, depends on the basis pairing encoded by the common index $a$.

The orbital correspondence may be constrained by Wannier centers, lattice-site assignments, orbital character, symmetry representation, spatial localization, and continuity as the impurity is introduced. These criteria determine whether $\hat{U}_d$ represents a material correspondence rather than an arbitrary unitary map.

## Overlap Matrix and Principal Angles
If the bulk and dopant states have been embedded in a common ambient Hilbert space, define the overlap matrix
$$
\left[
\mathbf{S}_d
\right]_{ab}
=
\langle
w_{a,d}
\vert
w_{b,b}
\rangle.
$$
The matrix $\mathbf{S}_d\in\mathbb{C}^{M_{\mathrm{c}}\times M_{\mathrm{c}}}$ compares the two retained bases. Its singular-value decomposition is
$$
\mathbf{S}_d
=
\mathbf{L}_d
\boldsymbol{\Sigma}_d
\mathbf{R}_d^\dagger,
$$
where $\mathbf{L}_d$ and $\mathbf{R}_d$ are unitary matrices and
$$
\boldsymbol{\Sigma}_d
=
\operatorname{diag}
\left(
\sigma_{1,d},\ldots,\sigma_{M_{\mathrm{c}},d}
\right)
$$
contains the nonnegative singular values.

The singular values determine the principal angles $\theta_{a,d}$ between the two retained subspaces through
$$
\sigma_{a,d}
=
\cos\theta_{a,d},
\qquad
0\leq\theta_{a,d}\leq\frac{\pi}{2}.
$$
Values $\sigma_{a,d}$ close to one indicate strongly corresponding subspace directions. Values close to zero indicate directions with little or no overlap.

If $\mathbf{S}_d$ has full rank, its unitary polar factor is
$$
\mathbf{G}_d
=
\mathbf{L}_d
\mathbf{R}_d^\dagger.
$$
The matrix $\mathbf{G}_d$ is the unitary matrix closest to $\mathbf{S}_d$ in the Frobenius norm and provides an overlap-maximizing coordinate alignment. If $\mathbf{S}_d$ is singular, the unitary polar factor is not unique; if its smallest singular value is very small, an overlap-based identification is numerically ill-conditioned.

For a matrix $\mathbf{A}$, the Frobenius norm is
$$
\left\|
\mathbf{A}
\right\|_{\mathrm{F}}
=
\left(
\sum_{a,b}
\left|
A_{ab}
\right|^2
\right)^{1/2}.
$$
When overlap maximization is adopted as the identification criterion, $\mathbf{G}_d$ provides a candidate matrix representation of the map $\hat{U}_d$ between the two Wannier coordinate spaces.

Overlap-based alignment is available only after a common ambient representation has been established. Similar basis dimensions alone do not make overlaps between independently represented states meaningful.

## Transported Bulk Operator
Given a validated identification map $\hat{U}_d$, define the bulk operator transported to the retained dopant space by
$$
\boxed{
\hat{H}_{b\rightarrow d}^{(P)}
=
\hat{U}_d
\hat{H}_b^{(P)}
\hat{U}_d^\dagger
}.
$$
The transported operator acts as
$$
\hat{H}_{b\rightarrow d}^{(P)}
:
\mathcal{H}_d^{(P)}
\rightarrow
\mathcal{H}_d^{(P)}.
$$
The unitary conjugation changes the state space and representation in which the bulk operator is expressed but preserves its spectrum.

## Energy Alignment
Independent first-principles calculations may employ different additive energy references. Define the aligned projected operator
$$
\overline{\hat{H}}_s^{(P)}
=
\hat{H}_s^{(P)}
-
E_{\mathrm{ref},s}
\hat{I}_s^{(P)},
$$
where $E_{\mathrm{ref},s}$ is the reference energy selected for system $s$ and $\hat{I}_s^{(P)}$ is the identity operator on $\mathcal{H}_s^{(P)}$.

The reference may be obtained from a bulk-like electrostatic potential, a specified band edge, a deep bulk-like state, or another reproducible alignment convention. The same physical convention must be applied to the bulk and dopant calculations. Stability with respect to the alignment region and numerical parameters must be reported.

Energy alignment removes only a scalar offset. It does not correct differences caused by incompatible state spaces, gauges, geometries, or target projectors.

## Projected Impurity Perturbation
After state-space and energy alignment, define the projected dopant-induced perturbation by
$$
\boxed{
\Delta\hat{H}_d^{(P)}
=
\overline{\hat{H}}_d^{(P)}
-
\hat{U}_d
\overline{\hat{H}}_b^{(P)}
\hat{U}_d^\dagger
}.
$$
Both terms on the right-hand side act on $\mathcal{H}_d^{(P)}$, so their difference is well defined. Equivalently,
$$
\overline{\hat{H}}_d^{(P)}
=
\hat{U}_d
\overline{\hat{H}}_b^{(P)}
\hat{U}_d^\dagger
+
\Delta\hat{H}_d^{(P)}.
$$
The operator $\Delta\hat{H}_d^{(P)}$ represents the change in the retained one-particle Hamiltonian associated with introducing dopant $d$, conditional on the chosen first-principles approximation, target subspaces, identification map, structural convention, and energy alignment.

It is therefore a constructed projected impurity operator rather than an automatically unique difference between two raw first-principles Hamiltonians.

## Wannier-Matrix Representation
In the finite comparison supercell, assemble the real-space blocks $\mathbf{H}_{\mathrm{W},s}(\mathbf{R})$ defined in [[ksdft2Effmass.03]] into the full Wannier Hamiltonian matrix $\mathbf{H}_{\mathrm{W},s}$. Using the dopant Wannier basis, define
$$
\left[
\Delta\mathbf{H}_{\mathrm{W},d}
\right]_{ab}
=
\left\langle
w_{a,d}
\middle|
\Delta\hat{H}_d^{(P)}
\middle|
w_{b,d}
\right\rangle.
$$
The subscript $\mathrm{W}$ denotes a Wannier-basis matrix, while the indices $a$ and $b$ are the composite orbital indices defined above.

Let $\mathbf{U}_d$ denote the matrix representation of $\hat{U}_d$ between the chosen bulk and dopant Wannier bases. The impurity matrix is
$$
\boxed{
\Delta\mathbf{H}_{\mathrm{W},d}
=
\overline{\mathbf{H}}_{\mathrm{W},d}
-
\mathbf{U}_d
\overline{\mathbf{H}}_{\mathrm{W},b}
\mathbf{U}_d^\dagger
}.
$$
If the Wannier bases have been aligned so that corresponding bulk and dopant orbitals carry identical coordinate labels, then $\mathbf{U}_d=\mathbf{I}_{M_{\mathrm{c}}}$ and
$$
\boxed{
\Delta\mathbf{H}_{\mathrm{W},d}
=
\overline{\mathbf{H}}_{\mathrm{W},d}
-
\overline{\mathbf{H}}_{\mathrm{W},b}
}.
$$
This direct matrix subtraction is the endpoint of the projection and alignment procedure. It is not valid merely because the two matrices have the same dimensions.

## Gauge Covariance
Let $\mathbf{G}_b$ and $\mathbf{G}_d$ be independent unitary changes of basis within the retained bulk and dopant spaces. Their Hamiltonian matrices transform as
$$
\overline{\mathbf{H}}_{\mathrm{W},b}
\mapsto
\mathbf{G}_b^\dagger
\overline{\mathbf{H}}_{\mathrm{W},b}
\mathbf{G}_b,
\qquad
\overline{\mathbf{H}}_{\mathrm{W},d}
\mapsto
\mathbf{G}_d^\dagger
\overline{\mathbf{H}}_{\mathrm{W},d}
\mathbf{G}_d.
$$
The matrix representation of the identification map transforms as
$$
\mathbf{U}_d
\mapsto
\mathbf{G}_d^\dagger
\mathbf{U}_d
\mathbf{G}_b.
$$
Substitution into the definition of the impurity matrix gives
$$
\Delta\mathbf{H}_{\mathrm{W},d}
\mapsto
\mathbf{G}_d^\dagger
\Delta\mathbf{H}_{\mathrm{W},d}
\mathbf{G}_d.
$$
The impurity matrix therefore transforms covariantly as an operator represented in the dopant space. Its eigenvalues, singular values, trace, determinant, and unitarily invariant norms are unchanged by the admissible gauge transformation.

Individual onsite and hopping matrix elements are not generally gauge invariant. Any decomposition of $\Delta\mathbf{H}_{\mathrm{W},d}$ into scalar onsite, orbital-dependent onsite, and nonlocal hopping components must therefore be defined relative to a specified aligned and localized gauge.

## Identification Diagnostics
The unitarity error of a numerical identification matrix is
$$
\varepsilon_{\mathrm{unit},d}
=
\left\|
\mathbf{U}_d^\dagger
\mathbf{U}_d
-
\mathbf{I}_{M_{\mathrm{c}}}
\right\|,
$$
where $\|\cdot\|$ is a specified matrix norm. A second diagnostic is the smallest overlap singular value,
$$
\sigma_{\min,d}
=
\min_a
\sigma_{a,d},
$$
which measures the weakest matched subspace direction.

Gauge covariance may be tested numerically by applying controlled unitary transformations and evaluating
$$
\varepsilon_{\mathrm{cov},d}
=
\left\|
\Delta\mathbf{H}'_{\mathrm{W},d}
-
\mathbf{G}_d^\dagger
\Delta\mathbf{H}_{\mathrm{W},d}
\mathbf{G}_d
\right\|.
$$
Here, $\Delta\mathbf{H}'_{\mathrm{W},d}$ is the impurity matrix recomputed after transforming all input matrices. A correct implementation gives $\varepsilon_{\mathrm{cov},d}$ at the level of numerical roundoff and solver tolerances.

## Validation Requirements
The bulkâ€“dopant identification and resulting impurity operator are accepted only after the following properties have been established:

1. the bulk and dopant calculations use a common comparison lattice or an explicitly validated folding map;
2. the retained subspaces have compatible dimensions and orbital content;
3. the Wannier centers, site labels, and symmetry sectors admit a reproducible correspondence;
4. the overlap singular values and principal angles indicate a well-conditioned matched subspace;
5. the selected energy reference is stable under reasonable changes in alignment procedure;
6. the identification matrix is unitary within numerical tolerance;
7. the impurity matrix obeys the stated gauge-covariance relation;
8. the extracted operator is stable under controlled variations of Wannier windows, initial projections, and structural choices.

Failure of any of these tests indicates that the difference may contain representation mismatch in addition to the physical dopant perturbation.

## Role in the Reduction Program
The construction established in this section is
$$
\boxed{
\left(
\overline{\hat{H}}_b^{(P)},
\overline{\hat{H}}_d^{(P)}
\right)
\xrightarrow{\hat{U}_d}
\Delta\hat{H}_d^{(P)}
\xleftrightarrow{\text{Wannier representation}}
\Delta\mathbf{H}_{\mathrm{W},d}
}.
$$
The map $\hat{U}_d$ is part of the scientific construction. Equal rank guarantees the existence of an abstract unitary isomorphism but does not guarantee a unique physical correspondence.

The operator $\Delta\mathbf{H}_{\mathrm{W},d}$ is the atomistically resolved impurity perturbation that will be decomposed and reduced in the subsequent research stages. Bulk Wannier-to-tight-binding reduction is developed in [[ksdft2Effmass.05]], while the systematic extraction and reduction of impurity operators are developed in [[ksdft2Effmass.06]] and [[ksdft2Effmass.07]].

## References
[1] A. Bjorck and G. H. Golub, "Numerical methods for computing angles between linear subspaces," *Math. Comp.*, vol. 27, no. 123, pp. 579-594, 1973. [https://doi.org/10.1090/S0025-5718-1973-0348991-3](https://doi.org/10.1090/S0025-5718-1973-0348991-3)

[2] N. J. Higham, "Computing the polar decomposition - with applications," *SIAM J. Sci. Stat. Comput.*, vol. 7, no. 4, pp. 1160-1174, 1986. [https://doi.org/10.1137/0907079](https://doi.org/10.1137/0907079)

[3] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, "Maximally localized Wannier functions: Theory and applications," *Rev. Mod. Phys.*, vol. 84, pp. 1419-1475, 2012. [https://doi.org/10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419)