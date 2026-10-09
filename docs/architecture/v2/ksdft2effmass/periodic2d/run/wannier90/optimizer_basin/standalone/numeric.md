# Numerical contract

## Finite design

The standalone study retains 16 explicit configuration/optimizer groups and 16 ordered
deterministic initial gauges per group, giving 256 initial processes. An effective
endpoint is the initial native endpoint when that endpoint reports native convergence.
Otherwise it is the exact retained continuation endpoint, whether that continuation
converged or stopped. Process completion and native Wannier90 convergence remain
distinct fields.

## Spread reconstruction

For every initial, present continuation, and effective native endpoint, the verifier
checks

\[
\widetilde\Omega = \Omega_D + \Omega_{OD},
\qquad
\Omega = \Omega_I + \Omega_D + \Omega_{OD},
\]

using absolute tolerance \(2\times 10^{-8}a^2\). Every consumed ordinary real must be
representable as finite binary64. The native endpoint is retained field by field,
including center coordinates, orbital spreads, iteration and trace counts, and terminal
diagnostics. Effective/initial or effective/continuation equality is exact at that typed
record boundary.

A continuation must occur exactly when the initial endpoint lacks the native convergence
statement. Its total effective iteration count is the sum of initial and continuation
iterations.

## Terminal-trace classification

For stopped effective endpoints, the retained exploratory classification is reconstructed
in this order:

1. median absolute spread change at most \(10^{-8}\) and median RMS gradient at most
   \(10^{-3}\): `near_stationary_without_window_convergence`;
2. spread slope below \(-10^{-8}\) per iteration:
   `continuing_descent_at_iteration_limit`;
3. detrended spread RMS above \(10^{-5}\): `oscillatory_or_stalled`;
4. otherwise: `stalled_or_nondescent`.

The aggregate diagnostic counts are accumulated from this route and compared with the
retained summary.

## Observed basin arithmetic

Within each group, only effective native-converged endpoints enter the retained observed
basin partition. The best observed endpoint minimizes \(\widetilde\Omega\), with start
identity as the explicit deterministic tie-breaker. Basin members must form a unique,
complete partition of converged start identities. The verifier reconstructs basin order
from that endpoint order, binds every representative to its effective spread, requires
one threshold-passing member diagnostic for every nonrepresentative member, and derives
start-block presence from the explicit gauge-design positions.

Rejected direct comparisons retain a periodic center-set distance and matched active-plane
density mismatch. Their identities must equal the earlier representatives eligible under
the frozen spread threshold, in comparison order. A bare positive `Infinity` means no
finite admissible comparison was recorded; it is allowed only at the complete indexed
paths of those two historical fields. The verifier confirms that no rejected pair
satisfies both frozen proposal thresholds and reconstructs direct-match counts at every
retained density tolerance. When a rejected representative is the best endpoint, the
reported relaxed-threshold match identity is the current candidate representative.

Post-hoc controls reconstruct the maximum center and density mismatches and exact frozen
threshold flags. No arbitrary size cap is imposed; allocation failure may propagate as
`MemoryError`, and unrepresentable integer-to-binary64 conversion may propagate as
`OverflowError`.
