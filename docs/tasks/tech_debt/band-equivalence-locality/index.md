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

- **Disposition:** owner adoption under review.
- **Numerical owner:** Optimization commit
  `2c6dd7f717722f6b0495feb8cfe1287a104268a6`, consumed through the canonical
  Procrustes contracts and the finite-periodic mesh, matrix-transform, tensor-product
  evaluation, Parseval, and Hermiticity contracts under `projectkoios.numerics`.
- **Compatible geometry owner:** PhysKit commit
  `d81febb811fbc4feb014530fcae6cf6d9ad9ead5`, whose ancestry provides the
  `DirectLatticeMetric` façade and whose dependency source advances to the exact
  Optimization revision above without changing PhysKit behavior.
- **Current mechanism:** KSD submits complete tensor-grid neighbor-overlap batches to
  `NumpyBatchedComplexUnitaryProcrustesSolver`. Optimization owns transformation
  selection, additive rank cutoffs, diagnostic deficient completions, squared-residual
  roundoff cutoffs, and fail-closed unique-transformation access. KSD owns reciprocal
  paths, axis and plaquette inventories, closure applicability, scientific gates,
  family identity, and evidence disposition.
- **Failure semantics:** one deficient neighbor link makes closure and plaquette channels
  inapplicable. KSD records the deficient-link count and stable reason rather than
  constructing zero-valued topology. Owner failures propagate; KSD does not substitute a
  local SVD or plausible default.
- **Geometry boundary:** `BandEquivalenceLocalityCase` requires an already validated
  PhysKit
  `DirectLatticeMetric`. KSD retains only campaign shell scaling and scientific
  aggregation. The v1 input document serializes the primitive-basis matrix by rows and
  declares that primitive vectors occupy columns; its strict schema requires a $2\times2$
  or $3\times3$ matrix matching the case dimension. No unpublished PhysKit wire identity
  is invented.
- **Completed software checks:** full-rank numerical parity, right-action orientation,
  additive-cutoff equality, rank-deficient fail-closed behavior, owner-failure
  propagation, roundoff evidence, strict schema relations, complete canonical-document
  request-to-result binding, campaign-owned SHA-256 wire identity, canonical derivation
  of refinement source identities, and independent verifier comparisons are covered by
  the bounded software-verification suite. The later owner cleanup enforces canonical
  constructors and validation boundaries; KSD consumes the defensive-copy construction
  paths. Centered transforms, bounded or separable evaluation, Parseval arithmetic, and
  twisted/ordinary Hermiticity now come directly from Numerics. KSD retains physical
  metric-shell selection, energy/rank normalization, interpolation/truncation/total
  error channels, thresholds, and scientific dispositions.
- **Independent review:** the initial review found incomplete request/result and
  refinement-source hash binding. Both findings were corrected; focused re-review
  reported `NO_BLOCKING_FINDINGS`. A later ownership correction removed serialization,
  schemas, filesystem writing, and plotting from the analysis package; campaign plots
  now consume typed diagnostics rather than decoded JSON. That post-review correction
  still requires fresh independent review.
- **Bounded resource check:** the 38-test locality suite completed in 4.95 seconds with
  a reported maximum resident set size of 146,604,032 bytes on the local review host.
  This is a development resource observation, not a cross-platform guarantee.
- **Remaining exit condition:** separately authorize regeneration of v1 retained
  schemas, results, refinements, and images. Passing these software checks does not
  qualify scientific evidence.

While either debt remains open, the affected calculations remain bounded
software-development mechanisms only. They cannot support qualified convergence,
retained evidence, or a scientific claim at their resolution scales.
