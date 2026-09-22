# Spatial Residual and Crossover Radius

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 4. Well-Posed Atomistic-to-Continuum Crossover

### 4.1 Atomistic–continuum difference

Define

$$
\hat D_d
=
\Delta\hat H_d
-
\hat V_{\mathrm{cont},d}.
$$

### 4.2 Exterior tail error

Define

$$
\eta_d(R)
=
\left\|
\hat P_{>R}
\hat D_d
\hat P_{>R}
\right\|.
$$

### 4.3 Lemma 1: Monotonicity

For nested exterior spaces,

$$
R_2\geq R_1
\quad\Longrightarrow\quad
\hat P_{>R_2}\leq\hat P_{>R_1}.
$$

Prove, for the operator norm,

$$
\eta_d(R_2)
\leq
\eta_d(R_1).
$$

### 4.4 Assumption: Asymptotic locality

Assume

$$
\lim_{R\rightarrow\infty}
\eta_d(R)
=
0.
$$

This assumption asserts that the residual atomistic structure becomes negligible after subtracting the appropriate continuum potential.

### 4.5 Theorem 2: Existence of the crossover radius

For every tolerance $\tau_H>0$, define

$$
r_{c,d}(\tau_H)
=
\inf
\left\{
R:
\eta_d(R)\leq\tau_H
\right\}.
$$

Prove that $r_{c,d}(\tau_H)$ exists under the asymptotic-locality assumption.

### 4.6 Numerical proof obligation

The calculation must test whether:

$$
\eta_d(R)\rightarrow 0
$$

before finite-supercell and periodic-image effects dominate.

### 4.7 Interpretation

The crossover radius is tolerance dependent:

$$
r_{c,d}=r_{c,d}(\tau_H).
$$

It is not automatically a unique material constant.

---
