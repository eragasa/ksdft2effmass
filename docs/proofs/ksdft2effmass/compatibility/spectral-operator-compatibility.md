# Spectral–Operator Compatibility

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 9. Spectral–Operator Compatibility

### 9.1 Spectral admissible set

For model class $m$, define

$$
\mathcal A_{\mathrm{spec}}^{(m)}
=
\left\{
\boldsymbol\theta:
\epsilon_{\mathrm{spec}}(\boldsymbol\theta)
\leq
\tau_{\mathrm{spec}}
\right\}.
$$

### 9.2 Operator admissible set

Define

$$
\mathcal A_{\mathrm{op}}^{(m)}
=
\left\{
\boldsymbol\theta:
\epsilon_{\mathrm{op}}(\boldsymbol\theta)
\leq
\tau_{\mathrm{op}}
\right\}.
$$

### 9.3 Compatibility question

Determine whether

$$
\mathcal A_{\mathrm{spec}}^{(m)}
\cap
\mathcal A_{\mathrm{op}}^{(m)}
\neq\varnothing.
$$

### 9.4 Theorem 8: Minimum separation

For compact admissible sets, define

$$
\delta_m
=
\inf_{
\substack{
\boldsymbol\theta_s\in\mathcal A_{\mathrm{spec}}^{(m)}\\
\boldsymbol\theta_o\in\mathcal A_{\mathrm{op}}^{(m)}
}
}
d_m(
\boldsymbol\theta_s,
\boldsymbol\theta_o
).
$$

Prove that the minimum is attained.

If the sets are disjoint and compact, then

$$
\delta_m>0.
$$

### 9.5 Certified incompatibility

Failure of an ordinary optimizer to find an intersection is not a proof.

A certified incompatibility result requires one of:

- analytical parameter bounds;
- interval arithmetic;
- branch-and-bound global optimization;
- exhaustive finite reduction with certified error;
- convex relaxation with a valid separation certificate.

### 9.6 Publishable claim

The strongest result would be:

> No member of a specified Slater–Koster model class can simultaneously satisfy the declared spectral and operator tolerances.

---
