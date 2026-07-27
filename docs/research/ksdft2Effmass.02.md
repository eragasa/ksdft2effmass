back_to: [[ksdft2Effmass.00]]
# Projected Bloch State Spaces and Operators
## Scope
This section defines the state spaces, projectors, and compressed operators used throughout the reduction program. The construction is stated for Kohn-Sham operators, although it applies to any periodic one-particle Bloch Hamiltonian.

The principal distinction is among:
1. the full one-particle operator;
2. the family of target Bloch subspaces;
3. the operator compressed to those subspaces;
4. a matrix representation of the compressed operator.

Wannier construction supplies a localized representation of the projected family and is developed separately in [[ksdft2Effmass.03]]. Identification and comparison of state spaces obtained from different calculations are developed in [[ksdft2Effmass.04]].

## First-Principles Systems
Let $\mathcal{D}=\{\mathrm{P},\mathrm{B}\}$ denote the set of dopant species considered in this work, where $\mathrm{P}$ and $\mathrm{B}$ represent phosphorus and boron, respectively. For each dopant $d\in\mathcal{D}$, define the corresponding set of system labels by $\mathcal{S}_d=\{b,d\}$. The index $s\in\mathcal{S}_d$
labels either pristine bulk silicon, denoted by $s=b$, or silicon containing the substitutional dopant $d$, denoted by $s=d$.

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

### Construction of the Finite-Dimensional Operator Difference
The objective is to construct a finite-dimensional representation of the dopant-induced operator difference. Formally, one would like to write
$$
\Delta\hat{H}_d
=
\hat{H}_d
-
\hat{H}_{\mathrm{b}},
$$
where $\hat{H}_d$ and $\hat{H}_{\mathrm{b}}$ are the dopant and pristine-bulk Hamiltonians, respectively. This expression is well defined only if both operators act on the same Hilbert space and use a common physical energy reference.

In the general case, the bulk and dopant calculations may employ different periodic cells, Brillouin zones, geometries, or numerical representations. The required operator difference must therefore be constructed through the sequence
$$
\boxed{
\left(
\hat{H}_{\mathrm{b}},
\hat{H}_d
\right)
\xrightarrow{\text{projection}}
\left(
\hat{H}_{\mathrm{b}}^{(P)},
\hat{H}_d^{(P)}
\right)
\xrightarrow{\text{alignment and identification}}
\Delta\hat{H}_d^{(P)}
\xrightarrow{\text{matrix representation}}
\Delta\mathbf{H}_{\mathrm{W},d}
}.
$$
Here, $\hat{H}_s^{(P)}$ denotes the Hamiltonian for system $s\in\{\mathrm{b},d\}$ projected onto its retained finite-rank subspace $\mathcal{H}_s^{(P)}$. Before subtraction, the two projected operators must be placed on a common state space.

Suppose there exists a unitary identification map from the retained bulk subspace to the retained dopant subspace, $\hat{U}_d:\mathcal{H}_{\mathrm{b}}^{(P)}\rightarrow\mathcal{H}_d^{(P)}$ (existence to be discussed in [[ksdft2Effmass.04]]). Then corresponding bulk operator transported to $\mathcal{H}_d^{(P)}$ is
$$
\hat{H}_{\mathrm{b}\rightarrow d}^{(P)}
=
\hat{U}_d \hat{H}_{\mathrm{b}}^{(P)} \hat{U}_d^\dagger.
$$
Independent calculations may also employ different energy zeros. Define the energy-aligned projected Hamiltonian by
$$
\overline{\hat{H}}_s^{(P)}
= \hat{H}_s^{(P)}
	- E_{\mathrm{ref},s} \hat{I}_s^{(P)},
$$
where $E_{\mathrm{ref},s}$ is the selected reference energy and $\hat{I}_s^{(P)}$ is the identity operator on $\mathcal{H}_s^{(P)}$.

The projected dopant-induced perturbation is then
$$
\boxed{
\Delta\hat{H}_d^{(P)}
=
\overline{\hat{H}}_d^{(P)}
-
\hat{U}_d
\overline{\hat{H}}_{\mathrm{b}}^{(P)}
\hat{U}_d^\dagger
}.
$$
Both terms on the right-hand side now act on the same retained dopant space $\mathcal{H}_d^{(P)}$, so their difference is mathematically well defined.

Let $\left\{\lvert w_{\alpha,d}\rangle\right\}_{\alpha=1}^{M}$ be an orthonormal localized basis for $\mathcal{H}_d^{(P)}$, where $M$ is the dimension of the retained subspace. The matrix representation of the impurity perturbation is
$$
\left[
\Delta\mathbf{H}_{\mathrm{W},d}
\right]_{\alpha\beta}
=
\left\langle
w_{\alpha,d}
\middle|
\Delta\hat{H}_d^{(P)}
\middle|
w_{\beta,d}
\right\rangle.
$$
If the bulk and dopant bases have already been aligned so that the matrix representation of $\hat{U}_d$ is the identity, then the operator difference reduces to the direct matrix subtraction
$$
\boxed{
\Delta\mathbf{H}_{\mathrm{W},d}
	= \overline{\mathbf{H}}_{\mathrm{W},d}
	- \overline{\mathbf{H}}_{\mathrm{W},\mathrm{b}}
}.
$$

Thus, the finite-dimensional expression

$$
\Delta\mathbf{H}_d
=
\mathbf{H}_d
-
\mathbf{H}_{\mathrm{b}}
$$

is the endpoint of the projection and alignment procedure, rather than its starting assumption.

## Bloch-Fiber Decomposition

For a periodic system, the one-particle Hilbert space decomposes into Bloch fibers:

$$
\mathcal H_s
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\mathcal H_{s,\mathbf k}\,
\mathrm d\mathbf k,
$$

and the periodic Hamiltonian decomposes accordingly:

$$
\hat H_s
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\hat H_s(\mathbf k)\,
\mathrm d\mathbf k.
$$

Here:

- $\mathrm{BZ}_s$ is the Brillouin zone of system $s$;
- $\mathcal H_{s,\mathbf k}$ is the Hilbert space of cell-periodic states at Bloch wavevector $\mathbf k$;
- $\hat H_s(\mathbf k)$ is the Bloch-fiber Hamiltonian acting on $\mathcal H_{s,\mathbf k}$.

Its eigenproblem is

$$
\hat H_s(\mathbf k)
\lvert\psi_{n\mathbf k,s}\rangle
=
\varepsilon_{n,s}(\mathbf k)
\lvert\psi_{n\mathbf k,s}\rangle.
$$

The target of the reduction is therefore a family of subspaces over the Brillouin zone, rather than a single finite collection of eigenstates.

## Target Projector Field

At each $\mathbf k$, select an $M_s$-dimensional target subspace

$$
\mathcal H_{s,\mathbf k}^{(P)}
=
\operatorname{Range}\!\left(\hat P_s(\mathbf k)\right)
\subseteq
\mathcal H_{s,\mathbf k},
$$

where

$$
\hat P_s(\mathbf k)
:
\mathcal H_{s,\mathbf k}
\longrightarrow
\mathcal H_{s,\mathbf k}
$$

is an orthogonal projector satisfying

$$
\hat P_s(\mathbf k)^\dagger
=
\hat P_s(\mathbf k),
\qquad
\hat P_s(\mathbf k)^2
=
\hat P_s(\mathbf k).
$$

The superscript $(P)$ labels the subspace selected by the projector. The projector itself remains the operator $\hat P_s(\mathbf k)$; writing $\mathcal H_{s,\mathbf k}^{(\hat P)}$ would add operator notation to a label without improving the definition.

For a fixed-rank construction,

$$
\operatorname{rank}\hat P_s(\mathbf k)=M_s
$$

for every $\mathbf k$ in $\mathrm{BZ}_s$. The global retained space is

$$
\mathcal H_s^{(P)}
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\mathcal H_{s,\mathbf k}^{(P)}
\,
\mathrm d\mathbf k.
$$

Although each fiber $\mathcal H_{s,\mathbf k}^{(P)}$ has finite dimension $M_s$, the direct-integral space $\mathcal H_s^{(P)}$ is not itself finite-dimensional. A finite-dimensional global matrix arises only after discretizing the Brillouin zone.

For Wannier construction, the projector field must also possess adequate periodicity and regularity in $\mathbf k$. Selecting the correct dimension at each $\mathbf k$ is therefore insufficient: the selected subspaces must vary coherently across the Brillouin zone.

## Range, Kernel, and Complementary Space

For each fiber,

$$
\operatorname{Range}\!\left(\hat P_s(\mathbf k)\right)
=
\left\{
\hat P_s(\mathbf k)\lvert\psi\rangle
:
\lvert\psi\rangle\in\mathcal H_{s,\mathbf k}
\right\}.
$$

Define the complementary projector

$$
\hat Q_s(\mathbf k)
=
\hat I_{s,\mathbf k}
-
\hat P_s(\mathbf k).
$$

Because $\hat P_s(\mathbf k)$ is orthogonal,

$$
\operatorname{Kernel}\!\left(\hat P_s(\mathbf k)\right)
=
\operatorname{Range}\!\left(\hat Q_s(\mathbf k)\right),
$$

and

$$
\mathcal H_{s,\mathbf k}
=
\mathcal H_{s,\mathbf k}^{(P)}
\oplus
\mathcal H_{s,\mathbf k}^{(Q)}.
$$

The spaces $\mathcal H_{s,\mathbf k}^{(P)}$ and $\mathcal H_{s,\mathbf k}^{(Q)}$ contain the retained and discarded components, respectively.

## Isolated Band Subspaces

Suppose a set of $M_s$ bands is separated from the remaining spectrum at every $\mathbf k$. If $\mathcal I_s$ indexes these bands, the corresponding spectral projector is

$$
\hat P_s(\mathbf k)
=
\sum_{n\in\mathcal I_s}
\lvert\psi_{n\mathbf k,s}\rangle
\langle\psi_{n\mathbf k,s}\rvert.
$$

Equivalently, when a contour $\Gamma$ encloses the target eigenvalues and no others,

$$
\hat P_s(\mathbf k)
=
\frac{1}{2\pi i}
\oint_\Gamma
\left(
z-\hat H_s(\mathbf k)
\right)^{-1}
\mathrm dz.
$$

Because this is a spectral projector,

$$
\left[
\hat H_s(\mathbf k),
\hat P_s(\mathbf k)
\right]
=
0.
$$

The target space is invariant under $\hat H_s(\mathbf k)$, and compression retains the selected eigenpairs exactly.

An isolated band subspace does not require each band to be separated from the other retained bands. Crossings within the retained group are permitted. What is required is separation of the entire retained group from its complement.

## Entangled Band Subspaces

The target bands are entangled when no fixed set of band indices defines the desired $M_s$-dimensional subspace throughout the Brillouin zone. Crossings, avoided crossings, or energy overlap with other bands can cause the orbital character of interest to move among different eigenvalue branches.

Band entanglement is a general feature of multiband Bloch Hamiltonians. It is not specific to density-functional theory or to Wannier90. It becomes an explicit computational problem whenever a reduced Bloch model must be extracted from a larger band manifold.

Let an outer window contain $J_s(\mathbf k)\geq M_s$ Bloch eigenstates. A disentanglement procedure selects $M_s$ orthonormal combinations

$$
\lvert\widetilde\psi_{\alpha\mathbf k,s}\rangle
=
\sum_{n=1}^{J_s(\mathbf k)}
\lvert\psi_{n\mathbf k,s}\rangle
U^{\mathrm{dis}}_{n\alpha,s}(\mathbf k),
$$

where

$$
\mathbf U_s^{\mathrm{dis}}(\mathbf k)^\dagger
\mathbf U_s^{\mathrm{dis}}(\mathbf k)
=
\mathbf I_{M_s}.
$$

The selected projector is then

$$
\hat P_s(\mathbf k)
=
\sum_{\alpha=1}^{M_s}
\lvert\widetilde\psi_{\alpha\mathbf k,s}\rangle
\langle\widetilde\psi_{\alpha\mathbf k,s}\rvert.
$$

If a frozen window is imposed, its spectral projector $\hat P_{s,\mathrm f}(\mathbf k)$ must satisfy

$$
\operatorname{Range}\!\left(\hat P_{s,\mathrm f}(\mathbf k)\right)
\subseteq
\operatorname{Range}\!\left(\hat P_s(\mathbf k)\right),
$$

or equivalently,

$$
\hat P_s(\mathbf k)\hat P_{s,\mathrm f}(\mathbf k)
=
\hat P_{s,\mathrm f}(\mathbf k).
$$

Unlike an isolated-band spectral projector, a disentangled projector need not commute with the parent Hamiltonian:

$$
\left[
\hat H_s(\mathbf k),
\hat P_s(\mathbf k)
\right]
\neq
0.
$$

Disentanglement therefore changes the retained subspace and the compressed operator. Subsequent localization changes the basis within that selected subspace. These are mathematically distinct operations.

## Projected Operators

Assume that

$$
\mathcal H_{s,\mathbf k}^{(P)}
\subset
D\!\left(\hat H_s(\mathbf k)\right).
$$

The projected, or compressed, fiber Hamiltonian is

$$
\boxed{
\hat H_s^{(P)}(\mathbf k)
=
\hat P_s(\mathbf k)
\hat H_s(\mathbf k)
\hat P_s(\mathbf k)
\big|_{\mathcal H_{s,\mathbf k}^{(P)}}
}.
$$

It acts as

$$
\hat H_s^{(P)}(\mathbf k)
:
\mathcal H_{s,\mathbf k}^{(P)}
\longrightarrow
\mathcal H_{s,\mathbf k}^{(P)}.
$$

The restriction is essential. It identifies $\hat H_s^{(P)}(\mathbf k)$ as an operator on the retained subspace, rather than as the ambient-space operator $\hat P_s\hat H_s\hat P_s$ with a null action on the discarded subspace.

The corresponding global projected operator is

$$
\hat H_s^{(P)}
\cong
\int_{\mathrm{BZ}_s}^{\oplus}
\hat H_s^{(P)}(\mathbf k)
\,
\mathrm d\mathbf k.
$$

This operator contains the first-principles information retained for subsequent localization and model reduction.

## Spectral Projection and General Compression

The interpretation of $\hat H_s^{(P)}(\mathbf k)$ depends on the relation between the projector and the parent Hamiltonian.

### Invariant target subspace

If

$$
\left[
\hat H_s(\mathbf k),
\hat P_s(\mathbf k)
\right]
=
0,
$$

then

$$
\hat P_s\hat H_s\hat Q_s
=
\hat Q_s\hat H_s\hat P_s
=
0.
$$

The parent operator is block diagonal with respect to

$$
\mathcal H_{s,\mathbf k}
=
\mathcal H_{s,\mathbf k}^{(P)}
\oplus
\mathcal H_{s,\mathbf k}^{(Q)},
$$

and $\hat H_s^{(P)}(\mathbf k)$ is the exact restriction of the parent operator to an invariant spectral subspace.

### Non-invariant target subspace

For a general disentangled or physically selected projector,

$$
\hat P_s\hat H_s\hat Q_s
\neq
0.
$$

With the $\mathbf k$ and $s$ labels suppressed, the parent operator has the block form

$$
\hat H
=
\begin{pmatrix}
\hat P\hat H\hat P
&
\hat P\hat H\hat Q
\\
\hat Q\hat H\hat P
&
\hat Q\hat H\hat Q
\end{pmatrix}.
$$

Simple compression retains the $\hat P\hat H\hat P$ block and omits coupling through $\mathcal H^{(Q)}$. Its eigenvalues are Ritz values in the selected subspace and need not coincide exactly with a fixed set of parent eigenvalues outside any frozen window.

A useful invariance diagnostic is

$$
\eta_{\mathrm{inv},s}(\mathbf k)
=
\left\|
\left[
\hat H_s(\mathbf k),
\hat P_s(\mathbf k)
\right]
\right\|.
$$

The choice of norm and normalization must be specified in a computational study.

## Projection and Downfolding

Projection by itself should be distinguished from an effective Hamiltonian that accounts for virtual coupling to the discarded space. Formally eliminating the $Q$ component of an eigenstate produces the energy-dependent Schur-complement operator

$$
\hat H_{\mathrm{eff}}(E)
=
\hat P\hat H\hat P
+
\hat P\hat H\hat Q
\left(
E-\hat Q\hat H\hat Q
\right)^{-1}
\hat Q\hat H\hat P,
$$

whenever the resolvent exists.

Therefore,

$$
\hat H^{(P)}
=
\hat P\hat H\hat P
\big|_{\operatorname{Range}(\hat P)}
$$

is a compression, whereas $\hat H_{\mathrm{eff}}(E)$ is an energy-dependent downfolded operator. They agree when the retained space is invariant or when the coupling correction is negligible within the stated tolerance.

This distinction will be required when assessing whether a compact tight-binding or continuum operator reproduces the target physics because of a well-chosen invariant subspace or because discarded-space effects have been absorbed into fitted parameters.

## Numerical Matrix Representation

Let

$$
\mathbf V_s(\mathbf k)
\in
\mathbb C^{D_s(\mathbf k)\times M_s}
$$

contain an orthonormal basis for the retained subspace in a finite numerical basis of dimension $D_s(\mathbf k)$. Then

$$
\mathbf V_s(\mathbf k)^\dagger
\mathbf V_s(\mathbf k)
=
\mathbf I_{M_s},
$$

and the projector matrix is

$$
\mathbf P_s(\mathbf k)
=
\mathbf V_s(\mathbf k)
\mathbf V_s(\mathbf k)^\dagger.
$$

The reduced matrix acting on retained coordinates is

$$
\boxed{
\mathbf H_s^{(P)}(\mathbf k)
=
\mathbf V_s(\mathbf k)^\dagger
\mathbf H_s(\mathbf k)
\mathbf V_s(\mathbf k)
}
\in
\mathbb C^{M_s\times M_s}.
$$

This matrix must be distinguished from the ambient representation

$$
\mathbf P_s(\mathbf k)
\mathbf H_s(\mathbf k)
\mathbf P_s(\mathbf k)
\in
\mathbb C^{D_s(\mathbf k)\times D_s(\mathbf k)}.
$$

The two matrices encode the same compressed action on the retained subspace, but they have different dimensions and different null-space structure.

On a discrete mesh

$$
\mathcal K_s
=
\left\{
\mathbf k_1,\ldots,\mathbf k_{N_k}
\right\},
$$

the retained numerical space has dimension

$$
N_kM_s.
$$

It is this discretized direct sum,

$$
\bigoplus_{\mathbf k\in\mathcal K_s}
\mathcal H_{s,\mathbf k}^{(P)},
$$

that is represented by a finite collection of matrices in electronic-structure and Wannier codes.

## Role in the Reduction Program

The construction established here is

$$
\boxed{
\hat H_s
\longrightarrow
\left\{
\hat P_s(\mathbf k)
\right\}_{\mathbf k\in\mathrm{BZ}_s}
\longrightarrow
\hat H_s^{(P)}
}.
$$

It resolves three points needed by the later analysis:

1. the retained object is a fixed-rank family of Bloch subspaces;
2. isolated-band selection and disentanglement define different kinds of projectors;
3. the projected operator is distinct from both its numerical matrix and its later Wannier representation.

The next stage constructs localized Wannier bases for these projected spaces. Only after the bulk and dopant spaces have been represented and physically identified can their operator difference be defined.

## References

[1] I. Souza, N. Marzari, and D. Vanderbilt, â€œMaximally localized Wannier functions for entangled energy bands,â€ *Phys. Rev. B*, vol. 65, Art. no. 035109, 2001, doi: 10.1103/PhysRevB.65.035109.

[2] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, â€œMaximally localized Wannier functions: Theory and applications,â€ *Rev. Mod. Phys.*, vol. 84, pp. 1419â€“1475, 2012, doi: 10.1103/RevModPhys.84.1419.

[3] P.-O. LÃ¶wdin, â€œA note on the quantum-mechanical perturbation theory,â€ *J. Chem. Phys.*, vol. 19, pp. 1396â€“1401, 1951, doi: 10.1063/1.1748067.