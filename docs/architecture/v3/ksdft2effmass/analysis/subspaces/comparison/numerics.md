# Numerical contract

For candidate injection `Q_c` and reference injection `Q_r`, both with shape `N` by
`K`, the comparator constructs

$$
P_c=Q_cQ_c^{\mathsf T},
\qquad
P_r=Q_rQ_r^{\mathsf T},
$$

and

$$
\Delta_P=P_c-P_r.
$$

All outputs are unitless `N`-by-`N` matrices. The action applies no norm or tolerance.

An outward experiment may select

$$
\frac{\lVert\Delta_P\rVert_F}{\sqrt{2K}}
=\sqrt{\frac{1}{K}\sum_{j=1}^{K}\sin^2\theta_j}
$$

as an aggregate principal-angle observation. That Frobenius normalization is not part
of the comparator contract.

Projector comparison is invariant under column signs and orthogonal rotations within
each retained subspace.
