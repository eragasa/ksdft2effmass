# Reduction-Path Commutativity

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 10. Commutativity of Reduction Paths

### 10.1 Competing impurity paths

Compare:

$$
\text{full atomistic operators}
\rightarrow
\text{impurity extraction}
\rightarrow
\text{reduction}
$$

with

$$
\text{full atomistic operators}
\rightarrow
\text{separate reductions}
\rightarrow
\text{reduced impurity extraction}.
$$

### 10.2 Commutator defect

Define a path-consistency residual

$$
\epsilon_{\mathrm{path}}
=
\left\|
\mathcal R(
\hat H_d-\hat H_b
)
-
\left[
\mathcal R(\hat H_d)
-
\mathcal R(\hat H_b)
\right]
\right\|.
$$

### 10.3 Theorem 9: Exact commutativity conditions

Identify sufficient conditions under which

$$
\mathcal R(
\hat H_d-\hat H_b
)
=
\mathcal R(\hat H_d)
-
\mathcal R(\hat H_b).
$$

Possible conditions include:

- a common retained subspace;
- a common linear reduction map;
- consistent gauges;
- consistent energy references;
- identical basis ordering.

### 10.4 Approximate commutativity bound

When the two reduction maps differ, derive an upper bound on $\epsilon_{\mathrm{path}}$ in terms of:

- projector mismatch;
- gauge-alignment error;
- truncation error;
- energy-reference mismatch.

---


---

## 5. Move from one path to path consistency

Suppose there are two constructions of a reduced impurity operator:

$$
\mathcal R_1(H_b,H_d)
$$

and

$$
\mathcal R_2(H_b,H_d).
$$

For example,

$$
\mathcal R_1

\text{Wannierize}
\rightarrow
\text{subtract}
\rightarrow
\text{truncate},
$$

while

$$
\mathcal R_2

\text{fit TB}
\rightarrow
\text{subtract reduced models}.
$$

The path residual is

$$
\mathcal E(H_b,H_d)

\mathcal R_1(H_b,H_d)

\mathcal R_2(H_b,H_d).
$$

If both paths are equivariant under the same output action,

$$
\mathcal R_j(H_b',H_d')

G^\dagger
\mathcal R_j(H_b,H_d)
G,
$$

then

$$
\mathcal E(H_b',H_d')

G^\dagger
\mathcal E(H_b,H_d)
G.
$$

Consequently,

$$
|\mathcal E(H_b',H_d')|

|\mathcal E(H_b,H_d)|
$$

for every unitarily invariant norm.

This is the natural theorem underlying the entire path-consistency program.

## 6. Distinguish equivariance from commutativity

These are different claims.

Gauge equivariance asks whether

$$
\mathcal R\circ\rho_G

\rho_G\circ\mathcal R.
$$

Path commutativity asks whether two physical reductions give the same result:

$$
\mathcal R_1
\stackrel{?}{=}
\mathcal R_2.
$$

The first says the result does not depend on coordinates.

The second says the result does not depend on the chosen reduction route.

Gauge equivariance must be established before a path residual can be interpreted physically. Otherwise, a nonzero residual may merely reflect incompatible coordinate choices.

The logical hierarchy should therefore be

$$
\boxed{
\text{gauge consistency}
\longrightarrow
\text{well-defined path residual}
\longrightarrow
\text{test of physical commutativity}.
}
$$
