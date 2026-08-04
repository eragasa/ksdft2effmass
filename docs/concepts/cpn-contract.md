# Executable backend-neutral CPN contract

P1 implements the project-owned Colored Petri Net (CPN) contract at
`ksdft2effmass.workflows.cpn`. It represents

$$
\mathcal N=(P,T,A,\Sigma,C,G,E,I),
$$

where `places`, `transitions`, directed `arcs`, `colors`, place color
assignments, declarative guards, arc inscriptions, and `initial_marking` map to
$P,T,A,\Sigma,C,G,E,I$, respectively. A marking stores a complete tuple of
places, including empty places. Each place contains a multiset of independently
identified immutable tokens. It never reduces completion to a Boolean.

## Tokens and outcomes

`CpnToken` is a routing envelope, not a scientific payload. Stable fields expose
workflow/run/attempt identity, parent run, retry parent attempt, iteration index,
all-or-none payload reference, provenance and parent-token identities,
correlation, authorization, and optional `TokenOutcome`. P1 generates no UUID or
time value. Callers supply every identity.

Outcomes distinguish `accepted`, `rejected`, `failed`, and `blocked`, carry an
`attempt`, `branch`, `gate`, or `workflow` scope plus scope identity, and state
terminality. Accepted, rejected, and failed outcomes are terminal. Blocked
outcomes may be recoverable or terminal. These are workflow-control states; an
accepted token is not evidence that a physical model or calculation is valid.

## Declarative execution

Guards and output inscriptions use a closed tagged expression model. Literals,
enumerated token fields, and ordered bound-token IDs are the only value sources.
Version 1 performs no arithmetic, including no automatic
`iteration_index = current + 1` operation. There is no source string, callable,
lambda, `eval`, import, attribute traversal, or I/O operation. Exact routing
comparisons require equal tagged value kinds and own no physical unit conversion
or numerical tolerance.

The numeric tagged union is fixed for version 1. `ContractValue.INTEGER` accepts
only exact built-in Python `int` values except `bool` in the signed i64 interval
$[-2^{63}, 2^{63}-1]$. `ContractValue.REAL` accepts finite exact built-in `int`
or `float` values except `bool` and canonicalizes every accepted value to an
IEEE-754 binary64 built-in `float`. Conversion uses round-to-nearest,
ties-to-even, so a large integer-valued `REAL` can round. Let

$$
M=(2-2^{-52})2^{1023}=2^{1024}-2^{971}
$$

be the maximum finite binary64 value. General noninteger number values are
bounded inclusively by $\pm M$. Built-in Python `int` values and integer-valued
JSON `real` inputs have the larger exact inclusive conversion domain $\pm L$,
where

$$
L=2^{1024}-2^{970}-1.
$$

Integers between $M$ and $L$, including $M+1$, are therefore admitted and round
to finite $\pm M$ as appropriate; $\pm(L+1)$ overflows conversion and is
rejected. Conversion overflow and a nonfinite input or result raise `ValueError`.
The tagged-`real` schema represents these two domains separately rather than
rejecting every mathematical input above $M$. Strict JSON has no `NaN`,
`Infinity`, or `-Infinity` value. An in-memory Python `nan` passed directly to
`jsonschema` is outside this wire contract even if that validator's
ordered-bound behavior does not reject it. The intended Rust mappings are `i64`
and `f64`, respectively. There is no unsigned `ContractValue` kind.

`TransitionEnabler.execute()` validates the net and marking, orders input arcs by
`arc_id`, orders token candidates by `token_id`, enumerates every multiset
binding, and evaluates the guard. A token can satisfy more than one read pattern,
but cannot satisfy two consume patterns. Terminal outcome tokens are excluded
from consume bindings.

`TransitionFirer.execute()` confirms the binding is currently enabled, applies
read and consume inscriptions, evaluates output templates, increments the
marking revision once, and returns a new complete marking. Output token IDs are
supplied in `(arc_id, template_index)` order. `FiringRequest` rejects duplicate
or empty output identities intrinsically; the firer reports a structured
collision when a requested identity already exists in the current marking.
Terminal tokens cannot be consumed.

## Representable control-flow patterns

A synchronization join binds separate tokens and uses `all` plus exact field
equality (for example run, correlation, or provenance identity). Two similarly
colored completion tokens alone do not establish compatible lineage.

A retry pattern reads a retained terminal failure, consumes or reads a separate
retry authorization according to net policy, and copies a new attempt identity,
retry-parent identity, authorization, and iteration index from bound control
tokens. A recoverable blocked token may be consumed by recovery; a terminal
blocked token may only be read. P1 supports repeated transition firing and cyclic
net execution when successive markings enable the transition. Every
expression-visible nonnegative version-1 control, including marking and prior
revisions, `iteration_index`, and `payload_schema_version`, is limited to
$[0,2^{63}-1]$ so it remains representable by `ContractValue.INTEGER` and Rust
`i64`. Firing a marking at revision $2^{63}-1$ raises a structured
`CpnFiringError` with `CpnErrorCode.REVISION_OVERFLOW` before output evaluation
or successor construction.

These bounds do not introduce iteration arithmetic. `iteration_index` is
explicitly supplied or copied routing data and may repeat; firing advances only
the separate marking revision. Future automatic index advancement would belong
to a future ActionObject or a separately authorized expression revision, not
the version-1 expression language.

## Errors and validation

Intrinsic wrong semantic types raise `TypeError`; values of the correct type
that violate an invariant raise `ValueError`. Booleans are rejected as integers,
numeric strings are not converted, and only built-in Python scalar types are
accepted. Ordered `string_sequence` values require nonempty strings but preserve
duplicates, which permits two read variables to identify the same token.
ResultObjects enforce matching transition identities, successor revision equal
to the prior revision plus one, and unique nonempty consumed/read identity
tuples. Cross-object validators return stable `CpnIssueCode` values.
Operational failures raise `CpnContractError` subclasses retaining immutable
`CpnErrorDetail`; its code is authoritative rather than its message.

## Boundaries

P1 does not implement SNAKES adaptation, authoritative persistence, external
execution, provenance/tool objects, scientific payloads, a concrete workflow,
QE/Wannier integration, identity generation, or Rust code. True u64 artifact
sizes or counters are not P1 expression values; explicitly typed fields for
those quantities are deferred to P2 and are not implemented. The JSON schemas
and synthetic tests are software-verification and contract-conformance evidence.
They are not numerical verification, scientific validation, uncertainty
quantification, SNAKES verification, or permission to execute calculations. `P1-HC01` Option A and `P1-HC02` Option B are resolved. Final P1
acceptance was granted as Option A through `P1-HC03` on 2026-08-04, after
reviews and parent verification; P1 is closed as human-accepted `PASS`. No
successor was selected or launched, and P2--P11 and production or scientific
execution remain blocked and unauthorized.
