# Bloch-Fiber Correspondence

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## Bloch-fiber correspondence

Under the direct-sum structure introduced in the mathematical setting, the global operators in Definitions 1 and 2 have equivalent fiberwise representations. Assuming that $\hat H_s$ and $\hat P_s$ preserve the Bloch-fiber decomposition associated with the common translation group,

$$
\hat H_s
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\hat H_s(\mathbf k),
\qquad
\hat P_s
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\hat P_s(\mathbf k).
$$

The retained Hamiltonian therefore decomposes as

$$
\hat H_s^{(P)}
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\hat H_s^{(P)}(\mathbf k),
$$

where

$$
\hat H_s^{(P)}(\mathbf k)
=
\left.
\hat P_s(\mathbf k)
\hat H_s(\mathbf k)
\hat P_s(\mathbf k)
\right|_{\mathcal H_s^{(P)}(\mathbf k)}.
$$

Thus, the global retained Hamiltonian $\hat H_s^{(P)}$ is uniquely determined by the family

$$
\left\{
\hat H_s^{(P)}(\mathbf k)
\right\}_{\mathbf k\in\mathcal K_L},
$$

and conversely this family defines the global operator through the direct sum. This correspondence is the Bloch-fiber form of the standard compression of a self-adjoint operator to a retained subspace [@kato1995; @reedsimon1980]. In Wannier-based model construction, the retained fiber operators are represented in a smooth Bloch gauge and subsequently transformed into a localized basis [@marzarivanderbilt1997; @souzamarzarivanderbilt2001; @mostofietal2008; @wannier90docs].

If the identification map is required to preserve the Bloch-fiber decomposition, it has the form

$$
\hat U_d
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\hat U_d(\mathbf k),
$$

where

$$
\hat U_d(\mathbf k):
\mathcal H_b^{(P)}(\mathbf k)
\longrightarrow
\mathcal H_d^{(P)}(\mathbf k)
$$

is unitary for every $\mathbf k$. Such a fiberwise unitary correspondence exists if and only if

$$
M_b(\mathbf k)=M_d(\mathbf k)
\qquad
\text{for every }\mathbf k\in\mathcal K_L.
$$

The fixed-rank fiber condition is also the structure used in disentanglement procedures to construct a smooth active subspace across the sampled Brillouin zone [@souzamarzarivanderbilt2001; @mostofietal2008; @wannier90docs]. For doped systems, band shifts and impurity-derived subbands can alter which states intersect a fixed energy window, so this rank correspondence must be enforced by the retained-subspace construction rather than assumed from the energy window alone [@mazzolaetal2020; @mahan1983].

Under the fiberwise correspondence, transport of the pristine retained Hamiltonian into the doped retained space decomposes as

$$
\hat U_d
\hat H_b^{(P)}
\hat U_d^\dagger
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\hat U_d(\mathbf k)
\hat H_b^{(P)}(\mathbf k)
\hat U_d(\mathbf k)^\dagger.
$$

It follows that the doped-space aligned difference decomposes as

$$
\Delta\hat H_{b\rightarrow d}^{(P)}
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\Delta\hat H_{b\rightarrow d}^{(P)}(\mathbf k),
$$

with

$$
\Delta\hat H_{b\rightarrow d}^{(P)}(\mathbf k)
=
\hat H_d^{(P)}(\mathbf k)
-
\hat U_d(\mathbf k)
\hat H_b^{(P)}(\mathbf k)
\hat U_d(\mathbf k)^\dagger.
$$

The pristine-space dual decomposes as

$$
\Delta\hat H_{d\rightarrow b}^{(P)}
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\left[
\hat U_d(\mathbf k)^\dagger
\hat H_d^{(P)}(\mathbf k)
\hat U_d(\mathbf k)
-
\hat H_b^{(P)}(\mathbf k)
\right].
$$

Because every $\hat U_d(\mathbf k)$ is unitary, the two fiberwise families are unitarily equivalent representations of the same aligned operator difference. The global and fiberwise formulations therefore describe the same aligned operator: each global formulation acts on its declared retained space, while the fiberwise formulation resolves that action independently at each Bloch wavevector. Transporting both Hamiltonians into a common retained representation is the operator-level correspondence underlying downfolding and common-subspace comparisons [@georgesetal1996; @kunes2011].
