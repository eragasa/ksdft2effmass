# Bulk-Silicon Wannier-to-Tight-Binding Operator Reduction

back_to: [[ksdft2Effmass.00]]
## Scope

This section defines the reduction of the validated bulk-silicon Wannier Hamiltonian from [[ksdft2Effmass.03]] within a hierarchy of prescribed tight-binding model classes. For each model class, the reduction is examined through two complementary reconstruction procedures. The first is an inverse spectral reconstruction from retained band data. The second is a direct operator reconstruction from matrix elements in an aligned localized representation.

Each procedure defines a set of admissible tight-binding Hamiltonians rather than necessarily selecting a unique reconstruction. The purpose is to determine

1. which restricted lattice Hamiltonians reproduce the prescribed bulk band-edge physics;
2. which Hamiltonians approximate the aligned Wannier operator within the prescribed operator tolerance;
3. whether the two procedures admit at least one common Hamiltonian;
4. which first-principles operator components are lost under the restriction; and
5. the smallest tested model class for which spectral and operator compatibility is achieved.

The reference object is the bulk Wannier Hamiltonian $\mathbf{H}_{\mathrm{W},b}(\mathbf{R}) \in \mathbb{C}^{M_{\mathrm{W}}\times M_{\mathrm{W}}},$ where $\mathbf{R}$ is a bulk-silicon lattice vector and $M_{\mathrm{W}}$ is the number of Wannier orbitals per unit cell.

For model class $\mathfrak{M}_m$, the candidate reduced object is the parameterized tight-binding Hamiltonian

$$
\mathbf{H}_{\mathrm{TB},b}^{(m)}
\left(
\mathbf{R};
\boldsymbol{\theta}
\right),
\qquad
\boldsymbol{\theta}\in\Theta_m,
$$

where $\Theta_m$ is the admissible parameter domain of $\mathfrak{M}_m$. The nested model hierarchy permits the orbital content, interaction range, or symmetry-allowed matrix elements to be enlarged systematically when a smaller class cannot satisfy the prescribed requirements.

The spectral reconstruction constrains $\boldsymbol{\theta}$ through selected eigenvalues and derived band-edge observables. The operator reconstruction constrains the same parameter vector through the difference between the candidate tight-binding Hamiltonian and the aligned Wannier Hamiltonian. Compatibility requires that a single parameter vector satisfy both sets of constraints.

The subscript $\mathrm{W}$ identifies the Wannier representation, while $\mathrm{TB}$ identifies the prescribed tight-binding representation. The two Hamiltonians may be compared at the matrix level only after their state spaces, orbital ordering, phase conventions, and local coordinate systems have been aligned. The residual remaining after this alignment identifies the operator content that cannot be represented within model class $\mathfrak{M}_m$.
## Parallel Reconstructions from the First-Principles Reference

The converged bulk Kohn–Sham calculation first defines the selected projected operator. Wannierization then represents this operator in a localized basis:

$$
\hat{H}_{\mathrm{KS},b}
\longrightarrow
\hat{H}_{b}^{(P)}
\longrightarrow
\mathbf{H}_{\mathrm{W},b}.
$$

Here, $\hat{H}_{b}^{(P)}$ is the Kohn–Sham operator restricted to the target subspace defined in [[ksdft2Effmass.03]], and $\mathbf{H}_{\mathrm{W},b}$ is its validated Wannier representation. Wannierization is principally a representation problem: it selects a localized basis for the projected operator without imposing the restricted structure of a prescribed Slater–Koster model class.

The Wannier Hamiltonian then supports two parallel tight-binding reconstruction problems:

$$
\mathbf{H}_{\mathrm{W},b}
\longrightarrow
\begin{cases}
\text{retained spectral data},\\
\text{aligned localized matrix elements},
\end{cases}
\longrightarrow
\begin{cases}
\mathcal{A}_{\mathrm{spec}}^{(m)},\\
\mathcal{A}_{\mathrm{op}}^{(m)}.
\end{cases}
$$

The retained spectral data are used in an inverse problem to infer parameters of the prescribed tight-binding class $\mathfrak{M}_m$. These data include selected band energies and derived bulk observables such as the indirect gap, conduction-valley position, and effective masses. They define the spectrally admissible parameter set

$$
\mathcal{A}_{\mathrm{spec}}^{(m)}
\subseteq
\Theta_m.
$$

The aligned localized matrix elements are used in a direct approximation problem. The candidate tight-binding Hamiltonian is compared with the Wannier Hamiltonian after their state spaces and orbital coordinates have been aligned. This comparison defines the operator-admissible parameter set

$$
\mathcal{A}_{\mathrm{op}}^{(m)}
\subseteq
\Theta_m.
$$

Both procedures therefore produce candidate Hamiltonians within the same model class,

$$
\mathbf{H}_{\mathrm{TB},b}^{(m)}
\left(
\mathbf{R};
\boldsymbol{\theta}
\right),
\qquad
\boldsymbol{\theta}\in\Theta_m,
$$

but they constrain the parameter vector using different information from the common first-principles reference. The spectral reconstruction constrains the eigenvalue behavior of the candidate Hamiltonian, while the operator reconstruction constrains its aligned real-space matrix representation.

The Wannier Hamiltonian is adopted as their common parent because it retains the selected projected Kohn–Sham information, reproduces the validated band data, and exposes the onsite, orbital, hopping, and spatial structure required for direct operator comparison. The retained spectral targets may be evaluated from either the projected Kohn–Sham calculation or its validated Wannier representation, provided that their agreement has already been established over the relevant bands and wavevectors.

Complete spectral information can reconstruct a finite-dimensional operator when both its eigenvalues and spectral projectors are retained:

$$
\hat{H}
=
\sum_n
E_n
\hat{P}_n.
$$

Eigenvalues alone do not generally determine an operator because they omit the spectral projectors and are invariant under unitary changes of eigenvectors. Within a sufficiently restricted and identifiable parameterized model class, however, a prescribed collection of eigenvalues may uniquely determine the model parameters.

The finite spectral targets retained here are not assumed to provide such uniqueness. Instead, they define a set of spectrally admissible tight-binding Hamiltonians. Likewise, the finite operator tolerance defines a set of operator-admissible Hamiltonians. Compatibility requires that the two reconstruction problems admit at least one common parameter vector:

$$
\boxed{
\mathcal{A}_{\mathrm{spec}}^{(m)}
\cap
\mathcal{A}_{\mathrm{op}}^{(m)}
\neq
\varnothing
}.
$$

The two tight-binding reductions are therefore parallel only after the common Wannier reference has been constructed. Their purpose is not to determine which reconstruction is preferable, but to determine whether spectral preservation and aligned-operator approximation can be realized by the same restricted lattice Hamiltonian.

## Tight-Binding State Space
Let
$$
\left\{
\lvert\chi_{\mu\mathbf{R}}\rangle
\right\}_{\mu=1}^{M_{\mathrm{TB}}}
$$
be an orthonormal tight-binding basis, where $\mu$ labels an orbital in the unit cell and $\mathbf{R}$ labels the lattice cell. The tight-binding state space is generated by all lattice translations of the $M_{\mathrm{TB}}$ cell orbitals.

For the initial bulk-silicon study, the prescribed model is an orthogonal $sp^3s^*$ model. Each silicon site carries the orbital set
$$
\left\{
\lvert s\rangle,
\lvert p_x\rangle,
\lvert p_y\rangle,
\lvert p_z\rangle,
\lvert s^*\rangle
\right\}.
$$
The symbols $s$, $p_x$, $p_y$, and $p_z$ denote the usual valence-like atomic-orbital channels, while $s^*$ denotes an additional excited $s$-like orbital introduced to improve the conduction-band description.

The orbital count $M_{\mathrm{TB}}$ depends on the number of silicon sites in the chosen unit cell and on whether spin is included explicitly. The initial model must state this count, orbital ordering, spin convention, and hopping range before parameter fitting begins.

## Tight-Binding Hamiltonian
The real-space tight-binding matrix elements are
$$
\left[
\mathbf{H}_{\mathrm{TB},b}(\mathbf{R};\boldsymbol{\theta})
\right]_{\mu\nu}
=
\left\langle
\chi_{\mu\mathbf{0}}
\middle|
\hat{H}_{\mathrm{TB},b}(\boldsymbol{\theta})
\middle|
\chi_{\nu\mathbf{R}}
\right\rangle.
$$
The onsite block corresponds to $\mathbf{R}=\mathbf{0}$, while $\mathbf{R}\neq\mathbf{0}$ contains intercell hopping terms.

The Bloch Hamiltonian is obtained by Fourier transformation:
$$
\mathbf{H}_{\mathrm{TB},b}(\mathbf{k};\boldsymbol{\theta})
=
\sum_{\mathbf{R}}
e^{i\mathbf{k}\cdot\mathbf{R}}
\mathbf{H}_{\mathrm{TB},b}(\mathbf{R};\boldsymbol{\theta}),
$$
where $\mathbf{k}$ is a Bloch wavevector in the bulk Brillouin zone. Hermiticity requires
$$
\mathbf{H}_{\mathrm{TB},b}(-\mathbf{R};\boldsymbol{\theta})
=
\mathbf{H}_{\mathrm{TB},b}(\mathbf{R};\boldsymbol{\theta})^\dagger.
$$

In a Slater-Koster parameterization, crystal symmetry and bond geometry determine the angular dependence of the hopping matrices. The parameter vector $\boldsymbol{\theta}$ contains only the independent onsite energies and two-center hopping integrals retained by the chosen model class.

## Common Operator Representation
Let
$$
\mathcal{H}_{\mathrm{W},\mathbf{k}}
\cong
\mathbb{C}^{M_{\mathrm{W}}},
\qquad
\mathcal{H}_{\mathrm{TB},\mathbf{k}}
\cong
\mathbb{C}^{M_{\mathrm{TB}}}
$$
denote the Wannier and tight-binding coordinate spaces at wavevector $\mathbf{k}$. A raw matrix residual is defined only after these spaces have been related.

If $M_{\mathrm{W}}=M_{\mathrm{TB}}=M$ and a physically justified orbital correspondence exists, let
$$
\mathbf{C}(\mathbf{k})
\in
U(M)
$$
be the unitary alignment matrix from tight-binding coordinates to Wannier coordinates. The aligned tight-binding Hamiltonian is
$$
\widetilde{\mathbf{H}}_{\mathrm{TB},b}(\mathbf{k};\boldsymbol{\theta})
=
\mathbf{C}(\mathbf{k})
\mathbf{H}_{\mathrm{TB},b}(\mathbf{k};\boldsymbol{\theta})
\mathbf{C}(\mathbf{k})^\dagger.
$$
Both $\widetilde{\mathbf{H}}_{\mathrm{TB},b}$ and $\mathbf{H}_{\mathrm{W},b}$ then act on the Wannier coordinate space.

If $M_{\mathrm{W}}\neq M_{\mathrm{TB}}$, direct full-space operator matching is not available. The comparison must instead be restricted to a common matched subspace or to specified spectra and observables. Any unmatched operator content must be reported as part of the model-class limitation.

## Operator Residual
After alignment, define the Bloch-space residual by
$$
\boxed{
\mathbf{R}_{\mathrm{TB}}(\mathbf{k};\boldsymbol{\theta})
=
\mathbf{H}_{\mathrm{W},b}(\mathbf{k})
-
\widetilde{\mathbf{H}}_{\mathrm{TB},b}(\mathbf{k};\boldsymbol{\theta})
}.
$$
The matrix $\mathbf{R}_{\mathrm{TB}}(\mathbf{k};\boldsymbol{\theta})$ contains the operator content present in the Wannier reference but not reproduced by the tight-binding model at wavevector $\mathbf{k}$.

When the real-space bases are aligned by a cell-local unitary matrix $\mathbf{C}$ that is independent of $\mathbf{k}$, the real-space residual is
$$
\mathbf{R}_{\mathrm{TB}}(\mathbf{R};\boldsymbol{\theta})
=
\mathbf{H}_{\mathrm{W},b}(\mathbf{R})
-
\mathbf{C}
\mathbf{H}_{\mathrm{TB},b}(\mathbf{R};\boldsymbol{\theta})
\mathbf{C}^\dagger.
$$
This representation permits the residual to be resolved by hopping distance, orbital channel, and lattice symmetry.

## Restricted Operator Model Class
Let
$$
\mathfrak{M}_m
=
\operatorname{span}
\left\{
\mathbf{B}_1^{(m)},
\ldots,
\mathbf{B}_{N_m}^{(m)}
\right\}
$$
be a tight-binding model class at complexity level $m$. The matrices $\mathbf{B}_a^{(m)}(\mathbf{R})$ are allowed Hermitian operator components, $N_m$ is the number of independent components, and the span is restricted by the crystal symmetry, orbital basis, and hopping range.

A model in this class is
$$
\mathbf{H}_m(\mathbf{R};\boldsymbol{\theta})
=
\sum_{a=1}^{N_m}
\theta_a
\mathbf{B}_a^{(m)}(\mathbf{R}),
$$
where $\theta_a$ is the coefficient of the $a$th allowed operator component.

Let $\Theta_m\subseteq\mathbb{R}^{N_m}$ denote the admissible parameter domain for class $\mathfrak{M}_m$, including all declared physical, symmetry, and boundedness constraints.

The initial hierarchy may be chosen as
$$
\mathfrak{M}_1
\subset
\mathfrak{M}_2
\subset
\mathfrak{M}_3,
$$
where $\mathfrak{M}_1$ is the nearest-neighbor orthogonal $sp^3s^*$ model, $\mathfrak{M}_2$ adds second-neighbor terms, and $\mathfrak{M}_3$ adds only those symmetry-allowed channels identified as important in the residual of $\mathfrak{M}_2$.

## Spectral Observation Map
Let
$$
\mathcal{S}
:
\mathbf{H}(\mathbf{k})
\longmapsto
\mathbf{y}_{\mathrm{spec}}[\mathbf{H}]
$$
denote the spectral observation map. For the bulk-silicon pilot, the vector $\mathbf{y}_{\mathrm{spec}}$ contains the retained band energies, indirect gap, conduction-valley position, and longitudinal and transverse electron effective masses.

The reference spectral vector is
$$
\mathbf{y}_{\mathrm{spec}}^{\mathrm{ref}}
=
\mathcal{S}
\left[
\mathbf{H}_{\mathrm{W},b}
\right].
$$

For model class $\mathfrak{M}_m$, the corresponding spectral forward map is
$$
\mathcal{F}_{\mathrm{spec}}^{(m)}
:
\boldsymbol{\theta}
\longmapsto
\mathcal{S}
\left[
\mathbf{H}_m(\boldsymbol{\theta})
\right].
$$

The model class is spectrally identifiable on a parameter domain $\Theta_m$ only if $\mathcal{F}_{\mathrm{spec}}^{(m)}$ is injective after known gauge, sign, orbital-label, and parameter symmetries have been quotiented out. Identifiability is a property to be tested, not assumed.
## Weighted Operator Inner Product
For two real-space operator matrices $\mathbf{A}(\mathbf{R})$ and $\mathbf{B}(\mathbf{R})$, define
$$
\left\langle
\mathbf{A},
\mathbf{B}
\right\rangle_w
=
\sum_{\mathbf{R}}
w_{\mathbf{R}}
\operatorname{Tr}
\left[
\mathbf{A}(\mathbf{R})^\dagger
\mathbf{B}(\mathbf{R})
\right].
$$
Here, $w_{\mathbf{R}}\geq0$ is a specified weight assigned to displacement $\mathbf{R}$, and $\operatorname{Tr}$ is the matrix trace. The induced norm is
$$
\left\|
\mathbf{A}
\right\|_w
=
\left[
\left\langle
\mathbf{A},
\mathbf{A}
\right\rangle_w
\right]^{1/2}.
$$
The weights may emphasize short-range blocks, particular orbital sectors, or all retained matrix elements equally. Their choice is part of the model definition and must be recorded.

## Direct Aligned-Operator Reconstruction
Before parameter-domain constraints are imposed, the closest operator in the linear span $\mathfrak{M}_m$ is
$$
\boxed{
\mathbf{H}_m^*
=
\Pi_{\mathfrak{M}_m}
\mathbf{H}_{\mathrm{W},b}
=
\operatorname*{arg\,min}_{\mathbf{H}\in\mathfrak{M}_m}
\left\|
\mathbf{H}_{\mathrm{W},b}
-
\mathbf{H}
\right\|_w^2
}.
$$
The symbol $\Pi_{\mathfrak{M}_m}$ denotes orthogonal projection onto the linear model span with respect to the weighted operator inner product. The discarded operator content is
$$
\mathbf{E}_{\mathrm{class},m}
=
\left(
\mathcal{I}_{\mathrm{op}}
-
\Pi_{\mathfrak{M}_m}
\right)
\mathbf{H}_{\mathrm{W},b},
$$
where $\mathcal{I}_{\mathrm{op}}$ denotes the identity map on the vector space of represented operators.

If the implemented parameterized model is $\mathbf{H}_m(\boldsymbol{\theta}_m^*)$, the total residual separates as
$$
\boxed{
\mathbf{H}_{\mathrm{W},b}
-
\mathbf{H}_m(\boldsymbol{\theta}_m^*)
=
\mathbf{E}_{\mathrm{class},m}
+
\mathbf{E}_{\mathrm{fit},m}
},
$$
where
$$
\mathbf{E}_{\mathrm{fit},m}
=
\Pi_{\mathfrak{M}_m}
\mathbf{H}_{\mathrm{W},b}
-
\mathbf{H}_m(\boldsymbol{\theta}_m^*)
$$
is the fitting or implementation error within the selected model class. This decomposition distinguishes failure of the model class from failure of the fitting procedure.

When the parameterization spans the declared class exactly, a representative direct operator reconstruction may be written as
$$
\boldsymbol{\theta}_{\mathrm{op},m}^{*}
\in
\operatorname*{arg\,min}_{\boldsymbol{\theta}\in\Theta_m}
\left\|
\mathbf{H}_{\mathrm{W},b}
-
\widetilde{\mathbf{H}}_m(\boldsymbol{\theta})
\right\|_w^2.
$$
The use of $\in$ permits multiple minimizers.

## Inverse Spectral Reconstruction
Let $\mathbf{W}_{\mathrm{spec}}$ be a declared diagonal scaling-and-weighting matrix for the heterogeneous spectral targets. Define
$$
\varepsilon_{\mathrm{spec},m}(\boldsymbol{\theta})
=
\left\|
\mathbf{W}_{\mathrm{spec}}
\left(
\mathcal{F}_{\mathrm{spec}}^{(m)}(\boldsymbol{\theta})
-
\mathbf{y}_{\mathrm{spec}}^{\mathrm{ref}}
\right)
\right\|_2.
$$

A representative inverse spectral reconstruction is
$$
\boldsymbol{\theta}_{\mathrm{spec},m}^{*}
\in
\operatorname*{arg\,min}_{\boldsymbol{\theta}\in\Theta_m}
\varepsilon_{\mathrm{spec},m}(\boldsymbol{\theta}).
$$
This optimizer is not assumed to be unique.

Define the normalized aligned-operator error by
$$
\varepsilon_{\mathrm{op},m}(\boldsymbol{\theta})
=
\frac{
\left\|
\mathbf{H}_{\mathrm{W},b}
-
\widetilde{\mathbf{H}}_m(\boldsymbol{\theta})
\right\|_w
}{
\left\|
\mathbf{H}_{\mathrm{W},b}
\right\|_w
}.
$$

## Admissible Sets and Compatibility
For prescribed tolerances $\tau_{\mathrm{spec},m}$ and $\tau_{\mathrm{op},m}$, define
$$
\mathcal{A}_{\mathrm{spec}}^{(m)}
=
\left\{
\boldsymbol{\theta}\in\Theta_m:
\varepsilon_{\mathrm{spec},m}(\boldsymbol{\theta})
\leq
\tau_{\mathrm{spec},m}
\right\}
$$
and
$$
\mathcal{A}_{\mathrm{op}}^{(m)}
=
\left\{
\boldsymbol{\theta}\in\Theta_m:
\varepsilon_{\mathrm{op},m}(\boldsymbol{\theta})
\leq
\tau_{\mathrm{op},m}
\right\}.
$$

The model class $\mathfrak{M}_m$ is compatible with the retained spectral and aligned-operator information if
$$
\boxed{
\mathcal{A}_{\mathrm{spec}}^{(m)}
\cap
\mathcal{A}_{\mathrm{op}}^{(m)}
\neq
\varnothing
}.
$$

This condition requires one Hamiltonian to satisfy both criteria. Agreement between two separately selected best fits is neither necessary nor sufficient for compatibility. When the intersection is empty, the separation of the Hamiltonian images of the two admissible sets is evaluated using the normalized real-space metric defined in [[ksdft2Effmass.08]].

The smallest compatible tested class is
$$
m^*
=
\min
\left\{
m:
\mathcal{A}_{\mathrm{spec}}^{(m)}
\cap
\mathcal{A}_{\mathrm{op}}^{(m)}
\neq
\varnothing
\right\}.
$$
If this index set is empty, no tested model class is compatible at the prescribed tolerances.

## Combined Operator and Spectral Objective
Operator matching may be supplemented by band-edge constraints. Define
$$
\mathcal{L}(\boldsymbol{\theta})
=
\lambda_H
\mathcal{L}_H(\boldsymbol{\theta})
+
\lambda_E
\mathcal{L}_E(\boldsymbol{\theta})
+
\lambda_O
\mathcal{L}_O(\boldsymbol{\theta}),
$$
where $\mathcal{L}_H$ is the operator residual, $\mathcal{L}_E$ is a band-energy loss, $\mathcal{L}_O$ is an observable loss, and the nonnegative coefficients $\lambda_H$, $\lambda_E$, and $\lambda_O$ specify their relative weights.

A representative operator loss is
$$
\mathcal{L}_H(\boldsymbol{\theta})
=
\sum_{\mathbf{k}\in\mathcal{K}_{\mathrm{fit}}}
w_{\mathbf{k}}
\left\|
\mathbf{R}_{\mathrm{TB}}(\mathbf{k};\boldsymbol{\theta})
\right\|_{\mathrm{F}}^2,
$$
where $\mathcal{K}_{\mathrm{fit}}$ is the fitting set, $w_{\mathbf{k}}\geq0$ is a wavevector weight, and $\|\cdot\|_{\mathrm{F}}$ is the Frobenius norm.

For a matrix $\mathbf{A}$, the Frobenius norm is
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
\right]^{1/2}.
$$

The optimized parameter vector is
$$
\boldsymbol{\theta}^*
=
\operatorname*{arg\,min}_{\boldsymbol{\theta}\in\Theta}
\mathcal{L}(\boldsymbol{\theta}).
$$
A disjoint validation set $\mathcal{K}_{\mathrm{val}}$ must be retained so that interpolation and predictive errors are not evaluated only on fitted wavevectors.

## Bulk Physical Validation
The bulk model must be evaluated against the same definitions used for the DFT and Wannier references. The required quantities include the indirect band gap, conduction-valley position, longitudinal and transverse electron effective masses, selected valence-band curvatures, and validation-set band errors.

For a nondegenerate band extremum at $\mathbf{k}_0$, define the inverse effective-mass tensor by
$$
\left[
\mathbf{m}_n^{*-1}
\right]_{ij}
=
\frac{1}{\hbar^2}
\left.
\frac{\partial^2 E_n(\mathbf{k})}
{\partial k_i\partial k_j}
\right|_{\mathbf{k}=\mathbf{k}_0},
$$
where $E_n(\mathbf{k})$ is the band energy, $\hbar$ is the reduced Planck constant, and $i,j\in\{x,y,z\}$ label Cartesian reciprocal-space components.

Spectral reconstruction may recover the aligned operator when the retained data identify the model within the prescribed class. Spectral acceptance alone, however, does not establish that this has occurred. The operator residual must therefore be inspected to determine whether errors arise from omitted hopping range, orbital mixing, symmetry channels, or alignment failure.

## Error, Complexity, and Joint Feasibility

The reduction of an aligned Wannier Hamiltonian to a restricted Slater–Koster model requires both a choice of model class and a criterion for determining when that class is adequate. Wannier interpolation provides a localized representation of the projected first-principles operator, but restricting its orbital content, neighbor range, or symmetry-allowed matrix elements introduces a model-class residual [^3]. Empirical tight-binding models address this restriction by introducing compact parameterizations designed to reproduce selected electronic properties [^2] [^5] [^6] [^7].

Two complementary approaches can be used to select among the nested model classes, $\mathfrak{M}_1 \subset \mathfrak{M}_2 \subset \cdots \subset \mathfrak{M}_{M_{\mathrm{class}}}$.

The first examines how the best attainable errors change with model complexity. The second asks whether a single parameter vector can satisfy the spectral and aligned-operator requirements simultaneously.

### Approach 1: Error versus Complexity

For each model class $\mathfrak{M}_m$, let $\Theta_m$ denote its parameter space and let $N_m$ be the number of independent parameters. Define the best separately attainable spectral and aligned-operator errors defined respectively,

$$\begin{align}
\varepsilon_{\mathrm{spec},m}^{\min}
	= \inf_{\boldsymbol{\theta}\in\Theta_m}
		\varepsilon_{\mathrm{spec}}
		\left(\boldsymbol{\theta}\right)
\\
\varepsilon_{\mathrm{op},m}^{\min}
	= \inf_{\boldsymbol{\theta}\in\Theta_m}
	\varepsilon_{\mathrm{op}}
	\left(\boldsymbol{\theta}\right).
\end{align}$$
The sequence

$$
\left\{
\left(
N_m,
\varepsilon_{\mathrm{spec},m}^{\min},
\varepsilon_{\mathrm{op},m}^{\min}
\right)
\right\}_{m=1}^{M_{\mathrm{class}}}
$$

defines an error-versus-complexity relation for the nested model hierarchy. Physical validation errors, including errors in the indirect gap, conduction-valley position, and electron effective masses, may be recorded as additional components.

This approach has direct precedents in empirical tight-binding parameterization. The nearest-neighbor $sp^3s^*$ model of Vogl, Hjalmarson, and Dow introduced a compact parameterization capable of reproducing the principal features of the band structures of tetrahedrally bonded semiconductors [^2]. Larger bases, such as the $sp^3d^5s^*$ model of Jancu et al., were subsequently introduced to remove limitations of smaller model classes [^6].

For silicon, Klimeck et al. compared nearest- and second-nearest-neighbor $sp^3s^*$ models and found that no satisfactory global fit to the required electron and hole properties could be obtained within the nearest-neighbor class, whereas the second-neighbor class provided sufficient flexibility [^5]. More recent work has similarly constructed tight-binding Hamiltonians to prescribed band-structure accuracy while varying the retained real-space Hamiltonian matrices or interaction range [^7]. These studies support the use of a nested hierarchy in which additional orbitals, neighbor shells, or interaction terms are introduced only when a smaller model class cannot reproduce the required physics.

The error-versus-complexity relation identifies diminishing returns and resolved improvements associated with additional parameters. It does not, however, establish that the separately minimized spectral and operator errors are attained by the same parameter vector. It is possible that

$$
\varepsilon_{\mathrm{spec},m}^{\min}
<
\tau_{\mathrm{spec}}
$$

and

$$
\varepsilon_{\mathrm{op},m}^{\min}
<
\tau_{\mathrm{op}}
$$

while no single Hamiltonian satisfies both inequalities.

This limitation is physically important because spectral agreement alone does not determine the underlying operator representation. Tight-binding models with similar band energies can produce different eigenvectors, matrix elements, and response functions. Ghosh, Schankler, and Rappe demonstrated that accurate band structures are necessary but insufficient for accurate optoelectronic responses when the relevant wavefunctions and velocity matrix elements are not also preserved [^8].

### Approach 2: Joint Feasibility

The second approach treats each prescribed tolerance as defining an admissible subset of the parameter space. For model class $\mathfrak{M}_m$, define

$$\begin{align}
\mathcal{A}_{\mathrm{spec}}^{(m)}
	= \left\{
		\boldsymbol{\theta}\in\Theta_m
		: \varepsilon_{\mathrm{spec}}
		\left( \boldsymbol{\theta} \right)
		\leq \tau_{\mathrm{spec}}
	\right\} \\
\mathcal{A}_{\mathrm{op}}^{(m)}
	= \left\{
		\boldsymbol{\theta}\in\Theta_m
		: \varepsilon_{\mathrm{op}}
		\left( \boldsymbol{\theta} \right)
		\leq \tau_{\mathrm{op}}
	\right\}.
\end{align}$$

The model class is jointly feasible when

$$
\boxed{
\mathcal{A}_{\mathrm{spec}}^{(m)}
	\cap \mathcal{A}_{\mathrm{op}}^{(m)}
	\neq \varnothing
}.
$$

This construction is closely related to set-membership identification, in which bounded errors define a feasible parameter set containing all models consistent with the prescribed information [^9]. It is also a multiobjective optimization problem. Define the error map

$$
\mathbf{f}_m
\left(
\boldsymbol{\theta}
\right)
=
\left(
\varepsilon_{\mathrm{spec}}
\left(
\boldsymbol{\theta}
\right),
\varepsilon_{\mathrm{op}}
\left(
\boldsymbol{\theta}
\right),
\varepsilon_{\mathrm{phys}}
\left(
\boldsymbol{\theta}
\right)
\right)
$$

and its attainable error set

$$
\mathcal{Y}_m
=
\left\{
\mathbf{f}_m
\left(
\boldsymbol{\theta}
\right)
:
\boldsymbol{\theta}\in\Theta_m
\right\}.
$$

The prescribed tolerances define the acceptable error region

$$
\mathcal{T}
=
\left[
0,
\tau_{\mathrm{spec}}
\right]
\times
\left[
0,
\tau_{\mathrm{op}}
\right]
\times
\left[
0,
\tau_{\mathrm{phys}}
\right].
$$

Joint feasibility is then equivalent to

$$
\mathcal{Y}_m
\cap
\mathcal{T}
\neq
\varnothing.
$$

The boundary of $\mathcal{Y}_m$ relevant to simultaneous error reduction is its Pareto front [^10]. Parameter vectors on this front represent reductions for which one error cannot be decreased without increasing at least one other error.

Ragasa et al. used this construction in the parameterization of an interatomic potential for MgO [^11]. Rather than combining errors in different material properties through prespecified scalar weights, the method identified the Pareto hypersurface of attainable property errors and retained an ensemble of nondominated parameterizations. The present reduction problem uses the same underlying idea but applies it to errors with different mathematical content: spectral error measures the eigenvalue representation, whereas aligned-operator error measures the real-space Hamiltonian representation.

The admissible-set formulation adds an absolute physical decision to the relative ordering provided by the Pareto front. A parameter vector may be Pareto optimal without satisfying the required tolerances. Conversely, any point in

$$
\mathcal{Y}_m
\cap
\mathcal{T}
$$

corresponds to a Hamiltonian that is simultaneously acceptable under all retained criteria.

### Combined Model-Selection Criterion

The two approaches are complementary. The error-versus-complexity relation characterizes how the representational capacity of the model changes across the hierarchy. Joint feasibility determines whether that capacity is sufficient to produce one Hamiltonian satisfying all requirements simultaneously.

The preferred model class is therefore

$$
\boxed{
m^*
=
\min
\left\{
m
:
\mathcal{Y}_m
\cap
\mathcal{T}
\neq
\varnothing
\right\}
}.
$$

Equivalently, $m^*$ is the least complex class for which there exists a parameter vector

$$
\boldsymbol{\theta}_{m^*}^*
\in
\mathcal{A}_{\mathrm{spec}}^{(m^*)}
\cap
\mathcal{A}_{\mathrm{op}}^{(m^*)}
$$

that also satisfies the prescribed physical validation tolerances.

The error-versus-complexity curves and Pareto fronts remain diagnostically important even when the intersection is empty. They show whether increasing model complexity reduces both errors, merely transfers error between the two objectives, or exposes a residual that cannot be represented within the tested hierarchy.

Additional parameters are justified when they do at least one of the following:

1. establish a previously absent intersection with the acceptable error region;
2. enlarge an intersection that is too narrow or numerically unstable;
3. remove a resolved and physically relevant component of the operator residual; or
4. improve a retained bulk observable that remains outside its prescribed tolerance.

The resulting procedure does not impose a scalar trade-off between spectral preservation and operator alignment. It determines the attainable trade-off for each model class and selects the smallest class containing at least one jointly admissible and physically validated Hamiltonian.

## References



## Validation Requirements
The bulk reduction is accepted only after:

1. the DFT reference has been converged and frozen;
2. the Wannier Hamiltonian has passed the validation requirements of [[ksdft2Effmass.03]];
3. the Wannier and tight-binding state spaces have a documented orbital correspondence or alignment map;
4. the tight-binding implementation satisfies Hermiticity and silicon symmetry constraints;
5. model-class and fitting errors have been separated;
6. fitting and validation wavevectors are disjoint;
7. spectral identifiability or non-identifiability has been reported for each model class;
8. the spectral- and aligned-operator-admissible sets have been constructed using prespecified tolerances;
9. compatibility has been decided by testing their intersection;
10. band-edge quantities and operator residuals satisfy stated tolerances for at least one common Hamiltonian;
11. the dependence of the result on model complexity has been reported.

## Role in the Reduction Program

The bulk reduction is formulated as the joint feasibility problem

$$
\boxed{
\text{find }
\boldsymbol{\theta}
\in
\mathcal{A}_{\mathrm{spec}}^{(m)}
\cap
\mathcal{A}_{\mathrm{op}}^{(m)}
}.
$$

If this intersection is nonempty, a parameter vector $\boldsymbol{\theta}_m^* \in \mathcal{A}_{\mathrm{spec}}^{(m)} \cap\mathcal{A}_{\mathrm{op}}^{(m)}$ defines an admissible reduced Hamiltonian
$$
  \mathbf{H}_{\mathrm{TB},b}^{(m),*}
    =\mathbf{H}_{\mathrm{TB},b}^{(m)}
    \left(\boldsymbol{\theta}_m^*\right).
$$
Relative to the aligned bulk Wannier Hamiltonian, the resulting operator decomposition is

$$
\boxed{
\mathbf{H}_{\mathrm{W},b}
	= \mathbf{H}_{\mathrm{TB},b}^{(m),*}
	+ \mathbf{E}_{\mathrm{class},m}
},
$$

where $\mathbf{E}_{\mathrm{class},m}=\mathbf{H}_{\mathrm{W},b}-\mathbf{H}_{\mathrm{TB},b}^{(m),*}$ is the residual associated with model class $m$. This residual identifies the first-principles operator components that cannot be represented by the selected tight-binding Hamiltonian. Membership in $\mathcal{A}_{\mathrm{op}}^{(m)}$ bounds the magnitude and structure of this residual, while membership in $\mathcal{A}_{\mathrm{spec}}^{(m)}$ establishes that the required bulk band-edge physics survives the reduction.

If the intersection is empty, no Hamiltonian in model class $m$ satisfies both prescribed criteria. The model class must then be enlarged, the tolerances revised, or the incompatibility between spectral preservation and operator alignment explicitly quantified.

This bulk reduction must be validated before impurity terms are transferred into the same restricted lattice model. The extraction of the first-principles dopant perturbation is developed in [[ksdft2Effmass.06]].
## References
[^1]: J. C. Slater and G. F. Koster, "Simplified LCAO method for the periodic potential problem," *Phys. Rev.*, vol. 94, pp. 1498-1524, 1954, doi: 10.1103/PhysRev.94.1498.

[^2]: P. Vogl, H. P. Hjalmarson, and J. D. Dow, "A semi-empirical tight-binding theory of the electronic structure of semiconductors," *J. Phys. Chem. Solids*, vol. 44, no. 5, pp. 365-378, 1983, doi: 10.1016/0022-3697(83)90064-1.

[^3]: N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, "Maximally localized Wannier functions: Theory and applications," *Rev. Mod. Phys.*, vol. 84, pp. 1419-1475, 2012, doi: 10.1103/RevModPhys.84.1419.

[^4]: J. R. Yates, X. Wang, D. Vanderbilt, and I. Souza, "Spectral and Fermi surface properties from Wannier interpolation," *Phys. Rev. B*, vol. 75, Art. no. 195121, 2007, doi: 10.1103/PhysRevB.75.195121.

[^5]: G. Klimeck, R. C. Bowen, T. B. Boykin, C. Salazar-Lazaro, T. A. Cwik, and A. Stoica, "Si tight-binding parameters from genetic algorithm fitting," *Superlattices Microstruct.*, vol. 27, nos. 2--3, pp. 77--88, 2000, doi: 10.1006/spmi.1999.0797.

[^6]: Jancu, J.-M., Scholz, R., Beltram, F., and Bassani, F. “Empirical $spds^*$ tight-binding calculation for cubic semiconductors: General method and material parameters.” *Physical Review B* **57**, 6493–6507 (1998). [https://doi.org/10.1103/PhysRevB.57.6493](https://doi.org/10.1103/PhysRevB.57.6493)

[^7]: Wang, Z., Ye, S., Wang, H., He, J., Huang, Q., and Chang, S. “Machine learning method for tight-binding Hamiltonian parameterization from ab-initio band structure.” *npj Computational Materials* **7**, 11 (2021). [https://doi.org/10.1038/s41524-020-00490-5](https://doi.org/10.1038/s41524-020-00490-5)

[^8]: Ghosh, A., Schankler, A. M., and Rappe, A. M. “Choosing tight-binding models for accurate optoelectronic responses.” *Physical Review B* **111**, 125203 (2025). [https://doi.org/10.1103/PhysRevB.111.125203](https://doi.org/10.1103/PhysRevB.111.125203)

[^9]: Milanese, M., and Vicino, A. “Optimal estimation theory for dynamic systems with set membership uncertainty: An overview.” *Automatica* **27**, 997–1009 (1991). [https://doi.org/10.1016/0005-1098(91)90134-N](https://doi.org/10.1016/0005-1098(91)90134-N)

[^10]: Emmerich, M. T. M., and Deutz, A. H. “A tutorial on multiobjective optimization: Fundamentals and evolutionary methods.” *Natural Computing* **17**, 585–609 (2018). [https://doi.org/10.1007/s11047-018-9685-y](https://doi.org/10.1007/s11047-018-9685-y)

[^11]: Ragasa, E. J., O’Brien, C. J., Hennig, R. G., Foiles, S. M., and Phillpot, S. R. “Multi-objective optimization of interatomic potentials with application to MgO.” *Modelling and Simulation in Materials Science and Engineering* **27**, 074007 (2019). [https://doi.org/10.1088/1361-651X/ab28d9](https://doi.org/10.1088/1361-651X/ab28d9)
