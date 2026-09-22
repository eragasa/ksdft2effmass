# Adversarial review of the Stage A implementation

## Scope and definition of done

This review covers `run_stage_a.py`, `verify_stage_a.py`, the exact
schema-version-2 authorization contract, and the execution-free toy behavioral
tests. It does not interpret a Stage A scientific result. The implementation is
ready only if authority and paths fail closed, the verifier enforces the exact
design case inventory, numerical criterion failure is distinct from
reconstruction disagreement, and the required toy behaviors pass without
reading the accepted periodic-2D parent.

## First-pass outcome

**ReviewOutcome: CHANGES_REQUIRED**

The first adversarial pass identified six `MUST_FIX` findings:

1. the self-asserted JSON gate did not bind durable human authority or exact
   immutable artifacts;
2. relative provenance paths could be interpreted differently by runner and
   verifier;
3. the verifier checked eight records but not the exact frozen shape/twist
   Cartesian product and order;
4. independently reproduced numerical criterion failure was raised as verifier
   failure rather than retained negative evidence;
5. seam-phase sign and crossing behavior lacked an explicit analytical control;
   and
6. overwrite, malformed/stale authorization, canonical paths, exact inventory,
   stop behavior, seam sign, criterion disposition, and result mutation lacked
   execution-free behavioral tests.

The earlier `NO_BLOCKING_FINDINGS` disposition was withdrawn as unsupported.
The accepted study design itself was not reopened.

## Remediation assessment

### Durable authority and immutable bindings

Disposition: CORRECTED
Evidence: `StageAExecutionAuthorization` requires schema version 2 and binds the
resolved checkpoint path/hash, canonical repository root, exact design,
runner, scalar parent, output path, resource envelope, stage, authorization
identifier, and verbatim human response. The runner validates the checkpoint's
resolved state, task identity, response, scopes, and authoritative files before
loading parent hoppings. The independent verifier repeats these checks.
Residual limitation: This is a repository governance and integrity boundary,
not cryptographic protection against a malicious local writer.

### Canonical path confinement

Disposition: CORRECTED
Evidence: CLI paths are resolved canonically beneath the exact repository root;
retained paths must be canonical repository-relative spellings without absolute
or parent-traversal components. Symlink resolution cannot escape the root.
Output parents must already exist, and the result cannot be overwritten.
Residual limitation: The resource bounds are authorization limits, not runtime
or peak-memory measurements.

### Exact folding inventory

Disposition: CORRECTED
Evidence: The verifier deserializes shapes and twists from `study-design.json`,
forms the frozen shape-major Cartesian product, and compares each result record
to the corresponding exact shape/twist tuple. Missing, duplicated, reordered,
or substituted records are rejected.
Residual limitation: Passing inventory checks does not itself establish the
folding equations.

### Reconstruction versus criterion disposition

Disposition: CORRECTED
Evidence: The runner retains `criterion_evaluation.status` and exact failed
criterion identifiers. The verifier independently reconstructs every metric,
requires agreement with the retained values and failure inventory, reports
`reconstruction=PASS`, and separately reports `criteria=PASS` or `FAIL`.
Reproduced numerical failure is therefore valid negative evidence rather than a
verification disagreement.
Residual limitation: A reconstruction mismatch remains a verifier failure and
must not be relabeled as negative numerical evidence.

### Seam-phase analytical oracle

Disposition: CORRECTED
Evidence: The accepted design now fixes noncrossing, positive-crossing, and
negative-crossing controls on a six-site seam at twist 0.37 turns. The runner
reads amplitudes from its production seam assembly. The verifier compares them
to independently evaluated $1$, $\exp(+2\pi i\phi)$, and
$\exp(-2\pi i\phi)$ values and checks source, target, and displacement metadata.

Residual limitation: This bounded oracle covers the exact Stage A sign and
single-crossing contract, not arbitrary multiwrap displacement behavior.

### Execution-free behavioral evidence

Disposition: CORRECTED
Evidence: The artifact-owned routine software-verification module
`test__stage_a_execution_contract.py` uses only authored toy coefficients in an
isolated temporary repository. Eight tests cover stale design digest rejection,
malformed-record rejection, parent-traversal rejection, canonical retained
provenance and runner/verifier composition, substituted-case rejection, mutated
seam-sign rejection, reproduced numerical-failure disposition, and overwrite
refusal. The valid toy composition also exercises structured-stop precedence
with simultaneous geometry and boundary-phase mismatches, all four stop codes,
and all three seam controls. Ruff, strict mypy, the Python
evidence-conformance validator, and all eight tests pass.
Residual limitation: These tests establish the software contract only. They do
not numerically verify the accepted periodic-2D parent or authorize execution.

## Independent reconstruction structure

Disposition: NO_ACTION_REQUIRED
Evidence: The runner constructs supercells by explicit site-and-hop enumeration
and folding matrices entry by entry. The verifier imports no runner code and
uses Kronecker products of independently constructed one-dimensional seam and
Fourier matrices. Compatibility issue codes are independently derived from
retained metadata rather than copied.
Residual limitation: Agreement of two finite implementations is numerical
verification under the frozen contract, not a theorem or scientific validation.

## Re-review conclusion

**ReviewOutcome: NO_BLOCKING_FINDINGS**

All six first-pass `MUST_FIX` findings are corrected, and the execution-free
gates pass. The source is ready for the exact bounded Stage A execution already
authorized by the durable checkpoint and machine record. This outcome does not
establish a numerical result, scientific validation, uncertainty
quantification, material relevance, resource measurement, or authorization for
Stages B--E.

**OperatorRequest: NO_INPUT_REQUIRED**

Proceed only with the single local Stage A command bound to
`stage-a-result.json`, then run the independent verifier. Preserve any criterion
failure as negative evidence and stop on authority, provenance, reconstruction,
or resource-bound failure.
