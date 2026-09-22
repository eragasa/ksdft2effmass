# Continuum Fitting and Identifiability

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 8. Continuum-Parameter Existence and Identifiability

### 8.1 Parameterized continuum model

Let

$$
\hat V_{\mathrm{cont}}
=
\hat V_{\mathrm{cont}}(\boldsymbol\theta),
\qquad
\boldsymbol\theta\in\Theta.
$$

Possible parameters include:

- dielectric screening;
- screening length;
- central-cell strength;
- short-range cutoff;
- nonlocal correction coefficients.

### 8.2 Exterior fitting objective

Define

$$
J_R(\boldsymbol\theta)
=
\left\|
\hat P_{>R}
\left[
\Delta\hat H_d-
\hat V_{\mathrm{cont}}(\boldsymbol\theta)
\right]
\hat P_{>R}
\right\|.
$$

### 8.3 Theorem 7: Existence of an optimal parameter vector

If $\Theta$ is compact and $J_R$ is continuous, prove that

$$
\boldsymbol\theta_R^*
\in
\operatorname*{arg\,min}_{\boldsymbol\theta\in\Theta}
J_R(\boldsymbol\theta)
$$

exists.

### 8.4 Identifiability question

Determine whether

$$
\boldsymbol\theta_R^*
$$

is unique.

Nonuniqueness would indicate that the available atomistic data cannot separately identify all continuum corrections.

### 8.5 Numerical requirements

Report:

- optimizer uncertainty;
- parameter covariance;
- profile likelihoods or equivalent diagnostics;
- sensitivity to $R$;
- sensitivity to the operator norm;
- sensitivity to the retained subspace.

---
