# Numerical contract

For a real-symmetric operator `H` of shape `N` by `N` and an orthonormal injection `Q`
of shape `N` by `K`, the reducer constructs

$$
A_Q=Q^{\mathsf T}HQ,
\qquad
P_Q=QQ^{\mathsf T},
$$

$$
H_Q^{\mathrm{embedded}}=Q A_Q Q^{\mathsf T}=P_QHP_Q,
$$

and

$$
R_Q=HQ-QA_Q=(I-P_Q)HQ.
$$

`A_Q` has shape `K` by `K`; `P_Q` and the embedded operator have shape `N` by `N`;
`R_Q` has shape `N` by `K`. Operator-valued outputs retain the unit of `H`, while the
projector is unitless.

No norm or tolerance is applied to `R_Q`. For a spectral subspace it measures
represented eigensolver invariance; for a trial subspace it measures Galerkin leakage.
Those interpretations remain distinguishable through the request's nominal subspace
type.
