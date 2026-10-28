# `Periodic1DFourierLocalityMeshResult` numerics

Construction vectors and complete coefficient vectors have length `N`. Centered cyclic
representatives are `-N/2,...,N/2-1` for the configured even meshes. The complete
construction and evaluation candidates are explicit real vectors correlated with those
complex coefficients by the root record.

For an attained range `R`, the finite error--complexity objective is

\[
(2R+1, e_{\mathrm{tot}}(N,R)).
\]

A candidate is nondominated when no other attained support is no larger in both cost and
mediated total maximum error and strictly smaller in at least one. Near ties are
identified only among nondominated candidates within the configured absolute-relative
scale.

`first_joint_pass` is the least range whose mediated and direct total maximum errors both
pass the application threshold. It is `None` when no attained range passes.
`sustained_after_first_pass` additionally requires every later attained range to pass.
Both values are recomputed from the ordered range tuple.
