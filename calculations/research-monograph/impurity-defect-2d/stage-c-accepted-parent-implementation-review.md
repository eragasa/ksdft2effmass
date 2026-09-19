# Adversarial review of the execution-free accepted-parent Stage C implementation

## Review boundary

This review covers the HC13-authorized adversarial plan, authored compact
fixture, parent-contract runner, independent verifier, deterministic SVG
plotter, closed schema, maintained tests, and synchronized documentation. It
does not review an accepted-parent result because the new path did not read the
accepted periodic, Stage A, or Stage B contents and no accepted-parent execution
was authorized.

Finding dispositions are `MUST_FIX`, `HUMAN_DECISION_REQUIRED`,
`SAFE_TO_DEFER`, and `NO_ACTION_REQUIRED`. Technical outcome is separate from
human acceptance and execution authority.

## Adversarial questions

The review attacked route independence, gauge-dressed attacks, exact adopted-
design identity, hidden expected-class use, hopping criteria, basis support,
anisotropic preprocessing state, normal-equation leakage, schedule process
separation, adverse-control tautology, nonfinite serialization, output
replacement, schema closure, and claim-boundary wording.

## Findings and corrections

### `MUST_FIX` — Route B attacked candidate did not initially bridge

The first implementation applied the same coordinate-attack matrix directly in
both gauges. Parent, defect, and recovered matrices bridged, but the attacked
candidate differed by up to $7.577\times10^{-2}E_G$. This violated the adopted
attacked-candidate bridge.

**Correction:** Route B now independently constructs the gauge-dressed attack
$WGW^\dagger$ from its twist lift. Parent, defect, full, attacked, and recovered
bridge maxima are retained separately. The largest authored bridge residual is
$2.225\times10^{-16}E_G$.

**Disposition:** corrected and verified.

### `MUST_FIX` — Independent verifier initially hard-coded the wrong generic twist

The first verifier draft used the execution-free Stage C toy twist rather than
decoding the adopted parent-design twist. Near-zero invariant metrics concealed
the mistake.

**Correction:** the verifier now decodes both twists directly from the exact
human-adopted design and independently rebuilds every route record. Its maximum
retained-versus-independent scalar difference is
$1.922\times10^{-15}E_G$.

**Disposition:** corrected and verified.

### `MUST_FIX` — Initial schema used the wrong nonlocal defect identity

The first closed-schema draft named the authored nonlocal plant differently
from the adopted design, causing 104 schema errors.

**Correction:** the schema uses the exact design identity
`finite_range_diagonal_nonlocal`. A complete 2,205,921-byte result validates
without an error.

**Disposition:** corrected and verified.

### `MUST_FIX` — Initial aggregation omitted hopping-symmetry and selected-fit criteria

The first result retained hopping and fit diagnostics but did not separately
apply all adopted hopping, fit, exterior, and exact-support criteria. Its support
digest represented only the residual and its core-exterior value was a constant.

**Correction:** the runner now validates the isotropic $D_4$ inventory and the
pretruncation, compact, and swapped anisotropic $D_2$ inventories; separately
reports isotropic, anisotropic, and axis-swap covariance; computes selected-fit
maximum, Frobenius, exterior, and core-exterior diagnostics; and retains basis,
target, fitted, and residual support identities plus exact-support disposition.
All 17 named aggregate criteria pass. The largest hopping-symmetry residual is
$1.626\times10^{-16}E_G$.

**Disposition:** corrected and independently reconstructed.

### `MUST_FIX` — Route implementations and provenance adverse control were initially too coupled

The first draft selected uniform-link versus seam phases inside one construction
loop, and the route-provenance adverse status was a literal record. That was too
weak for the adopted independent-constructor claim.

**Correction:** uniform parent, seam parent, uniform defect, and seam defect are
separate construction methods. Every live route passes a provenance gate using
compact input as its source. The adverse control supplies a Route A matrix as a
mutated Route B source and obtains
`DEFECT_2D.ROUTE_INDEPENDENCE_VIOLATION` from the same gate.

**Disposition:** corrected and behaviorally verified.

### `MUST_FIX` — Exact adopted-design and executable provenance were not initially fail-closed

Field-level parsing alone allowed a structurally plausible mutation of the
human-adopted design. The first result also omitted executable identity.

**Correction:** the deserializer requires the exact adopted design SHA-256
`e5103eb95300095d46280fce5539b3e0a168c8c7b41f2f2473d1b3d2d8a48706`.
The result retains design, fixture, and runner identities plus Python and NumPy
versions. The independent verifier checks design, fixture, and runner identities.
A maintained test mutates the model-class order and confirms rejection before
output creation. JSON serialization uses `allow_nan=False` and refuses overwrite.

**Disposition:** corrected and verified.

## Revisit conditions

### `SAFE_TO_DEFER` — Accepted-parent adapter and execution

The current command intentionally exposes only
`AuthoredParentFixtureDeserializer`, which rejects any fixture claiming
accepted-parent status. It therefore cannot execute the accepted parent under
HC13. A later execution boundary must bind the exact accepted artifacts, runner,
schema, output path, repository, machine, and resource envelope before any new
adapter reads accepted contents. This is the intended authority boundary rather
than an implementation defect.

### `SAFE_TO_DEFER` — Spectral and physical-observable claims

Spectral, bound-state, wavefunction, and physical-observable conclusions remain
outside Stage C acceptance. The current operator, model-class, locality, route,
and schedule checks do not support those claims.

### `HUMAN_DECISION_REQUIRED`

None within the HC13 implementation scope. The technical review did not provide
human acceptance; the later verbatim human response ``1`` resolved HC14 and
human-accepted the exact execution-free implementation boundary.

## Verified authored behavior

- dimension 64;
- two distinct fresh spawned schedule processes;
- 225 anisotropic pretruncation coefficients reconstructed independently per
  schedule and 61 retained compact coefficients;
- 208 route evaluations, 104 bridges, 1,040 model fits, and 104 schedule
  comparisons;
- exact clean schedule differences;
- all selected model classes agree with the hidden post-selection expectations;
- invalid anisotropic $D_4$ and omitted-swapped-parent controls each produce
  $6.0\times10^{-3}E_G$, above the $10^{-3}E_G$ floors;
- independent inverse-Fourier, direct-matrix, bridge, and QR reconstruction
  passes without importing the runner or consuming runner matrices/caches;
- deterministic JSON and SVG reproduction and overwrite refusal pass; and
- a measured authored run completes in 1.56 seconds, uses 99,041,280 bytes
  maximum resident set size, and writes 2,205,921 bytes, within the proposed
  envelope.

These are synthetic software-verification observations, not accepted-parent or
material results.

## Technical outcome

`NO_BLOCKING_FINDINGS`

All `MUST_FIX` findings were corrected and rechecked. The implementation is
technically ready for separate human review of this exact execution-free
boundary. This outcome does not authorize accepted-parent reads, execution,
commit, push, Stage D/E work, scientific validation, publication, or release.
