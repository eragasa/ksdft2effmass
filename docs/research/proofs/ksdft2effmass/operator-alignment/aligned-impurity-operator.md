# Aligned Impurity Operator

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## Equivariance of the elementary operations

The aligned-subtraction theorem is assembled from projection, identification, transport, and subtraction lemmas. There are two valid common-space representations: pull the doped operator into the pristine retained space, or push the pristine operator into the doped retained space. Their covariance identities do not require the identification map itself to be unitary. Interpreting them as representations of the same aligned operator does require a unitary identification.

### Projection

For

$$
H^{(P)}=V^\dagger H V
$$

and

$$
V'=VG,
$$

one obtains

$$
H^{(P)\prime}=G^\dagger H^{(P)}G.
$$

Thus projection to a fixed retained subspace is gauge equivariant.

### Identification pullback and pushforward

Let

$$
U_d:
\mathcal H_b^{(P)}
\rightarrow
\mathcal H_d^{(P)}.
$$

Pull the doped operator into the pristine retained space by

$$
\mathcal A_{U_d}^{b}(H_d)
=
U_d^\dagger H_dU_d,
$$

or push the pristine operator into the doped retained space by

$$
\mathcal A_{U_d}^{d}(H_b)
=
U_dH_bU_d^\dagger.
$$

Under independent pristine and doped gauges,

$$
H_b'=G_b^\dagger H_bG_b,
\qquad
H_d'=G_d^\dagger H_dG_d,
\qquad
U_d'=G_d^\dagger U_dG_b,
$$

the two transported operators obey

$$
\mathcal A_{U_d'}^{b}(H_d')
=
G_b^\dagger
\mathcal A_{U_d}^{b}(H_d)
G_b,
$$

and

$$
\mathcal A_{U_d'}^{d}(H_b')
=
G_d^\dagger
\mathcal A_{U_d}^{d}(H_b)
G_d.
$$

### Aligned subtraction

Define the pristine-space and doped-space aligned differences by

$$
\Delta H_{d\to b}
=
U_d^\dagger H_dU_d-H_b,
$$

and

$$
\Delta H_{b\to d}
=
H_d-U_dH_bU_d^\dagger.
$$

Because each subtraction occurs in one common retained space,

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

If $U_d$ is a unitary identification, then

$$
\Delta H_{b\to d}
=
U_d\Delta H_{d\to b}U_d^\dagger,
\qquad
\Delta H_{d\to b}
=
U_d^\dagger\Delta H_{b\to d}U_d.
$$

The two matrices are then unitarily equivalent representations of the same aligned operator difference and have the same spectrum and unitarily invariant norms. Without unitarity of $U_d$, their separate covariance identities still hold, but this equivalence is not established.

State-space identification does not by itself align scalar energy references. The physical impurity-operator interpretation requires both prerequisites from the owning research convention.
