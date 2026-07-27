back_to: [[ksdft2Effmass.00]]
# Operator, Subspace, Spectral, and Observable Error Metrics
## Scope
This section defines the error measures used to evaluate every reduction in the program. A reduced model is not accepted solely because its band structure or a small number of eigenvalues appear visually similar to the reference. The comparison must state the common state space, reference operator, target subspace, observables, norms, and tolerances.

Let
$$
\mathbf{H}_{\mathrm{ref}}
\qquad\text{and}\qquad
\mathbf{H}_m
$$
denote a reference Hamiltonian and a level-$m$ reduced Hamiltonian represented on the same finite-dimensional Hilbert space. The corresponding error operator is
$$
\boxed{
\mathbf{E}_m
=
\mathbf{H}_m
-
\mathbf{H}_{\mathrm{ref}}
}.
$$
The sign convention is fixed throughout this section. Norm-based errors are unchanged if the opposite sign is used, but signed matrix elements and observable shifts are not.

## Common-Space Requirement
The expression $\mathbf{E}_m=\mathbf{H}_m-\mathbf{H}_{\mathrm{ref}}$ is defined only after the two matrices have been expressed in a common coordinate space. If $\mathbf{U}_m$ maps model coordinates to reference coordinates, the aligned model is
$$
\widetilde{\mathbf{H}}_m
=
\mathbf{U}_m
\mathbf{H}_m
\mathbf{U}_m^\dagger,
$$
and the error operator must instead be formed as
$$
\mathbf{E}_m
=
\widetilde{\mathbf{H}}_m
-
\mathbf{H}_{\mathrm{ref}}.
$$
The construction of the required alignment map is part of the comparison problem, not part of the error norm.

## Absolute and Relative Operator Errors
The absolute Frobenius error is
$$
\varepsilon_{\mathrm{F},m}^{\mathrm{abs}}
=
\left\|
\mathbf{E}_m
\right\|_{\mathrm{F}},
$$
where
$$
\left\|
\mathbf{A}
\right\|_{\mathrm{F}}
=
\left[
\operatorname{Tr}
\left(
\mathbf{A}^\dagger\mathbf{A}
\right)
\right]^{1/2}
$$
is the Frobenius norm.

The relative Frobenius error is
$$
\varepsilon_{\mathrm{F},m}
=
\frac{
\left\|
\mathbf{E}_m
\right\|_{\mathrm{F}}
}{
\left\|
\mathbf{H}_{\mathrm{ref}}
\right\|_{\mathrm{F}}
}.
$$
This metric measures the total matrix residual but weights all represented matrix elements quadratically.

The spectral-norm error is
$$
\varepsilon_{2,m}
=
\frac{
\left\|
\mathbf{E}_m
\right\|_2
}{
\left\|
\mathbf{H}_{\mathrm{ref}}
\right\|_2
},
$$
where $\|\mathbf{A}\|_2$ is the largest singular value of $\mathbf{A}$. This norm measures the maximum amplification of a normalized state by the error operator.

If the reference norm in a relative error vanishes, the corresponding absolute error must be reported instead.

## Weighted Real-Space Operator Error
For a translationally represented lattice operator, define
$$
\left\|
\mathbf{E}_m
\right\|_w^2
=
\sum_{\mathbf{R}}
w_{\mathbf{R}}
\left\|
\mathbf{E}_m(\mathbf{R})
\right\|_{\mathrm{F}}^2,
$$
where $\mathbf{R}$ is a lattice displacement and $w_{\mathbf{R}}\geq0$ is a stated weight. The normalized weighted error is
$$
\varepsilon_{H,m}
=
\frac{
\left\|
\mathbf{E}_m
\right\|_w
}{
\left\|
\mathbf{H}_{\mathrm{ref}}
\right\|_w
}.
$$
The quantity $\varepsilon_{H,m}$ is the global operator-reconstruction error used in the reduction program.

Weights may be chosen to compensate for shell multiplicity, emphasize short-range terms, or reflect a physical spatial measure. Results obtained with different weights are not directly comparable unless the weighting convention is reported.

## Reference and Model Eigenproblems
Let
$$
\mathbf{H}_{\mathrm{ref}}
\lvert\psi_{\ell}^{\mathrm{ref}}\rangle
=
E_{\ell}^{\mathrm{ref}}
\lvert\psi_{\ell}^{\mathrm{ref}}\rangle
$$
and
$$
\mathbf{H}_m
\lvert\psi_{\ell}^{(m)}\rangle
=
E_{\ell}^{(m)}
\lvert\psi_{\ell}^{(m)}\rangle
$$
be the reference and reduced eigenproblems. The index $\ell$ labels the states after a documented matching procedure. Eigenvalue ordering alone is insufficient near degeneracies or level crossings; state matching must use symmetry, overlap, or subspace comparison.

## Target Bound-State Subspace
Let $\mathcal{I}_d$ index the impurity-bound states relevant to dopant $d$, and let $r_d$ be their number. Define the reference projector matrix
$$
\mathbf{\Pi}_{\mathrm{ref},d}
=
\sum_{\ell\in\mathcal{I}_d}
\lvert\psi_{\ell}^{\mathrm{ref}}\rangle
\langle\psi_{\ell}^{\mathrm{ref}}\rvert.
$$
The matrix $\mathbf{\Pi}_{\mathrm{ref},d}$ projects onto the target bound-state subspace in the common finite-dimensional representation.

The operator error restricted to this subspace is
$$
\boxed{
\varepsilon_{\Pi,m,d}
=
\frac{
\left\|
\mathbf{\Pi}_{\mathrm{ref},d}
\mathbf{E}_m
\mathbf{\Pi}_{\mathrm{ref},d}
\right\|_2
}{
\left\|
\mathbf{\Pi}_{\mathrm{ref},d}
\mathbf{H}_{\mathrm{ref}}
\mathbf{\Pi}_{\mathrm{ref},d}
\right\|_2
}
}.
$$
This metric measures the error that acts entirely within the target bound-state subspace.

The leakage error is
$$
\varepsilon_{\mathrm{leak},m,d}
=
\frac{
\left\|
\left(
\mathbf{I}
-
\mathbf{\Pi}_{\mathrm{ref},d}
\right)
\mathbf{E}_m
\mathbf{\Pi}_{\mathrm{ref},d}
\right\|_2
}{
\left\|
\mathbf{H}_{\mathrm{ref}}
\mathbf{\Pi}_{\mathrm{ref},d}
\right\|_2
},
$$
where $\mathbf{I}$ is the identity matrix on the comparison space. This quantity measures error-induced coupling from the target subspace into its complement.

## Eigenvalue and Level-Splitting Errors
For a matched state $\ell$, the signed eigenvalue error is
$$
\delta E_{\ell,m}
=
E_{\ell}^{(m)}
-
E_{\ell}^{\mathrm{ref}}.
$$
The maximum target-spectrum error is
$$
\varepsilon_{E,m,d}^{\max}
=
\max_{\ell\in\mathcal{I}_d}
\left|
\delta E_{\ell,m}
\right|.
$$

For a pair of target states $\ell$ and $\ell'$, define the level-splitting error by
$$
\delta\Delta E_{\ell\ell',m}
=
\left[
E_{\ell}^{(m)}
-
E_{\ell'}^{(m)}
\right]
-
\left[
E_{\ell}^{\mathrm{ref}}
-
E_{\ell'}^{\mathrm{ref}}
\right].
$$
Level splittings are insensitive to a common scalar energy shift and are therefore useful for diagnosing orbital and valley structure.

## Binding-Energy Error
Let $E_{\mathrm{edge}}^{\mathrm{ref}}$ be the relevant host band-edge energy and $E_{\ell}^{\mathrm{ref}}$ the impurity-state energy. Define the positive reference binding energy by
$$
E_{b,\ell,d}^{\mathrm{ref}}
=
\left|
E_{\mathrm{edge}}^{\mathrm{ref}}
-
E_{\ell}^{\mathrm{ref}}
\right|.
$$
The same convention defines $E_{b,\ell,d}^{(m)}$ for the reduced model. The binding-energy error is
$$
\boxed{
\Delta E_{b,\ell,m,d}
=
E_{b,\ell,d}^{(m)}
-
E_{b,\ell,d}^{\mathrm{ref}}
}.
$$
The absolute or relative form must be specified when a tolerance is imposed. The band edge and impurity level must be evaluated using compatible finite-size and energy-alignment conventions.

## State Fidelity
For nondegenerate normalized states, define
$$
F_{\ell,m}
=
\left|
\left\langle
\psi_{\ell}^{\mathrm{ref}}
\middle|
\psi_{\ell}^{(m)}
\right\rangle
\right|^2.
$$
The state fidelity satisfies $0\leq F_{\ell,m}\leq1$. A value of one indicates agreement up to a global phase.

State fidelity is not reliable for arbitrarily rotated bases within a degenerate or nearly degenerate manifold. In that case, define the reduced-model target projector matrix
$$
\mathbf{\Pi}_{m,d}
=
\sum_{\ell\in\mathcal{I}_d}
\lvert\psi_{\ell}^{(m)}\rangle
\langle\psi_{\ell}^{(m)}\rvert
$$
and the subspace fidelity
$$
\boxed{
F_{m,d}
=
\frac{1}{r_d}
\operatorname{Tr}
\left(
\mathbf{\Pi}_{\mathrm{ref},d}
\mathbf{\Pi}_{m,d}
\right)
}.
$$
The quantity $F_{m,d}$ is the average squared cosine of the principal angles between the reference and reduced target subspaces. It is invariant under unitary rotations within either subspace.

## Observable Error
For an observable represented by the matrix $\mathbf{O}$, define
$$
\langle\mathbf{O}\rangle_{\ell}^{\mathrm{ref}}
=
\left\langle
\psi_{\ell}^{\mathrm{ref}}
\middle|
\mathbf{O}
\middle|
\psi_{\ell}^{\mathrm{ref}}
\right\rangle
$$
and the corresponding model expectation $\langle\mathbf{O}\rangle_{\ell}^{(m)}$. The observable error is
$$
\delta O_{\ell,m}
=
\langle\mathbf{O}\rangle_{\ell}^{(m)}
-
\langle\mathbf{O}\rangle_{\ell}^{\mathrm{ref}}.
$$
Relevant observables may include localization radii, valley populations, orbital populations, dipole moments, and transition matrix elements.

## Bulk Band-Edge Errors
For the bulk reduction in [[ksdft2Effmass.05]], the indirect-gap error is
$$
\delta E_{g,m}
=
E_{g,m}
-
E_{g,\mathrm{ref}},
$$
where $E_g$ is the indirect band gap. If $\mathbf{k}_{\mathrm{v},m}$ and $\mathbf{k}_{\mathrm{v},\mathrm{ref}}$ are the modeled and reference valley positions, define
$$
\delta k_{\mathrm{v},m}
=
\left|
\mathbf{k}_{\mathrm{v},m}
-
\mathbf{k}_{\mathrm{v},\mathrm{ref}}
\right|.
$$

For an effective-mass tensor $\mathbf{m}^*$, a dimensionless tensor error is
$$
\varepsilon_{m^*,m}
=
\frac{
\left\|
\mathbf{m}_m^{*-1}
-
\mathbf{m}_{\mathrm{ref}}^{*-1}
\right\|_{\mathrm{F}}
}{
\left\|
\mathbf{m}_{\mathrm{ref}}^{*-1}
\right\|_{\mathrm{F}}
}.
$$
The inverse tensor is used because it is directly proportional to the Hessian of the band energy.

## Spatially Resolved Error
For an impurity model, define
$$
\mathbf{E}_{m,d}
=
\Delta\mathbf{H}_{m,d}
-
\Delta\mathbf{H}_{\mathrm{ref},d},
$$
where $\Delta\mathbf{H}_{\mathrm{ref},d}$ is the extracted atomistic impurity matrix and $\Delta\mathbf{H}_{m,d}$ is its reduced approximation. Let $\mathbf{P}_{>r}$ project onto Wannier orbitals whose centers lie at least distance $r$ from the impurity. Define
$$
\mathbf{E}_{m,d}^{>r}
=
\mathbf{P}_{>r}
\mathbf{E}_{m,d}
\mathbf{P}_{>r}.
$$
The corresponding exterior error is
$$
\varepsilon_{H,m,d}^{>r}
=
\frac{
\left\|
\mathbf{E}_{m,d}^{>r}
\right\|
}{
\left\|
\mathbf{P}_{>r}
\Delta\mathbf{H}_{\mathrm{ref},d}
\mathbf{P}_{>r}
\right\|
}.
$$
This radial error profile is used in [[ksdft2Effmass.09]] to define the atomistic-to-continuum crossover.

## Gauge Behavior
Under a common unitary change of comparison basis,
$$
\mathbf{H}_{\mathrm{ref}}
\mapsto
\mathbf{G}^\dagger
\mathbf{H}_{\mathrm{ref}}
\mathbf{G},
\qquad
\mathbf{H}_m
\mapsto
\mathbf{G}^\dagger
\mathbf{H}_m
\mathbf{G},
$$
the error transforms as
$$
\mathbf{E}_m
\mapsto
\mathbf{G}^\dagger
\mathbf{E}_m
\mathbf{G}.
$$
Unitarily invariant norms, spectra, principal angles, and subspace fidelities are unchanged. Errors assigned to individual onsite and hopping matrix elements remain gauge dependent and must be reported only in the fixed aligned gauge.

## Error Propagation Across the Reduction Chain
Let
$$
\mathbf{H}_0
\rightarrow
\mathbf{H}_1
\rightarrow
\cdots
\rightarrow
\mathbf{H}_L
$$
be a sequence of $L$ reductions represented on compatible comparison spaces. Define the step error
$$
\mathbf{E}_{j\leftarrow j-1}
=
\mathbf{H}_j
-
\mathbf{H}_{j-1}.
$$
The total error is the telescoping sum
$$
\mathbf{H}_L
-
\mathbf{H}_0
=
\sum_{j=1}^{L}
\mathbf{E}_{j\leftarrow j-1}.
$$
For any norm satisfying the triangle inequality,
$$
\left\|
\mathbf{H}_L
-
\mathbf{H}_0
\right\|
\leq
\sum_{j=1}^{L}
\left\|
\mathbf{E}_{j\leftarrow j-1}
\right\|.
$$
This bound separates the contributions of projection, tight-binding reduction, impurity simplification, and continuum approximation.

## Acceptance Criteria
For model $m$ and dopant $d$, collect the required errors into
$$
\boldsymbol{\varepsilon}_{m,d}
=
\left(
\varepsilon_{H,m,d},
\varepsilon_{\Pi,m,d},
\left|\Delta E_{b,m,d}\right|,
1-F_{m,d},
\ldots
\right),
$$
where the ellipsis denotes additional prespecified observable errors. Let
$$
\boldsymbol{\tau}_d
=
\left(
\tau_{H,d},
\tau_{\Pi,d},
\tau_{E_b,d},
\tau_{F,d},
\ldots
\right)
$$
be the corresponding tolerances.

The model is accepted only if
$$
\boldsymbol{\varepsilon}_{m,d}
\leq
\boldsymbol{\tau}_d,
$$
where the inequality is applied component by component. Tolerances must be specified before inspecting the final reduced-model results whenever the study is intended to support a quantitative claim.

## Epistemic Interpretation
Every metric in this section measures fidelity to a specified reference operator. If the reference is a Kohnâ€“Sham or generalized Kohnâ€“Sham model, small reduction error establishes fidelity to that one-particle reference. It does not remove exchange-correlation, pseudopotential, finite-size, or quasiparticle errors already present in the parent calculation.

## References
[1] C. Davis and W. M. Kahan, "The rotation of eigenvectors by a perturbation. III," *SIAM J. Numer. Anal.*, vol. 7, no. 1, pp. 1-46, 1970, doi: 10.1137/0707001.

[2] G. W. Stewart and J.-G. Sun, *Matrix Perturbation Theory*. Boston, MA: Academic Press, 1990.