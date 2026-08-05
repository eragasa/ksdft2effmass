# External-tool lifecycle

The provenance package supplies a narrow common record seam around external
tools. It does not discover, authorize, import, probe, or execute them.

## Distinct lifecycle facts

Keep each fact separate and retain its provenance:

1. **Identity declared:** `ExternalToolIdentity` names a stable tool family.
2. **Installation specified:** `ExternalToolSpecification` states the requested
   version and executable/package identifier.
3. **Capability specified:** `DeclaredCapability` names one `EXECUTE`, `PARSE`,
   `RENDER`, or `TRANSFER` contract and its project-owned version.
4. **Installation observed:** `InstallationObservation` records observed version,
   executable/package identity, optional digest, a separately controlled
   environment-provenance record ID, and provenance. Observation does not imply
   capability.
5. **Capability verified:** `VerificationObservation` records `VERIFIED`,
   `REJECTED`, or `UNAVAILABLE` with evidence artifacts. Verification is not
   execution authorization.
6. **Authorization issued separately:** the execution authority remains a
   distinct durable record owned outside this package. A request carries only
   its `authorization_id`; constructing the request does not create authority.
7. **Request recorded:** `ExternalExecutionRequest` freezes request,
   correlation, explicit attempt, tool/capability/installation/authorization,
   sealed-input, expected-role, and provenance identities. An optional
   `retry_parent_request_id` names a distinct prior request for lineage only; it
   does not authorize a retry. The record performs no execution.
8. **Result recorded:** `ExternalExecutionResult` copies request, correlation,
   and attempt identities and records `COMPLETED`, output
   artifacts, manifest, and provenance. Completion is not parser acceptance,
   convergence, numerical acceptance, or scientific validation.
9. **Later adapter interpretation:** a concrete adapter/parser may subsequently
   interpret sealed result artifacts into backend-specific and neutral scientific
   records. That interpretation is not performed by the lifecycle seam.
10. **Failure recorded:** `ExternalExecutionFailure` preserves the request,
    correlation, and attempt IDs, observation stage, structured code, diagnostic
    paths, and provenance. It has no raw message field. A retry is a new,
    separately authorized request with a new request and attempt identity; it
    does not erase the failure.

A failure stage is `REQUEST_ACCEPTANCE`, `EXECUTION`, or `RESULT_CAPTURE`.
Failure codes are `UNAVAILABLE`, `NOT_AUTHORIZED`, `REJECTED`, `INTERRUPTED`,
`MALFORMED_RESULT`, and `INTERNAL_ERROR`. Failures and successful results are
alternative immutable outcomes.

## Correlation

Every outcome copies `request_id`, `correlation_id`, and `attempt_id`. Use
`ExecutionOutcomeCorrelator`, which checks all three fields and reports
`REQUEST_ID_MISMATCH`, `CORRELATION_ID_MISMATCH`, and/or
`ATTEMPT_ID_MISMATCH` in that deterministic order. Its status is derived from
the issue tuple and is not stored or serialized. Correlation does not validate
output contents, provenance truth, tool behavior, retry lineage, or
authorization.

## Pure external boundary

In a CPN workflow, a guard may inspect immutable fields but must never invoke a
tool or service. An external adapter outside guard evaluation consumes an
authorized immutable request and returns a correlated immutable result or
failure. A later transition records that outcome. Durable tokens keep IDs and
immutable values, never credentials, access tokens, private keys, open files,
subprocess/scheduler handles, mutable clients, closures, or SNAKES runtime
objects. The public records expose no generic raw argument, environment-value,
verification-detail, or failure-message channel. Lexical validation cannot
detect a secret hidden in an opaque identifier, version, or path, so callers
must never encode credentials, tokens, private keys, or other secrets in those
fields or referenced records.

Future Quantum ESPRESSO and Wannier90 tasks own concrete mappers, serializers,
parsers, scientific result adapters, capability names, and file semantics. They
will use this lifecycle seam; they do not register plugins. No plugin framework,
dynamic backend registry, generic adapter superclass, resolver framework, or
multi-engine framework is authorized.

The lifecycle evidence is software verification only. Numerical verification,
scientific validation, and uncertainty quantification are not applicable to the
record/correlation implementation and no such claims are made.
