# `periodic1d.campaign.reduction_challenge.numerical_verification`

## Responsibility

`Periodic1DReductionChallengeResultVerifier` independently reconstructs the typed
version-one observations from already correlated controls. It intentionally does not
import production plane-wave or finite-difference constructors, frame transport,
hopping transforms, or fitting algorithms.

The verifier separately evaluates potential-amplitude, potential-shape,
mesh/band/isolation, gauge-covariance, and route-assumption maximum absolute defects.
It returns one finite unitless quantity per channel and one aggregate pass defined by
an inclusive explicit tolerance. Expected-trend prose is not an oracle and does not
enter the aggregate disposition.

All public outputs must be representable finite binary64 or complex128 values. Dense
eigensystems and least-squares operations may propagate `numpy.linalg.LinAlgError`;
large requests may raise `MemoryError`; unrepresentable results raise `OverflowError`.
No arbitrary scientific size cap is imposed.

See [numerical techniques](../numerical-techniques-and-scientific-reasoning.md) and the
[verification contract](../verification-contract.md).
