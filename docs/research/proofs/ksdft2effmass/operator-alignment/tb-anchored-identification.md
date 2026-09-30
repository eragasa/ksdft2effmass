# TB-Anchored Identification

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 3. Gauge covariance and TB anchoring

Let $\mathbf{X}_{s}(\mathbf k)$ denote fixed TB reference orbitals with consistent orbital labeling. Define the projected reference orbitals
$$
\mathbf Y_s(\mathbf k)=\hat P_s(\mathbf k)\mathbf X_s(\mathbf k).
$$
Assume $\mathbf Y_s(\mathbf k)$ has full column rank, so that the Löwdin-orthonormalized frames
$$
\widetilde{\mathbf V}_s(\mathbf k) =\mathbf Y_s(\mathbf k)\left[\mathbf Y_s^\dagger(\mathbf k)\mathbf Y_s(\mathbf k)\right]^{-1/2}
$$
are well defined. This construction is the standard "projection + Löwdin orthonormalization" procedure used to generate an initial gauge for Wannier-function calculations: localized trial orbitals are projected onto the Bloch subspace at each $\mathbf k$, then orthonormalized to produce a smooth, gauge-fixed Bloch-like frame [^MarzariVanderbilt1997][^SouzaMarzariVanderbilt2001][^PizziEtAl2020].

Under a $\mathbf k$-dependent unitary gauge transformation of the underlying Bloch basis, $\mathbf X_s(\mathbf k)\mapsto \mathbf X_s(\mathbf k)\mathbf W_s(\mathbf k)$ with $\mathbf W_s(\mathbf k)$ unitary, the projected orbitals transform as
$$
\mathbf Y_s(\mathbf k)\mapsto \hat P_s(\mathbf k)\mathbf X_s(\mathbf k)\mathbf W_s(\mathbf k)=\mathbf Y_s(\mathbf k)\mathbf W_s(\mathbf k),
$$
and the overlap matrix transforms covariantly:
$$
\mathbf Y_s^\dagger(\mathbf k)\mathbf Y_s(\mathbf k)\mapsto \mathbf W_s^\dagger(\mathbf k)\left[\mathbf Y_s^\dagger(\mathbf k)\mathbf Y_s(\mathbf k)\right]\mathbf W_s(\mathbf k).
$$
Consequently,
$$
\left[\mathbf Y_s^\dagger(\mathbf k)\mathbf Y_s(\mathbf k)\right]^{-1/2}
\mapsto
\mathbf W_s^\dagger(\mathbf k)\left[\mathbf Y_s^\dagger(\mathbf k)\mathbf Y_s(\mathbf k)\right]^{-1/2}\mathbf W_s(\mathbf k),
$$
and the orthonormalized frame transforms as
$$
\widetilde{\mathbf V}_s(\mathbf k)\mapsto \widetilde{\mathbf V}_s(\mathbf k)\mathbf W_s(\mathbf k).
$$
Thus $\widetilde{\mathbf V}_s(\mathbf k)$ is gauge-covariant: it tracks the gauge of the reference orbitals while remaining orthonormal by construction. This property ensures that any Hamiltonian representation built in the $\widetilde{\mathbf V}_s(\mathbf k)$ basis inherits a well-defined gauge behavior, which is essential for comparing pristine and doped systems on an equal footing [^Kunes2011][^MostofiEtAl2008].

The frames $\widetilde{\mathbf V}_s(\mathbf k)$ provide a natural tight-binding anchoring: they define a common, orthonormal, gauge-covariant basis in which to express the retained Hamiltonians $\hat H_s^{(P)}(\mathbf k)$ and, subsequently, the aligned impurity operator $\Delta\hat H_d^{(P)}(\mathbf k)$. In practice, this is analogous to choosing a set of symmetry-adapted Wannier-like orbitals as the reference basis for downfolding, ensuring that the impurity perturbation is represented in a physically transparent, orbital-resolved form [^Kunes2011][^PizziEtAl2020].

## References

[^MarzariVanderbilt1997]: N. Marzari and D. Vanderbilt, "Maximally localized generalized Wannier functions for composite energy bands," *Phys. Rev. B* **56**, 12847 (1997).

[^SouzaMarzariVanderbilt2001]: I. Souza, N. Marzari, and D. Vanderbilt, "Maximally localized Wannier functions for entangled energy bands," *Phys. Rev. B* **65**, 035109 (2001).

[^Kato1995]: T. Kato, *Perturbation Theory for Linear Operators*, Springer (1995).

[^ReedSimon1980]: M. Reed and B. Simon, *Methods of Modern Mathematical Physics, Vol. I: Functional Analysis*, Academic Press (1980).

[^Kunes2011]: A. Kuneš, "Wannier Functions and Construction of Model Hamiltonians," in *Correlated Electrons: From Models to Materials*, Forschungszentrum Jülich (2011).

[^MostofiEtAl2008]: A. A. Mostofi *et al.*, "wannier90: A tool for obtaining maximally-localised Wannier functions," *Comput. Phys. Commun.* **178**, 685–699 (2008).

[^GeorgesEtAl1996]: A. Georges, G. Kotliar, W. Krauth, and M. J. Rozenberg, "Dynamical mean-field theory of the Mott transition," *Rev. Mod. Phys.* **68**, 13 (1996).

[^Wannier90Docs]: Wannier90 collaboration, "Wannier90 User Guide and Documentation," https://wannier.org (accessed 2026).

[^MazzolaEtAl2020]: F. Mazzola *et al.*, "The sub-band structure of atomically sharp dopant profiles in silicon," *npj Quantum Mater.* **5**, 34 (2020).

[^Mahan1983]: G. D. Mahan, "Band-gap narrowing in heavily doped silicon," *Phys. Rev. B* **28**, 2286 (1983).

[^PizziEtAl2020]: G. Pizzi *et al.*, "Wannier90 as a community code: new features and applications," *J. Phys.: Condens. Matter* **32**, 165902 (2020).


---

## TB-Anchored Projector Identification
## Assumptions

- $\mathbf P_s(\mathbf k)$ is the orthogonal projector onto the retained DFT subspace at wavevector $\mathbf k$.
- $\mathbf X_s(\mathbf k)$ contains fixed TB reference orbitals with a consistent orbital labeling across the pristine and doped systems.
- $\mathbf Y_s(\mathbf k)=\mathbf P_s(\mathbf k)\mathbf X_s(\mathbf k)$ has full column rank, so $\mathbf Y_s^\dagger(\mathbf k)\mathbf Y_s(\mathbf k)$ is positive definite.
- The retained pristine and doped subspaces have the same dimension, so an identification map between them can be defined.
- Any change of basis within the retained DFT space is unitary and does not alter the underlying projector as an operator.
- The orthonormalized projected orbitals $\widetilde{\mathbf V}_s(\mathbf k)=\mathbf Y_s(\mathbf k)\left[\mathbf Y_s^\dagger(\mathbf k)\mathbf Y_s(\mathbf k)\right]^{-1/2}$ are well defined.
- $\widetilde{\mathbf V}_b(\mathbf k)$ and $\widetilde{\mathbf V}_d(\mathbf k)$ are orthonormal bases for the pristine and doped retained subspaces, respectively.
- The identification operator $\hat U_d(\mathbf k)=\widetilde{\mathbf V}_d(\mathbf k)\widetilde{\mathbf V}_b^\dagger(\mathbf k)$ is therefore unitary on the retained subspace.
- The aligned impurity operator $\Delta\hat H_d(\mathbf k)=\hat H_d^{(P)}(\mathbf k)-\hat U_d(\mathbf k)\hat H_b^{(P)}(\mathbf k)\hat U_d^\dagger(\mathbf k)$ compares Hamiltonians expressed in the same identified retained subspace.
### Proposition 1: Spectral Data Do Not Identify a Projector

The eigenvalues of a reduced Hamiltonian do not uniquely determine its embedding in the ambient DFT state space. Unitarily related operators can have identical spectra while acting on differently embedded retained subspaces.

This is standard: the spectrum is invariant under unitary equivalence, but it does not by itself determine the embedding of a reduced operator in the ambient Hilbert space; see, for example, Taylor’s treatment of the spectral theorem and Kowalski’s notes on spectral theory. \cite{TaylorSpectralTheorem,KowalskiSpectralTheory}

@misc{TaylorSpectralTheorem,
  author       = {Taylor, Michael E.},
  title        = {The Spectral Theorem for Self-Adjoint and Unitary Operators},
  howpublished = {Lecture notes},
  url          = {https://mtaylor.web.unc.edu/wp-content/uploads/sites/16915/2018/04/specthm.pdf},
  note         = {Accessed 2026-08-05}
}

@misc{KowalskiSpectralTheory,
  author       = {Kowalski, Emmanuel},
  title        = {Spectral theory in Hilbert spaces},
  howpublished = {Lecture notes, ETH Z\"urich},
  url          = {https://people.math.ethz.ch/~kowalski/spectral-theory.pdf},
  note         = {Accessed 2026-08-05}
}
### Proposition 2: Orbital-Anchored Coordinates Are Independent of the Input DFT Gauge

Let $\mathbf P_s(\mathbf k)$ be a retained-space projector and let $\mathbf X_s(\mathbf k)$ contain fixed TB reference orbitals. Define

$$
\mathbf Y_s(\mathbf k)
=
\mathbf P_s(\mathbf k)\mathbf X_s(\mathbf k)
$$

and, when $\mathbf Y_s(\mathbf k)$ has full column rank,

$$
\widetilde{\mathbf V}_s(\mathbf k)
=
\mathbf Y_s(\mathbf k)
\left[
\mathbf Y_s(\mathbf k)^\dagger
\mathbf Y_s(\mathbf k)
\right]^{-1/2}.
$$
$\blacksquare$
The orbital-anchored basis defined by symmetric orthonormalization is invariant under changes of basis within the retained subspace, since the projector is basis-independent as an operator and Löwdin orthonormalization removes the internal gauge freedom of the projected reference orbitals. \cite{Lowdin1950,HelgakerJorgensenOlsen2000}

@article{Lowdin1950,
  author  = {L{\"o}wdin, Per-Olov},
  title   = {On the Non-Orthogonality Problem Connected with the Use of Atomic Wave Functions in the Theory of Molecules and Crystals},
  journal = {The Journal of Chemical Physics},
  volume  = {18},
  number  = {3},
  pages   = {365--375},
  year    = {1950},
  doi     = {10.1063/1.1747632}
}

@book{HelgakerJorgensenOlsen2000,
  author    = {Helgaker, Trygve and J{\o}rgensen, Poul and Olsen, Jeppe},
  title     = {Molecular Electronic-Structure Theory},
  publisher = {Wiley},
  year      = {2000}
}

Then $\widetilde{\mathbf V}_s(\mathbf k)$ depends only on the projector and reference orbitals, not on the particular basis used to represent the retained DFT subspace.

### Proposition 3: Corresponding TB Coordinates Induce an Identification Map

If the pristine and doped projected reference orbitals have equal dimension and full column rank, then

$$
\hat U_d(\mathbf k)
=
\widetilde{\mathbf V}_d(\mathbf k)
\widetilde{\mathbf V}_b(\mathbf k)^\dagger
$$

defines a unitary identification between their retained subspaces. The aligned impurity operator is

$$
\Delta\hat H_d(\mathbf k)
=
\hat H_d^{(P)}(\mathbf k)
-
\hat U_d(\mathbf k)
\hat H_b^{(P)}(\mathbf k)
\hat U_d(\mathbf k)^\dagger.
$$

---
