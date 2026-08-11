# Operator-to-Observable Error Bounds

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 5. Operator Error and Physical Observables

### 5.1 Reduction error

Write

$$
\hat H_{\mathrm{atom}}
=
\hat H_{\mathrm{red}}
+
\hat E.
$$

### 5.2 Theorem 3: Spectral stability

For self-adjoint operators, establish

$$
\operatorname{dist}
\left(
\sigma(\hat H_{\mathrm{atom}}),
\sigma(\hat H_{\mathrm{red}})
\right)
\leq
\|\hat E\|.
$$

### 5.3 Corollary 2: Binding-energy error

For a correctly identified isolated impurity state,

$$
\left|
E_{b,d}^{\mathrm{atom}}
-
E_{b,d}^{\mathrm{red}}
\right|
\leq
\|\hat E\|.
$$

### 5.4 Theorem 4: Eigenspace stability

Let $\gamma_d$ be the spectral separation between the target impurity state and the remaining spectrum.

Use a Davis–Kahan-type result to establish

$$
\sin\theta_d
\lesssim
\frac{\|\hat E\|}{\gamma_d}.
$$

### 5.5 Corollary 3: Fidelity bound

For normalized nondegenerate states,

$$
F_d
=
\left|
\langle
\psi_d^{\mathrm{atom}}
|
\psi_d^{\mathrm{red}}
\rangle
\right|^2,
$$

with

$$
1-F_d
\lesssim
\left(
\frac{\|\hat E\|}{\gamma_d}
\right)^2.
$$

### 5.6 Scientific consequence

Establish the validation chain

$$
\boxed{
\text{operator residual}
\Longrightarrow
\text{binding-energy bound}
\Longrightarrow
\text{wavefunction-fidelity bound}
}.
$$

---
