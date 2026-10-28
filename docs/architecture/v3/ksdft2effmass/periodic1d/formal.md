# Formal-method boundary

## Status

Formal methods may check exact finite propositions or soundness of bounded certificate
checkers for selected Periodic1D studies. They do not replace KSD calculation,
independent numerical verification, artifact retention, scientific assessment, or
publication review.

No current Formal promotion creates a KSD runtime request, result parser, retained
artifact, execution, or evidence package. The current runtime checked-certificate count
is zero. A future integration begins only after KSD freezes one native study contract and
one retained conforming package.

## Ownership

Formal owns:

- exact mathematical propositions;
- theorem implementations and proof checking;
- checker-soundness theorems; and
- the exact bounded conclusion discharged by a named theorem inventory.

KSD owns:

- the native family configuration and binary64 result wire;
- strict schemas and canonical serialization;
- the producer and byte-owning independent numerical verifier;
- the certificate request and result wires;
- directed-rounding or enclosure construction from numerical results;
- digest correlation, artifact retention, provenance, and package lifecycle; and
- the scientific applicability and interpretation of a checked proposition.

Formal must not invent KSD's runtime wire while proving a theorem. KSD must not present a
proof as a calculation result, evidence promotion, or scientific acceptance.

## Two-wire boundary

A checked study uses two layers rather than one universal Periodic1D document:

1. **Native family result wire.** A KSD-owned, family-specific typed record containing
   numerical values, units, finite spaces, conventions, diagnostics, and the exact bytes
   admitted by independent verification.
2. **Compact certificate export.** A separately versioned, proposition-specific request
   containing exact rational data or outward rational intervals derived from and bound
   to the native result digest.

The certificate export is not the native result and does not copy a binary64 decimal or
bit pattern into an exact-real field. An interval derived from binary64 requires a
documented directed-rounding or enclosure argument and an explicit error budget.
Canonical result bytes mean a byte-for-byte serialization contract; they do not make the
payload exact mathematical data.

## Study allocation

| Study | Formal may check | KSD must retain and verify numerically |
|---|---|---|
| Mathieu1D | Finite Fourier inversion, Parseval, exact support truncation and tail formulas, negation-closed Hermitian pairing, and later a source-faithful exact finite-matrix proposition after it is frozen. | Parent construction, band selection and isolation evidence, eigensolvers, conditioning, cutoff and mesh changes, fitting, withheld evaluation, and runtime bytes. |
| Compatible rank-one control | Scalar `U(1)` conjugation invariance and exact finite transform, reconstruction, and truncation formulas. | Coefficients, locality curves, fitting routes, tolerances, and all finite numerical cases. |
| Rank-two band equivalence | Exact finite Fourier and tail algebra, weighted Frobenius formulas, fixed-unitary equivariance, and a frozen exact or outward-rounded spectral certificate. | Numerical eigensystems, alignment search, hopping arrays, locality comparisons, mesh and cutoff behavior, and applicability of a supplied certificate. |
| Rank-two composite alignment | Sewing covariance, sampled Hermiticity and power formulas, exact weighted-loss expansions, and fixed-unitary Fourier equivariance. | Polar or Procrustes computation, conditioning failures, endpoint diagnostics, point-dependent alignment selection, and finite locality outcomes. |
| Confirmatory admissible sets | Exact loss geometry, restricted ellipse intersection or distance, sound rational or interval checking, and a bounded common-witness conclusion. | Field-derived scalars, conservative enclosures, full domain and alignment data, thresholds, native bytes, and independent numerical verification. |
| Scalar/direct demonstration | An exact witness and exact separation proposition when the construction is rational or algebraic. | Any binary64-derived example lacking an outward-rounded certificate and its bounded numerical interpretation. |
| Threshold sensitivity | A complete finite exact or interval decision table, dominance, feasibility, nondominated masks, and first/common first passage. | The post-hoc sweep, plot, threshold source, numerical values, and interpretation. |
| Higher rank | Arbitrary-rank fixed-unitary Frobenius or Fourier invariance and finite decision semantics already covered by frozen theorems. | Frame and projector construction, point-dependent alignment, sewing and conditioning, support completeness, and all runtime rank or dimension outcomes. |

Fixed-unitary equivariance does not cover a momentum-dependent `U(k)`: a point-dependent
transformation generally mixes Fourier modes. Rank-two proofs and tests do not transfer
to higher rank unless the theorem itself is rank-general and the KSD request satisfies
its hypotheses.

## Request obligations

A proposition-specific request records, as applicable:

- contract and owner-schema versions, study and execution identifiers, case identifier,
  decision identifier, and certificate identifier;
- requested theorem references and the exact bounded conclusion;
- KSD repository revision, dirty state, source and protocol digests, dependency lock,
  backend, precision, native result digest, and independent-verification digest;
- the complete ordered finite mesh, group, coordinate, support, and decision inventories;
- exact rational coordinates and weights or outward rational intervals, including
  normalization and positivity data;
- dimensions, ranks, shapes, array order, units, positive energy reference, basis,
  frame, subspace, and separate residual or error channels;
- alignment side, action, adjoint convention, fixed or point-dependent dependence,
  sewing, isometry, conditioning gates, and failure dispositions;
- Fourier sign and normalization, complete ordered modes, support membership,
  negation closure, tie rules, and retained or omitted summaries; and
- the certificate-production method and outward-rounding error budget linking every
  interval to the native result bytes.

Rational values use canonical integer numerators and positive integer denominators.
Intervals use two canonical rational endpoints. Decimal strings and binary64 bit patterns
are not accepted as exact real values.

## Checker result and fail-closed rules

The checker result records the request and certificate digests, native result digest,
KSD independent-verification digest and disposition, Formal repository and proof-tool
revisions, checker entry point, theorem references actually discharged, the exact bounded
conclusion, and one status per obligation:

- `accepted` — the obligation was proved under the supplied exact or enclosing data;
- `rejected` — a required proposition or precondition failed; or
- `unresolved` — available intervals overlap a decisive boundary.

The request and result reject unknown versions, unknown fields or enumerations, missing
mandatory data, noncanonical bytes, duplicate identifiers, digest mismatch, dirty
retained sources, incomplete mesh or support coverage, invalid weights, space or unit
mismatches, failed Hermiticity or sewing gates, split equal-radius ties, and failed
independent numerical verification.

Joint thresholds require one common candidate, support, and alignment. Combining minima
from different candidates, interpolating plot curves, or taking an unattainable envelope
does not produce an accepted joint decision. A finite table establishes only its declared
finite inventory; no continuum, uncertainty, global-optimum, or material claim follows.

## Required status vocabulary

Architecture, wires, and reports keep these statements distinct:

- `analytically exact`;
- `interval-certified`;
- `numerically verified within tolerance`; and
- `byte-for-byte equal`.

None implies the others without an explicit checked bridge.
