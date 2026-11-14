# Selected rank-one scalar parent

## Decision

The compatible rank-one control is the **lowest ordered eigenvalue field of the exact
four-state finite-range parent** described below. This is Option B from the prospective
review and was selected by explicit operator decision before implementation.

The phrase *isolated band* is reserved for a separately established global gap. Phase 2
requires only a clearly labelled sampled first-to-second gap qualification and does not
claim continuum isolation.

## Rejected alternative A — direct one-orbital finite-range parent

Define

\[
H(q)=\epsilon_0+t_1 e^{2\pi iq}+t_1^*e^{-2\pi iq},
\qquad -\tfrac12\le q<\tfrac12,
\]

with a positive declared energy scale `E_ref`.

**Advantages**

- exact scalar specialization of the onsite/nearest-neighbor Bloch form;
- no ambient-state-space or subspace-selection ambiguity;
- exact Fourier support and a simple independent oracle.

**Limitations**

- every support at or above one cell is exact, so the locality and first-passage study is
  nearly trivial;
- it does not exercise a nontrivial omitted-hopping tail unless additional harmonics are
  introduced, which would require another scientific choice.

## Selected option B — lowest ordered eigenvalue field of the controlled four-state parent

Use the controlled-family parent at exact hopping scale one,

\[
K(q)=T_0+e^{2\pi iq}T_{+1}+e^{-2\pi iq}T_{+1}^{\dagger}.
\]

The rank-one control does not sweep the development homotopy scale. Define the scalar field mathematically as its lowest ordered eigenvalue
`H(q)=λ₀(K(q))`, not as the output of a particular runtime eigensolver. The result must
separately qualify the sampled first-to-second eigenvalue gap. The scalar represented
operator then has no internal gauge action, while diagonalization of the finite-range
ambient parent generally produces a nontrivial scalar Fourier tail.

The selected parent identity is
`ksdft2effmass.periodic1d.controlled-four-state-parent.v1`. It uses the exact positive
energy reference `E_ref = 1`. Every matrix entry below is an exact dimensionless ratio
to `E_ref`; `K(q)` and `H(q)` have energy units `E_ref`. The block-diagonal onsite
matrices are

\[
L_0=\begin{pmatrix}-1.20&0.06\\0.06&-0.35\end{pmatrix},\qquad
U_0=\begin{pmatrix}1.00&0.04\\0.04&1.75\end{pmatrix},
\]

and positive-neighbor blocks

\[
L_1=\operatorname{diag}(0.15,-0.10),\quad
U_1=\operatorname{diag}(0.05,-0.04),\quad
C_1=\operatorname{diag}(0.12,0.10),
\]

with

\[
T_0=\operatorname{diag}(L_0,U_0),\qquad
T_{+1}=\begin{pmatrix}L_1&C_1\\0&U_1\end{pmatrix}.
\]

Every displayed terminating decimal is exact rational data: `-1.20 = -6/5`,
`0.06 = 3/50`, `-0.35 = -7/20`, `1.00 = 1`, `0.04 = 1/25`, `1.75 = 7/4`,
`0.15 = 3/20`, `-0.10 = -1/10`, `0.05 = 1/20`, `-0.04 = -1/25`,
`0.12 = 3/25`, and `0.10 = 1/10`. These values originated in a development
rank-two workflow but are now frozen prospectively under the parent identity above. This
decision does not promote that workflow, its results, or its evidence state. The later
rank-two successor must either bind this same immutable parent identity or explicitly
identify and justify a different scientific family.

**Advantages**

- strongest structural compatibility with the intended rank-two family;
- retains a meaningful scalar Fourier tail, support-truncation study, and sampled-gap
  qualification;
- cleanly demonstrates that nontrivial scalar locality can coexist with
  operator-trivial `U(1)` conjugation.

**Limitations**

- freezes a shared parent before the rank-two Phase 3 successor is complete;
- requires explicit ambient-space, ordered-band, gap, and sampled-qualification records;
- the sampled gap is a finite diagnostic, not a continuum isolation certificate.

## Rejected alternative C — independent analytic multi-harmonic scalar field

Choose a finite or analytically decaying scalar Fourier series independently of the
four-state parent.

**Advantages**

- exact coefficients and truncation tails can provide strong analytical controls;
- avoids subspace-selection and gap qualification.

**Limitations**

- it is not automatically a specialization of the controlled rank-two parent;
- coefficients and decay law would be new scientific inputs requiring their own
  justification;
- it risks becoming another scalar benchmark rather than the compatible null control.

## Excluded option — Mathieu1D or historical M1 identity

The Mathieu1D lowest band and historical M1 package remain method and parity donors only.
Reusing their `0.5 cos(x)` parent would collapse two deliberately separate scientific
families and is therefore excluded.

## Claim boundary after selection

Analytically exact statements are limited to the parent coefficients and conventions,
Hermiticity of `K(q)`, ambient Fourier support `{-1, 0, 1}`, definition of the least
ordered eigenvalue field, and scalar `U(1)` conjugation invariance. Conditional finite
Fourier and decision identities may also be exact when their hypotheses are supplied as
exact data.

Eigenvalue samples, sampled minimum gap, transform coefficients derived from samples,
interpolation and truncation errors, thresholds, and first-passage outcomes remain
finite numerical quantities unless separately enclosed by a proposition-specific
certificate. A sampled positive gap does not establish global isolation, continuum
convergence, or material applicability.

Those finite controls are now frozen in
[`numerical-control-decision.md`](numerical-control-decision.md). No execution or retained
result may precede the remaining family-specific typed-record, byte-owning verification,
authenticated-projection, and direct-script reviews.
