# Adversarial review of the proposed multi-route Stage B design

**Subsequent disposition:** the human response ``recommendation authorized``
adopted this design for execution-free implementation and resolved HC04. The
review below is retained in its pre-decision form; the implementation is assessed
separately in `stage-b-implementation-review.md`.

## Review scope

This review attacks only the execution-free proposal in
`stage-b-multiroute-design.json` and `stage-b-multiroute-protocol.md`. It applies
devil's-advocate, assumption-busting, red-team, defensive-design, and
trust-but-verify perspectives to finite-matrix gauge ownership, route
independence, schedule order, blind identifiability, criteria, provenance, and
authority. It does not inspect or execute the accepted scalar parent and does
not authorize implementation or calculation execution.

## Findings

### Route agreement could be tautological

**Disposition: NO_ACTION_REQUIRED**

Problem: A runner could construct the seam route by applying the declared gauge
to the uniform route, guaranteeing agreement without testing two constructors.

Evidence: The proposal now requires direct retained-hop construction in both
routes and forbids route-to-route matrix generation. The future verifier uses a
shifted-dispersion/Fourier route for Route A and independently assembled seam
shift factors for Route B.

Consequence: If this prohibition were absent, the bridge would test only its own
implementation.

Next action: Retain implementation mutations that replace Route B construction
with a transformed Route A matrix and require them to fail before execution
authorization.

### Calling the lift bridge a third route would overstate independence

**Disposition: NO_ACTION_REQUIRED**

Problem: The explicit-lift option reuses the two matrix representations and is
not a third independent numerical estimate.

Evidence: The proposal names it `gauge_bridge`, excludes route voting, and
requires two constructors plus one deterministic equivalence relation.

Consequence: Treating it as a third vote could make two correlated calculations
appear to outvote one failure.

Next action: Keep all result and report language at “two matrix routes and one
bridge.”

### Gauge orientation and row/column conventions are easy to reverse

**Disposition: NO_ACTION_REQUIRED**

Problem: Replacing $D$ by $D^\dagger$, changing source/target orientation, or
reversing $W_M$ can preserve unitarity while invalidating operator covariance.

Evidence: The proposal fixes matrix rows as sources, defines
$x+R=y+Nq$, states $H_B=D H_A D^\dagger$, and freezes
$W_M=D(M\phi)U_MD(\phi)^\dagger$. Required toy mutations reverse each choice.

Consequence: A sign error could produce internally consistent but physically
different matrices.

Next action: Require one-hop analytical phase oracles and every frozen mutation
before any execution request.

### Route order can expose hidden mutable state

**Disposition: NO_ACTION_REQUIRED**

Problem: Dismissing route order without testing could hide a cache, mutable
twist representative, adaptive tolerance, or favorable-route dependency.

Evidence: The revised proposal runs A-then-B and B-then-A in separate fresh
processes. A clean nearest-neighbour toy gave zero route-local schedule
differences. An intentionally invalid shared-twist-cache mutation produced a
Route A schedule difference and bridge mismatch of approximately $0.7654$ for
unit toy hopping, demonstrating discrimination.

Consequence: Without both schedules, a result could depend on which route first
initialized shared state.

Next action: Freeze both schedules, canonicalize serialization independently of
execution order, retain any clean schedule mismatch as failure, and forbid
post-hoc schedule selection.

### Assuming an order effect would manufacture a conclusion

**Disposition: NO_ACTION_REQUIRED**

Problem: “Assume order matters” could be misused to label an intentionally
stateful software defect as physical gauge dependence.

Evidence: The proposal treats order as a falsification factor. The clean toy did
not show an effect; only the declared adverse mutation did. The interpretation
explicitly classifies a future clean effect as software or protocol failure.

Consequence: Conflating a schedule effect with physics would create an
unsupported scientific claim.

Next action: Preserve the distinction between expected clean invariance,
discriminating adverse behavior, and any observed accepted-parent failure.

### Equal blind counts can hide different ambiguity sets

**Disposition: NO_ACTION_REQUIRED**

Problem: Both routes could report 512 and 64 while retaining different map
identities or orders.

Evidence: Cross-route and cross-schedule criteria compare the complete ordered
operation/translation identities, issue codes, null payloads, and median shifts.

Consequence: Count-only evidence could conceal a twist-compatibility or map-order
error.

Next action: Mutate one identity while preserving counts and require rejection.

### Modulo-one metadata can conceal the wrong lift

**Disposition: NO_ACTION_REQUIRED**

Problem: Route B matrices are periodic in reduced metadata, but its decorated
symmetry and bridge require the unreduced lift.

Evidence: Every record retains the lift, reduced value, and exact integer pair;
missing lift metadata is a stop.

Consequence: Reconstructing a convenient lift after seeing a favorable match
would make the bridge non-auditable.

Next action: Bind all lifts in any future authorization and mutate the integer
pair in behavioral tests.

### Spectral agreement is too weak

**Disposition: NO_ACTION_REQUIRED**

Problem: Gauge-related and incorrectly permuted matrices may remain isospectral.

Evidence: The proposal makes maximum-entry and Frobenius operator bridge defects
primary and keeps eigenvalue differences supplementary.

Consequence: A spectrum-only comparison would miss support, phase, and
covariance errors.

Next action: Do not weaken operator criteria when adding order comparisons.

### A disconnected phase graph invalidates blind phase synchronization

**Disposition: NO_ACTION_REQUIRED**

Problem: Fixing one phase at $(0,0)$ determines all phases only when the visible
pristine hopping graph is connected.

Evidence: Connectivity is now an explicit prerequisite with structured stop
`DEFECT_2D.PHASE_GRAPH_DISCONNECTED`; an authored disconnected toy is required.

Consequence: An implementation could otherwise fill unconstrained phases and
create artificial minima or ties.

Next action: Verify connectivity independently before candidate ranking.

### Doubling schedules expands the envelope

**Disposition: SAFE_TO_DEFER**

Problem: Two schedules double route-local and blind-candidate work relative to a
single multi-route schedule.

Evidence: The proposal now bounds 72 known-map route evaluations, 36 bridge
records, 2,304 blind candidates, 600 seconds, 2 GiB, and 30 MiB.

Consequence: These remain planning estimates and could be either excessive or
insufficient.

Next action: Reassess runtime, peak memory, and retained size using only authored
toy coefficients before any execution-authorization request.

### The proposal is not an existing checkpoint option

**Disposition: HUMAN_DECISION_REQUIRED**

Problem: The pending checkpoint offers three single-convention choices and a
stop choice; it does not define this two-route, two-schedule replacement.

Evidence: `RM-IMPURITY-DEFECT-2D-STAGE-B-TWIST-GAUGE-HC04` remains pending, and
the proposal explicitly declares itself non-authoritative.

Consequence: Implementing the proposal now would broaden the frozen case,
verification, resource, and serialization contracts without a normalized human
decision.

Next action: If the operator wants this proposal, replace or supersede the
pending choice with an explicit multi-route decision. Keep implementation and
execution as later separate boundaries.

## Synthesis

**ReviewOutcome: NO_BLOCKING_FINDINGS**

The bounded design review found no unresolved technical blocker in the proposed
two-route, one-bridge, two-schedule protocol. The order control is intentionally
discriminating without claiming a physical order effect. Resource bounds remain
provisional until toy benchmarking.

**OperatorRequest: DECISION_REQUIRED**

The immediate decision is whether to adopt the multi-route proposal as the
replacement Stage B convention. Adoption must not be interpreted as Stage B
execution authority, scientific validation, or activation of Stage C.
