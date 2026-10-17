# Band-equivalence/locality technical debt

## Status

`TECH_DEBT — DEFERRED`

This record tracks numerical mechanisms intentionally retained in the replaceable
Paper 2 dimensional-development implementation. It is not scientific qualification,
an evidence claim, or authorization for a production or retained calculation.

## Debt inventory

### `TD-BEL-001`: identity-gated correlation endpoint canonicalization

- **Disposition:** deferred.
- **Current owner:**
  `python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/alignment.py`,
  `restricted_alignment`.
- **Current mechanism:** after calculating the normalized restricted-alignment
  correlation, values within
  `64 * numpy.finfo(numpy.float64).eps` of either endpoint are replaced by exactly
  `+1.0` or `-1.0` before threshold evaluation.
- **Reason retained:** at zero gauge amplitude, analytically identical reference and
  comparison fields can produce `0.9999999999999999` instead of the exact identity
  value `1`. Substitution into the square-root threshold formula then creates a
  spurious nonzero threshold of order `1e-9 E_ref`.
- **Known limitation:** proximity to an endpoint alone does not prove an exact identity.
  The current rule could erase a genuine correlation departure smaller than about
  `1.42e-14`. It therefore must not be interpreted as a convergence tolerance or a
  physical equivalence decision.
- **Required replacement:** gate endpoint canonicalization on an independently verified
  exact-identity premise, such as the declared zero-amplitude transformation together
  with a direct reference/comparison equality defect bounded by a separately declared
  roundoff criterion. Near-endpoint correlations without that premise must remain
  unsnapped and retain their calculated value.
- **Required tests:** exact zero-amplitude identity; genuinely nonidentical near-endpoint
  fields; both endpoint signs where mathematically reachable; scale sensitivity;
  binary64 threshold reconstruction; and producer/verifier agreement.
- **Exit condition:** the identity premise, roundoff bound, serialized diagnostic, and
  independent verification are frozen in the family contract; the unconditional
  proximity-only rule is removed; all replaceable development records are regenerated;
  and the Paper 1 v3 calculation-parity audit is updated.

### `TD-BEL-002`: batched tensor-grid Procrustes transport

- **Disposition:** deferred upstream separation.
- **Current owner:**
  `python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/alignment.py`,
  `frame_transport_diagnostics`.
- **Current mechanism:** NumPy performs batched $2\times2$ SVDs over complete tensor-grid
  neighbor overlaps, then KSD aggregates singular values, Procrustes residuals,
  unitarity defects, loop holonomies, and plaquette phases.
- **Why it remains local:** the currently pinned Optimization dependency owns a reviewed
  one-pair complex-unitary Procrustes contract, but not a bounded batch contract.
  Converting every tensor-grid link into nested Python tuple objects and invoking the
  one-pair solver separately would discard the sparse/vectorized resource design.
- **Published adoption candidate:** the Optimization owner has published commit
  `f3a295fde4aeb905414da6375ec4f2794480628d`, with immutable batch definition/result
  semantics, source/target and right-action orientation, complete per-item singular
  spectra, per-item rank/cutoff and residual-roundoff evidence, fail-closed unique-
  transformation access, bounded vectorized execution, and backend/version identity.
  KSD has not yet pinned or adopted that revision.
- **Required KSD consumer contract:** preserve the published owner semantics, including
  additive rank cutoffs, squared-residual roundoff cutoffs, and diagnostic-only
  completions for deficient items; do not move KSD topology or scientific policy into
  Optimization.
- **KSD retained policy:** reciprocal-path identity, axis/plaquette inventory, closure
  interpretation, scientific gates, family identity, and evidence disposition.
- **Exit condition:** a reviewed pinned Optimization batch API exists, parity and resource
  tests pass against the local vectorized mechanism, the dependency revision update is
  separately authorized, and the local transformation-selecting SVD is removed.

While these debts are open, correlation snapping and local batched transport remain
bounded software-development mechanisms only. They cannot support qualified convergence,
retained evidence, or a scientific claim at their resolution scales.
