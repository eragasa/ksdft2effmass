# Wannier Construction and Localized Operator Representations

back_to: [[ksdft2Effmass.00]]
## Scope

This section constructs localized Wannier representations of the projected Bloch operators defined in [[ksdft2Effmass.02]]. Let $\mathcal{D}=\{\mathrm{P},\mathrm{B}\}$ denote the dopant species, and let $\mathcal{S}_d=\{b,d\}$ contain the bulk and dopant system labels for fixed $d\in\mathcal{D}$. For each system $s\in\mathcal{S}_d$, the input is the fixed-rank projector field
$$
\mathbf{k}
\mapsto
\hat{P}_s(\mathbf{k}),
$$
together with the projected fiber Hamiltonian
$$
\hat{H}_s^{(P)}(\mathbf{k})
:
\mathcal{H}_{s,\mathbf{k}}^{(P)}
\rightarrow
\mathcal{H}_{s,\mathbf{k}}^{(P)}.
$$
Here, $\mathbf{k}\in\mathrm{BZ}_s$ is a Bloch wavevector in the Brillouin zone $\mathrm{BZ}_s$, $\mathcal{H}_{s,\mathbf{k}}^{(P)}=\operatorname{Range}(\hat{P}_s(\mathbf{k}))$ is the retained $M_s$-dimensional Bloch subspace, and $\hat{H}_s^{(P)}(\mathbf{k})$ is the parent Hamiltonian compressed to that subspace.

Wannier construction does not, by itself, introduce a reduced physical model. It selects a smooth Bloch basis and Fourier transforms that basis into localized orbitals. Once the projector field has been fixed, the exact Wannier representation and the projected Bloch representation describe the same operator.

## Bloch Frames for the Projected Subspace
At each $\mathbf{k}\in\mathrm{BZ}_s$, choose an orthonormal basis
$$
\left\{
\lvert\phi_{\alpha\mathbf{k},s}\rangle
\right\}_{\alpha=1}^{M_s}
$$
for the retained subspace $\mathcal{H}_{s,\mathbf{k}}^{(P)}$. The index $\alpha\in\{1,\ldots,M_s\}$ labels the retained basis states. The ordered collection of these states is called a Bloch frame.

Orthonormality requires
$$
\langle
\phi_{\alpha\mathbf{k},s}
\vert
\phi_{\beta\mathbf{k},s}
\rangle
=
\delta_{\alpha\beta},
$$
where $\delta_{\alpha\beta}$ is the Kronecker delta. The target projector may therefore be reconstructed from the frame as
$$
\hat{P}_s(\mathbf{k})
=
\sum_{\alpha=1}^{M_s}
\lvert\phi_{\alpha\mathbf{k},s}\rangle
\langle\phi_{\alpha\mathbf{k},s}\rvert.
$$
Different orthonormal frames may generate the same projector and therefore the same retained subspace.

## Gauge Freedom
Let
$$
\mathbf{G}_s(\mathbf{k})
\in
U(M_s)
$$
be an $M_s\times M_s$ unitary matrix, where $U(M_s)$ denotes the unitary group of degree $M_s$. Its matrix elements satisfy
$$
\mathbf{G}_s(\mathbf{k})^\dagger
\mathbf{G}_s(\mathbf{k})
=
\mathbf{G}_s(\mathbf{k})
\mathbf{G}_s(\mathbf{k})^\dagger
=
\mathbf{I}_{M_s}.
$$
A new Bloch frame is obtained through
$$
\lvert\phi'_{\alpha\mathbf{k},s}\rangle
=
\sum_{\beta=1}^{M_s}
\lvert\phi_{\beta\mathbf{k},s}\rangle
\left[\mathbf{G}_s(\mathbf{k})\right]_{\beta\alpha}.
$$
This transformation changes the basis within $\mathcal{H}_{s,\mathbf{k}}^{(P)}$ but leaves the projector invariant:
$$
\sum_{\alpha=1}^{M_s}
\lvert\phi'_{\alpha\mathbf{k},s}\rangle
\langle\phi'_{\alpha\mathbf{k},s}\rvert
=
\hat{P}_s(\mathbf{k}).
$$
The $\mathbf{k}$-dependent choice of $\mathbf{G}_s(\mathbf{k})$ is the Bloch gauge. Wannier localization is therefore a gauge-selection problem within a previously selected family of subspaces.

## Construction from Kohn-Sham Eigenstates

For an isolated group of bands indexed by $\mathcal{I}_s$, a Bloch frame may be constructed from the Kohn-Sham eigenstates according to
$$
\lvert\phi_{\alpha\mathbf{k},s}\rangle
=
\sum_{n\in\mathcal{I}_s}
\lvert\psi_{n\mathbf{k},s}\rangle
U_{n\alpha,s}(\mathbf{k}),
$$
where $\mathbf{U}_s(\mathbf{k})\in U(M_s)$ is a unitary mixing matrix. The band index $n$ labels the retained Kohn-Sham eigenstates, whereas $\alpha$ labels the states in the selected Bloch frame.

For an entangled band manifold, [[ksdft2Effmass.02]] first constructs disentangled states
$$
\lvert\widetilde{\psi}_{\alpha\mathbf{k},s}\rangle
=
\sum_{n=1}^{J_s(\mathbf{k})}
\lvert\psi_{n\mathbf{k},s}\rangle
U_{n\alpha,s}^{\mathrm{dis}}(\mathbf{k}),
$$
where $J_s(\mathbf{k})$ is the number of candidate eigenstates in the outer energy window and $\mathbf{U}_s^{\mathrm{dis}}(\mathbf{k})$ is a $J_s(\mathbf{k})\times M_s$ semiunitary matrix. A subsequent unitary localization matrix $\mathbf{U}_s^{\mathrm{loc}}(\mathbf{k})\in U(M_s)$ defines the Bloch frame
$$
\lvert\phi_{\alpha\mathbf{k},s}\rangle
=
\sum_{\beta=1}^{M_s}
\lvert\widetilde{\psi}_{\beta\mathbf{k},s}\rangle
U_{\beta\alpha,s}^{\mathrm{loc}}(\mathbf{k}).
$$
The combined transformation from the outer-window eigenstates to the localized frame is
$$
\mathbf{U}_s^{\mathrm{tot}}(\mathbf{k})
=
\mathbf{U}_s^{\mathrm{dis}}(\mathbf{k})
\mathbf{U}_s^{\mathrm{loc}}(\mathbf{k}).
$$
Disentanglement determines the projector field, while localization selects a basis within that field. The matrices $\mathbf{U}_s^{\mathrm{dis}}(\mathbf{k})$ and $\mathbf{U}_s^{\mathrm{loc}}(\mathbf{k})$ therefore have different mathematical roles.

## Wannier Basis
Let $\mathcal{L}_s$ denote the Bravais lattice of system $s$, and let
$$
\mathcal{K}_s
=
\left\{
\mathbf{k}_1,\ldots,\mathbf{k}_{N_k}
\right\}
$$
be a uniform Brillouin-zone mesh containing $N_k$ wavevectors. Let $\mathcal{L}_s^{(N_k)}\subset\mathcal{L}_s$ denote the corresponding finite Bornâ€“von KÃ¡rmÃ¡n lattice containing $N_k$ lattice vectors $\mathbf{R}$.

Using the discrete Fourier-transform convention adopted here, the Wannier state associated with orbital $\alpha$ and lattice vector $\mathbf{R}$ is
$$
\boxed{
\lvert w_{\alpha\mathbf{R},s}\rangle
=
\frac{1}{\sqrt{N_k}}
\sum_{\mathbf{k}\in\mathcal{K}_s}
e^{-i\mathbf{k}\cdot\mathbf{R}}
\lvert\phi_{\alpha\mathbf{k},s}\rangle
}.
$$
Here, $i$ is the imaginary unit, $\mathbf{k}\cdot\mathbf{R}$ is the reciprocal-space pairing between a Bloch wavevector and a lattice vector, and the factor $N_k^{-1/2}$ gives a unitary discrete Fourier transform under the normalization convention used in this section.

The inverse transformation is
$$
\lvert\phi_{\alpha\mathbf{k},s}\rangle
=
\frac{1}{\sqrt{N_k}}
\sum_{\mathbf{R}\in\mathcal{L}_s^{(N_k)}}
e^{i\mathbf{k}\cdot\mathbf{R}}
\lvert w_{\alpha\mathbf{R},s}\rangle.
$$
The Bloch frame and the Wannier basis therefore contain the same information on the chosen finite mesh.

The Wannier states satisfy
$$
\langle
w_{\alpha\mathbf{R},s}
\vert
w_{\beta\mathbf{R}',s}
\rangle
=
\delta_{\alpha\beta}
\delta_{\mathbf{R}\mathbf{R}'},
$$
where $\delta_{\mathbf{R}\mathbf{R}'}$ is one when $\mathbf{R}=\mathbf{R}'$ and zero otherwise. Their lattice-translation property is
$$
\lvert w_{\alpha\mathbf{R},s}\rangle
=
\hat{T}_{\mathbf{R}}
\lvert w_{\alpha\mathbf{0},s}\rangle,
$$
where $\hat{T}_{\mathbf{R}}$ is the operator that translates a state by lattice vector $\mathbf{R}$.

## Wannier Centers and Quadratic Spreads
The center of the home-cell Wannier state $\lvert w_{\alpha\mathbf{0},s}\rangle$ is
$$
\overline{\mathbf{r}}_{\alpha,s}
=
\left\langle
w_{\alpha\mathbf{0},s}
\middle|
\hat{\mathbf{r}}
\middle|
w_{\alpha\mathbf{0},s}
\right\rangle,
$$
where $\hat{\mathbf{r}}$ is the position operator and $\overline{\mathbf{r}}_{\alpha,s}$ is the Wannier center. The quadratic spread of this state is
$$
\Omega_{\alpha,s}
=
\left\langle
w_{\alpha\mathbf{0},s}
\middle|
\hat{\mathbf{r}}^{\,2}
\middle|
w_{\alpha\mathbf{0},s}
\right\rangle
-
\left|
\overline{\mathbf{r}}_{\alpha,s}
\right|^2.
$$
The total spread of the $M_s$ home-cell Wannier states is
$$
\Omega_s
=
\sum_{\alpha=1}^{M_s}
\Omega_{\alpha,s}.
$$
Maximally localized Wannier functions are obtained by choosing the Bloch gauge that minimizes $\Omega_s$, subject to the selected projector field and any imposed symmetry constraints.

The numerical evaluation of position moments in a periodic crystal is performed through overlap matrices between neighboring Bloch states rather than through a direct application of an unbounded position operator to extended Bloch states. The center and spread formulas above define the corresponding real-space quantities represented by that procedure.

## Projected Hamiltonian in the Bloch Frame
The matrix representation of the projected fiber Hamiltonian in the selected Bloch frame is
$$
\left[
\mathbf{H}_s^{(P)}(\mathbf{k})
\right]_{\alpha\beta}
=
\left\langle
\phi_{\alpha\mathbf{k},s}
\middle|
\hat{H}_s^{(P)}(\mathbf{k})
\middle|
\phi_{\beta\mathbf{k},s}
\right\rangle.
$$
The matrix $\mathbf{H}_s^{(P)}(\mathbf{k})\in\mathbb{C}^{M_s\times M_s}$ acts on the retained coordinates at wavevector $\mathbf{k}$.

Under a gauge transformation $\mathbf{G}_s(\mathbf{k})$, the projected Hamiltonian matrix transforms as
$$
\mathbf{H}_s^{(P)}(\mathbf{k})
\mapsto
\mathbf{G}_s(\mathbf{k})^\dagger
\mathbf{H}_s^{(P)}(\mathbf{k})
\mathbf{G}_s(\mathbf{k}).
$$
This unitary similarity transformation changes the matrix entries but preserves the eigenvalues and the underlying projected operator.

## Real-Space Wannier Hamiltonian
Define the real-space Wannier Hamiltonian matrix by
$$
\left[
\mathbf{H}_{\mathrm{W},s}(\mathbf{R})
\right]_{\alpha\beta}
=
\left\langle
w_{\alpha\mathbf{0},s}
\middle|
\hat{H}_s^{(P)}
\middle|
w_{\beta\mathbf{R},s}
\right\rangle.
$$
The subscript $\mathrm{W}$ indicates that the operator is represented in the Wannier basis. The lattice vector $\mathbf{R}$ is the displacement from the home-cell orbital $\alpha$ to orbital $\beta$ in cell $\mathbf{R}$.

Using the discrete Fourier transform, the real-space matrix is
$$
\boxed{
\mathbf{H}_{\mathrm{W},s}(\mathbf{R})
=
\frac{1}{N_k}
\sum_{\mathbf{k}\in\mathcal{K}_s}
e^{-i\mathbf{k}\cdot\mathbf{R}}
\mathbf{H}_s^{(P)}(\mathbf{k})
}.
$$
The inverse transformation is
$$
\boxed{
\mathbf{H}_{\mathrm{W},s}(\mathbf{k})
=
\sum_{\mathbf{R}\in\mathcal{L}_s^{(N_k)}}
e^{i\mathbf{k}\cdot\mathbf{R}}
\mathbf{H}_{\mathrm{W},s}(\mathbf{R})
}.
$$
Here, $\mathbf{H}_{\mathrm{W},s}(\mathbf{k})$ is the Bloch Hamiltonian reconstructed from the real-space Wannier matrix elements. In the absence of truncation and numerical error, it is the same projected Hamiltonian expressed in the Wannier gauge.

For the bulk-silicon compatibility study, the accepted neutral `PeriodicElectronicStructureDataset` and its source manifest are the common workflow parent of both reduced-model reconstructions. The direct spectral branch consumes retained Kohn–Sham eigenvalue and band-derivative targets from that parent. The operator-mediated branch additionally consumes the validated Wannier Hamiltonian as a child representation and uses its aligned real-space matrix elements. A comparison may join the branches only after verifying common parentage, compatible specification versions, representation and energy metadata, artifact lineage, and required validation states.

Hermiticity of the parent operator implies
$$
\mathbf{H}_{\mathrm{W},s}(-\mathbf{R})
=
\mathbf{H}_{\mathrm{W},s}(\mathbf{R})^\dagger.
$$
The onsite block is $\mathbf{H}_{\mathrm{W},s}(\mathbf{0})$, while matrices with $\mathbf{R}\neq\mathbf{0}$ describe intercell hopping and other nonlocal couplings.

## Band Interpolation
The Wannier-interpolated energies are obtained from
$$
\mathbf{H}_{\mathrm{W},s}(\mathbf{k})
\mathbf{c}_{m,s}(\mathbf{k})
=
\widetilde{\varepsilon}_{m,s}(\mathbf{k})
\mathbf{c}_{m,s}(\mathbf{k}),
$$
where $m\in\{1,\ldots,M_s\}$ labels the interpolated bands, $\mathbf{c}_{m,s}(\mathbf{k})\in\mathbb{C}^{M_s}$ is an eigenvector in Wannier-orbital coordinates, and $\widetilde{\varepsilon}_{m,s}(\mathbf{k})$ is the corresponding interpolated eigenvalue.

On the construction mesh, an exact Fourier transform without real-space truncation reproduces the eigenvalues of the projected Hamiltonian up to numerical precision. Away from that mesh, agreement tests the quality and smoothness of the selected subspace and gauge.

## Localization and Operator Truncation
Wannier localization and Hamiltonian truncation must be distinguished. Localization changes the basis used to represent $\hat{H}_s^{(P)}$; truncation changes the represented operator.

For a real-space cutoff $R_c$, define the truncated Wannier matrix
$$
\mathbf{H}_{\mathrm{W},s}^{(R_c)}(\mathbf{R})
=
\begin{cases}
\mathbf{H}_{\mathrm{W},s}(\mathbf{R}),
&
\lvert\mathbf{R}\rvert\leq R_c,
\\
\mathbf{0},
&
\lvert\mathbf{R}\rvert>R_c.
\end{cases}
$$
Here, $R_c$ is the maximum retained hopping distance and $\mathbf{0}$ is the zero matrix. The resulting Bloch-space truncation error is
$$
\delta\mathbf{H}_s^{(R_c)}(\mathbf{k})
=
\mathbf{H}_{\mathrm{W},s}^{(R_c)}(\mathbf{k})
-
\mathbf{H}_{\mathrm{W},s}(\mathbf{k}).
$$
Unlike a gauge transformation, this truncation generally changes the spectrum and observables. It is therefore an operator reduction rather than a change of representation.

## Numerical Inputs to Wannier Construction
For a plane-wave electronic-structure calculation, Wannier construction uses the Kohnâ€“Sham eigenvalues together with overlaps between the cell-periodic parts of neighboring Bloch states. Write the real-space Bloch eigenfunction as
$$
\psi_{n\mathbf{k},s}(\mathbf{r})
=
e^{i\mathbf{k}\cdot\mathbf{r}}
u_{n\mathbf{k},s}(\mathbf{r}),
$$
where $u_{n\mathbf{k},s}(\mathbf{r})$ has the periodicity of the chosen unit cell. A representative neighbor-overlap matrix is
$$
\left[
\mathbf{M}_s^{(\mathbf{k},\mathbf{b})}
\right]_{mn}
=
\left\langle
u_{m\mathbf{k},s}
\middle|
u_{n,\mathbf{k}+\mathbf{b},s}
\right\rangle,
$$
where $\mathbf{b}$ connects neighboring points on the Brillouin-zone mesh, and $m$ and $n$ label candidate Bloch states. Initial orbital information may be supplied through projection amplitudes
$$
\left[
\mathbf{A}_s(\mathbf{k})
\right]_{n\alpha}
=
\left\langle
\psi_{n\mathbf{k},s}
\middle|
g_{\alpha,s}
\right\rangle,
$$
where $\lvert g_{\alpha,s}\rangle$ is a localized trial orbital. The eigenvalues, neighbor overlaps, and trial-orbital projections provide the numerical data required for subspace selection and localization.

## Validation Requirements
A Wannier construction is accepted only after the following properties have been checked:

1. the Wannier-interpolated bands reproduce the projected Kohnâ€“Sham bands within a stated energy window and tolerance;
2. the Wannier states remain orthonormal to numerical precision;
3. the Hamiltonian satisfies the Hermiticity relation $\mathbf{H}_{\mathrm{W},s}(-\mathbf{R})=\mathbf{H}_{\mathrm{W},s}(\mathbf{R})^\dagger$;
4. the Wannier centers, orbital characters, and symmetry relations are physically consistent;
5. the quadratic spreads are finite and stable under reasonable changes in initial projections and numerical parameters;
6. the real-space matrix elements decay sufficiently with $\lvert\mathbf{R}\rvert$ for subsequent truncation studies;
7. the construction is stable under controlled changes in the outer window, frozen window, and localization settings.

These tests distinguish faithful representation of a selected projected operator from the separate question of whether that projected operator is itself the appropriate physical reduction.

## Role in the Reduction Program
The construction established in this section is
$$
\boxed{
\left\{
\hat{H}_s^{(P)}(\mathbf{k})
\right\}_{\mathbf{k}\in\mathrm{BZ}_s}
\xleftrightarrow{\text{Wannier representation}}
\left\{
\mathbf{H}_{\mathrm{W},s}(\mathbf{R})
\right\}_{\mathbf{R}\in\mathcal{L}_s}
}.
$$
The double arrow denotes an exact change of representation when the same projector field is retained and the Fourier transform is not truncated. Disentanglement precedes this equivalence because it determines which projected operator is being represented.

The construction is performed independently for the bulk and dopant systems. Their Wannier matrices cannot yet be subtracted merely because both are localized. The required correspondence between their orbital labels, state spaces, gauges, and energy references is developed in [[ksdft2Effmass.04]].

## References
	[1] N. Marzari and D. Vanderbilt, Maximally localized generalized Wannier functions for composite energy bands. *Phys. Rev. B*, vol. 56, pp. 12847â€“12865, 1997, doi: 10.1103/PhysRevB.56.12847.

[2] I. Souza, N. Marzari, and D. Vanderbilt, â€œMaximally localized Wannier functions for entangled energy bands,â€ *Phys. Rev. B*, vol. 65, Art. no. 035109, 2001, doi: 10.1103/PhysRevB.65.035109.

[3] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, â€œMaximally localized Wannier functions: Theory and applications,â€ *Rev. Mod. Phys.*, vol. 84, pp. 1419â€“1475, 2012, doi: 10.1103/RevModPhys.84.1419.

[4] A. A. Mostofi et al., â€œAn updated version of Wannier90: A tool for obtaining maximally-localised Wannier functions,â€ *Comput. Phys. Commun.*, vol. 185, pp. 2309â€“2310, 2014, doi: 10.1016/j.cpc.2014.05.003.