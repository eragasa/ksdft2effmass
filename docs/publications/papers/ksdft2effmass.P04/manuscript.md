# Representation-Controlled Impurity Extraction and Atomistic-to-Continuum Reduction for Doped Semiconductors

> Status: Working cross-paper manuscript and repository projection organized under P04. The publication registry remains authoritative: impurity extraction is P04, while phosphorus and boron continuum-crossover claims remain assigned to P06 and P08. See the workspace [proof status](../../../proofs/ksdft2effmass/proof-status.md). Prospective statements authorize the corresponding in-repository work described below, but do not represent that work as completed or scientifically validated.

## Working-Document Contract

This Markdown manuscript is a living projection of the scientific, mathematical, computational, and software work represented in the repository. It is not merely a narrative written after the work is finished.

- Links identify existing repository owners for definitions, assumptions, implementations, workflows, evidence, and proof obligations.
- A proposed link identifies an intended repository owner that does not yet exist or is not yet assigned; it is a work item, not evidence of completion.
- A prospective statement authorizes creation or refinement of the in-repository artifacts needed to realize that statement within the manuscript's declared scope.
- A statement becomes a calculated result, proved result, verified result, or validated claim only when its owning repository artifacts and required evidence exist.
- This authorization does not silently change frozen scientific settings, publication scope, or human-acceptance status, and it does not replace the applicable checkpoint for protected external or production execution.

## Repository Projection

| Manuscript concern | Repository owner or proposed link | Projection status |
|---|---|---|
| Physical parent problems for pristine Si, P:Si, and B:Si | [Physical specification](../../../../specification/ksdft2Effmass.physical-specification.v1.md) | Existing authoritative contract |
| Numerical protocols and provenance requirements | [Numerical specification](../../../../specification/ksdft2Effmass.numerical-specification.v1.md) | Existing authoritative contract |
| Pristine–doped alignment | [Alignment research](../../../research/ksdft2Effmass.04.md) and [alignment proof units](../../../proofs/ksdft2effmass/operator-alignment/) | Existing research owner plus proposed proofs |
| Impurity-operator extraction | [Extraction research](../../../research/ksdft2Effmass.06.md) and [aligned impurity proof](../../../proofs/ksdft2effmass/operator-alignment/aligned-impurity-operator.md) | Existing research owner plus proposed proof |
| Local and nonlocal impurity reduction | [Impurity reduction research](../../../research/ksdft2Effmass.07.md) | Existing research owner |
| Atomistic-to-continuum reduction | [Continuum research](../../../research/ksdft2Effmass.08.md) and [continuum proof unit](../../../proofs/ksdft2effmass/reduction/atomistic-to-continuum.md) | Existing research owner plus proposed proof |
| Crossover and observable-error bounds | [Crossover proof](../../../proofs/ksdft2effmass/bounds/spatial-residual-and-crossover.md) and [observable-error proof](../../../proofs/ksdft2effmass/bounds/operator-to-observable-errors.md) | Proposed proof development |
| Excluded-space correction | [Feshbach proof unit](../../../proofs/ksdft2effmass/reduction/feshbach-reduction.md) | Proposed proof development |
| Computational stages | [Computational workflow index](../../../computational/ksdft2effmass.computational.00.md), [Stage 05](../../../computational/ksdft2Effmass.computational.05.md), [Stage 06](../../../computational/ksdft2Effmass.computational.06.md), [Stage 08](../../../computational/ksdft2Effmass.computational.08.md), and [Stage 09](../../../computational/ksdft2Effmass.computational.09.md) | Existing workflow owners; execution remains gate-controlled |
| Represented impurity-operator software | [`python/src/ksdft2effmass/operators/`](../../../../python/src/ksdft2effmass/operators/) | Existing implementation surface; manuscript-specific actions are proposed |
| Impurity fitting and crossover implementation | Proposed link: manuscript-specific action owners under the approved Python architecture | Authorized in-repository work; owner paths not yet fixed |
| Figures, tables, and retained result artifacts | Proposed links: versioned compact artifacts referenced from this manuscript | Authorized in-repository work; no calculated result yet |
| LaTeX realization | [`latex/`](latex/) | Reserved publication source surface |

## Abstract

We develop a mathematically controlled framework for extracting impurity operators from first-principles electronic-structure calculations and for connecting those operators to effective-mass continuum models. The construction is based on TB-anchored retained subspaces, gauge-covariant operator alignment, and explicit comparison maps between atomistic and continuum representations. We prove that aligned impurity operators transform covariantly under basis changes, establish conditions for a well-defined subspace identification map, derive a crossover-radius criterion under asymptotic locality, and state error bounds linking operator residuals to spectral and wavefunction observables. The resulting framework separates representation mismatch from physical impurity content and yields a validation protocol for comparing atomistic and continuum descriptions of doped semiconductors.

## 1. Introduction

Doped semiconductors are commonly modeled at multiple levels: atomistic Kohn–Sham calculations, reduced tight-binding or Wannier representations, and effective-mass continuum theories. Each level introduces its own coordinate choices, truncations, and gauge freedoms, so naive comparison of matrix elements across models can conflate physical differences with basis mismatch.

This paper develops a representation-controlled framework for comparing pristine and doped systems. The central idea is to anchor the retained atomistic subspaces to fixed TB labels, align the reduced Hamiltonians within a common identified coordinate space, and then compare the resulting impurity operator with an effective-mass continuum model. The analysis is organized so that each reduction step has an explicit mathematical domain, codomain, and error interpretation.

Our main contributions are:

- a gauge-covariant definition of aligned impurity extraction;
- a TB-anchored identification map between pristine and doped retained subspaces;
- a well-posed spatial residual and crossover-radius criterion;
- operator-to-observable error bounds;
- excluded-space correction estimates;
- a framework for fitting continuum corrections with identifiability diagnostics.

## 2. Proof dependencies

The result statements below remain a manuscript-level summary. Detailed arguments are maintained in:

- [state-space assumptions](../../../proofs/ksdft2effmass/foundations/state-space-assumptions.md);
- [Bloch-fiber correspondence](../../../proofs/ksdft2effmass/foundations/bloch-fiber-correspondence.md);
- [representation and reduction maps](../../../proofs/ksdft2effmass/foundations/representation-maps.md);
- [TB-anchored identification](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md); and
- [gauge equivariance](../../../proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md).

## 3. Gauge covariance and TB anchoring

The extracted section is maintained by the [TB-anchored identification](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md) and [gauge-equivariance](../../../proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md) proof units.

### Theorem 1. Gauge covariance of impurity extraction.
If the pristine and doped retained subspaces are transformed by a common unitary gauge \(\hat G\), then the aligned impurity operator transforms covariantly:

$$
\Delta\hat H_d^{(P)}\mapsto \hat G^\dagger \Delta\hat H_d^{(P)}\hat G.
$$

### Corollary 1.
Any unitarily invariant norm of \(\Delta\hat H_d^{(P)}\) is gauge invariant.

### Proposition 1. TB-anchored identification.
If \(\widetilde{\mathbf V}_b(\mathbf k)\) and \(\widetilde{\mathbf V}_d(\mathbf k)\) are orthonormal bases of equal dimension, then

$$
\hat U_d(\mathbf k)=\widetilde{\mathbf V}_d(\mathbf k)\widetilde{\mathbf V}_b^\dagger(\mathbf k)
$$

defines a unitary identification between the corresponding retained subspaces.

## 4. Impurity extraction and spatial residuals

Let \(\hat P_{>R}\) denote an exterior projector associated with radius \(R\). Define the atomistic-minus-continuum discrepancy

$$
\hat D_d=\Delta\hat H_d-\hat V_{\mathrm{cont},d}.
$$

The exterior tail error is

$$
\eta_d(R)=\left\|\hat P_{>R}\hat D_d\hat P_{>R}\right\|.
$$

### Lemma 1. Monotonicity.
If $R_2\ge R_1$, then  $\eta_d(R_2)\le \eta_d(R_1).$

### Assumption 1. Asymptotic locality.
$$
\lim_{R\to\infty}\eta_d(R)=0.
$$

### Theorem 2. Existence of crossover radius.
For any tolerance $\tau_H>0$, define

$$
r_{c,d}(\tau_H)=\inf\{R:\eta_d(R)\le \tau_H\}.
$$
Under asymptotic locality, $r_{c,d}(\tau_H)$ exists.

## 5. Error propagation to observables

Write $\hat H_{\mathrm{atom}}=\hat H_{\mathrm{red}}+\hat E$.

### Theorem 3. Spectral stability.
For self-adjoint operators,

\[
\operatorname{dist}\bigl(\sigma(\hat H_{\mathrm{atom}}),\sigma(\hat H_{\mathrm{red}})\bigr)\le \|\hat E\|.
\]

### Corollary 2. Binding-energy bound.
If \(E_{b,d}^{\mathrm{atom}}\) and \(E_{b,d}^{\mathrm{red}}\) are correctly identified isolated impurity levels, then

\[
|E_{b,d}^{\mathrm{atom}}-E_{b,d}^{\mathrm{red}}|\le \|\hat E\|.
\]

### Theorem 4. Eigenspace stability.
If \(\gamma_d\) is the spectral gap isolating the target impurity state, then a Davis–Kahan-type bound yields

\[
\sin\theta_d\lesssim \frac{\|\hat E\|}{\gamma_d}.
\]

### Corollary 3. Fidelity bound.
For normalized nondegenerate states,

\[
1-F_d\lesssim \left(\frac{\|\hat E\|}{\gamma_d}\right)^2.
\]

## 6. Excluded-space corrections

### Feshbach effective operator and relation to retained Hamiltonians

Let $\hat P+\hat Q=\hat I$ with $\hat P^2=\hat P$, $\hat Q^2=\hat Q$, and $\hat P\hat Q=\hat Q\hat P=0$. Then the exact Feshbach effective operator in the $\hat P$-space is
$$
\hat H_{\mathrm{eff}}(E)=\hat P\hat H\hat P+\hat P\hat H\hat Q\,(E-\hat Q\hat H\hat Q)^{-1}\,\hat Q\hat H\hat P.
$$

This expression is obtained by eliminating the $\hat Q$-component of the Schrödinger equation $(E-\hat H)|\Psi\rangle=0$ and yields an energy-dependent, non-Hermitian operator whose poles determine resonance positions and widths [^Feshbach1958][^Feshbach1962][^Rotter2009]. In the notation $\hat H_{PP}=\hat P\hat H\hat P$, $\hat H_{PQ}=\hat P\hat H\hat Q$, etc., one writes
$$
\hat H_{\mathrm{eff}}(E)=\hat H_{PP}+\hat H_{PQ}\,(E-\hat H_{QQ})^{-1}\,\hat H_{QP},
$$
which is the standard form used in nuclear, atomic, and mesoscopic physics to describe open quantum systems and resonance phenomena [^Rotter2009][^Mielnik2014][^HyodoNotes].

The first term, $\hat P\hat H\hat P$, coincides with the retained (compressed) Hamiltonian introduced earlier when $\hat P$ is identified with the projector onto the retained subspace. The second term encodes the dynamical feedback from the eliminated $\hat Q$-space and is responsible for level shifts, widths, and non-Hermiticity [^Feshbach1958][^Rotter2009]. In the limit where the coupling $\hat P\hat H\hat Q$ is neglected or the energy denominator is approximated by a constant, $\hat H_{\mathrm{eff}}(E)$ reduces to an energy-independent effective Hamiltonian in the $\hat P$-space, which is often used as a starting point for downfolding and model-Hamiltonian constructions [Kuneš (2011)](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md#references) and [Georges et al. (1996)](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md#references).

In the Bloch-fiber setting, one may define fiber-wise projectors $\hat P(\mathbf k)$ and $\hat Q(\mathbf k)=\hat I(\mathbf k)-\hat P(\mathbf k)$ and construct
$$
\hat H_{\mathrm{eff}}(\mathbf k;E)=\hat P(\mathbf k)\hat H(\mathbf k)\hat P(\mathbf k)
+\hat P(\mathbf k)\hat H(\mathbf k)\hat Q(\mathbf k)\,[E-\hat Q(\mathbf k)\hat H(\mathbf k)\hat Q(\mathbf k)]^{-1}\,\hat Q(\mathbf k)\hat H(\mathbf k)\hat P(\mathbf k),
$$
which provides an exact, energy-dependent effective band structure in the retained subspace. This formalism underlies rigorous treatments of impurity resonances, embedding methods, and self-energy corrections in periodic systems [^Feshbach1958][^Rotter2009] and [Kuneš (2011)](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md#references).

[^Feshbach1958]: H. Feshbach, "Unified theory of nuclear reactions," *Ann. Phys.* **5**, 357 (1958).

[^Feshbach1962]: H. Feshbach, "Unified theory of nuclear reactions. II," *Ann. Phys.* **19**, 287 (1962).

[^Rotter2009]: I. Rotter, "A non-Hermitian Hamilton operator and the physics of open quantum systems," *J. Phys. A: Math. Theor.* **42**, 153001 (2009).

[^Mielnik2014]: M. Mielnik et al., "Computing resonance widths using square integrable basis," *Acta Phys. Pol. B* **45**, 113 (2014).

[^HyodoNotes]: H. Hyodo, "Theory of Feshbach resonances," lecture notes, RCNP Osaka University (2020), https://www.rcnp.osaka-u.ac.jp/~hyodo/class/2020/Tokuron/Tokuron_Note_e3.pdf.

### Theorem 5. Excluded-space bound.
If \(\Delta_Q=\operatorname{dist}(E,\sigma(\hat Q\hat H\hat Q))\), then

$$
\left\|\hat P\hat H\hat Q(E-\hat Q\hat H\hat Q)^{-1}\hat Q\hat H\hat P\right\|
\le \frac{\|\hat P\hat H\hat Q\|^2}{\Delta_Q}.
$$

This gives a criterion for when single-band reduction is sufficient and when multivalley or valence-band mixing must be retained.

## 7. Atomistic-to-envelope consistency

Assume \(a/L\ll 1\), where \(a\) is the lattice spacing and \(L\) the envelope scale. Near a band extremum \(\mathbf k_0\),

$$
E_n(\mathbf k_0+\mathbf q)=E_n(\mathbf k_0)+\frac{\hbar^2}{2}\mathbf q^{\mathsf T}\mathbf m_n^{*-1}\mathbf q+O(|\mathbf q|^3).
$$

### Theorem 6. Effective-mass consistency.
Replacing the atomistic host operator by the quadratic effective-mass operator incurs an error controlled by higher-order terms in \(a/L\), with the leading residual entering at the order dictated by the first neglected band-expansion term.

For silicon, the proof must retain multivalley conduction structure, valence-band degeneracy, anisotropic masses, and spin–orbit coupling where relevant.

## 8. Continuum fitting and identifiability

Let $\hat V_{\mathrm{cont}}(\boldsymbol\theta)$ be a parameterized continuum correction. Define

$$
J_R(\boldsymbol\theta)=\left\|\hat P_{>R}\bigl[\Delta\hat H_d-\hat V_{\mathrm{cont}}(\boldsymbol\theta)\bigr]\hat P_{>R}\right\|.
$$

### Theorem 7. Existence of best-fit continuum parameters.
If $\Theta$ is compact and $J_R$ is continuous, then for $\boldsymbol{\theta}_R^* \in \Theta$,

$$
\boldsymbol\theta_R^*\in\arg\min_{\boldsymbol\theta\in\Theta}J_R(\boldsymbol\theta)
$$
exists.

Uniqueness is a separate identifiability question and should be assessed with sensitivity analysis, covariance estimates, and profile likelihoods.

## 9. Spectral and operator compatibility

Define spectral- and operator-admissible sets:

\[
\mathcal A_{\mathrm{spec}}^{(m)}=\{\boldsymbol\theta:\epsilon_{\mathrm{spec}}(\boldsymbol\theta)\le \tau_{\mathrm{spec}}\},
\qquad
\mathcal A_{\mathrm{op}}^{(m)}=\{\boldsymbol\theta:\epsilon_{\mathrm{op}}(\boldsymbol\theta)\le \tau_{\mathrm{op}}\}.
\]

### Theorem 8. Minimum separation.
If the admissible sets are compact, then the minimum separation between them is attained. If they are disjoint, the separation is strictly positive.

A certified incompatibility result requires analytic bounds, interval methods, branch-and-bound, exhaustive certified reduction, or valid convex relaxation.

## 10. Reduction-path commutativity

Let \(\mathcal R\) be a reduction map. Define

$$
\epsilon_{\mathrm{path}}
=
\left\|
\mathcal R(\hat H_d-\hat H_b)
-
\left[\mathcal R(\hat H_d)-\mathcal R(\hat H_b)\right]
\right\|.
$$

### Theorem 9. Exact commutativity conditions.
Sufficient conditions for

\[
\mathcal R(\hat H_d-\hat H_b)=\mathcal R(\hat H_d)-\mathcal R(\hat H_b)
\]

include a common retained subspace, a common linear reduction map, consistent gauges, consistent energy references, and identical basis ordering.

## 11. Conclusions

We have presented a representation-controlled framework for impurity extraction in doped semiconductors, based on TB-anchored retained spaces, gauge-covariant alignment, and explicit comparison maps between atomistic and continuum descriptions. The framework separates physical impurity content from basis mismatch, provides a route to crossover-radius estimates, and supplies operator-to-observable error bounds needed for validation. The agentic-workflow proof track remains intentionally separate.

---
