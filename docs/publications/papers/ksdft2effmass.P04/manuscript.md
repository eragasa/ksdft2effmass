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
| Mechanized finite-dimensional lemma layer | [Mechanized-proof architecture](../../../architecture/mechanized-proof-system.md), [PRF-05 status](../../../proofs/ksdft2effmass/status/proof.05-mechanized-lemmas.md), [theorem catalog](../../../../formal/theorem-catalog/PRF-05.md), and [Lean backend](../../../../formal/lean/README.md) | Nine contracts are frozen; `PRF-05.01` is Lean checked under the pinned bounded trial, while all other backend targets remain unencoded |
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

This working manuscript develops a mathematically controlled framework for extracting impurity operators from first-principles electronic-structure calculations and connecting those operators to effective-mass continuum models. The construction uses TB-anchored retained subspaces, dual pristine-space and doped-space representations of the aligned operator difference, gauge-covariant comparison maps, and explicit atomistic-to-continuum reductions. We formulate covariance and unitary-equivalence contracts, conditions for a well-defined subspace identification map, a crossover-radius criterion under asymptotic locality, and candidate bounds linking operator residuals to spectral and wavefunction observables. The finite-dimensional `PRF-05` identities are standard linear algebra; their prospective contribution is coordinated mechanization and composition within this operator-reduction framework. Only `PRF-05.01` is currently represented as checked by one pinned Lean backend. No other frozen contract or later scientific claim is represented as proved, cross-checked, numerically verified, or scientifically validated.

## 1. Introduction

Doped semiconductors are commonly modeled at multiple levels: atomistic Kohn–Sham calculations, reduced tight-binding or Wannier representations, and effective-mass continuum theories. Each level introduces its own coordinate choices, truncations, and gauge freedoms, so naive comparison of matrix elements across models can conflate physical differences with basis mismatch.

This paper develops a representation-controlled framework for comparing pristine and doped systems. The central idea is to anchor the retained atomistic subspaces to fixed TB labels, align the reduced Hamiltonians within a common identified coordinate space, and then compare the resulting impurity operator with an effective-mass continuum model. The analysis is organized so that each reduction step has an explicit mathematical domain, codomain, and error interpretation.

The intended contributions are:

- dual pristine-space and doped-space definitions of aligned impurity extraction, with separate covariance laws and a unitary-equivalence bridge;
- a TB-anchored identification map between pristine and doped retained subspaces;
- coordinated Lean, Isabelle, and Rocq mechanization of the standard finite-dimensional foundation, subject to separate toolchain authorization;
- a proposed spatial residual and crossover-radius criterion;
- proposed operator-to-observable and excluded-space bounds; and
- a framework for fitting continuum corrections with identifiability diagnostics.

## 2. Proof dependencies

The result statements below remain a manuscript-level summary. Detailed arguments are maintained in:

- [state-space assumptions](../../../proofs/ksdft2effmass/foundations/state-space-assumptions.md);
- [Bloch-fiber correspondence](../../../proofs/ksdft2effmass/foundations/bloch-fiber-correspondence.md);
- [representation and reduction maps](../../../proofs/ksdft2effmass/foundations/representation-maps.md);
- [TB-anchored identification](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md); and
- [gauge equivariance](../../../proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md);
- [the PRF-05 theorem catalog](../../../../formal/theorem-catalog/PRF-05.md); and
- [the multi-prover architecture](../../../architecture/mechanized-proof-system.md).

### 2.1 Mathematical novelty and mechanization boundary

The projector, compression, pullback, subtraction, and norm identities collected in `PRF-05` are standard consequences of finite-dimensional linear algebra. This manuscript does not claim them as new mathematical proofs. Wavevector-dependent unitary freedom and the dependence of Wannier localization on that freedom are established in Wannier theory.[^MarzariVanderbilt1997][^SouzaMarzariVanderbilt2001][^MarzariEtAl2012]

The potential contribution is instead the application-specific organization and prospective mechanization of those identities: one prover-neutral contract set, independent Lean–Isabelle–Rocq encodings, semantic conformance review, dual common-space treatment of aligned pristine–doped subtraction, and composition with later reduction and error arguments. No claim is made that this exact contract collection has priority over all prior formalization work; establishing that would require a dedicated prior-art review.

The defensible manuscript claim is:

> The individual identities are standard; their coordinated machine-checked formulation and composition into a gauge-equivariant operator-reduction framework may be new.

The current evidence establishes only a bounded first step toward that mechanization claim: `PRF-05.01` is checked in Lean 4 under the pinned trial toolchain, while eight Lean targets and every Isabelle and Rocq target remain unencoded. No cross-backend semantic conformance result exists. Potentially new research theorems would instead concern identification uniqueness or equivariance, gauge-invariant distances between operator equivalence classes, gauge–truncation commutation conditions, quantitative truncation bounds, operator-to-observable bounds, or atomistic-to-continuum crossover conditions.

## 3. Gauge covariance and TB anchoring

This section is maintained by the [aligned-impurity](../../../proofs/ksdft2effmass/operator-alignment/aligned-impurity-operator.md), [TB-anchored-identification](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md), and [gauge-equivariance](../../../proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md) proof units. The exact draft mechanization targets are `PRF-05.03` and `PRF-05.04` in the [theorem catalog](../../../../formal/theorem-catalog/PRF-05.md).

Let

$$
U:
\mathcal H_b^{(P)}
\to
\mathcal H_d^{(P)}
$$

identify the pristine and doped retained spaces. Two aligned differences are available.

The pristine-space pullback is

$$
\Delta H_{d\to b}
=
U^\dagger H_dU-H_b
:
\mathcal H_b^{(P)}
\to
\mathcal H_b^{(P)},
$$

and the doped-space pushforward is

$$
\Delta H_{b\to d}
=
H_d-UH_bU^\dagger
:
\mathcal H_d^{(P)}
\to
\mathcal H_d^{(P)}.
$$

### Proposed theorem 1a. Covariance of both common-space representations

Under independent frame transformations

$$
H_b'=G_b^\dagger H_bG_b,
\qquad
H_d'=G_d^\dagger H_dG_d,
\qquad
U'=G_d^\dagger UG_b,
$$

with unitary $G_b$ and $G_d$, the two differences satisfy

$$
\Delta H_{d\to b}'
=
G_b^\dagger\Delta H_{d\to b}G_b,
$$

and

$$
\Delta H_{b\to d}'
=
G_d^\dagger\Delta H_{b\to d}G_d.
$$

These covariance identities require conformable dimensions but do not require $U$ itself to be unitary.

### Proposed theorem 1b. Unitary equivalence of the aligned differences

If $U$ is a unitary identification,

$$
U^\dagger U=I_b,
\qquad
UU^\dagger=I_d,
$$

then

$$
\Delta H_{b\to d}
=
U\Delta H_{d\to b}U^\dagger,
\qquad
\Delta H_{d\to b}
=
U^\dagger\Delta H_{b\to d}U.
$$

The two matrices then represent the same aligned operator difference in unitarily identified retained spaces. They have the same spectrum and the same unitarily invariant norms, including

$$
\left\lVert\Delta H_{b\to d}\right\rVert_F
=
\left\lVert\Delta H_{d\to b}\right\rVert_F,
$$

and

$$
\left\lVert\Delta H_{b\to d}\right\rVert_2
=
\left\lVert\Delta H_{d\to b}\right\rVert_2.
$$

Without unitarity of $U$, the separate covariance identities remain valid, but the two differences are not thereby established as representations of the same physical operator. State-space identification also does not align scalar energy references; energy alignment remains an independent prerequisite.

### Proposed proposition 1. TB-anchored identification

If $\widetilde{\mathbf V}_b(\mathbf k)$ and $\widetilde{\mathbf V}_d(\mathbf k)$ are orthonormal bases of equal dimension, then

$$
\hat U_d(\mathbf k)
=
\widetilde{\mathbf V}_d(\mathbf k)
\widetilde{\mathbf V}_b^\dagger(\mathbf k)
$$

defines a unitary identification between the corresponding retained subspaces. Establishing its physical adequacy, smoothness, symmetry compatibility, or uniqueness requires additional assumptions and is not supplied by the elementary `PRF-05` contracts.

## 4. Impurity extraction and spatial residuals

For the remainder of this working manuscript, $\Delta\hat H_d$ abbreviates the doped-space representation $\Delta H_{b\to d}$. When $U$ is unitary, every unitarily invariant statement may equivalently be expressed using the pristine-space representation $\Delta H_{d\to b}$. This abbreviation does not remove the need to record the chosen common space in calculations and retained artifacts.

Let $\hat P_{>R}$ denote an exterior projector associated with radius $R$. Define the atomistic-minus-continuum discrepancy

$$
\hat D_d=\Delta\hat H_d-\hat V_{\mathrm{cont},d}.
$$

The exterior tail error is

$$
\eta_d(R)=\left\|\hat P_{>R}\hat D_d\hat P_{>R}\right\|.
$$

### Proposed lemma 1. Monotonicity.
If $R_2\ge R_1$, then  $\eta_d(R_2)\le \eta_d(R_1).$

### Assumption 1. Asymptotic locality.
$$
\lim_{R\to\infty}\eta_d(R)=0.
$$

### Proposed theorem 2. Existence of crossover radius.
For any tolerance $\tau_H>0$, define

$$
r_{c,d}(\tau_H)=\inf\{R:\eta_d(R)\le \tau_H\}.
$$
Under asymptotic locality, $r_{c,d}(\tau_H)$ exists.

## 5. Error propagation to observables

Write $\hat H_{\mathrm{atom}}=\hat H_{\mathrm{red}}+\hat E$.

### Proposed theorem 3. Spectral stability.
For self-adjoint operators,

$$
\operatorname{dist}\bigl(\sigma(\hat H_{\mathrm{atom}}),\sigma(\hat H_{\mathrm{red}})\bigr)\le \|\hat E\|.
$$

### Proposed corollary 2. Binding-energy bound.
If $E_{b,d}^{\mathrm{atom}}$ and $E_{b,d}^{\mathrm{red}}$ are correctly identified isolated impurity levels, then

$$
|E_{b,d}^{\mathrm{atom}}-E_{b,d}^{\mathrm{red}}|\le \|\hat E\|.
$$

### Proposed theorem 4. Eigenspace stability.
If $\gamma_d$ is the spectral gap isolating the target impurity state, then a Davis–Kahan-type bound yields

$$
\sin\theta_d\lesssim \frac{\|\hat E\|}{\gamma_d}.
$$

### Proposed corollary 3. Fidelity bound.
For normalized nondegenerate states,

$$
1-F_d\lesssim \left(\frac{\|\hat E\|}{\gamma_d}\right)^2.
$$

## 6. Excluded-space corrections

### Feshbach effective operator and relation to retained Hamiltonians

Let $\hat P+\hat Q=\hat I$ with $\hat P^2=\hat P$, $\hat Q^2=\hat Q$, and $\hat P\hat Q=\hat Q\hat P=0$. Then the exact Feshbach effective operator in the $\hat P$-space is
$$
\hat H_{\mathrm{eff}}(E)=\hat P\hat H\hat P+\hat P\hat H\hat Q\,(E-\hat Q\hat H\hat Q)^{-1}\,\hat Q\hat H\hat P.
$$

This expression is obtained by eliminating the $\hat Q$-component of the Schrödinger equation $(E-\hat H)|\Psi\rangle=0$. It is energy dependent. For a self-adjoint $\hat H$ and real $E$ in the resolvent set of $\hat Q\hat H\hat Q$, the displayed effective operator is self-adjoint; non-Hermiticity arises in open-system or analytically continued resonance formulations, where poles may determine resonance positions and widths.[^Feshbach1958][^Feshbach1962][^Rotter2009] In the notation $\hat H_{PP}=\hat P\hat H\hat P$, $\hat H_{PQ}=\hat P\hat H\hat Q$, etc., one writes
$$
\hat H_{\mathrm{eff}}(E)=\hat H_{PP}+\hat H_{PQ}\,(E-\hat H_{QQ})^{-1}\,\hat H_{QP},
$$
which is the standard form used in nuclear, atomic, and mesoscopic physics to describe open quantum systems and resonance phenomena [^Rotter2009][^Mielnik2014][^HyodoNotes].

The first term, $\hat P\hat H\hat P$, coincides with the retained compressed Hamiltonian when $\hat P$ projects onto the retained subspace. The second term encodes dynamical feedback from the eliminated $\hat Q$-space and can produce level shifts; widths and non-Hermiticity require the applicable open-system or resonance setting.[^Feshbach1958][^Rotter2009] In the limit where the coupling $\hat P\hat H\hat Q$ is neglected or the energy denominator is approximated by a constant, $\hat H_{\mathrm{eff}}(E)$ reduces to an energy-independent effective Hamiltonian in the $\hat P$-space, which is often used as a starting point for downfolding and model-Hamiltonian constructions [Kuneš (2011)](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md#references) and [Georges et al. (1996)](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md#references).

In the Bloch-fiber setting, one may define fiber-wise projectors $\hat P(\mathbf k)$ and $\hat Q(\mathbf k)=\hat I(\mathbf k)-\hat P(\mathbf k)$ and construct
$$
\hat H_{\mathrm{eff}}(\mathbf k;E)=\hat P(\mathbf k)\hat H(\mathbf k)\hat P(\mathbf k)
+\hat P(\mathbf k)\hat H(\mathbf k)\hat Q(\mathbf k)\,[E-\hat Q(\mathbf k)\hat H(\mathbf k)\hat Q(\mathbf k)]^{-1}\,\hat Q(\mathbf k)\hat H(\mathbf k)\hat P(\mathbf k),
$$
which provides an exact, energy-dependent effective band structure in the retained subspace. This formalism underlies rigorous treatments of impurity resonances, embedding methods, and self-energy corrections in periodic systems [^Feshbach1958][^Rotter2009] and [Kuneš (2011)](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md#references).

[^MarzariVanderbilt1997]: N. Marzari and D. Vanderbilt, “Maximally localized generalized Wannier functions for composite energy bands,” *Physical Review B* **56**, 12847–12865 (1997), [doi:10.1103/PhysRevB.56.12847](https://doi.org/10.1103/PhysRevB.56.12847).

[^SouzaMarzariVanderbilt2001]: I. Souza, N. Marzari, and D. Vanderbilt, “Maximally localized Wannier functions for entangled energy bands,” *Physical Review B* **65**, 035109 (2001), [doi:10.1103/PhysRevB.65.035109](https://doi.org/10.1103/PhysRevB.65.035109).

[^MarzariEtAl2012]: N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012), [doi:10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419).

[^Feshbach1958]: H. Feshbach, "Unified theory of nuclear reactions," *Ann. Phys.* **5**, 357 (1958).

[^Feshbach1962]: H. Feshbach, "Unified theory of nuclear reactions. II," *Ann. Phys.* **19**, 287 (1962).

[^Rotter2009]: I. Rotter, "A non-Hermitian Hamilton operator and the physics of open quantum systems," *J. Phys. A: Math. Theor.* **42**, 153001 (2009).

[^Mielnik2014]: M. Mielnik et al., "Computing resonance widths using square integrable basis," *Acta Phys. Pol. B* **45**, 113 (2014).

[^HyodoNotes]: H. Hyodo, "Theory of Feshbach resonances," lecture notes, RCNP Osaka University (2020), https://www.rcnp.osaka-u.ac.jp/~hyodo/class/2020/Tokuron/Tokuron_Note_e3.pdf.

### Proposed theorem 5. Excluded-space bound.
If $\Delta_Q=\operatorname{dist}(E,\sigma(\hat Q\hat H\hat Q))$, then

$$
\left\|\hat P\hat H\hat Q(E-\hat Q\hat H\hat Q)^{-1}\hat Q\hat H\hat P\right\|
\le \frac{\|\hat P\hat H\hat Q\|^2}{\Delta_Q}.
$$

Together with a declared tolerance and spectral regime, this bound can support a criterion for when a selected retained space is adequate or when additional valley or valence-band components must be considered.

## 7. Atomistic-to-envelope consistency

Assume $a/L\ll 1$, where $a$ is the lattice spacing and $L$ the envelope scale. Near a band extremum $\mathbf k_0$,

$$
E_n(\mathbf k_0+\mathbf q)=E_n(\mathbf k_0)+\frac{\hbar^2}{2}\mathbf q^{\mathsf T}\mathbf m_n^{*-1}\mathbf q+O(|\mathbf q|^3).
$$

### Proposed theorem 6. Effective-mass consistency.
Replacing the atomistic host operator by the quadratic effective-mass operator incurs an error controlled by higher-order terms in $a/L$, with the leading residual entering at the order dictated by the first neglected band-expansion term.

For silicon, the proof must retain multivalley conduction structure, valence-band degeneracy, anisotropic masses, and spin–orbit coupling where relevant.

## 8. Continuum fitting and identifiability

Let $\hat V_{\mathrm{cont}}(\boldsymbol\theta)$ be a parameterized continuum correction. Define

$$
J_R(\boldsymbol\theta)=\left\|\hat P_{>R}\bigl[\Delta\hat H_d-\hat V_{\mathrm{cont}}(\boldsymbol\theta)\bigr]\hat P_{>R}\right\|.
$$

### Proposed theorem 7. Existence of best-fit continuum parameters.
If $\Theta$ is compact and $J_R$ is continuous, then for $\boldsymbol{\theta}_R^* \in \Theta$,

$$
\boldsymbol\theta_R^*\in\arg\min_{\boldsymbol\theta\in\Theta}J_R(\boldsymbol\theta)
$$
exists.

Uniqueness is a separate identifiability question and should be assessed with sensitivity analysis, covariance estimates, and profile likelihoods.

## 9. Spectral and operator compatibility

Define spectral- and operator-admissible sets:

$$
\mathcal A_{\mathrm{spec}}^{(m)}=\{\boldsymbol\theta:\epsilon_{\mathrm{spec}}(\boldsymbol\theta)\le \tau_{\mathrm{spec}}\},
\qquad
\mathcal A_{\mathrm{op}}^{(m)}=\{\boldsymbol\theta:\epsilon_{\mathrm{op}}(\boldsymbol\theta)\le \tau_{\mathrm{op}}\}.
$$

### Proposed theorem 8. Minimum separation.
If the admissible sets are compact, then the minimum separation between them is attained. If they are disjoint, the separation is strictly positive.

A certified incompatibility result requires analytic bounds, interval methods, branch-and-bound, exhaustive certified reduction, or valid convex relaxation.

## 10. Reduction-path commutativity

Unaligned pristine and doped operators must not be subtracted. In the doped common space, define

$$
\overline H_b:=UH_bU^\dagger,
\qquad
\Delta H_{b\to d}:=H_d-\overline H_b.
$$

For a reduction map $\mathcal R$ whose domain contains both aligned operands, define

$$
\epsilon_{\mathrm{path}}
=
\left\lVert
\mathcal R(\Delta H_{b\to d})
-
\left[\mathcal R(H_d)-\mathcal R(\overline H_b)\right]
\right\rVert.
$$

The pristine-space formulation is obtained by replacing both operands with their pullback representations.

### Proposed theorem 9. Exact commutativity conditions.

A sufficient algebraic condition for

$$
\mathcal R(\Delta H_{b\to d})
=
\mathcal R(H_d)-\mathcal R(\overline H_b)
$$

is that the same linear map $\mathcal R$ act on both operands in the same identified coordinate space. Applying this identity to a physical reduction additionally requires consistent gauges, energy references, dimensions, basis ordering, and reduction settings. Nonlinear fitting, independently selected model classes, truncation after a gauge-dependent representation change, or separate alignment choices need not commute with impurity extraction.

## 11. Conclusions

This working manuscript organizes a representation-controlled framework for impurity extraction in doped semiconductors using TB-anchored retained spaces, dual common-space aligned differences, gauge-covariant comparison maps, and explicit atomistic-to-continuum reductions. The elementary `PRF-05` identities are standard mathematics and are positioned as a prospective machine-checked foundation rather than novel proofs. The later crossover, observable-error, excluded-space, compatibility, and continuum claims remain proposed work requiring their declared analytical, numerical, and scientific evidence. Only the bounded Lean check of `PRF-05.01` is reported here; no cross-backend result, calculated crossover result, or scientific validation is reported. The agentic-workflow proof track remains intentionally separate.

---
