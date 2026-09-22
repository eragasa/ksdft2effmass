# Model-Class Expressiveness

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

This observation leads naturally from parameter optimization to model-class geometry. Let
$$
\mathcal{M}_m
=
\left\{
\mathbf H_{\mathrm{TB}}(\theta)
:
\theta\in\Theta_m
\right\}
$$
denote a parameterized tight-binding model class of complexity $m$, and let

$$
\mathcal O_{\mathrm{phys}}(\mathbf H_W)
=
\left\{
\mathbf Q^\dagger\mathbf H_W\mathbf Q
:
\mathbf Q\in\mathcal G_{\mathrm{phys}}
\right\}
$$

denote the physically admissible orbit of a reference Wannier Hamiltonian. For a unitarily invariant norm $|\cdot|_{\mathcal K}$ defined over the selected $\mathbf k$ mesh or Brillouin-zone measure, the intrinsic operator discrepancy of the model class is

$$
d_m
=
\inf_{\theta\in\Theta_m}
\inf_{\mathbf Q\in\mathcal G_{\mathrm{phys}}}
\left|
\mathbf H_{\mathrm{TB}}(\theta)
-
\mathbf Q^\dagger
\mathbf H_W
\mathbf Q
\right|_{\mathcal K}.
$$

This quantity is not merely the residual of a particular parameter fit. It measures the separation between a constrained model class and the admissible orbit of the reference operator. If $d_m=0$, or is smaller than a prescribed numerical tolerance, then the model class contains a representation equivalent to the reference within the stated gauge and discretization assumptions. If $d_m>0$ after the infimum has been resolved, then no admissible change of coordinates can remove the discrepancy. The residual is therefore evidence of a limitation of the chosen model class, rather than an artifact of basis choice. Importantly, such a conclusion remains conditional on the specified retained subspace, admissible gauge group, norm, sampling measure, and model-class constraints.

This geometric formulation also extends the admissible-set view of tight-binding validation. Let $\mathcal A_{\mathrm{spec}}^{(m)}$ denote the parameter values satisfying prescribed spectral tolerances and let $\mathcal A_{\mathrm{op}}^{(m)}$ denote those satisfying a gauge-aligned operator tolerance. The relevant feasibility question is

$$
\mathcal A_{\mathrm{spec}}^{(m)}
\cap
\mathcal A_{\mathrm{op}}^{(m)}
\neq
\varnothing.
$$

A nonempty intersection establishes that the model class contains at least one parameterization satisfying both forms of validation. An empty intersection establishes incompatibility only for the chosen class, tolerances, and physical gauge restrictions; it does not imply the failure of all tight-binding descriptions. This separates three sources of disagreement that are otherwise easily conflated: coordinate mismatch, unsuccessful optimization, and insufficient model-class expressiveness.
