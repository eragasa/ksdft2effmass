# Aligned Impurity Operator

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 4. Prove equivariance of the elementary operations

The next theorem should be assembled from lemmas.

### Projection

For

$$
H^{(P)}

V^\dagger H V,
$$

and

$$
V'=VG,
$$

one obtains

$$
H^{(P)\prime}

G^\dagger H^{(P)}G.
$$

Thus projection to a fixed retained subspace is gauge equivariant.

### Identification and pullback

For an identification map

$$
U_d:
\mathcal H_b^{(P)}
\rightarrow
\mathcal H_d^{(P)},
$$

define the pullback

$$
\mathcal A_{U_d}(H_d)

U_d^\dagger H_dU_d.
$$

Under independent pristine and doped gauges,

$$
U_d'

G_d^\dagger U_dG_b,
$$

the pullback obeys

$$
\mathcal A_{U_d'}(H_d')

G_b^\dagger
\mathcal A_{U_d}(H_d)
G_b.
$$

Hence alignment is equivariant, provided the identification map is transformed consistently.

### Subtraction

If

$$
A'

G^\dagger AG,
\qquad
B'

G^\dagger BG,
$$

then

$$
(A-B)'

G^\dagger(A-B)G.
$$

Therefore subtraction is equivariant only when both operands have first been represented in the same coordinate system.

This gives the formal reason that unaligned bulk–dopant subtraction is not meaningful.
