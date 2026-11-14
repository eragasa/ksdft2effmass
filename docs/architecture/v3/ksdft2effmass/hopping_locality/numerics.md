# Hopping-locality numerical contract

## Shared coefficient inventory

All resolutions analyze one unchanged periodic block-hopping model

\[
T:\mathbb Z^d\longrightarrow\mathbb C^{r\times r}
\]

with an exact ordered retained basis and declared gauge. The analyzer does not remove
coefficients or construct a truncated operator. Support truncation remains a separate
operation that may consume a locality result.

When the model is Hermitian,

\[
T(-\mathbf n)=T(\mathbf n)^\dagger.
\]

A locality request must state whether its inventory is directed or pair symmetric. It
must not sum both members of a Hermitian pair and then describe the result as
single-counted without an explicit weighting convention.

## Cell-block power

The elementary cell-block power is

\[
P_{\mathrm{block}}(\mathbf n)=\lVert T(\mathbf n)\rVert_F^2
=\sum_{\alpha=1}^{r}\sum_{\beta=1}^{r}
  \lvert T_{\alpha\beta}(\mathbf n)\rvert^2.
\]

This identity is the required reconciliation between cell-block and element-resolved
results. If both analyzers consume the same admitted coefficient bytes, their
per-displacement powers must agree under the declared summation and normalization
conventions.

Normalization is not inferred. A result must distinguish raw squared-energy power from
a dimensionless normalized value and retain the denominator identity. The existing
metric-shell path uses retained-rank normalization for its established result; that
choice is not automatically imposed on every future locality analyzer.

## Orbital-resolved displacement and power

For an ordered basis embedding with fractional direct-basis centers
$\mathbf s_\alpha$, the directed element displacement is

\[
\mathbf d_{\alpha\beta\mathbf n}
=A\left(\mathbf n+\mathbf s_\beta-\mathbf s_\alpha\right),
\]

and the elementary power is

\[
P_{\alpha\beta}(\mathbf n)
=\lvert T_{\alpha\beta}(\mathbf n)\rvert^2.
\]

Rows are source states and columns are target states under one declared convention. The
request must retain that convention rather than relying on an undocumented matrix
orientation. Hermiticity gives

\[
P_{\alpha\beta}(\mathbf n)=P_{\beta\alpha}(-\mathbf n),
\qquad
\mathbf d_{\beta\alpha,-\mathbf n}
=-\mathbf d_{\alpha\beta\mathbf n}.
\]

A pair-symmetric result must define its canonical representative and whether it retains
one member, the pair sum, or an explicitly weighted average. Directed results preserve
the complete ordered coefficient inventory and are the simplest exact decomposition of
block Frobenius power.

## Center-attributed MLWF-pair locality

The initial MLWF-resolved numerical observable uses the orbital-resolved equations with
centers and identities supplied by a correlated MLWF embedding:

\[
P^{\mathrm{MLWF}}_{ab}(\mathbf n)=\lvert T_{ab}(\mathbf n)\rvert^2.
\]

It is a center-attributed coefficient diagnostic. The MLWF quadratic spread
$\Omega_a$ is retained, when available, as a separately named value with its unit and
provenance. The initial power and distance are not multiplied, divided, or broadened by
$\Omega_a$.

A later spread-aware observable would require its own dimensional analysis,
normalization, physical interpretation, and validation. A full-shape locality observable
would additionally require admitted wavefunction or density information and must not be
reconstructed from centers and spreads alone.

## Center representatives and lattice images

MLWF centers are periodic. The embedding must retain the selected fractional center
representative and any integer lattice-image displacement used to correlate it with the
ordered hopping basis. Replacing $\mathbf s_a$ by $\mathbf s_a+\mathbf m_a$ changes the
index attached to an element unless the hopping coefficients are transformed
consistently. A locality analyzer must reject an uncorrelated center inventory rather
than choosing nearest images independently for each matrix element.

The primitive-basis orientation and physical length unit come from the exact model
geometry. Center coefficients are dimensionless; the resulting physical displacement
has the geometry's length unit. Squared hopping power has squared-energy units unless a
declared normalization makes it dimensionless.

## Admission requirements

A prospective orbital- or MLWF-resolved request must validate at least:

1. exact model identity and immutable coefficient representation;
2. exact geometry identity and dimension;
3. exact equality between model basis size and embedding length;
4. exact equality between model `basis_identifier` and embedding correlation identity;
5. unique ordered state or MLWF identifiers;
6. finite exact-dimensional center coefficients;
7. declared matrix source/target orientation;
8. declared directed or pair-symmetric counting convention;
9. declared power unit and normalization; and
10. for MLWFs, complete localization and gauge provenance required by the scientific
    comparison.

Boolean values, numeric strings, nonfinite centers, unknown-dimensional arrays, and
implicit producer fallbacks are not admitted.

## Numerical failure and verification

Finite binary64 element powers and sums must report overflow or nonfinite arithmetic;
they must not clip. Distances require the exact geometry mapping rather than a bare
Euclidean norm of fractional coefficients.

Independent verification should reconstruct selected element powers directly from the
admitted coefficient bytes, check the block-sum reconciliation, check Hermitian partner
relations, and independently map selected embedded displacements through the primitive
basis. Passing those checks establishes software agreement for the declared finite
inventory only.
