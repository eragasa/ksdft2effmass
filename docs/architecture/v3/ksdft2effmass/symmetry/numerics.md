# Symmetry numerics

**Prospective contracts, not implemented algorithms or an approved public API.** Initial
scope is an explicitly supplied ordinary finite group and complex-linear actions in
finite coefficient spaces. Additional representation classes require their own contracts.

## Spaces, metrics and actions

Identify the coordinate spaces and ordered bases before comparing matrices. In the
initial coefficient-space setting, symmetry-action matrices and positive-definite
Hermitian Gram metrics are dimensionless; any wider unit-bearing contract must be explicit. For a linear action
`M_g` from source metric `G_s` to target metric `G_t`, isometry requires

\[
M_g^\dagger G_t M_g=G_s.
\]

An identity metric is an explicit, justified choice, not a default inferred from a square
matrix or a parser. In particular, raw plane-wave coefficients of an ultrasoft calculation
must not be interpreted with an identity overlap metric by convenience. A qualified
S-orthonormal parent-band basis can instead have an identity coefficient metric; these
are different representations of the physical inner product. Ideal backend frames and
computed/printed matrices are distinct: qualification must account for numerical defects
rather than assert exact isometry from the intended convention.

An antiunitary action has the form `M_g K`, where `K` is conjugation in the declared
coordinate bases. Its corresponding metric condition is

\[
M_g^\dagger G_t M_g=\overline{G_s}.
\]

It cannot be implemented by silently treating `M_g` as a complex-linear map. Antiunitary
composition and sector theory remain outside the initial executable scope.

For an ordinary representation on one identified space, check identity, inverses and
`D(gh)=D(g)D(h)` against the declared multiplication law. Do not infer a group from spatial
dimension, operation labels or approximate matrix similarity. Projective phases, spinful
double-valued representations and momentum-dependent sewing are not ordinary group-law
errors to be repaired or ignored.

## Subspace closure before representation claims

For full-column-rank frames `F_s`, `F_t`, the induced metrics are
`G_Fs=F_s† G_s F_s` and `G_Ft=F_t† G_t F_t`. A proposed induced linear action `D_g`
has leakage

\[
L_g=M_gF_s-F_tD_g.
\]

Report it in a declared metric-compatible norm with appropriate numerical/input bounds.
For an antiunitary action the source term is `M_g overline(F_s)`, not `M_g F_s`.
Nonzero resolved leakage means the supplied action does not close on those subspaces;
a square compressed matrix does not fix that defect. Numerical uncertainty can make
closure inconclusive rather than establish or refute it.

The metric-orthogonal projector associated with a qualified full-rank frame is
`P_F=F(F† G F)^(-1)F† G`. This identity does not prescribe an implementation by explicit
inversion. Rank, conditioning, metric and source-space compatibility must be established
before selecting a stable factorization/solve. No hidden pseudoinverse, discarded
direction, polar repair or invented completion may turn a failed check into closure.

## Operators, overlaps and intertwiners are different objects

For coefficient-action matrices of linear operators, covariance is
`H_t M_g = M_g H_s`. Operator self-adjointness in a nonorthogonal basis is
`H† G = G H`; it need not be Euclidean Hermiticity. Matrix-element quadratic forms
must not be substituted for these coefficient-action matrices without the basis/metric
conversion.

For ordinary closed representations, a linear intertwiner `T` satisfies
`D_W(g) T = T D_C(g)`. In contrast, an overlap matrix `B=W† G C` between two frames in
the same ambient space obeys the invariance relation

\[
D_W(g)^\dagger B D_C(g)=B
\]

when both frame actions are qualified and the ambient action preserves `G`. In general
`B` is not itself the coefficient map into the nonorthogonal `W` frame. The projected
coefficient map is `T=(W† G W)^(-1)B`; closure and representation qualification remain
separate. Do not collapse operator maps, overlap forms and their coordinate conventions
into one generic transformation check.

## Sector projectors

For a qualified ordinary finite-group representation and a complete, compatible set of
irreducible characters, the isotypic projector is

\[
\Pi_\alpha=\frac{d_\alpha}{|\mathcal G|}
\sum_{g\in\mathcal G}\chi_\alpha(g)^*D(g).
\]

Qualify character data and group correspondence before using this formula. Check
idempotence, mutual orthogonality, completeness when claimed, metric self-adjointness
(`Pi† G = G Pi`) and sector dimensions. Isotypic sectors may contain several copies of
an irrep; this formula does not choose a unique basis or split equivalent copies.
Neither antiunitary corepresentations nor unspecified projective representations may be
fed through this ordinary-character formula.

## Numeric and verification policy

- Maintained data/results must be operationally immutable. Deliberate public imports,
  scalar/container types, units, precision and overflow/resource-failure behavior must
  be documented before implementation; reuse admitted PhysKit value primitives.
- Reject booleans and numeric strings at numeric boundaries. Wire encodings are explicit
  serializer contracts, not permission for hidden coercion in numerical APIs.
- Separate arithmetic residual/error bounds, native printing/parsing uncertainty,
  representation/truncation error, and physical-model/solver error. No universal tolerance
  or arithmetic escalation schedule is selected here.
- Test analytic synthetic groups and representations, basis changes including
  nonorthogonal coordinates, leakage counterexamples, invalid metrics, incompatible
  spaces/gauges, unsupported action kinds, and rejected scalar types. Test nonzero-
  momentum phases before claiming reciprocal-space support.
- Passing synthetic software tests does not authenticate an electronic action or validate
  silicon. Actual sector claims require source-bound action and closure evidence.

See [schematics](schematics.md), [science](science.md), and [index](index.md).
