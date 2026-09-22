# The Kohn–Sham Operator as the Computational Starting Point
back_to: [[ksdft2effmass.00]]
## Scope of the Electronic-Structure Description
The operator reductions developed in this dissertation are conditional on a parent electronic-structure description. The parent object is the self-consistent effective one-particle operator obtained from a Kohn–Sham density-functional calculation. Subsequent claims of operator, spectral, or state fidelity are therefore claims relative to this specified first-principles reference.

The purpose of this section is to define that reference and delimit its physical interpretation. The derivation of density-functional theory from the interacting many-electron problem is not itself part of the dissertation. Only the distinctions required for the later projection, Wannierization, and model-reduction steps are retained here.
## Interacting Electronic Problem
Within the Born–Oppenheimer approximation, and for a fixed nuclear configuration, the electronic system is described by an interacting $N$-electron Hamiltonian
$$
\hat{H}_{\mathrm{MB}}
:\mathcal{D}(\hat H_{\mathrm{MB}})
\subset
\mathcal{H}_{\mathrm{MB}}
\rightarrow
\mathcal{H}_{\mathrm{MB}},
$$
where $\mathcal{H}_{\mathrm{MB}}=\bigwedge^N\mathcal{H}_1$ is the antisymmetric $N$-electron Hilbert space constructed from a one-particle space $\mathcal H_1$. Schematically,
$$
\hat H_{\mathrm{MB}}
= \sum_{i=1}^{N}
	\left[
		- \frac{\hbar^2}{2m_e}\nabla_i^2
		+ v_{\mathrm{ext}}(\mathbf r_i)
	\right]
	+
	\frac{1}{2}
	\sum_{\substack{i,j=1\\i\neq j}}^{N}
		\frac{e^2}
			 {
				 4\pi\varepsilon_0
				 \lvert\mathbf r_i-\mathbf r_j\rvert
			 }.
$$
A stationary many-electron state satisfies
$$
\hat H_{\mathrm{MB}} \lvert\Psi_j\rangle
=
E_j
\lvert\Psi_j\rangle.
$$
The ground-state density is obtained from $\Psi_0$ according to
$$
n_0(\mathbf r)
=
N 
\int
	\left|
		\Psi_0(
			\mathbf r,
			\mathbf r_2,
			\ldots,
			\mathbf r_N)
	\right|^2
\mathrm d\mathbf r_2
\cdots
\mathrm d\mathbf r_N,

$$
with spin variables suppressed. The many-electron wavefunction depends on $3N$ spatial coordinates in addition to spin, and its representation in a finite one-particle basis grows combinatorially with system size. This scaling motivates a reformulation in terms of reduced variables.
## Density-Functional and Kohn–Sham Formulation
For a nondegenerate ground state, the Hohenberg–Kohn results establish that the ground-state density determines the external potential up to an additive constant and that the ground-state energy follows from a variational density functional [^1]. Kohn and Sham introduced an auxiliary noninteracting system constructed to reproduce the interacting ground-state density [^2].

Subject to the required representability conditions, the conceptual relation may be written as
$$
\left(
	\hat H_{\mathrm{MB}},
	\lvert\Psi_0\rangle
\right)
\rightarrow n_0(\mathbf r)
\rightarrow v_{\mathrm s}[n_0](\mathbf r)
\rightarrow \hat H_{\mathrm{KS}}[n_0].
$$
This relation is a density-functional reformulation of specified ground-state information. It is not obtained by projecting the many-electron Hamiltonian onto a one-particle subspace. An expression of the form $\hat{P}\hat{H}_{\mathrm{MB}}\hat{P}$ continues to define an operator on a subspace of $\mathcal H_{\mathrm{MB}}$; it does not produce an operator on $\mathcal H_1$ without an additional map between the two state spaces. The Kohn–Sham construction and the spectral projections introduced later in the dissertation are therefore mathematically distinct operations.
## Periodic Self-Consistent Kohn–Sham Problem
For a periodic crystal, the self-consistent Kohn–Sham operator is invariant under translations by direct-lattice vectors. Bloch decomposition expresses the periodic operator as a family of fiber operators:
$$
\hat H_{\mathrm{KS}}[n]
\cong
\int_{\mathrm{BZ}}^{\oplus}
	\hat H_{\mathrm{KS}}(\mathbf k;n)
	\,\mathrm{d}\mathbf k,
$$
where $\mathbf k$ lies in the first Brillouin zone. The Bloch-resolved eigenproblem is
$$
\hat H_{\mathrm{KS}}(\mathbf k;n)
\lvert\psi_{n\mathbf k}\rangle
=
\epsilon_{n\mathbf k}
\lvert\psi_{n\mathbf k}\rangle.
$$
For a pseudopotential calculation, the effective one-particle operator may be written as
$$
\hat H_{\mathrm{KS}}[n]
=
\hat T
+ \hat V_{\mathrm{ion}}^{\mathrm{loc}}
+ \hat V_{\mathrm{ion}}^{\mathrm{nl}}
+ \hat V_{\mathrm H}[n]
+ \hat V_{\mathrm{xc}}[n],
$$
where:
- $\hat T$ is the one-electron kinetic-energy operator;
- $\hat V_{\mathrm{ion}}^{\mathrm{loc}}$ is the local part of the electron–ion interaction;
- $\hat V_{\mathrm{ion}}^{\mathrm{nl}}$ is the nonlocal pseudopotential contribution;
- $\hat V_{\mathrm H}[n]$ is the Hartree potential;
- $\hat V_{\mathrm{xc}}[n]$ is the exchange-correlation potential

The nonlocal ionic contribution is retained explicitly because nonlocal operator structure may already be present before any hybrid-functional, DFT+$U$, projection, or model-reduction step [^4].

The current semilocal silicon path is accurately described by the Kohn–Sham notation above. The longer-term periodic integration boundary also permits generalized Kohn–Sham methods. A hybrid GKS operator is represented schematically as

$$
\hat H_{\mathrm{GKS}}
=
\hat T
+
\hat V_{\mathrm{ext}}
+
\hat V_{\mathrm H}
+
\hat V_{\mathrm{xc}}^{\mathrm{local}}
+
\alpha\hat V_{\mathrm x}^{\mathrm{Fock}},
$$

where $\alpha$ is the exact-exchange fraction; range-separated hybrids may additionally require a parameter $\omega$. Global, screened, and range-separated hybrid GKS calculations require method-specific pseudopotential compatibility, numerical implementation, convergence, and verification evidence. They are planned but not implemented or qualified. Semilocal KS evidence cannot be used as hybrid GKS qualification. DFT+$U$ is not assigned a current integration profile by this architecture correction.

Both KS and GKS calculations remain inside the present integration domain only when they are periodic crystalline calculations organized in Bloch fibers. Molecular-orbital and finite-system implementations remain outside scope.

For a continuous Brillouin-zone representation, the density is
$$
n(\mathbf r)
= \sum_n
	\int_{\mathrm{BZ}}
		f_{n\mathbf k}
		\left|\psi_{n\mathbf k}(\mathbf r)\right|^2
		\frac{\mathrm d\mathbf k}
		{\Omega_{\mathrm{BZ}}},
$$
where $f_{n\mathbf k}$ is the occupation and $\Omega_{\mathrm{BZ}}$ is the Brillouin-zone volume. On a discrete numerical mesh,
$$
n(\mathbf r)
\approx
\sum_{\mathbf k}
w_{\mathbf k}
\sum_n
f_{n\mathbf k}
\left|\psi_{n\mathbf k}(\mathbf r)\right|^2,
$$
where $w_{\mathbf k}$ is the integration weight.

Let
$$
\mathcal F_{\mathrm{KS}}
:
n_{\mathrm{in}}
	\longmapsto
	n_{\mathrm{out}}
$$
denote the density map defined by constructing $\hat H_{\mathrm{KS}}[n_{\mathrm{in}}]$, solving its occupied eigenstates, and reconstructing the unmixed output density. A numerical SCF algorithm may form the next input through a mixing map,
$$
n_{\mathrm{in}}^{(i+1)}
=
\mathcal M_i\!\left(
n_{\mathrm{in}}^{(i)},
n_{\mathrm{out}}^{(i)}
\right),
$$
so the reconstructed output density and the next mixed input density are not generally identical. Mixing is numerical solver behavior; it does not change the physical fixed point. The self-consistent density is a fixed point:
$$
\boxed{
	n_0
	=
\mathcal F_{\mathrm{KS}}[n_0].
}
$$
In a numerical calculation, the code applies its declared SCF convergence criterion to an implementation-specific residual or energy estimate. A density-residual criterion may, for example, take the form
$$
\left\|
	n_{\mathrm{out}}
	- n_{\mathrm{in}}
\right\|
\leq
\tau_{\mathrm{SCF}},
$$
but this expression is illustrative unless the selected backend and retained provenance establish that exact norm and tolerance. Satisfaction of an iterative SCF criterion is also distinct from convergence with respect to basis cutoffs, Brillouin-zone sampling, retained bands, geometry, or a downstream observable. The converged parent operator is consequently $\hat{H}_{\mathrm{KS}}[n_0],$ together with the exchange-correlation approximation, electron–ion representation, crystal geometry, boundary conditions, basis or discretization, Brillouin-zone sampling, and self-consistency criterion used to construct it.
## Interpretation of the Parent Operator
With the exact density functional, ground-state density-functional theory yields the exact ground-state density and energy. Practical calculations use approximate exchange-correlation functionals, so functional error enters before the subsequent projection and model-reduction steps.

The Kohn–Sham eigenstates and eigenvalues belong to the auxiliary one-particle problem. They are not generally identical to the quasiparticle states and excitation energies of the interacting system. For a semiconductor, the fundamental gap is not generally equal to the Kohn–Sham eigenvalue gap [3].

Accordingly, the reduced models constructed later inherit the information content and approximations of $\hat H_{\mathrm{KS}}[n_0]$. Agreement with the parent operator establishes fidelity to the selected Kohn–Sham reference. It does not, by itself, establish fidelity to the exact interacting excitation spectrum or to experiment.
## Projection and Wannier Representation
The first reduction applied within the one-particle description is the selection of a target band subspace. At each $\mathbf k$, let
$$
\hat{P}(\mathbf k)
:\mathcal H_{1,\mathbf k}
	\rightarrow
	\mathcal{H}_{1,\mathbf k}
$$
be the orthogonal projector onto the retained Bloch subspace. The projected fiber operator is
$$
\hat H^{(P)}(\mathbf{k})
= \hat{P}(\mathbf{k})
	\hat{H}_{\mathrm{KS}}(\mathbf{k})
	\hat{P}(\mathbf{k})
	\big|_{\operatorname{Range}(\hat{P}(\mathbf{k}))}.
$$
Projection changes the retained state space and may discard electronic information. The geometry and comparison of these projected state spaces are developed in [[ksdft2Effmass.02]].

Wannierization is the subsequent construction of a localized basis for the family of retained Bloch subspaces. For an isolated group of bands, a $\mathbf k$-dependent unitary matrix $\mathbf U(\mathbf k)$ defines Wannier states
$$
\lvert w_{\alpha\mathbf R} \rangle
=
\frac{1}{N_k}
\sum_{\mathbf k}
	e^{-i\mathbf k\cdot\mathbf R}
\sum_n
	\lvert \psi_{n\mathbf k} \rangle
U_{n\alpha}(\mathbf k).
$$
The real-space Wannier Hamiltonian is
$$
H_{\mathrm W,\alpha\beta}(\mathbf{R})
	= \frac{1}{N_k}
	\sum_{\mathbf k}
	e^{-i\mathbf k\cdot\mathbf{R}}
\left[
	\mathbf{U}^\dagger(\mathbf{k})
	\mathbf{H}^{(P)}(\mathbf{k})
	\mathbf U(\mathbf{k})
\right]_{\alpha\beta}.
$$
The projected operator and its Wannier matrix representation must therefore be distinguished:
$$
\hat{H}^{(P)}
	\quad \overset{\text{Wannier representation}}{\longleftrightarrow}
	\quad \mathbf{H}_{\mathrm{W}}.
$$
For an isolated band subspace, Wannierization changes the basis but preserves the projected operator up to unitary equivalence [^5]. When the target bands are entangled with other bands, a disentanglement procedure first selects an optimized subspace and thereby modifies the projector itself [^6]. The detailed construction, localization functional, and gauge dependence are developed in [[ksdft2Effmass.03]].
## Adopted Reduction Chain
The sequence analyzed in the dissertation is
$$
\boxed{
	\hat{H}_{\mathrm{KS}}
	\longrightarrow \hat{H}^{(P)}
	\overset{\text{Wannier representation}}{\longleftrightarrow}
		\mathbf{H}_{\mathrm W}
	\longrightarrow
		\mathbf{H}_{\mathrm{red}}
	\longrightarrow
		\hat{H}_{\mathrm{continuum}}
}.
$$
The arrows have different meanings:

| Step                                                             | Mathematical action                     | Immediate consequence                           |
| ---------------------------------------------------------------- | --------------------------------------- | ----------------------------------------------- |
| $\hat H_{\mathrm{KS}}\rightarrow\hat H^{(P)}$                    | Target-subspace projection              | Changes the retained state space                |
| $\hat H^{(P)}\leftrightarrow\mathbf H_{\mathrm W}$               | Wannier basis construction              | Changes the representation                      |
| $\mathbf H_{\mathrm W}\rightarrow\mathbf H_{\mathrm{red}}$       | Restriction of operator content         | Introduces a lattice-model approximation        |
| $\mathbf H_{\mathrm{red}}\rightarrow\hat H_{\mathrm{continuum}}$ | Coarse-graining or asymptotic reduction | Changes the state space and spatial description |
The first two steps establish the localized first-principles reference from which the later bulk and impurity operator reductions are defined.

The lattice-model step is not restricted to a single fitting procedure. In [[ksdft2Effmass.05]], the same validated localized reference supplies both the spectral observations used in an inverse tight-binding reconstruction and the matrix elements used in a direct aligned-operator reconstruction. Sufficiently complete spectral information may identify an operator within a restricted model class. The computational question is whether the finite spectral constraints and the aligned-operator constraints admit a common reduced Hamiltonian
#### References
[^1]: P. Hohenberg and W. Kohn, “Inhomogeneous electron gas,” *Phys. Rev.*, vol. 136, pp. B864–B871, 1964, doi: 10.1103/PhysRev.136.B864.
[^2]: W. Kohn and L. J. Sham, “Self-consistent equations including exchange and correlation effects,” *Phys. Rev.*, vol. 140, pp. A1133–A1138, 1965, doi: 10.1103/PhysRev.140.A1133.
[^3]: L. J. Sham and M. Schlüter, “Density-functional theory of the energy gap,” *Phys. Rev. Lett.*, vol. 51, pp. 1888–1891, 1983, doi: 10.1103/PhysRevLett.51.1888.
[^4]: L. Kleinman and D. M. Bylander, “Efficacious form for model pseudopotentials,” *Phys. Rev. Lett.*, vol. 48, pp. 1425–1428, 1982, doi: 10.1103/PhysRevLett.48.1425.
[^5]: N. Marzari and D. Vanderbilt, “Maximally localized generalized Wannier functions for composite energy bands,” *Phys. Rev. B*, vol. 56, pp. 12847–12865, 1997, doi: 10.1103/PhysRevB.56.12847.
[^6]: I. Souza, N. Marzari, and D. Vanderbilt, “Maximally localized Wannier functions for entangled energy bands,” *Phys. Rev. B*, vol. 65, Art. no. 035109, 2001, doi: 10.1103/PhysRevB.65.035109.