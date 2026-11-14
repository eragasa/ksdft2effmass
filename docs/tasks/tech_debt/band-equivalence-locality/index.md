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
  `python/src/ksdft2effmass/band_equivalence_hopping_locality/alignment.py`,
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
  `7120b735c7e3e450aa8924780a71deb59d812632`, whose ancestry provides the
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
- **Geometry boundary:** `BandEquivalenceHoppingLocalityCase` requires an already validated
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

### `TD-BEL-003`: rank-N non-onsite summary subtraction

- **Disposition:** deferred numerical robustness debt.
- **Current owners:** the periodic-2D and periodic-3D rank-N
  `BandEquivalenceHoppingLocalityCaseAnalyzer`,
  `BandEquivalenceHoppingLocalityFourierReferenceAnalyzer`, and
  `BandEquivalenceHoppingLocalityLocalitySummary` specializations under
  `python/src/ksdft2effmass/periodic2d/rankN/` and
  `python/src/ksdft2effmass/periodic3d/rankN/`.
- **Current mechanism:** the producer calculates normalized non-onsite power as
  `max(0.0, total_power - onsite_power)` after total and onsite powers have been
  rounded separately in binary64. The Fourier reference repeats the same subtraction,
  so agreement of those two routes does not independently exclude a subtraction-induced
  false zero.
- **Bounded current impact:** the selected analytic baseline has retained energies of
  magnitude at most `0.7` in the declared unit scale. Unitary gauge action preserves
  Frobenius power, so normalized total power is at most approximately `0.49`. Within
  this bounded family, the subtraction can hide only roundoff-scale power. The summary
  does not drive support selection: shell decisions use direct
  `normalized_power_beyond_shell(...)` sums and reconstruction-error channels.
- **Interpretation limit:** a serialized zero non-onsite summary is not a certificate
  that every nonzero-displacement hopping block vanishes exactly. No current result may
  use that scalar alone to claim a strictly onsite model.
- **Required replacement:** classify the complete hopping inventory into disjoint,
  exhaustive zero- and nonzero-displacement sets; sum each set directly with stable
  binary64 summation; and make the independent route reconstruct those partitions
  without calling or repeating the producer formula. Total-versus-partition checking
  must preserve the existing `1.0e-12` absolute floor while admitting only a bounded
  representational-ULP allowance and no broad relative tolerance.
- **Required tests:** a high-dynamic-range synthetic inventory retaining a representable
  non-onsite contribution, exact zero and ordinary baseline cases, producer/reference
  agreement through independent partition sums, tampered partition rejection, and
  confirmation that support selections remain unchanged.
- **Revisit condition:** resolve before any admitted scale expansion, retained production
  execution, or categorical strictly-onsite claim. Resolving this debt does not itself
  authorize a calculation or establish scientific validation.

While any debt remains open, the affected calculations remain bounded
software-development mechanisms only. They cannot support qualified convergence,
retained evidence, or a scientific claim at their resolution scales.
