# PRF-05 Mechanized Operator Lemma Contracts

[Catalog conventions](README.md) · [Proof package](../../docs/proofs/ksdft2effmass/status/proof.05-mechanized-lemmas.md) · [Architecture](../../docs/architecture/mechanized-proof-system.md)

## Contract registry

| Identity     | Contract                                                             | Contract status | Lean        | Isabelle    | Rocq        |
| ------------ | -------------------------------------------------------------------- | --------------- | ----------- | ----------- | ----------- |
| `PRF-05.01`  | Projector invariance under unitary frame rotation                    | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.02`  | Covariance of a compressed operator representation                   | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.03`  | Covariance of identification pullback                                | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.04`  | Covariance and unitary equivalence of aligned subtraction            | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.05a` | Frobenius-norm invariance under unitary conjugation                  | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.05b` | Induced Euclidean operator-norm invariance under unitary conjugation | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.06`  | Gauge invariance of an equivariant path residual                     | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.07`  | Two-point counterexample to gauge–truncation commutation             | `frozen`        | `unencoded` | `unencoded` | `unencoded` |
| `PRF-05.08`  | Shell-Frobenius invariance under constant local rotations            | `frozen`        | `unencoded` | `unencoded` | `unencoded` |

All nine contracts in this file are frozen as the current common backend targets. None is encoded, checked, cross-checked, numerically verified, or scientifically validated.

**Human review disposition:** The package received `CONDITIONAL_PASS`; the requested revisions were applied, and subsequent explicit human confirmation authorized freezing the revised contracts. `PRF-05.04` retains both common-space orientations and their unitary equivalence, the former combined `PRF-05.05` is split into `PRF-05.05a` and `PRF-05.05b`, `PRF-05.06` names both norm dependencies, and `PRF-05.07` is explicitly titled as a counterexample. Freezing fixes the current theorem targets but does not authorize prover implementation or establish any proof.

## PRF-05.01: Projector invariance under unitary frame rotation

**Identity:** `PRF-05.01`

**Status:** `frozen`

**Purpose:** Establish that changing the orthonormal coordinate frame inside one retained subspace does not change the ambient-space orthogonal projector onto that subspace.

**Authority references:**

- [Projection and Wannier research](../../docs/research/ksdft2Effmass.01.md)
- [State-space assumptions](../../docs/proofs/ksdft2effmass/foundations/state-space-assumptions.md)
- [Gauge equivariance](../../docs/proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md)
- [Representation maps](../../docs/proofs/ksdft2effmass/foundations/representation-maps.md)

**Mathematical setting:** Let $D,M\in\mathbb N$ satisfy $1\le M\le D$. Work over the scalar field $\mathbb C$. Let

$$
V\in\mathbb C^{D\times M},
\qquad
G\in\mathbb C^{M\times M}.
$$

The conjugate transpose is denoted by $\dagger$ and matrix equality is exact equality over $\mathbb C$.

**Definitions:** Define

$$
P:=VV^\dagger,
\qquad
V':=VG,
\qquad
P':=V'V'^\dagger.
$$

**Assumptions:**

1. $V^\dagger V=I_M$. This assumption is required to interpret $VV^\dagger$ as the orthogonal projector onto the retained subspace, although the bare equality $P'=P$ uses only the unitarity of $G$.
2. $G$ is unitary:

   $$
   G^\dagger G=I_M,
   \qquad
   GG^\dagger=I_M.
   $$

**Conclusion:**

$$
P'=P.
$$

Equivalently,

$$
(VG)(VG)^\dagger=VV^\dagger.
$$

**Equivalent formulation:** A backend may represent $V$ as an isometric linear map from an $M$-dimensional complex inner-product space into a $D$-dimensional complex inner-product space and $G$ as a unitary endomorphism of the source, provided the exported conclusion is equality of the induced ambient orthogonal projectors.

**Nonclaims:**

- This theorem does not establish existence, smoothness, periodicity, or symmetry compatibility of a wavevector-dependent frame.
- It does not identify pristine and doped retained spaces.
- It does not show that $V$ or $G$ corresponds to a physically admissible localized gauge.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `projector_invariant_under_unitary_frame_rotation` |
| Isabelle | `projector_invariant_under_unitary_frame_rotation` |
| Rocq | `projector_invariant_under_unitary_frame_rotation` |

**Conformance questions:**

- Does the backend theorem use rectangular matrices or abstract finite-dimensional linear maps?
- Is unitarity represented by one equation with a derived inverse property or by both displayed equations?
- Is the resulting projector the ambient operator $VV^\dagger$, rather than the retained-coordinate identity $V^\dagger V$?

## PRF-05.02: Covariance of a compressed operator representation

**Identity:** `PRF-05.02`

**Status:** `frozen`

**Purpose:** Establish the coordinate transformation law for the matrix representing one ambient operator after compression to a fixed retained subspace.

**Authority references:**

- [Bulk reduction research](../../docs/research/ksdft2Effmass.05.md)
- [Representation maps](../../docs/proofs/ksdft2effmass/foundations/representation-maps.md)
- [Gauge equivariance](../../docs/proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md)

**Mathematical setting:** Let $D,M\in\mathbb N$ satisfy $1\le M\le D$. Work over $\mathbb C$. Let

$$
A\in\mathbb C^{D\times D},
\qquad
V\in\mathbb C^{D\times M},
\qquad
G\in\mathbb C^{M\times M}.
$$

No Hermiticity assumption on $A$ is required for the covariance identity.

**Definitions:** Define the original and rotated retained frames and represented operators by

$$
V':=VG,
$$

$$
H:=V^\dagger A V,
\qquad
H':=V'^\dagger A V'.
$$

**Assumptions:**

1. $V^\dagger V=I_M$.
2. $G$ is unitary:

   $$
   G^\dagger G=I_M,
   \qquad
   GG^\dagger=I_M.
   $$

**Conclusion:**

$$
H'=G^\dagger H G.
$$

Equivalently,

$$
(VG)^\dagger A(VG)
=
G^\dagger(V^\dagger A V)G.
$$

**Equivalent formulation:** A backend may use finite-dimensional inner-product spaces and adjointable linear maps instead of matrices, provided the source and target spaces and the represented endomorphisms are explicit.

**Nonclaims:**

- This theorem does not assert that $A$ preserves the retained subspace.
- It does not establish Hermiticity, spectral equivalence to the full ambient operator, or physical admissibility of the frame.
- It does not address a change of retained projector; $V$ and $V'$ span the same retained space by construction.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `compressed_operator_covariant_under_frame_rotation` |
| Isabelle | `compressed_operator_covariant_under_frame_rotation` |
| Rocq | `compressed_operator_covariant_under_frame_rotation` |

**Conformance questions:**

- Is $A$ an arbitrary endomorphism or unnecessarily restricted to a Hermitian matrix?
- Is $H'$ defined from the rotated frame rather than postulated to equal a conjugation?
- Does the theorem distinguish the ambient dimension $D$ from the retained dimension $M$?

## PRF-05.03: Covariance of identification pullback

**Identity:** `PRF-05.03`

**Status:** `frozen`

**Purpose:** Establish that pulling a doped represented operator into pristine coordinates transforms covariantly under independent changes of pristine and doped retained-space frames.

**Authority references:**

- [Pristine–doped alignment research](../../docs/research/ksdft2Effmass.04.md)
- [TB-anchored identification](../../docs/proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md)
- [Aligned impurity operator](../../docs/proofs/ksdft2effmass/operator-alignment/aligned-impurity-operator.md)
- [Gauge equivariance](../../docs/proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md)

**Mathematical setting:** Let $M_b,M_d\in\mathbb N$ be positive dimensions. Work over $\mathbb C$. Let

$$
H_d\in\mathbb C^{M_d\times M_d},
\qquad
U\in\mathbb C^{M_d\times M_b},
$$

and let

$$
G_b\in\mathbb C^{M_b\times M_b},
\qquad
G_d\in\mathbb C^{M_d\times M_d}
$$

be unitary coordinate transformations. The algebraic covariance identity does not require $U$ to be unitary or $M_b=M_d$.

**Definitions:** Define the pullback of the doped operator to pristine coordinates by

$$
A_U(H_d):=U^\dagger H_dU.
$$

Under independent coordinate changes, define

$$
H_d':=G_d^\dagger H_dG_d,
\qquad
U':=G_d^\dagger U G_b.
$$

**Assumptions:**

1. $G_b$ is unitary:

   $$
   G_b^\dagger G_b=I_{M_b},
   \qquad
   G_bG_b^\dagger=I_{M_b}.
   $$

2. $G_d$ is unitary:

   $$
   G_d^\dagger G_d=I_{M_d},
   \qquad
   G_dG_d^\dagger=I_{M_d}.
   $$

**Conclusion:**

$$
A_{U'}(H_d')
=
G_b^\dagger A_U(H_d)G_b.
$$

Expanded,

$$
U'^\dagger H_d'U'
=
G_b^\dagger(U^\dagger H_dU)G_b.
$$

**Equivalent formulation:** A backend may encode $U$ as a linear map between distinct finite-dimensional complex inner-product spaces. The transformed map must have the source and target gauge orientation shown above.

**Nonclaims:**

- This theorem does not prove that a physical identification $U$ exists.
- It does not prove that $U$ is unitary, well conditioned, smooth, periodic, or symmetry compatible.
- It does not align scalar energy references.
- It does not yet prove covariance or equivalence of aligned pristine–doped differences; those are subclaims of `PRF-05.04`.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `identification_pullback_covariant` |
| Isabelle | `identification_pullback_covariant` |
| Rocq | `identification_pullback_covariant` |

**Conformance questions:**

- Are pristine and doped coordinate spaces represented as distinct types or only by dimensions?
- Does the transformation of $U$ use $G_d^\dagger U G_b$ with the correct source and target orientation?
- Is unitarity of $U$ excluded from the assumptions?
- Is the output conjugated by the pristine gauge $G_b$?

## PRF-05.04: Covariance and unitary equivalence of aligned subtraction

**Identity:** `PRF-05.04`

**Status:** `frozen`

**Purpose:** Retain both common-space representations of the aligned pristine–doped matrix difference, establish their separate covariance laws, and establish their equivalence when $U$ is a unitary identification.

**Authority references:**

- [Pristine–doped alignment research](../../docs/research/ksdft2Effmass.04.md)
- [Identification-pullback contract](#prf-0503-covariance-of-identification-pullback)
- [Aligned impurity operator](../../docs/proofs/ksdft2effmass/operator-alignment/aligned-impurity-operator.md)
- [Gauge equivariance](../../docs/proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md)

**Mathematical setting:** Let $M_b,M_d\in\mathbb N$ be positive. Work over $\mathbb C$. Let

$$
H_b\in\mathbb C^{M_b\times M_b},
\qquad
H_d\in\mathbb C^{M_d\times M_d},
\qquad
U\in\mathbb C^{M_d\times M_b}.
$$

Let

$$
G_b\in\mathbb C^{M_b\times M_b},
\qquad
G_d\in\mathbb C^{M_d\times M_d}
$$

be unitary coordinate transformations.

**Definitions:** Define the pristine-space pullback and doped-space pushforward differences by

$$
\Delta H_{d\to b}:=U^\dagger H_dU-H_b
\in\mathbb C^{M_b\times M_b},
$$

and

$$
\Delta H_{b\to d}:=H_d-UH_bU^\dagger
\in\mathbb C^{M_d\times M_d}.
$$

Under independent frame transformations, define

$$
H_b':=G_b^\dagger H_bG_b,
\qquad
H_d':=G_d^\dagger H_dG_d,
\qquad
U':=G_d^\dagger UG_b,
$$

and construct $\Delta H_{d\to b}'$ and $\Delta H_{b\to d}'$ from the primed inputs by the same definitions.

**Assumptions for covariance:**

1. $G_b$ and $G_d$ are unitary.
2. All displayed matrix dimensions are conformable.
3. Each subtraction occurs only after both operands have been represented in its declared common coordinate space.

No unitarity assumption on $U$ is required for the covariance subclaims.

**Conclusion — subclaim 1, pristine-space covariance:**

$$
\Delta H_{d\to b}'
=
G_b^\dagger\Delta H_{d\to b}G_b.
$$

**Conclusion — subclaim 2, doped-space covariance:**

$$
\Delta H_{b\to d}'
=
G_d^\dagger\Delta H_{b\to d}G_d.
$$

**Additional assumption for subclaim 3:** The identification is unitary:

$$
U^\dagger U=I_{M_b},
\qquad
UU^\dagger=I_{M_d}.
$$

**Conclusion — subclaim 3, unitary equivalence:**

$$
\Delta H_{b\to d}
=
U\Delta H_{d\to b}U^\dagger,
$$

and

$$
\Delta H_{d\to b}
=
U^\dagger\Delta H_{b\to d}U.
$$

Consequently, the two representations have the same spectrum and the same Frobenius and induced Euclidean operator norms:

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

The norm consequences use `PRF-05.05a` and `PRF-05.05b`, respectively.

**Equivalent formulation:** A backend may use linear maps between distinct finite-dimensional inner-product spaces. It must preserve the declared domains, covariance groups, and the additional unitarity assumption for the equivalence subclaim.

**Nonclaims:**

- The covariance subclaims do not establish existence, unitarity, or physical adequacy of $U$.
- Without unitarity of $U$, the two differences are not claimed to represent the same physical operator.
- This theorem does not align the scalar energy references of $H_b$ and $H_d$.
- The physical term “impurity operator” applies only after the owning state-space, identification, and energy-alignment prerequisites are satisfied.
- It does not prove that either aligned difference is localized, small, or physically complete.

**Backend bindings:**

| Backend | Intended exported theorem names |
|---|---|
| Lean | `aligned_subtraction_pullback_covariant`, `aligned_subtraction_pushforward_covariant`, `aligned_subtraction_unitarily_equivalent` |
| Isabelle | `aligned_subtraction_pullback_covariant`, `aligned_subtraction_pushforward_covariant`, `aligned_subtraction_unitarily_equivalent` |
| Rocq | `aligned_subtraction_pullback_covariant`, `aligned_subtraction_pushforward_covariant`, `aligned_subtraction_unitarily_equivalent` |

**Conformance questions:**

- Are the pristine-space and doped-space differences both retained with explicit domains?
- Do their covariance actions use $G_b$ and $G_d$, respectively?
- Is unitarity of $U$ absent from the first two subclaims and present in the third?
- Are energy-reference alignment and state-space identification kept as separate prerequisites?
- Are all three subclaims independently checkable?

## PRF-05.05a: Frobenius-norm invariance under unitary conjugation

**Identity:** `PRF-05.05a`

**Status:** `frozen`

**Purpose:** Establish unitary-conjugation invariance of the finite-matrix Frobenius norm.

**Authority references:**

- [Bulk reduction research](../../docs/research/ksdft2Effmass.05.md)
- [Operator-error research](../../docs/research/ksdft2Effmass.08.md)
- [Gauge equivariance](../../docs/proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md)

**Mathematical setting:** Let $M\in\mathbb N$ be positive. Work over $\mathbb C$. Let $A,G\in\mathbb C^{M\times M}$.

**Definitions:** Define

$$
\lVert A\rVert_F
:=
\left(
\sum_{i=1}^{M}\sum_{j=1}^{M}|A_{ij}|^2
\right)^{1/2},
\qquad
A':=G^\dagger AG.
$$

**Assumptions:** The matrix $G$ is unitary:

$$
G^\dagger G=I_M,
\qquad
GG^\dagger=I_M.
$$

**Conclusion:**

$$
\lVert A'\rVert_F=\lVert A\rVert_F.
$$

**Equivalent formulation:** A backend may use a library Frobenius norm if cross-backend review confirms that its normalization equals the displayed entrywise definition.

**Nonclaims:**

- This contract does not assert invariance of entrywise, blockwise, or spatially truncated quantities.
- It does not assert invariance under nonunitary similarity or congruence transformations.
- It does not cover infinite-dimensional norms.
- It does not claim that this norm is the scientifically appropriate residual for every comparison.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `frobenius_norm_unitary_conjugation` |
| Isabelle | `frobenius_norm_unitary_conjugation` |
| Rocq | `frobenius_norm_unitary_conjugation` |

**Conformance questions:**

- Does each backend use the same normalization of the Frobenius norm?
- Is the result proved for the displayed finite complex matrix space?
- Is the zero-dimensional edge case excluded consistently by $M>0$?

## PRF-05.05b: Induced Euclidean operator-norm invariance under unitary conjugation

**Identity:** `PRF-05.05b`

**Status:** `frozen`

**Purpose:** Establish unitary-conjugation invariance of the finite-dimensional operator norm induced by the Euclidean vector norm.

**Authority references:**

- [Operator-error research](../../docs/research/ksdft2Effmass.08.md)
- [Operator-to-observable bounds](../../docs/proofs/ksdft2effmass/bounds/operator-to-observable-errors.md)
- [Gauge equivariance](../../docs/proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md)

**Mathematical setting:** Let $M\in\mathbb N$ be positive. Work over $\mathbb C$. Let $A,G\in\mathbb C^{M\times M}$.

**Definitions:** Define

$$
\lVert A\rVert_2
:=
\sup_{x\in\mathbb C^M,\,x\ne0}
\frac{\lVert Ax\rVert_{\ell^2}}{\lVert x\rVert_{\ell^2}},
\qquad
A':=G^\dagger AG.
$$

**Assumptions:** The matrix $G$ is unitary:

$$
G^\dagger G=I_M,
\qquad
GG^\dagger=I_M.
$$

**Conclusion:**

$$
\lVert A'\rVert_2=\lVert A\rVert_2.
$$

**Equivalent formulation:** A backend may use the norm of an endomorphism of a finite-dimensional complex Hilbert space if cross-backend review confirms equality with the displayed induced matrix norm.

**Nonclaims:**

- This contract does not assert invariance under nonunitary similarity or congruence transformations.
- It does not cover infinite-dimensional operator norms.
- It does not claim that this norm is the scientifically appropriate residual for every comparison.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `operator_norm_unitary_conjugation` |
| Isabelle | `operator_norm_unitary_conjugation` |
| Rocq | `operator_norm_unitary_conjugation` |

**Conformance questions:**

- Is the norm induced by the Euclidean norm over $\mathbb C^M$?
- Is the result proved for the displayed finite complex matrix space?
- Is the zero-dimensional edge case excluded consistently by $M>0$?

## PRF-05.06: Gauge invariance of an equivariant path residual

**Identity:** `PRF-05.06`

**Status:** `frozen`

**Purpose:** Establish that the norm of the difference between two outputs with the same gauge-covariance law is independent of the common coordinate frame.

**Authority references:**

- [Compositional reduction research](../../docs/research/ksdft2Effmass.10.md)
- [Frobenius-norm contract](#prf-0505a-frobenius-norm-invariance-under-unitary-conjugation)
- [Operator-norm contract](#prf-0505b-induced-euclidean-operator-norm-invariance-under-unitary-conjugation)
- [Reduction-path commutativity](../../docs/proofs/ksdft2effmass/reduction/reduction-path-commutativity.md)

**Mathematical setting:** Let $M\in\mathbb N$ be positive, let $X$ be an input space carrying an action $\sigma$ of the unitary group $U(M)$, and let

$$
\mathcal R_1,\mathcal R_2:X\to\mathbb C^{M\times M}
$$

be two reduction paths.

**Definitions:** For $x\in X$, define

$$
E(x):=\mathcal R_1(x)-\mathcal R_2(x).
$$

Define the two norm-specific residuals by

$$
\varepsilon_F(x):=\lVert E(x)\rVert_F,
\qquad
\varepsilon_2(x):=\lVert E(x)\rVert_2.
$$

**Assumptions:** For every $G\in U(M)$, every $x\in X$, and $j\in\{1,2\}$, both paths are equivariant under the same output action:

$$
\mathcal R_j(\sigma_Gx)
=
G^\dagger\mathcal R_j(x)G.
$$

The two outputs act on the same identified $M$-dimensional coordinate space and use compatible energy references.

**Conclusion:** For every $G\in U(M)$ and $x\in X$,

$$
E(\sigma_Gx)=G^\dagger E(x)G,
$$

and, separately for the two declared norms,

$$
\varepsilon_F(\sigma_Gx)=\varepsilon_F(x),
\qquad
\varepsilon_2(\sigma_Gx)=\varepsilon_2(x).
$$

**Equivalent formulation:** A backend may state one generic lemma for a reviewed unitarily invariant norm and instantiate it for the Frobenius and induced Euclidean operator norms.

**Nonclaims:**

- This theorem does not assert $E=0$ or that the reduction paths commute.
- It does not show that either path is physically adequate.
- It does not apply when the outputs use incompatible spaces, gauges, dimensions, or energy references.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `equivariant_path_residual_gauge_invariant` |
| Isabelle | `equivariant_path_residual_gauge_invariant` |
| Rocq | `equivariant_path_residual_gauge_invariant` |

**Conformance questions:**

- Are both path outputs transformed by one common action?
- Is path commutativity kept distinct from gauge invariance of the defect norm?
- Are both declared norm instances checked?

## PRF-05.07: Two-point counterexample to gauge–truncation commutation

**Identity:** `PRF-05.07`

**Status:** `frozen`

**Purpose:** Provide a finite explicit counterexample showing that real-space truncation is not equivariant under all wavevector-dependent unitary gauges.

**Authority references:**

- [Localized impurity-reduction research](../../docs/research/ksdft2Effmass.07.md)
- [Compositional reduction research](../../docs/research/ksdft2Effmass.10.md)
- [Gauge-constrained locality](../../docs/proofs/ksdft2effmass/reduction/gauge-constrained-locality.md)
- [Representation maps](../../docs/proofs/ksdft2effmass/foundations/representation-maps.md)

**Mathematical setting:** Use a two-point reciprocal set $K=\{0,\pi\}$, a two-point real-space index set $R=\{0,1\}$, and $2\times2$ complex matrices. For a reciprocal-space family $H(k)$, define the normalized discrete Fourier blocks

$$
H_R
:=
\frac12\sum_{k\in K}e^{-ikR}H(k),
$$

with inverse

$$
H(k)=\sum_{R\in\{0,1\}}e^{ikR}H_R.
$$

Let $\mathcal F$ denote this reciprocal-to-real discrete Fourier transform and let $P_0$ set the $R=1$ block to zero while preserving the $R=0$ block. Define the reciprocal-family truncation map explicitly by

$$
\mathcal T_0:=\mathcal F^{-1}P_0\mathcal F.
$$

Define the gauge action

$$
(\rho_GH)(k):=G(k)^\dagger H(k)G(k).
$$

**Definitions:** Let

$$
H(0)=H(\pi)
=
\begin{pmatrix}
1&0\\
0&0
\end{pmatrix},
$$

and

$$
G(0)=I_2,
\qquad
G(\pi)=
\begin{pmatrix}
0&1\\
1&0
\end{pmatrix}.
$$

Both gauge matrices are unitary.

**Assumptions:** The Fourier and truncation maps are exactly the finite maps displayed above.

**Conclusion:**

$$
\mathcal T_0(\rho_GH)
\ne
\rho_G(\mathcal T_0H).
$$

More explicitly, $H_1=0$, so $\mathcal T_0H=H$. After the gauge transformation,

$$
(\rho_GH)_0=\frac12I_2,
\qquad
(\rho_GH)_1
=
\frac12
\begin{pmatrix}
1&0\\
0&-1
\end{pmatrix}
\ne0.
$$

Thus $\mathcal T_0(\rho_GH)$ is the constant reciprocal-space family $\frac12I_2$, whereas $\rho_G(\mathcal T_0H)=\rho_GH$ retains a nonzero $R=1$ block.

**Equivalent formulation:** A backend may use the cyclic group of order two and its discrete Fourier transform instead of the labels $0$, $\pi$, $0$, and $1$, provided the explicit matrices and noncommutation result are equivalent.

**Nonclaims:**

- The theorem is an existence counterexample, not a claim that every wavevector-dependent gauge fails to commute with every truncation.
- It does not identify the physically admissible gauge group for silicon.
- It does not quantify truncation error or establish a crossover radius.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `wavevector_dependent_gauge_truncation_counterexample` |
| Isabelle | `wavevector_dependent_gauge_truncation_counterexample` |
| Rocq | `wavevector_dependent_gauge_truncation_counterexample` |

**Conformance questions:**

- Do all backends use the same normalized two-point Fourier transform?
- Is truncation applied in real-space block coordinates and then transformed back for comparison?
- Is the conclusion existential/nonuniversal rather than an overgeneralized statement about all gauges?

## PRF-05.08: Shell-Frobenius invariance under a constant local rotation

**Identity:** `PRF-05.08`

**Status:** `frozen`

**Purpose:** Establish invariance of shell-resolved Frobenius weights when one constant unitary orbital rotation acts independently at every lattice cell without mixing lattice vectors.

**Authority references:**

- [Localized impurity-reduction research](../../docs/research/ksdft2Effmass.07.md)
- [Operator-error research](../../docs/research/ksdft2Effmass.08.md)
- [Frobenius-norm contract](#prf-0505a-frobenius-norm-invariance-under-unitary-conjugation)
- [Gauge-constrained locality](../../docs/proofs/ksdft2effmass/reduction/gauge-constrained-locality.md)

**Mathematical setting:** Let $\Lambda$ be a finite set of lattice-vector labels, let $\mathcal S\subseteq\Lambda$ be one shell, and let

$$
H(R)\in\mathbb C^{M\times M}
$$

for every $R\in\Lambda$, with $M>0$. Let $G\in\mathbb C^{M\times M}$ be one unitary matrix independent of $R$.

**Definitions:** Define

$$
H'(R):=G^\dagger H(R)G
$$

and the shell weights

$$
w_{\mathcal S}(H)
:=
\left(
\sum_{R\in\mathcal S}\lVert H(R)\rVert_F^2
\right)^{1/2},
$$

$$
w_{\mathcal S}(H')
:=
\left(
\sum_{R\in\mathcal S}\lVert H'(R)\rVert_F^2
\right)^{1/2}.
$$

**Assumptions:**

1. $G$ is unitary and independent of $R$.
2. The gauge action does not permute or mix lattice-vector labels.
3. The shell $\mathcal S$ is unchanged by the coordinate rotation.

**Conclusion:**

$$
w_{\mathcal S}(H')=w_{\mathcal S}(H).
$$

**Equivalent formulation:** A backend may use a finite index type for $\Lambda$ and finite sums over a shell predicate.

**Nonclaims:**

- This theorem does not apply to general wavevector-dependent gauges that mix Fourier blocks.
- It does not make individual matrix elements or orbital blocks invariant.
- It does not establish that the chosen shell decomposition is physically unique.
- It does not establish invariance under transformations that mix lattice sites or shell labels.

**Backend bindings:**

| Backend | Intended exported theorem name |
|---|---|
| Lean | `shell_frobenius_weight_constant_rotation` |
| Isabelle | `shell_frobenius_weight_constant_rotation` |
| Rocq | `shell_frobenius_weight_constant_rotation` |

**Conformance questions:**

- Is the same unitary applied to every lattice block?
- Is the shell a finite unchanged index subset?
- Does the proof reduce explicitly to Frobenius invariance block by block?

## Contract review boundary

All nine `PRF-05` contracts are frozen following conditional review, correction, and explicit human confirmation. The two norm constructions are tracked as `PRF-05.05a` and `PRF-05.05b`, and `PRF-05.04` retains both common-space orientations. No backend source exists, and freezing does not authorize toolchain installation or implementation.
