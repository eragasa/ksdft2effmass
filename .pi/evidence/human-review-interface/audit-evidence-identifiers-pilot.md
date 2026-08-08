# AuditEvidenceIdentifiers human-review packet

## Packet identity

| Field | Value |
|---|---|
| Review ID | `human-review.audit-evidence-identifiers.pilot` |
| Reviewed revision | `201f038a006cd48829d570b0de59bde83a53a881` |
| Correction revision | `ecd260042257efb868ad4262cc3a1b9a0159c16b` |
| Represented subject | `AuditEvidenceIdentifiers` |
| Evidence class | `software_verification` |
| Packet status | `ready_for_human_review` |
| Pilot workflow status | `human_accepted_pass` |

This packet is derived review material prepared through the explicit-input
`PrepareHumanReviewPacket` API. Repeated construction from identical inputs returned
equal packets with the same canonical observation order. Its public runtime status
remains `ready_for_human_review`; final acceptance is a separate human decision now
recorded below.

## Exact review paths

1. `python/src/ksdft2effmass/harness/pi/evidence.py`
2. `python/tests/software_verification/ksdft2effmass/harness/pi/test__AuditEvidenceIdentifiers.py`
3. `python/src/ksdft2effmass/harness/pi/local/audit_evidence_identifiers.py`
4. `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__audit_evidence_identifiers_command_api_agreement.py`

All four paths were byte-unchanged between the reviewed revision and initial packet
preparation. No evidence implementation or existing evidence test was modified by
that initial slice. The later bounded correction changes only the authorized behavior
and evidence within these paths.

## Applicable contract references

- `docs/harness/ksdft2effmass.harness.001.004.000.md`
- `.pi/skills/develop-python-test-evidence/references/test-evidence-conventions.md`

## Public contract summary

`AuditEvidenceIdentifiers` is a fieldless ActionObject. It receives only explicit
Python module path/byte pairs and one explicit `ProjectProfile`. It does not discover
repository files. The action parses normalized fielded evidence declarations and the
retained historical first-line declaration, expands one valid inclusive same-prefix
range, applies explicit scope, marker, namespace, width, and range rules, and reports
structured issues for invalid inputs.

Retained occurrences report the evidence identifier, root-relative module path, and
one-based test-function line. Successful occurrences are ordered by evidence
identifier, path, and line. Validation issues use the maintained deterministic result
ordering. Duplicate evidence owners fail through a structured issue rather than a
human disposition.

The maintained local command accepts an explicit absolute root, profile, and
content-addressed module inventory. It confines named files beneath the root, verifies
SHA-256 identities, invokes the public ActionObject, emits canonical JSON, and maps
public validation status to documented exit codes. These command-side filesystem
operations are separate from the pure explicit-byte ActionObject.

## Deterministic checks actually run

| Observation ID | Check | Observed result |
|---|---|---|
| `human-review.audit.source-identity` | Git path identity at the reviewed revision | The four pilot paths were unchanged. |
| `human-review.audit.action-tests` | Focused `AuditEvidenceIdentifiers` class-owned module | 19 cases collected as part of the focused run; all completed without failure. |
| `human-review.audit.cli-tests` | Focused maintained CLI/API agreement module | 5 cases collected as part of the focused run; all completed without failure. |
| `human-review.audit.packet-idempotency` | Repeated packet preparation from identical explicit inputs | Equal packets, canonical observation order, empty findings, and `ready_for_human_review`. |

The combined existing subject run completed 24 focused software-verification cases
without failure. The new packet API run completed 81 focused cases without failure.
Maintained structural validation of the six new test modules reported 30 unique
evidence owners, 63 static parameter cases, and no structural findings.

Branch or behavior coverage was not measured and is not claimed.

## Relevant test inventory

### ActionObject class-owned evidence

`test__AuditEvidenceIdentifiers.py` covers:

- fieldless stateless construction;
- rejection of an empty caller-supplied module inventory;
- normalized fielded declaration parsing and source-line retention;
- retained historical first-line ownership;
- inclusive range expansion and occurrence ordering;
- invalid, empty, ambiguous, descending, and cross-prefix declarations;
- source, scope, marker, and namespace failures;
- deterministic duplicate-owner and protected-gap reporting; and
- explicit-input behavior independent of current working directory discovery.

### Maintained CLI/API artifact evidence

`test__audit_evidence_identifiers_command_api_agreement.py` covers:

- successful exact-inventory projection and nonmutation;
- rejection and nonmutation of an explicit empty inventory before audit;
- failed-audit exit mapping;
- root confinement and content-identity rejection; and
- absolute-root requirements without request-file mutation.

## Candidate findings

Deterministic preparation initially reported no candidate finding. This statement was
not a human judgment that the implementation was correct or complete. Direct human
review subsequently identified HRI-PILOT-F01, and the required maintained audit during
correction preflight exposed HRI-PILOT-F02.

## Human review

### HRI-PILOT-F01

Severity: high

Finding: an empty public module tuple and zero-module CLI inventory can pass without
auditing evidence.

Disposition: bounded correction authorized.

Direct human review identified the empty-inventory fail-open condition after
deterministic preparation had reported no candidate finding. The bounded correction
was authorized and is now implemented. Correction validation does not constitute
final human acceptance.

## Correction preflight

### HRI-PILOT-F02

Severity: high

Finding: the maintained SV-HARNESS allocation stopped at 122 although existing pilot
evidence occupies 123 through 152.

Disposition: bounded profile synchronization through 154 authorized.

The required maintained repository audit exposed this allocation mismatch. The
profile boundary and its selected resource identity were synchronized through 154 as
explicitly authorized. Both HRI-PILOT-F01 and HRI-PILOT-F02 are bounded corrections;
neither constitutes final human acceptance. The packet awaits renewed direct human
review.

## Correction checks actually run

| Check | Observed result |
|---|---|
| Affected ActionObject and CLI/API modules | 26 software-verification cases passed in the focused correction run and again in the focused regression run. |
| Maintained structural test-evidence validation | PASS for 2 modules, 14 unique evidence owners, and 15 static collected parameter cases. |
| Ruff format and lint | PASS for the 4 affected Python files. |
| Focused mypy | PASS for the 4 affected Python files. |
| Explicit resource refresh | PASS; only `ksdft2effmass.profile.v2` was proposed with digest `446e6fe3e5990474549cadf48d4a1b0f367f905fbb13323b829b9ae759f2cd5a`. |
| Profile and generic/local composition | PASS; `SV-HARNESS` loaded as `(1, 154, 3)` and the manifest identity matched the profile bytes. |
| Focused resource and skill-resource tests | 17 cases passed. |
| Maintained repository test-evidence validation | PASS with 207 modules, 2,824 collected nodes, and 1,134 unique evidence owners. |
| Maintained nonempty repository evidence audit | PASS with 207 inventoried modules, 1,134 occurrences, 1,134 unique IDs, zero issues, and both new IDs present. |
| Final empty/valid behavior selection | 4 cases passed: empty action and CLI requests were rejected, while valid nonempty action and CLI behavior remained passing. |
| Final bounded state checks | PASS for authorized paths, unchanged existing evidence IDs, profile-rule isolation, chain/task parsing, dependency and lockfile identity, `human_review.py` identity, documentation links, and `git diff --check`. |

The corrected affected test modules contain 26 focused collected cases rather than the
initial packet's 24. These counts are descriptive observations, not hard-coded
acceptance gates.

## Unresolved limitations

- The focused cases use controlled source examples and do not establish completeness
  for every possible Python docstring or AST form.
- Static structural validation does not establish semantic cohesion or oracle
  independence.
- The CLI tests invoke `main` directly and do not verify installation or interpreter
  entry-point behavior.
- Branch coverage was not measured.
- The full repository evidence inventory was not audited during initial packet
  preparation; one maintained nonempty audit was performed for this correction.
- Software verification does not establish numerical verification, scientific
  validation, uncertainty quantification, provenance truth, or human acceptance.
- The reviewed Git revision does not represent uncommitted external state.

## Final human acceptance

Human response (preserved exactly):

> Accept the corrected AuditEvidenceIdentifiers review-packet pilot as software-verification PASS and close the pilot only. HRI-PILOT-F01 and HRI-PILOT-F02 are resolved. This acceptance does not authorize SQLite, automatic review acceptance, successor activation, scientific execution, or protected work.

Disposition: `human_accepted_pass` for the corrected review-packet pilot only.

- HRI-PILOT-F01: resolved.
- HRI-PILOT-F02: resolved.
- Claim scope: software verification only.

The original reviewed revision, correction revision, deterministic observations,
correction observations, and limitations remain part of this packet. The maintained
human-facing decision artifact is
[`audit-evidence-identifiers-pilot-decision.md`](audit-evidence-identifiers-pilot-decision.md).

## Human authority boundary

The human accepted and closed only the corrected review-packet pilot. The packet's
public runtime status remains `ready_for_human_review` because packet preparation and
human decision recording are separate contracts. The acceptance does not authorize
SQLite, automatic review acceptance, successor activation, scientific execution, or
protected work. No checkpoint or replay was created.
