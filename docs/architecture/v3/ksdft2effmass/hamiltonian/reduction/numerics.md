# Numerical contract

For an orthonormal injection $\Phi_M$ of shape $N$ by $M$,

$$
H_M=\Phi_M^{\mathsf T}H\Phi_M,
\qquad
P_M=\Phi_M\Phi_M^{\mathsf T},
$$

$$
H_M^{\mathrm{embedded}}=\Phi_M H_M\Phi_M^{\mathsf T}.
$$

$H_M$ has shape $M$ by $M$ and the embedded matrix has shape $N$ by $N$.
Both retain the unit of $H$; $P_M$ is unitless.

The general `SpectralSubspace` contract does not derive reduction from a projector.
Concrete nonorthogonal spaces supply their own left reduction and right embedding
behavior. No norm or tolerance is applied by `SpectralReduction`.
