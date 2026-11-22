# Independent common-space rank verifier

This calculation-owned incubation package implements independent overlap reconstruction,
Gram-rank enclosures, conditional input-error bounds, deficient-direction controls,
complete 216-point composition, separate result artifacts, and subsequent producer
comparison. **The separately authorized [retained CSD1-V checkpoint](../../analysis/common-space-verification/)
now authenticates the complete real evidence bundle and passes independent all-point
verification and original-producer correlation under the adopted source/finite-input
contract.** This does not establish material validation or production qualification.
The separate [window-remedy diagnostic checkpoint](../../analysis/wannier-window-remedy/)
remains exploratory development evidence, not a substitute for that verification. Numerical records report bounds and findings, not workflow permissions or
scientific approval.

The arithmetic internal surface is `CommonSpaceGramRankEncloser`, its immutable
`CommonSpaceGramRankEnclosure` result, `GramEigenvalueInterval`, and the closed
`GramRankDisposition` / `GramRankFailure` enums. These are not supported reusable
`ksdft2effmass` library imports. Ownership of reusable numerical mechanisms must be
resolved before a separately reviewed migration.

Native composition additionally exports `CommonSpaceNativeInputContract`,
`CommonSpaceNativeInputLoader`, `CommonSpaceParsedNativeInputs`,
`CommonSpaceProviderModuleIdentity`, `CommonSpaceProviderBinding`,
`CommonSpaceTrialConvention`, `CommonSpaceNativeOverlapReconstruction`, and
`CommonSpaceReconstructedOverlap` as internal calculation surfaces. Conditional
uncertainty propagation additionally exports `CommonSpaceNativeRoundingModel`,
`CommonSpaceMatrixUncertainty`, `CommonSpaceOverlapUncertainty`,
`CommonSpaceNativePrecisionAssessment`, and `CommonSpaceNativeRankAssessment`.

## Native-byte correlation and independent reconstruction

The initialized loader consumes three immutable provider `Wannier90NativeArtifact`
records and separately declared expected identities. Roles are explicit fields, not
inferred from filenames, tuple position, or dimensions. It verifies the declared
Simulations distribution version and complete consumed source-module closure, including
the provider's native-artifact correlator. It then uses that shared correlator to
check the complete name/size/SHA-256 inventory **before any parser runs**. The caller
must obtain expected identities from reviewed source declarations; deriving them from
newly observed bytes is not production admission. Source-file hashes do not attest an
untampered process or replace complete environment provenance.

Parsing is exclusively through the maintained provider's AMN, gauge, and
rectangular disentanglement parsers. AMN uses the constructor-owned
`Wannier90TrialOrbitalOverlapParser(payload=...).parse()` boundary. No second native
parser, compatibility alias, guessed transpose, or fallback is implemented.

The native contract declares parent-band count, ten atomic-trial basis coordinates in
the frozen two-center order, the explicit eight-hybrid-plus-two-radial-s trial convention,
geometry and energy-reference labels, and the complete ordered fractional point list.
Gauge and disentanglement coordinates must equal that declared list exactly as numeric
triples; no tolerance, modulo reduction, origin shift, or grid inference occurs.
**AMN does not contain physical k-point coordinates.** Its index-to-point association
comes from the caller's cross-artifact declaration, not equal point counts. Geometry,
energy-reference, native projection semantics, and AMN order still require independent
CSD0 provenance. Equal dimensions do not authenticate a common parent-band or gauge
state space. These native receipts alone do not establish the complete CSD0 ledger.
Parsing also does not establish gauge unitarity or disentanglement isometry: their
finite-precision controls remain separate, and the raw overlap is never silently
normalized or completed. The supported convention is spinless scalar-relativistic non-SOC. Native overlaps and
coordinates are dimensionless, and no Hamiltonian energy subtraction takes place.

After this shared parsed-record boundary, the separate reconstructor derives the
atomic transformation coefficients from the four declared hybrid directions at each
center and the two additional radial s channels. It checks exact unitarity of T, then
forms `W = U_dis U`, `C = A T†`, and `B = W† C` with exact rational complex products.
All native matrices retain their provider-defined logical orientation. The reconstructed
record exposes exact rational real/imaginary components with explicit built-in integer
indices, preserving terms that a binary64 B intermediate would round away.

`CommonSpaceReconstructedOverlap.enclose_rank(rank_threshold=...)` feeds this exact B
straight into the Gram certificate. Thus B reconstruction and Gram formation have zero
arithmetic rounding error **relative to the supplied parsed binary64 matrices and the
declared exact T**. Decimal-to-binary parsing error and native-format uncertainty remain
separate obligations, quantified only under the explicit conditional models below.
A source or correlation failure raises before any product; arithmetic inconclusiveness
never advances the scientific sequence.

## Conditional native and parsing-error propagation

`CommonSpaceNativeRoundingModel` declares a nonnegative exact absolute error bound per
real/imaginary component for each of AMN, gauge, and disentanglement matrices. Its
`from_nearest_decimal_places` constructor assumes nearest rounding to an **absolute**
decimal step: the error is exactly `1/(2*10**places)`. This is not mantissa-digit
rounding in scientific notation, inferred precision, or evidence that a formatter
honors a declaration. There are no default precision counts. These assumptions must
be admitted by the complete CSD0 provenance contract before retained use.

For each finite parsed binary64 real component `f`, correctly rounded decimal-to-binary
conversion implies an absolute parsing-error bound `ulp(f)/2`. The implementation
converts the ULP to an exact Fraction **before** halving, including zero/subnormals and
the largest finite binary64 values. It does not parse native text again or claim a
measured conversion error. Correctly rounded binary64 conversion is an explicit model
assumption of this layer; source fingerprints are not process/rounding-mode attestation.

For a parsed rectangular matrix `X`, nominal spectral norm is bounded using the exact
Gram matrix: `m_X >= sqrt(b(X† X))`. Component parsing errors are summed in squares to
bound the Frobenius norm `p_X`; uniform native component bound `h_X` gives
`n_X >= sqrt(2 * rows * columns) * h_X`. Frobenius norms bound spectral norms. Every
square-root upper bound uses exact integers: for `q = n/d >= 0`,
`ceil(sqrt(n*d))/d` is at least `sqrt(q)`. No chosen arithmetic tolerance or underflowing
floating square root is used. Parsed gauge unitarity or disentanglement isometry is
**not** assumed when computing `m_X`.

For `B = U† U_dis† A T†`, exact `T` is unitary. Let the three parsed norm bounds be
`m_X`, the parsing perturbation bounds `p_X`, and native rounding perturbation bounds
`n_X`, for `X` in `(U, U_dis, A)`. Submultiplicativity and the complete product expansion
give

```math
\epsilon_{\mathrm{parse}}=
 \prod_X(m_X+p_X)-\prod_Xm_X,
\qquad
\epsilon_{\mathrm{native}}=
 \prod_X(m_X+p_X+n_X)-\prod_X(m_X+p_X),
```

and their sum bounds the overlap perturbation relative to the exact reconstructed
parsed-input B. The second term uses `m_X+p_X` to bound the decimal-input matrices;
thus **all native/parse mixed terms are retained**. Adding separate native-only and
parse-only expansions would miss those terms. These are conditional deterministic
bounds, not probabilistic confidence intervals or parent-model/reduction errors.

`CommonSpaceNativePrecisionAssessment` keeps the raw Gram arithmetic certificate and
these overlap-level perturbation bounds separate. Overlap errors bound singular-value
perturbations; the Gram spectral error bounds eigenvalues (squared singular values).
They are not added as though they were the same error quantity.

The caller supplies the exact prospectively frozen singular-value threshold. The
assessment checks whether the combined native-plus-parsing bound is covered by it,
then uses the **unchanged** raw-overlap rank gate. It neither shifts the threshold nor
widens the raw spectrum by that threshold (which would double-count its purpose).
An uncovered conservative bound means inconclusiveness, not proof that the actual
error exceeds the threshold. Covered uncertainty cannot override an inconclusive Gram
certificate. Neither outcome passes CSD0, CSD1-V, or scientific acceptance.

## Standalone finite-overlap inputs, model, and limits

The initialized action owns a nonempty square dimensionless overlap represented as
nested built-in tuples of **finite built-in complex numbers**. Integers, real scalars,
NumPy scalars, strings, booleans, lists, and nonfinite components are not admitted at
this boundary. Conversion from provider arrays must be explicit in future independent
composition. The nonnegative rank threshold is an exact built-in `Fraction`; it must
be supplied from a prospectively declared contract, not selected from observed output.

Each complex component is embedded as its exact binary64 rational value. The result
bounds the mathematical spectrum of **that supplied finite matrix**. It does not bound
native decimal uncertainty, parsing error, overlap-reconstruction error, parent-model
error, or reduction error. These remain separate obligations. In particular, a future
verifier must independently reconstruct its overlap after authenticated provider parsing;
it must never feed a producer-generated overlap into this action as verification input.

Gram formation and the a posteriori certificate use exact rational complex arithmetic.
There is no rounding error in those operations relative to this input model. The
native-composition path also retains exact reconstruction products, rather than first
rounding them through the standalone binary64-overlap input boundary. NumPy's
Hermitian eigensolver supplies candidates only; no LAPACK error estimate, fixed epsilon
multiplier, or scientific comparison tolerance is assumed. An unrepresentable floating
Gram matrix, eigensolver failure, invalid candidate, or unresolved interval yields a
numerically inconclusive result. Floating underflow is permitted in the candidate
matrix because the certificate retains the exact Gram matrix. Resource exhaustion
propagates as an error and cannot produce a resolved result.

## Derived arithmetic enclosure

For the supplied finite matrix `B`, form `G = B† B` exactly. Let `V` and the real diagonal
`D` be finite binary64 eigensolver candidates, embedded exactly as rationals. Define

```math
F=V^\dagger V-I,\qquad E=V^\dagger G V-D.
```

For an exact Hermitian matrix `H`, use the rational bound

```math
b(H)=\max_i\sum_j\bigl(|\operatorname{Re}H_{ij}|+
                              |\operatorname{Im}H_{ij}|\bigr)
      \geq \|H\|_2.
```

This follows from the induced infinity norm and the equality of spectral radius and
spectral norm for Hermitian matrices. The implementation checks exact Hermiticity
before using this bound; a violated software invariant raises an error, not a rank.
Put `d = b(F)`, `e = b(E)`, and `m = b(G)`.
When `d >= 1`, this construction cannot certify an invertible eigenvector frame and
stops inconclusively. For `0 <= d < 1`, the polar factor
`Q = V (V† V)^(-1/2)` is unitary. Its distance from the candidate satisfies

```math
\|V-Q\|_2 \leq \frac{d}{1+\sqrt{1-d}}
                  \leq \frac{d}{2-d},\qquad
\|V\|_2\leq \sqrt{1+d}\leq 1+d.
```

Therefore

```math
\|Q^\dagger GQ-D\|_2
\leq e + m\frac{d}{2-d}(2+d)=:\epsilon.
```

All quantities on the right are exact rationals. Since `Q† G Q` has the spectrum of
`G`, the ordered Hermitian eigenvalue perturbation bound places each ordered true
Gram eigenvalue inside `[D_jj - epsilon, D_jj + epsilon]`. The candidate eigenvalues
and corresponding vector columns are sorted together before certification. Eigenpair
residual norms are reported with independent exact upper bounds

```math
\|Gv_j-D_{jj}v_j\|_2
\leq\sum_i (|\operatorname{Re}r_{ij}|+|\operatorname{Im}r_{ij}|).
```

Hermiticity defect is zero for the exactly formed Gram matrix. Orthonormality defect,
residual bounds, and the spectral error bound remain available as diagnostics; none
is silently folded into the native-decimal threshold.

## Rank classification without a rounded square root

For nonnegative threshold `t`, `sigma_j > t` is equivalent to `lambda_j > t²`.
Comparisons therefore use exact rational squared quantities, avoiding a second rounding
step in a displayed square root. A materially negative eigenvalue interval (`upper < 0`)
cannot be clamped or classified successfully. If an interval includes zero, its
nonnegative lower endpoint may be set to zero using the known positive-semidefiniteness
of `G`, without discarding its upper uncertainty endpoint.

- `lower > t²`: definitely above the gate.
- `upper <= t²`: definitely not above the gate, including exact equality.
- Otherwise: unresolved contribution; the complete rank is inconclusive.

The result reports lower and upper possible ranks, and a resolved rank only when they
agree and there is no arithmetic failure. Resolving a deficient rank is not passing a
full-rank gate, and neither disposition passes CSD1-V.

## Reviewed source declarations and producer prerequisites

`CommonSpaceSourceAdmission` correlates a **caller-supplied reviewed declaration** with
immutable parsed inputs, precision assumptions, and explicit band/gauge identities.
It requires 20 parent bands, ten retained coordinates, and 216 unique points beginning
at Gamma with six declared coordinate values per axis. These cardinalities establish
Cartesian coverage; physical spacings and native coordinate conventions still require
review. No coordinate snapping, inferred rounding precision, or tolerance is used.

The closed `CommonSpaceEvidenceRole` inventory covers the request, historical full-source,
full-support and blocked-alignment records, controlling protocol, reviewed state
assertions, producer completion declaration, and two prerequisite artifacts: full-grid
reconstruction and symmetry-related point inventory. Higher arithmetic precision is not
an unconditional admission prerequisite.
Simulations' existing artifact correlator authenticates all evidence bytes before this
layer decodes any assertion. Producer prerequisite bytes are hashed but are **not parsed
for numerical values** before independent computation. The completion declaration binds
both prerequisite identities and the reviewed source assertion. Producing a matching
declaration is not scientific substantiation, authorship verification, or review.

Expected identities, semantic associations, completion judgments, and review references
must originate outside this verifier from an admitted review process. In particular,
`assertion_payload()` describes the expected assertion; generating its bytes cannot
review one's own sources. The verifier neither checks the legacy records' entire
scientific content nor implements the full upstream path/root admission workflow.
Native data enter this API as bytes/parsed records, not filesystem paths. A client must
complete upstream source/path review before shared parsing; this API does not retroactively
establish that review. There is no second generic provenance ledger or native parser.

Synthetic fixtures explicitly use `CommonSpaceReviewScope.synthetic`; their prerequisite
placeholders and completion declarations are test data, not completed silicon work.
Enum members use lowercase names and explicit `.to_wire()` / `.from_wire()` vocabulary.
Historical S30/S105/S110 names remain provenance identifiers, not numerical outcomes.

## Conditional arithmetic-precision escalation

The controlling protocol's prospective amendment retains source authentication,
independent reconstruction, and justified arithmetic/native-input bounds. If those bounds
are decisive and the independent routes agree, no higher-precision run or completion
artifact is required. Accordingly, the admission inventory has no routine precision-
sensitivity artifact or completion flag. This removes an unconditional software gate,
not an error bound or a scientific acceptance requirement.

Arithmetic ambiguity or a plausibly arithmetic independent-route disagreement requires
a bounded follow-up before progression, after checking source conventions and software
errors. It may target affected points; no blanket 128/256-bit campaign is required.
The same parsed inputs, exact transformation, native-error model, and frozen threshold
must be retained. Extra arithmetic digits cannot restore source digits or resolve
uncertain physical associations. Native-input-limited ambiguity needs source review,
not automatic precision escalation. Existing inconclusive/mismatch outcomes still stop
progression; there is no bypass or automatic high-precision execution here.

## Isolated deficient-direction bounds

`CommonSpaceDeficientDirectionAnalysis` uses the independently retained minimum-vector
candidate, not a producer vector. Normalize it exactly by its squared rational norm.
For the exact parsed-input Gram matrix, let `mu` be its Rayleigh quotient and `r` its
normalized residual norm. If the certified second eigenvalue lower endpoint `l1` exceeds
`mu`, projection onto all higher eigenvectors gives

```math
\|P_{\mathrm{candidate}}-P_{\min}\|_2
\leq r/(l_1-\mu).
```

An exact rational upper bound on the squared ratio supplies the arithmetic projector
bound. Lack of separation or a bound reaching one is unresolved, not an enclosed
orbital diagnosis. This control is separate from certifying the complete eigenframe.

For conditional input perturbation `e = ||Delta B||` bounded by the propagated model,
let `s0` upper-bound the minimum singular value and `s1` lower-bound the next one.
Require `s1-s0 > 2e`. For a normalized minimum right singular vector `u` of `B`,
`||(B+Delta B)u|| <= s0+e`; all higher right singular directions of the perturbed
matrix have singular values at least `s1-e`. Hence

```math
\|P_{\min}(B)-P_{\min}(B+\Delta B)\|_2
\leq (s_0+e)/(s_1-e).
```

When `e=0`, the input contribution is exactly zero. Square-root endpoints use exact
integer floor/ceiling bounds. This singular-gap argument avoids unnecessarily squaring
the input-gap conditioning; it does not adjust the frozen rank threshold. Adding the
arithmetic and input projector bounds controls each orbital probability and each
orthogonal coordinate-group probability. Groups are `s=(0,5)`,
`p=(1,2,3,6,7,8)`, and `s-star=(4,9)`. A total bound reaching one remains inconclusive.
Multiple threshold-deficient directions do not manufacture a unique orbital diagnosis.

`CommonSpaceUnitaryInvariance` applies one fixed exact rational unitary retained-basis
change, checks exact Gram equality, and separately encloses the rotated spectrum.
This is a finite numerical control, not a fitted alignment or a symmetry attribution.

## Complete computation, persistence, and later comparison

The calculation-local facade exports the typed source records and roles above;
`CommonSpaceDeficientDirection`, `CommonSpaceWeightInterval`, their analysis and outcome;
`CommonSpacePointVerification`, `CommonSpaceIndependentGridResult`,
`CommonSpaceIndependentVerification`, and `CommonSpaceVerificationOutcome`; and
`CommonSpaceProducerPoint`, `CommonSpaceProducerReference`,
`CommonSpaceProducerCorrelation`, `CommonSpaceProducerResultAdapter`,
`CommonSpaceIndependentResultSerializer`, `CommonSpaceVerificationRun`, and
`CommonSpaceProducerCorrelationRun`. These remain internal incubation imports, not
supported reusable library APIs. Nontrivial behavior stays with these domain actions;
the JSON facade only handles this verifier's wire representation.

`CommonSpaceIndependentVerification` completes every declared point before accepting a
numerical comparison reference. Rank ambiguity, uncovered input uncertainty, eigensolver
failure, direction-gap failure, and failed unitary controls remain explicit. No point
is dropped. `CommonSpaceVerificationRun` rejects existing output roots, including dangling
symlinks, before verifier admission or arithmetic (shared upstream parsing has already
occurred). It exclusively creates `independent-verification.json` and a `manifest.json`
with its byte identity and verifier source-file hashes. It serializes interval endpoints
as reduced `[hex(numerator), hex(denominator)]` string pairs, avoiding floating conversion
and Python's decimal integer-string limits. Integers, booleans, and numeric strings are
not interchangeable at numeric APIs. Nonfinite JSON, duplicate keys, and noncanonical
rational wire values are rejected. Exact integers have no fixed-width overflow; resource
and storage failures raise rather than producing a successful result.

Only **after** that independent result exists may `CommonSpaceProducerResultAdapter`
decode the original producer result held in the reviewed evidence inventory. It
reauthenticates all evidence bytes before reading producer numerical values. No separately
normalized substitute, legacy fallback, filename-based source selection, producer helper,
or producer serializer is used. The earlier draft normalized-reference wire format is
not admitted. The internal `CommonSpaceProducerReference` is a typed numerical view,
not a second accepted artifact format.

The adapter consumes the campaign producer's actual version-one JSON contract. It checks
the request identity and identifier; all seven source identities against both the reviewed
inventory and the authenticated request; consumed provider version and module fingerprints;
exact dimensions, basis, geometry label, spin, energy unit/reference; declared decimal
precision against the admitted error model; and the unchanged frozen threshold. Every
point index and native coordinate must match the complete declared order. Every deficient
point must provide all ten atomic weights and all three reported group weights; full-rank
points must provide empty direction arrays. Deficient-point and Gamma duplicate views
must agree with the complete table. Historical `CSD0`/`CSD1` names are consumed only as
literal fields of that existing producer wire contract, not propagated as permission flags.
Metadata paths are not followed or reauthorized; their explicit filenames and byte
identities are correlated, while source/path review remains upstream.

Spectrum order in the typed numerical view is maximum, next-to-minimum, minimum.
Integer numeric values become exact Fractions; finite JSON floats become exact Fractions
of their parsed binary64 values. Booleans, numeric strings, absent weights, and unknown
schema versions are rejected. The adapter does not recompute producer group weights
from atomic weights: reported groups are separately compared with independently derived
group intervals. Comparison uses derived spectral and projector intervals, not an
invented tolerance. Source mismatches raise; numerical mismatches are reported.
`CommonSpaceProducerCorrelationRun` checks the stored independent bytes and matching
completion manifest before adaptation, then exclusively writes a separate
`producer-correlation.json` binding both independent artifacts and the original producer
result. It never revises independence or turns inconclusiveness into agreement.

For an explicitly linked source association, descriptive legacy request fields are
compared to the exact authenticated request; they are not equated with content-addressed
geometry/energy IDs in different declaration fields. The adapter requires matching
review scope, source-assertion identity, geometry ID and complete native provider binding.
The assertion already binds the effective IDs and the request digest. Retained sources
cannot bypass that link; unlinked descriptions are not aliases, and numeric/state/unit/
threshold checks are unchanged. The retained checkpoint preserves the first metadata-
comparison failure and the byte-identical numerical replay after this focused fix.

Adapting a complete reconstruction table does **not** declare the overall producer
scientifically complete. Its rank-reconstruction subset remains explicit. Reviewed,
source-bound reconstruction and symmetry-inventory evidence must separately satisfy
source admission; neither producer execution success nor a matching comparison invents
those prerequisites. Higher arithmetic precision is required only under the conditional
policy above, not before every independently checked reconstruction. The positive end-to-end test runs the actual producer action on synthetic
native bytes, deliberately mocks only upstream legacy scientific-source semantics, and
uses explicitly synthetic prerequisite declarations. It is not retained evidence.
JSON readback supports artifact inspection and exact rational decoding, not
reconstruction of a complete typed independent result without its source records. File
writes are exclusive, not transactional or hardened against a hostile concurrent
filesystem. A storage error may leave a partial output root; it must not be treated as
a complete record or silently overwritten. Source hashes identify files, not an
untampered running process.

## Remaining scientific and integration work

The [retained producer checkpoint](../../analysis/common-space-producer/) now binds the
reviewed/adopted full-S30 source identification and supplies the original-schema 216-point
producer result, exhaustive geometric construction-index inventory and actual completion
receipt. Its index relations are not electronic symmetry actions or exact native physical-k
identities. The subsequent retained CSD1-V checkpoint completed verifier-bundle
authentication and numerical verification/correlation at all 216 points, retaining two
resolved rank-nine points under the unchanged gate. CSD2 electronic symmetry actions
remain unestablished and unrun. Higher-precision arithmetic remains unimplemented and
was not triggered by the decisive bounds/agreement; it is not a blanket prerequisite. The controlling protocol
and its unretained development-request digest binding were prospectively amended for this
policy; historical protocols, retained evidence, and dependency pins are unchanged. Protocol identifiers such as CSD0/CSD1/CSD1-V remain historical cross-references
in the controlling protocol, not new numerical-record permission fields.

Only synthetic numerical/software tests may exercise this package without separate
retained-analysis authorization. They check the implemented finite-matrix contract,
not silicon rank results, material validation, or production qualification.
