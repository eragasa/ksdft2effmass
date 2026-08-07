# Projected Bloch State Spaces and Operators

back_to: [[ksdft2Effmass.00]]
## Scope
This section defines the state spaces, projectors, and compressed operators used throughout the reduction program. The construction is stated for Kohn-Sham operators, although it applies to any periodic one-particle Bloch Hamiltonian.

The principal distinction is among:
1. the full one-particle operator;
2. the family of target Bloch subspaces;
3. the operator compressed to those subspaces;
4. a matrix representation of the compressed operator.

Wannier construction supplies a localized representation of the projected family and is developed separately in [[ksdft2Effmass.03]]. Identification and comparison of state spaces obtained from different calculations are developed in [[ksdft2Effmass.04]].

## First-Principles Systems

Let $\mathcal{D}=\{\mathrm{P},\mathrm{B}\}$ denote the set of dopant species considered in this work, where $\mathrm{P}$ and $\mathrm{B}$ represent phosphorus and boron, respectively. For each dopant $d\in\mathcal{D}$, define the corresponding set of system labels by $\mathcal{S}_d=\{b,d\}$. The index $s\in\mathcal{S}_d$ labels either pristine bulk silicon, denoted by $s=b$, or silicon containing the substitutional dopant $d$, denoted by $s=d$.

Each system $s$ is associated with a self-consistent one-particle Hamiltonian
$$
\hat{H}_s : D(\hat{H}_s) \subseteq \mathcal{H}_s \rightarrow \mathcal{H}_s,
$$
where $\mathcal{H}_s$ is the one-particle Hilbert space associated with system $s$, and $D(\hat{H}_s)$ is the domain on which the generally unbounded operator $\hat{H}_s$ is defined. The mapping specifies that, for every state
$$
\lvert\psi\rangle
\in
D(\hat{H}_s),
$$
the state obtained by applying the Hamiltonian satisfies
$$
\hat{H}_s\lvert\psi\rangle
\in
\mathcal{H}_s.
$$
In the present research program, the parent one-particle operator is the converged Kohn–Sham Hamiltonian,
$$
\hat{H}_s
=
\hat{H}_{\mathrm{KS},s}
\left[n_s^\star\right],
$$
where $\hat{H}_{\mathrm{KS},s}[n]$ denotes the Kohn–Sham Hamiltonian for system $s$ evaluated at electron density $n$, and $n_s^\star(\mathbf{r})$ is the corresponding converged self-consistent electron density. Here, $\mathbf{r}$ denotes the electron position, while the superscript $\star$ identifies the density obtained at self-consistency.

The physical and mathematical specification of $\hat{H}_s$ includes the exchange-correlation approximation, electron–ion interaction, crystal geometry, and boundary conditions adopted for system $s$. The basis set, kinetic-energy cutoffs, Brillouin-zone sampling, and convergence tolerances specify the numerical approximation used to represent and solve the corresponding Kohn–Sham problem.

For an orthonormal finite numerical basis $\left\{\lvert\chi_{\mu,s}\rangle\right\}_{\mu=1}^{N_s},$ the operator $\hat{H}_s$ is represented by the Hamiltonian matrix
$$
\left[\mathbf{H}_s\right]_{\mu\nu}
=
\left\langle
\chi_{\mu,s}
\middle|
\hat{H}_s
\middle|
\chi_{\nu,s}
\right\rangle,
\qquad
\mathbf{H}_s
\in
\mathbb{C}^{N_s\times N_s}.
$$
Here, $\lvert\chi_{\mu,s}\rangle$ denotes the $\mu$th numerical basis state for system $s$, $N_s$ is the number of retained basis states, and $\mu,\nu\in\{1,\ldots,N_s\}$ are basis indices. The space $\mathbb{C}^{N_s\times N_s}$ is the set of complex matrices with $N_s$ rows and $N_s$ columns.

The operator and its matrix representation must be distinguished. The symbol $\hat{H}_s$ denotes an operator acting on the Hilbert space $\mathcal{H}_s$, whereas $\mathbf{H}_s$ denotes its finite-dimensional representation in the selected numerical basis. A change in numerical basis changes $\mathbf{H}_s$ but does not, by itself, change the underlying operator $\hat{H}_s$.

The bulk and dopant operators need not initially act on canonically identified state spaces. In general, $\mathcal{H}_{\mathrm{b}}\neq\mathcal{H}_d$, because the corresponding calculations may employ different periodic cells, atomic configurations, boundary conditions, or relaxed geometries. Their finite numerical representations may likewise have different dimensions, $N_{\mathrm{b}}\neq N_d$.

Consequently, the formal difference $\hat{H}_d-\hat{H}_b$ is not assumed to be defined at this stage. The present section first constructs the projected state spaces and operators for each system separately. The subsequent identification of the bulk and dopant spaces, including the existence and nonuniqueness of a unitary identification map, is developed in [[ksdft2Effmass.04]].

## Bloch-Fiber Decomposition
Because the systems under consideration are periodic, their state spaces and Hamiltonians may be decomposed at fixed Bloch wavevector. For system $s$,
$$
\mathcal{H}_s
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\mathcal{H}_{s,\mathbf{k}}\,
\mathrm{d}\mathbf{k},
\qquad
\hat{H}_s
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\hat{H}_s(\mathbf{k})\,
\mathrm{d}\mathbf{k}.
$$
The symbol $\mathrm{BZ}_s$ denotes the Brillouin zone of system $s$, and $\mathbf{k}\in\mathrm{BZ}_s$ is a Bloch wavevector. The direct-integral symbol $\int^\oplus$ indicates that the full state space is assembled from the family of Bloch-fiber spaces $\mathcal{H}_{s,\mathbf{k}}$. The symbol $\cong$ denotes unitary equivalence under the Bloch transformation rather than literal equality of the two representations.

For each $\mathbf{k}$, the Bloch-fiber Hamiltonian acts as
$$
\hat{H}_s(\mathbf{k})
:
D\!\left(\hat{H}_s(\mathbf{k})\right)
\subseteq
\mathcal{H}_{s,\mathbf{k}}
\rightarrow
\mathcal{H}_{s,\mathbf{k}},
$$
where $D(\hat{H}_s(\mathbf{k}))$ is the domain of the fiber operator. Its eigenproblem is
$$
\hat{H}_s(\mathbf{k})
\lvert\psi_{n\mathbf{k},s}\rangle
=
\varepsilon_{n,s}(\mathbf{k})
\lvert\psi_{n\mathbf{k},s}\rangle.
$$
Here, $n$ is the band index, $\lvert\psi_{n\mathbf{k},s}\rangle\in\mathcal{H}_{s,\mathbf{k}}$ is a normalized Bloch eigenstate, and $\varepsilon_{n,s}(\mathbf{k})$ is its corresponding Kohnâ€“Sham eigenvalue.

The object retained by the reduction is therefore a family of finite-dimensional subspaces indexed by $\mathbf{k}$, rather than a single finite collection of eigenstates over the entire crystal.

## Target Projector Field

At each Bloch wavevector $\mathbf{k}$, select an $M_s$-dimensional target subspace
$$
\mathcal{H}_{s,\mathbf{k}}^{(P)}
=
\operatorname{Range}\!\left(\hat{P}_s(\mathbf{k})\right)
\subseteq
\mathcal{H}_{s,\mathbf{k}},
$$
where $M_s$ is the number of retained states per Bloch fiber and
$$
\hat{P}_s(\mathbf{k})
:
\mathcal{H}_{s,\mathbf{k}}
\rightarrow
\mathcal{H}_{s,\mathbf{k}}
$$
is the corresponding orthogonal projector. The projector satisfies
$$
\hat{P}_s(\mathbf{k})^\dagger
=
\hat{P}_s(\mathbf{k}),
\qquad
\hat{P}_s(\mathbf{k})^2
=
\hat{P}_s(\mathbf{k}).
$$
The dagger denotes the Hilbert-space adjoint. The first equality states that the projector is self-adjoint, while the second states that repeated projection has the same effect as a single projection.

The superscript $(P)$ labels a state space selected by the projector $\hat{P}_s(\mathbf{k})$. It is a label and does not itself denote an operator. The fixed-rank condition is
$$
\operatorname{rank}\hat{P}_s(\mathbf{k})
=
M_s
$$
for every $\mathbf{k}\in\mathrm{BZ}_s$.

The global retained state space is the direct integral
$$
\mathcal{H}_s^{(P)}
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\mathcal{H}_{s,\mathbf{k}}^{(P)}
\,
\mathrm{d}\mathbf{k}.
$$
Each fiber $\mathcal{H}_{s,\mathbf{k}}^{(P)}$ has finite dimension $M_s$. The global space $\mathcal{H}_s^{(P)}$, however, is not finite-dimensional because $\mathbf{k}$ varies continuously over the Brillouin zone. A finite-dimensional global representation arises only after the Brillouin zone has been discretized.

The projector field $\mathbf{k}\mapsto\hat{P}_s(\mathbf{k})$ must also vary periodically and with sufficient regularity across the Brillouin zone for a localized Wannier representation to be constructed. The detailed regularity and gauge requirements are developed in [[ksdft2Effmass.03]].

## Range, Kernel, and Complementary Space
The range of $\hat{P}_s(\mathbf{k})$ is
$$
\operatorname{Range}\!\left(\hat{P}_s(\mathbf{k})\right)
=
\left\{
\hat{P}_s(\mathbf{k})\lvert\psi\rangle
:
\lvert\psi\rangle\in\mathcal{H}_{s,\mathbf{k}}
\right\}.
$$
It contains all states retained by the projection. Define the complementary projector by
$$
\hat{Q}_s(\mathbf{k})
=
\hat{I}_{s,\mathbf{k}}
-
\hat{P}_s(\mathbf{k}),
$$
where $\hat{I}_{s,\mathbf{k}}$ is the identity operator on $\mathcal{H}_{s,\mathbf{k}}$. The range of $\hat{Q}_s(\mathbf{k})$ defines the complementary state space,
$$
\mathcal{H}_{s,\mathbf{k}}^{(Q)}
=
\operatorname{Range}\!\left(\hat{Q}_s(\mathbf{k})\right).
$$

Because $\hat{P}_s(\mathbf{k})$ is an orthogonal projector,
$$
\operatorname{Kernel}\!\left(\hat{P}_s(\mathbf{k})\right)
=
\operatorname{Range}\!\left(\hat{Q}_s(\mathbf{k})\right),
$$
where $\operatorname{Kernel}(\hat{P}_s(\mathbf{k}))$ is the set of states mapped to zero by $\hat{P}_s(\mathbf{k})$. The full fiber therefore decomposes as
$$
\mathcal{H}_{s,\mathbf{k}}
=
\mathcal{H}_{s,\mathbf{k}}^{(P)}
\oplus
\mathcal{H}_{s,\mathbf{k}}^{(Q)}.
$$
The direct-sum symbol $\oplus$ denotes an orthogonal decomposition into the retained subspace $\mathcal{H}_{s,\mathbf{k}}^{(P)}$ and the discarded subspace $\mathcal{H}_{s,\mathbf{k}}^{(Q)}$.

## Isolated Band Subspaces

Suppose that a group of $M_s$ bands is separated from the remaining spectrum at every $\mathbf{k}\in\mathrm{BZ}_s$. Let $\mathcal{I}_s$ denote the set of band indices belonging to this isolated group. The corresponding spectral projector is
$$
\hat{P}_s(\mathbf{k})
=
\sum_{n\in\mathcal{I}_s}
\lvert\psi_{n\mathbf{k},s}\rangle
\langle\psi_{n\mathbf{k},s}\rvert.
$$
Each term $\lvert\psi_{n\mathbf{k},s}\rangle\langle\psi_{n\mathbf{k},s}\rvert$ is the rank-one projector onto the Bloch eigenstate $\lvert\psi_{n\mathbf{k},s}\rangle$. Their sum projects onto the complete isolated band subspace.

Equivalently, the spectral projector may be expressed as
$$
\hat{P}_s(\mathbf{k})
=
\frac{1}{2\pi i}
\oint_{\Gamma}
\left[
z-\hat{H}_s(\mathbf{k})
\right]^{-1}
\mathrm{d}z.
$$
Here, $i$ is the imaginary unit, $z$ is a complex spectral parameter, and $\Gamma$ is a closed contour in the complex plane that encloses the retained eigenvalues of $\hat{H}_s(\mathbf{k})$ and excludes the remaining spectrum. The operator $[z-\hat{H}_s(\mathbf{k})]^{-1}$ is the resolvent of the fiber Hamiltonian.

Because $\hat{P}_s(\mathbf{k})$ is a spectral projector,
$$
\left[
\hat{H}_s(\mathbf{k}),
\hat{P}_s(\mathbf{k})
\right]
=
0,
$$
where $[\hat{A},\hat{B}]=\hat{A}\hat{B}-\hat{B}\hat{A}$ denotes the operator commutator. The vanishing commutator states that the target subspace is invariant under $\hat{H}_s(\mathbf{k})$.

An isolated band subspace does not require the retained bands to be separated from one another. Crossings within the retained group are permitted. The required separation is between the retained group as a whole and its complementary spectrum.

## Entangled Band Subspaces

A target band manifold is entangled when no fixed set of $M_s$ band indices defines the desired subspace throughout the Brillouin zone. Crossings, avoided crossings, and energetic overlap with other bands may cause the orbital character of interest to move among different eigenvalue branches.

Band entanglement is a general feature of multiband Bloch Hamiltonians. It is not specific to density-functional theory or to Wannier90. It becomes a model-reduction problem whenever a fixed-dimensional Bloch subspace must be extracted from a larger band manifold.

Let an outer energy window contain $J_s(\mathbf{k})$ Bloch eigenstates at wavevector $\mathbf{k}$, with
$$
J_s(\mathbf{k})
\geq
M_s.
$$
A disentanglement procedure selects $M_s$ orthonormal states from the span of these $J_s(\mathbf{k})$ candidate states:
$$
\lvert\widetilde{\psi}_{\alpha\mathbf{k},s}\rangle
=
\sum_{n=1}^{J_s(\mathbf{k})}
\lvert\psi_{n\mathbf{k},s}\rangle
U_{n\alpha,s}^{\mathrm{dis}}(\mathbf{k}),
\qquad
\alpha\in\{1,\ldots,M_s\}.
$$
Here, $\alpha$ indexes the retained states, and $U_{n\alpha,s}^{\mathrm{dis}}(\mathbf{k})$ is the coefficient relating the selected state $\lvert\widetilde{\psi}_{\alpha\mathbf{k},s}\rangle$ to the candidate Bloch eigenstates. Collecting these coefficients gives the rectangular matrix
$$
\mathbf{U}_s^{\mathrm{dis}}(\mathbf{k})
\in
\mathbb{C}^{J_s(\mathbf{k})\times M_s},
$$
which satisfies
$$
\mathbf{U}_s^{\mathrm{dis}}(\mathbf{k})^\dagger
\mathbf{U}_s^{\mathrm{dis}}(\mathbf{k})
=
\mathbf{I}_{M_s}.
$$
The matrix $\mathbf{I}_{M_s}$ is the $M_s\times M_s$ identity matrix. This relation states that the columns of $\mathbf{U}_s^{\mathrm{dis}}(\mathbf{k})$ are orthonormal; such a rectangular matrix is semiunitary.

The disentangled projector is
$$
\hat{P}_s(\mathbf{k})
=
\sum_{\alpha=1}^{M_s}
\lvert\widetilde{\psi}_{\alpha\mathbf{k},s}\rangle
\langle\widetilde{\psi}_{\alpha\mathbf{k},s}\rvert.
$$

If a frozen energy window is imposed, let $\hat{P}_{s,\mathrm{f}}(\mathbf{k})$ denote the spectral projector onto the states inside that window. Requiring every frozen state to belong to the selected subspace is expressed by
$$
\operatorname{Range}\!\left(\hat{P}_{s,\mathrm{f}}(\mathbf{k})\right)
\subseteq
\operatorname{Range}\!\left(\hat{P}_s(\mathbf{k})\right),
$$
or equivalently,
$$
\hat{P}_s(\mathbf{k})
\hat{P}_{s,\mathrm{f}}(\mathbf{k})
=
\hat{P}_{s,\mathrm{f}}(\mathbf{k}).
$$

Unlike an isolated-band spectral projector, a disentangled projector need not commute with the parent Hamiltonian:
$$
\left[
\hat{H}_s(\mathbf{k}),
\hat{P}_s(\mathbf{k})
\right]
\neq
0.
$$
Disentanglement therefore changes the retained subspace and the corresponding compressed operator. The subsequent choice of a localized basis changes the representation within the selected subspace. These are mathematically distinct operations.

## Projected Operators
Assume that the retained subspace lies within the domain of the parent fiber Hamiltonian,
$$
\mathcal{H}_{s,\mathbf{k}}^{(P)}
\subseteq
D\!\left(\hat{H}_s(\mathbf{k})\right).
$$
The projected, or compressed, fiber Hamiltonian is
$$
\boxed{
\hat{H}_s^{(P)}(\mathbf{k})
=
\hat{P}_s(\mathbf{k})
\hat{H}_s(\mathbf{k})
\hat{P}_s(\mathbf{k})
\big|_{\mathcal{H}_{s,\mathbf{k}}^{(P)}}
}.
$$
The vertical restriction symbol indicates that $\hat{H}_s^{(P)}(\mathbf{k})$ is regarded as an operator on the retained subspace. It acts as
$$
\hat{H}_s^{(P)}(\mathbf{k})
:
\mathcal{H}_{s,\mathbf{k}}^{(P)}
\rightarrow
\mathcal{H}_{s,\mathbf{k}}^{(P)}.
$$
This restricted operator must be distinguished from the ambient-space operator $\hat{P}_s(\mathbf{k})\hat{H}_s(\mathbf{k})\hat{P}_s(\mathbf{k})$, which acts as zero on the discarded subspace.

The corresponding global projected operator is
$$
\hat{H}_s^{(P)}
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\hat{H}_s^{(P)}(\mathbf{k})
\,
\mathrm{d}\mathbf{k}.
$$
The operator $\hat{H}_s^{(P)}$ contains the first-principles information retained for subsequent localization and model reduction.

The spectral data used in later reductions are derived from this same operator. A complete spectral resolution, consisting of eigenvalues together with their spectral projectors, reconstructs the finite-dimensional projected operator. Retaining only selected eigenvalues and derived quantities instead defines a partial observation of the operator. Whether that partial spectral information identifies a unique reduced Hamiltonian depends on the prescribed model class and is tested in [[ksdft2Effmass.05]].

## Spectral Projection and General Compression

The interpretation of $\hat{H}_s^{(P)}(\mathbf{k})$ depends on whether the selected subspace is invariant under the parent fiber Hamiltonian.

### Invariant Target Subspace
If
$$
\left[
\hat{H}_s(\mathbf{k}),
\hat{P}_s(\mathbf{k})
\right]
=
0,
$$
then
$$
\hat{P}_s(\mathbf{k})
\hat{H}_s(\mathbf{k})
\hat{Q}_s(\mathbf{k})
=
\hat{Q}_s(\mathbf{k})
\hat{H}_s(\mathbf{k})
\hat{P}_s(\mathbf{k})
=
0.
$$
The two vanishing terms are the operator blocks that couple the retained and discarded subspaces. The parent Hamiltonian is therefore block diagonal with respect to
$$
\mathcal{H}_{s,\mathbf{k}}
=
\mathcal{H}_{s,\mathbf{k}}^{(P)}
\oplus
\mathcal{H}_{s,\mathbf{k}}^{(Q)}.
$$
In this case, $\hat{H}_s^{(P)}(\mathbf{k})$ is the exact restriction of the parent Hamiltonian to an invariant spectral subspace and retains the selected eigenpairs exactly.

### Non-Invariant Target Subspace

For a general disentangled or physically selected projector,
$$
\hat{P}_s(\mathbf{k})
\hat{H}_s(\mathbf{k})
\hat{Q}_s(\mathbf{k})
\neq
0.
$$
Suppressing the system label $s$ and wavevector $\mathbf{k}$ for compactness, the parent Hamiltonian has the block representation
$$
\hat{H}
=
\begin{pmatrix}
\hat{P}\hat{H}\hat{P}
&
\hat{P}\hat{H}\hat{Q}
\\
\hat{Q}\hat{H}\hat{P}
&
\hat{Q}\hat{H}\hat{Q}
\end{pmatrix}.
$$
The diagonal blocks describe the action of $\hat{H}$ within the retained and discarded subspaces. The off-diagonal blocks describe coupling between them. Simple compression retains the block $\hat{P}\hat{H}\hat{P}$ and omits the effects mediated through the discarded space.

The eigenvalues of the compressed operator are therefore Ritz values in the selected subspace. Outside any frozen window, they need not coincide exactly with a fixed set of eigenvalues of the parent Hamiltonian.

The departure of the target subspace from invariance may be quantified by
$$
\eta_{\mathrm{inv},s}(\mathbf{k})
=
\left\|
\left[
\hat{H}_s(\mathbf{k}),
\hat{P}_s(\mathbf{k})
\right]
\right\|,
$$
where $\eta_{\mathrm{inv},s}(\mathbf{k})$ is the invariance error and $\|\cdot\|$ is a specified operator or matrix norm. The norm and its normalization must be stated when this quantity is evaluated numerically.

## Projection and Downfolding

Projection must be distinguished from a downfolded Hamiltonian that incorporates coupling through the discarded subspace. Suppressing the system and wavevector labels, formal elimination of the discarded component produces the energy-dependent effective operator
$$
\hat{H}_{\mathrm{eff}}(E)
=
\hat{P}\hat{H}\hat{P}
+
\hat{P}\hat{H}\hat{Q}
\left(
E-\hat{Q}\hat{H}\hat{Q}
\right)^{-1}
\hat{Q}\hat{H}\hat{P}.
$$
Here, $E$ is the spectral energy at which the reduction is evaluated, and $(E-\hat{Q}\hat{H}\hat{Q})^{-1}$ is the resolvent of the discarded-space block. The expression is defined whenever $E$ lies outside the spectrum of $\hat{Q}\hat{H}\hat{Q}$, so that the inverse exists.

The compressed operator is
$$
\hat{H}^{(P)}
=
\hat{P}\hat{H}\hat{P}
\big|_{\operatorname{Range}(\hat{P})},
$$
whereas $\hat{H}_{\mathrm{eff}}(E)$ contains the additional energy-dependent correction generated by virtual coupling through the discarded space. The two coincide when the retained subspace is invariant. They may also be treated as approximately equivalent when the coupling correction is negligible relative to a specified error tolerance.

This distinction is required when assessing whether a compact tight-binding or continuum model reproduces the target physics through an invariant subspace or through parameters that implicitly absorb discarded-space effects.

## Numerical Matrix Representation

Let $\mathbf{H}_s(\mathbf{k}) \in \mathbb{C}^{N_s(\mathbf{k})\times N_s(\mathbf{k})}$ denote the finite matrix representation of the Bloch-fiber Hamiltonian in a numerical basis of dimension $N_s(\mathbf{k})$ [^5]. Let
$$
\mathbf{V}_s(\mathbf{k})
	\in \mathbb{C}^{N_s(\mathbf{k})\times M_s}
$$
contain, as its columns, an orthonormal basis for the retained $M_s$-dimensional subspace [^2][^6]. The orthonormality condition is

$$
\mathbf{V}_s(\mathbf{k})^\dagger
\mathbf{V}_s(\mathbf{k})
=
\mathbf{I}_{M_s}.
$$

The matrix representation of the projector in the ambient numerical basis is
$$
\mathbf{P}_s(\mathbf{k})
=
\mathbf{V}_s(\mathbf{k})
\mathbf{V}_s(\mathbf{k})^\dagger,
$$
where
$$
\mathbf{P}_s(\mathbf{k})
\in
\mathbb{C}^{N_s(\mathbf{k})\times N_s(\mathbf{k})}.
$$
The reduced Hamiltonian matrix acting on retained coordinates is
$$
\boxed{
\mathbf{H}_s^{(P)}(\mathbf{k})
=
\mathbf{V}_s(\mathbf{k})^\dagger
\mathbf{H}_s(\mathbf{k})
\mathbf{V}_s(\mathbf{k})
}
\in
\mathbb{C}^{M_s\times M_s}.
$$
This construction is the finite-dimensional form of compressing the Bloch-fiber Hamiltonian to a selected Bloch subspace [^2][^4]. The matrix $\mathbf{H}_s^{(P)}(\mathbf{k})$ is the finite-dimensional representation of the compressed operator $\hat{H}_s^{(P)}(\mathbf{k})$ in the basis defined by the columns of $\mathbf{V}_s(\mathbf{k})$.

By contrast,
$$
\mathbf{P}_s(\mathbf{k})
\mathbf{H}_s(\mathbf{k})
\mathbf{P}_s(\mathbf{k})
\in
\mathbb{C}^{N_s(\mathbf{k})\times N_s(\mathbf{k})}
$$
is the ambient-space matrix representation of the compression. It has the same action on retained states but has a null action on the orthogonal complement. Indeed,
$$
\mathbf{P}_s(\mathbf{k})
\mathbf{H}_s(\mathbf{k})
\mathbf{P}_s(\mathbf{k})
=
\mathbf{V}_s(\mathbf{k})
\mathbf{H}_s^{(P)}(\mathbf{k})
\mathbf{V}_s(\mathbf{k})^\dagger.
$$
The two matrices therefore encode the same compressed operator on different coordinate spaces.

Let
$$
\mathcal{K}_s
=
\left\{
\mathbf{k}_1,\ldots,\mathbf{k}_{N_k}
\right\}
\subset
\mathrm{BZ}_s
$$
denote a discrete Brillouin-zone mesh containing $N_k$ wavevectors. The corresponding retained numerical space is
$$
\bigoplus_{\mathbf{k}\in\mathcal{K}_s}
\mathcal{H}_{s,\mathbf{k}}^{(P)},
$$
which is the finite-mesh analogue of the direct-integral decomposition over Bloch fibers [1]. It has dimension $N_kM_s$ when the retained rank $M_s$ is constant over the mesh. Electronic-structure and Wannier codes represent the projected Bloch problem through this finite collection of $M_s\times M_s$ matrices [^4][^6].

## Role in the Reduction Program

The construction established in this section is
$$
\boxed{
\hat{H}_s
\longrightarrow
\left\{
\hat{H}_s(\mathbf{k})
\right\}_{\mathbf{k}\in\mathrm{BZ}_s}
\longrightarrow
\left\{
\hat{P}_s(\mathbf{k})
\right\}_{\mathbf{k}\in\mathrm{BZ}_s}
\longrightarrow
\hat{H}_s^{(P)}
}.
$$
The first step is the Bloch decomposition of the periodic parent operator. The second selects a fixed-rank family of target subspaces, and the third compresses the parent Hamiltonian to those retained spaces.

This construction establishes three distinctions required by the later analysis. First, the retained object is a family of Bloch subspaces rather than a finite list of low-rank eigenpair reconstructions. Second, isolated-band selection and disentanglement define mathematically different projector fields. Third, the projected operator must be distinguished from both its finite matrix representation and its later Wannier representation.

The next stage, developed in [[ksdft2Effmass.03]], constructs localized Wannier bases for the projected spaces. The comparison of the independently constructed bulk and dopant spaces is deferred to [[ksdft2Effmass.04]]. Equal projected dimensions guarantee the existence of an abstract unitary isomorphism, but they do not determine a unique physically meaningful identification. Only after such an identification and a common energy reference have been established can a dopant-induced operator difference be defined.


## References

[^1] I. Souza, N. Marzari, and D. Vanderbilt, “Maximally localized Wannier functions for entangled energy bands,” _Phys. Rev. B_, vol. 65, Art. no. 035109, 2001, doi: 10.1103/PhysRevB.65.035109.

[^2] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” _Rev. Mod. Phys._, vol. 84, pp. 1419–1475, 2012, doi: [10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419).

[^3] P.-O. Löwdin, “A note on the quantum-mechanical perturbation theory,” _J. Chem. Phys._, vol. 19, pp. 1396–1401, 1951, doi: 10.1063/1.1748067

[^4] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally Localized Wannier Functions: Theory and Applications,” *Reviews of Modern Physics*, vol. 84, pp. 1419–1475, 2012. [https://doi.org/10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419)

[^5] P. Kuchment, “An Overview of Periodic Elliptic Operators,” *Bulletin of the American Mathematical Society*, vol. 53, no. 3, pp. 343–414, 2016. [https://doi.org/10.1090/bull/1528](https://doi.org/10.1090/bull/1528)

[^6] A. A. Mostofi, J. R. Yates, Y.-S. Lee, I. Souza, D. Vanderbilt, and N. Marzari, “wannier90: A Tool for Obtaining Maximally-Localised Wannier Functions,” *Computer Physics Communications*, vol. 178, no. 9, pp. 685–699, 2008. [https://doi.org/10.1016/j.cpc.2007.11.016](https://doi.org/10.1016/j.cpc.2007.11.016)