# P1 implementation progress

Status: closed as human-accepted `PASS` through `P1-HC03` on 2026-08-04.
Deterministic implementation, test-completeness and iteration-semantics
corrections, resolved numeric-contract correction, final independent reviews,
parent verification, and closeout validation pass. No successor is active;
P2--P11 remain blocked.

## Test-ownership correction

The human-authorized deterministic correction prohibited mutation of production
source, schemas, fixtures, dependencies, lockfiles, and the protected numeric
contract. Current hashes and manual semantic comparison show no detected change
to those protected surfaces. The recorded writer tool-call transcript contains
no direct write/edit call to them. Because no durable per-file pre-correction
hash baseline exists, byte identity across the correction is not independently
attested; `test-ownership-mutation-audit.json` records this residual provenance
limitation without treating unlike aggregates as proof of equality.

Maintained object-level P1 pytest evidence uses
`python/tests/software_verification/ksdft2effmass/workflows/cpn/`; maintained
artifact-owned package, schema, fixture, dependency, and isolation evidence uses
the neighboring `integration/` subtree. Historical initial/correction/
precheckpoint reviews remain unchanged; their earlier paths and counts describe
superseded evidence surfaces.

The current surface contains 32 exact `test__ClassName.py` object modules and
five exact integration modules: four are manifest-declared
`artifact_owned_integration` owners and the Python/JSON agreement module is the
manifest-declared `boundary_owned` owner. Its 88 test functions/evidence
items collect 91 parameter cases and preserve the contiguous range
`SV-CPN-001` through `SV-CPN-088`. IDs `023` and `027`--`033` are ordinary pytest
evidence; `040`--`057` own the 18 previously missing public classes;
`058`--`079` cover deterministic missing branches for nine existing owners; and
`080`--`088` verify the resolved numeric contract.

Durable correction artifacts:

- `test-ownership-manifest.json`: all 49 exports, 32 one-class modules, five
  artifact modules, `001`--`088`, and old -> temporary-gate -> restored-pytest
  traceability;
- `test-completeness-matrix.json`: deterministic-now IDs plus resolved numeric
  evidence; no branch remains blocked by `P1-HC01` or `P1-HC02`;
- `test-ownership-mutation-audit.json`: earlier bounded mutation-path evidence and
  its explicit unavailable-baseline limitation;
- `validate_test_ownership.py`: structural owner, evidence-ID, classification,
  and traceability audit;
- `contract_gates.py`: external replay that invokes the five authoritative
  artifact-owned pytest modules without duplicating their assertions;
- `checksums.sha256`: current P1 source, specification, documentation,
  task/checkpoint, ownership evidence, object tests, and artifact tests.

## Iteration-semantics correction

The human PI clarified that repeated transition firing and cyclic CPN execution
do not imply automatic iteration-index advancement. Version 1 has no arithmetic
expression and does not compute `iteration_index = current + 1`.
`iteration_index` remains explicitly supplied or copied routing data and may
retain the same value across repeated firings while the marking revision advances
once per firing.

Maintained `SV-CPN-006` now asserts the exact three-member nonarithmetic
`ValueExpressionKind` vocabulary. Maintained `SV-CPN-020` executes two firings
with explicit nonzero index 7, proves that both output tokens retain 7, and
separately proves revision advancement from 0 through 1 to 2. Concept, API, and
verification documentation state the same boundary. No production source,
schema, fixture, dependency, numeric contract, or arithmetic expression was
changed. Future automatic index advancement requires a future ActionObject or a
separately authorized expression-language revision.

## Numeric-contract correction

The human PI resolved `P1-HC01` as Option A and `P1-HC02` as Option B. Tagged
`REAL` accepts finite exact built-in Python `int` or `float` values except
`bool`, canonicalizes to built-in IEEE-754 binary64 `float`, documents possible
rounding of large integer-valued inputs, and rejects conversion overflow or a
nonfinite result as `ValueError`. Tagged `INTEGER` is bounded to signed i64.
Every expression-visible nonnegative control—including marking/prior revisions,
`iteration_index`, and `payload_schema_version`—is bounded to
`[0, 2^63 - 1]`. Firing at revision `2^63 - 1` raises structured
`CpnErrorCode.REVISION_OVERFLOW` before output evaluation or successor marking
construction.

Python runtime, JSON Schema, specification, focused tests, concept/API/
verification documentation, and intended Rust `f64`/`i64` mappings now state the
same contract. The tagged-`REAL` schema distinguishes general numbers bounded
to maximum finite binary64 from integer-valued inputs admitted through the exact
finite-conversion limit $L=2^{1024}-2^{970}-1$; such large integers may round to
maximum finite, while $L+1$ overflows. NaN/Infinity remain outside strict JSON
wire syntax. No unsigned `ContractValue` kind or dependency was
added. True
u64 artifact sizes or counters are deferred to explicitly typed future P2
fields. Automatic iteration-index arithmetic remains absent from version 1.

## Public-class inventory

Dedicated modules exist for all 32 public DataObjects, ResultObjects,
ActionObjects, and independent constructor-invariant owners. The remaining 17
exports are exactly the 11 enum types and six marker exception subclasses
explicitly classified by the task-ownership manifest; no low-value modules are
fabricated for them.

## Verification commands

The authoritative ownership/gate command is:

```text
cd python
uv run python ../.pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py
```

Focused pytest targets the 32 object modules and five declared artifact modules.
Current correction validation results are:

- ownership validator: passed, 32 class modules, five artifact modules, 49
  exports, 88 IDs, and eight restored pytest gates;
- focused pytest: 91 collected parameter cases from 88 test functions, passed;
- artifact-owned external gate replay: ten ordinary pytest tests passed;
- full Python suite: 1012 passed;
- Ruff format/check: 42 focused source/test files passed;
- mypy: focused source/test files passed after one test-local inference correction;
- Sphinx `-W`: 33 sources built successfully to a temporary directory;
- evidence audit: 403 owned IDs, the same 22 pre-existing non-P1 unowned-test
  warnings, and `audit_errors=0`; strict mode remains nonzero only for that
  separately catalogued non-P1 baseline;
- checkpoint validation: seven records valid and zero unresolved;
- pre-correction checksum comparison: all 33 protected P1 production/schema/
  fixture files retained their hashes;
- final checksum inventory: 116 entries, including both numeric checkpoint
  resolutions, final review records, parent verification, the P1 final-acceptance
  checkpoint, current control-plane state, and maintained status-bearing user-
  guide pages, regenerated and verified;
- `git diff --check` and no-staged-file check: passed.

The first final numeric architecture and integration reviews found stale
maintained test limitation prose and three stale user-guide status statements;
the assigned writers corrected them. Consolidated architecture re-review then
found that the tagged-`REAL` schema lacked conversion-overflow bounds. An initial
maximum-finite bound was too strict for Option A because large integer-valued
inputs may round to finite maximum. The implementation, test, and documentation
owners therefore aligned the exact finite-conversion domain, including
$L=2^{1024}-2^{970}-1$, without a new public-contract choice. Final bounded
architecture and integration rechecks pass, and parent verification passes.
The correction remains software-verification evidence and does not advance P1
acceptance.

The closed P0A external replay was executed against the present tree but fails
its historical exact Sphinx `include_patterns` assertion because authorized P1
added the CPN concept and API pages. This is expectation drift between the
accepted historical snapshot and the current task tree, not a P1 completeness
failure; it is not reported as a pass. Accepted P0A evidence and historical P1
review files remain intentionally unchanged. Exact P0A replay requires the
corresponding historical tree; present-tree validation reports the drift
separately.

## Acceptance boundary

`P1-HC01` and `P1-HC02` are resolved, and the human PI granted final P1
acceptance through `P1-HC03` after independent review and parent verification
passed. P1 is closed. Acceptance does not launch a successor: P2--P11, SNAKES
adaptation, persistence, concrete workflow execution, and scientific execution
remain blocked.

Passing these gates is software verification only. It is not numerical
verification, scientific validation, uncertainty quantification, Rust
conformance, or scientific-execution evidence.

## Post-close maintenance note

The separately authorized `EVIDENCE-DOC-1` maintenance adds a shared structural
and semantic documentation convention. Under resolved `EVIDENCE-DOC-1-HC02`
Option B, all 32 class-owned modules in the P1 CPN workflow test directory now
carry the grammar across 78 stable evidence owners, and the 11 manifest-declared
helpers document their complete supported-ID lists without independent IDs. The
maintenance preserves P1 assertions, fixtures, parameterization, IDs,
production/schema behavior, and the resolved `P1-HC01`--`P1-HC03` decisions.
Its complete-directory validator and 78-function node map establish structural
traceability only. The architecture-reviewed artifact follow-up uses five
lowercase descriptive `workflow_cpn` integration filenames. It preserves
`SV-CPN-028` as one accepted conjunctive nonnumeric Python/JSON boundary
agreement, without a split or new IDs; `SV-CPN-087` and `SV-CPN-088` remain the
separate numeric agreements. The test writer synchronized the renamed modules,
ten evidence owners, P1 manifest/validator, and complete rename mappings. The
implementation/control-plane writer synchronized the completion validator,
contract-gate replay paths, current completeness and mutation-audit records,
and migration inventory. Accepted reviews and explicit predecessor mappings
that cite old paths remain historical. The documentation writer synchronized the two owned verification pages, and
the final checksum catalogs now reference the current five integration
filenames and the complete migrated module surface. Obsolete integration paths
remain only in accepted historical reviews, baselines, or explicit predecessor
mappings. P1 remains closed as human-accepted `PASS`; this maintenance is not P2 and does
not claim scientific-validation or UQ capability. Its persisted final
architecture/VVUQ and integration reviews both conclude PASS. Fresh parent
closeout validation reports the full Python suite at 1012 passed, Sphinx 9.1.0
with `-W` passed, contract replay at ten passed, and the focused P1 suite at 91
passed. Completion, P1 ownership, task-ownership, skill, checkpoint, both
checksum, chain-JSON, and diff gates pass. The known 22 protected historical
evidence-owner warnings remain out of scope. The human PI resolved
`EVIDENCE-DOC-1-HC03` as Option A, closing EVIDENCE-DOC-1 as human-accepted
`PASS`. No successor was launched. P2--P11 and production/scientific execution
remain blocked.
