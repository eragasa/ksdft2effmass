# H1 issue-code and deterministic-ordering contract

Status: corrected under resolved `H1-HC01` Option B and pending final H1 human
acceptance; H1 implements no validator.

## Namespace

Generic version-1 issue codes are case-sensitive opaque identifiers with the
registered form `PIH.<AREA>.<CONDITION>`. `PIH` and the generic codes below are
owned by public contract version 1. Version 1 has no local-code registration surface. Generic `ValidationIssue`
accepts only the closed generic registry below. Project-local adapters may own
separate local diagnostic types, but those are not generic `ValidationIssue`
instances and cannot be inserted into a generic `ValidationResult`. Renaming or changing the represented condition of a code is
contract-breaking. The version-1 registry is closed. Adding a new code requires a new integer
public-contract version and explicit consumer compatibility; there is no implicit
major/minor negotiation.
Human-readable `message` text is explanatory and may change without changing the
machine contract.

## Version-1 generic registry

| Area | Stable codes |
| --- | --- |
| Wire | `PIH.WIRE.INVALID_UTF8`, `PIH.WIRE.INVALID_JSON`, `PIH.WIRE.DUPLICATE_KEY`, `PIH.WIRE.UNKNOWN_FIELD`, `PIH.WIRE.MISSING_FIELD`, `PIH.WIRE.INVALID_TYPE`, `PIH.WIRE.INVALID_VALUE`, `PIH.WIRE.UNSUPPORTED_VERSION` |
| Identifier | `PIH.ID.EMPTY`, `PIH.ID.INVALID_ASCII`, `PIH.ID.DUPLICATE` |
| Path | `PIH.PATH.EMPTY`, `PIH.PATH.ABSOLUTE`, `PIH.PATH.INVALID_SEGMENT`, `PIH.PATH.INVALID_CHARACTER`, `PIH.PATH.NONCANONICAL_UNICODE`, `PIH.PATH.WINDOWS_SYNTAX`, `PIH.PATH.CASE_MISMATCH`, `PIH.PATH.ESCAPE`, `PIH.PATH.SYMLINK`, `PIH.PATH.MISSING`, `PIH.PATH.NOT_FILE`, `PIH.PATH.ROOT_INVALID` |
| Artifact | `PIH.ARTIFACT.ALGORITHM_UNSUPPORTED`, `PIH.ARTIFACT.DIGEST_INVALID`, `PIH.ARTIFACT.HASH_MISMATCH` |
| Resource | `PIH.RESOURCE.MANIFEST_MISMATCH`, `PIH.RESOURCE.DUPLICATE_ID`, `PIH.RESOURCE.DUPLICATE_PATH`, `PIH.RESOURCE.MISSING_DEPENDENCY`, `PIH.RESOURCE.DEPENDENCY_CYCLE`, `PIH.RESOURCE.GENERIC_TO_LOCAL_DEPENDENCY`, `PIH.RESOURCE.OVERLAY_REPLACEMENT`, `PIH.RESOURCE.KIND_UNSUPPORTED`, `PIH.RESOURCE.VERSION_INCOMPATIBLE`, `PIH.RESOURCE.NOT_FOUND`, `PIH.RESOURCE.AMBIGUOUS_SELECTION` |
| Profile | `PIH.PROFILE.IDENTITY_MISMATCH`, `PIH.PROFILE.CONTRACT_INCOMPATIBLE`, `PIH.PROFILE.POLICY_REFERENCE_UNKNOWN`, `PIH.PROFILE.VOCABULARY_OVERLAP`, `PIH.PROFILE.EXTENSION_UNSUPPORTED` |
| Skill | `PIH.SKILL.DUPLICATE_ID`, `PIH.SKILL.ENTRY_MISSING`, `PIH.SKILL.ENTRY_KIND_INVALID`, `PIH.SKILL.CLOSURE_INCOMPLETE`, `PIH.SKILL.POLICY_INCOMPATIBLE`, `PIH.SKILL.BEHAVIOR_INCOMPATIBLE` |
| Ownership | `PIH.OWNERSHIP.TASK_MISMATCH`, `PIH.OWNERSHIP.AGENT_MISMATCH`, `PIH.OWNERSHIP.ROLE_DUPLICATE`, `PIH.OWNERSHIP.PATH_OVERLAP`, `PIH.OWNERSHIP.REVIEWER_NOT_INDEPENDENT`, `PIH.OWNERSHIP.COMPLETION_INVALID`, `PIH.OWNERSHIP.PROFILE_UNSUPPORTED` |
| Checkpoint | `PIH.CHECKPOINT.DUPLICATE_ID`, `PIH.CHECKPOINT.TASK_UNKNOWN`, `PIH.CHECKPOINT.STATUS_UNKNOWN`, `PIH.CHECKPOINT.STATE_CONTRADICTION`, `PIH.CHECKPOINT.DECISION_DUPLICATE` |
| Chain | `PIH.CHAIN.TASK_DUPLICATE`, `PIH.CHAIN.PREREQUISITE_MISSING`, `PIH.CHAIN.PREREQUISITE_CYCLE`, `PIH.CHAIN.ACTIVE_CONTRADICTION`, `PIH.CHAIN.ACTIVATION_MISSING`, `PIH.CHAIN.ACTIVATION_UNEXPECTED`, `PIH.CHAIN.STATUS_UNKNOWN` |
| Evidence | `PIH.EVIDENCE.SOURCE_INVALID`, `PIH.EVIDENCE.ID_INVALID`, `PIH.EVIDENCE.ID_DUPLICATE`, `PIH.EVIDENCE.NAMESPACE_UNDECLARED`, `PIH.EVIDENCE.MARKER_UNDECLARED`, `PIH.EVIDENCE.RANGE_CONFLICT`, `PIH.EVIDENCE.PROTECTED_GAP` |
| Checksum | `PIH.CHECKSUM.ENTRY_DUPLICATE`, `PIH.CHECKSUM.FILE_MISSING`, `PIH.CHECKSUM.HASH_MISMATCH` |

A condition that has no registered generic code must not be squeezed into an
unrelated code. The implementation reports an internal programming failure when the condition
is not expected input invalidity, and a contract revision adds a generic code if
an expected-invalidity condition becomes part of the generic surface. No
profile-owned local code is permitted in a generic result.

## Severity

- `ERROR`: supplied input does not satisfy the contract; aggregate status is
  `FAIL`.
- `WARNING`: structurally usable input has an explicitly profiled compatibility
  or migration limitation; aggregate status is `WARN` unless an error exists.
- `INFO`: deterministic explanatory fact with no invalidity; an all-info result
  remains `PASS`.

Every registered version-1 code is fixed at `ERROR` except
`PIH.EVIDENCE.PROTECTED_GAP`, which is fixed at `WARNING`. Version 1 registers no
`INFO` code; the severity remains defined for a future explicit contract version. `PIH.EVIDENCE.PROTECTED_GAP` is emitted only when the explicit profile marks
the exact evidence scope as protected. Without that profile fact, the applicable
missing/invalid evidence code is `ERROR`. Severity cannot be downgraded by a local profile.

Capability-specific codes own failures once an action has accepted an
intrinsically valid record: `ValidateChecksumManifest` uses only
`PIH.CHECKSUM.ENTRY_DUPLICATE`, `PIH.CHECKSUM.FILE_MISSING`, and
`PIH.CHECKSUM.HASH_MISMATCH` for entry comparison; `PIH.PATH.*` and
`PIH.ARTIFACT.*` are used while constructing records or resolving resources.
`LoadProjectProfile` uses `PIH.PROFILE.IDENTITY_MISMATCH` when valid expected and
actual artifact identities differ, and `PIH.ARTIFACT.*` only when an identity
field is itself malformed. This precedence prevents duplicate codes for one
condition.

## Action-to-code ownership and precedence

Validation stages are: (1) wire syntax, (2) intrinsic record construction,
(3) action-specific relational checks, and (4) filesystem/content checks. A
failure that prevents a later stage suppresses that later stage. One condition
uses the most specific code in this table; generic `PIH.ID.*`, `PIH.PATH.*`, and
`PIH.ARTIFACT.*` codes own intrinsic values unless a row explicitly assigns an
action-specific comparison code.

| Action | Owned condition families in precedence order |
| --- | --- |
| `DeserializeJsonRecord` / `LoadProjectProfile` | `PIH.WIRE.INVALID_UTF8`, `INVALID_JSON`, `DUPLICATE_KEY`; then `UNKNOWN_FIELD`, `MISSING_FIELD`, `INVALID_TYPE`, `INVALID_VALUE`,
`UNSUPPORTED_VERSION`; then intrinsic `ID`, `PATH`, `ARTIFACT`, and profile invariants. For `LoadProjectProfile`, comparison of two valid identities uses `PIH.PROFILE.IDENTITY_MISMATCH`. |
| `SerializeJsonRecord` | a value outside `HarnessWireRecord` raises Python `TypeError`; a valid record produces no issue; bypassed/impossible internal invalidity raises `HarnessInternalError`. It never uses structured invalidity for an out-of-union call. |
| `ValidateResourceManifest` | manifest identity/base mismatch; duplicate resource ID; duplicate resource path; unsupported kind; unsupported `(kind, format_version)` pair; missing dependency; generic-to-local edge; dependency cycle; forbidden overlay replacement. One duplicate uses `PIH.RESOURCE.*`, not `PIH.ID.DUPLICATE`. |
| `ResolveResource` | manifest validation first; then `NOT_FOUND`/`AMBIGUOUS_SELECTION`; then intrinsic `PIH.PATH.*` in lexical, root, exact-case, symlink, escape, missing, not-file order; then `PIH.ARTIFACT.HASH_MISMATCH`. |
| `ValidateOwnershipManifest` | task mismatch; missing/mismatched agent; duplicate role; intrinsic scope path; cross-writer overlap; reviewer independence; completion binding; unsupported orchestration profile. Ownership duplicates use `PIH.OWNERSHIP.*`. |
| `ValidateCheckpointSet` | duplicate checkpoint ID; unknown task; unknown status; state contradiction; duplicate normalized decision. Checkpoint identity duplicates use `PIH.CHECKPOINT.DUPLICATE_ID`. |
| `EvaluateChainState` | duplicate task; unknown task prerequisite; unknown declared external prerequisite; prerequisite cycle; unknown task status; active contradiction; missing or unexpected explicit activation. Chain duplicates use
`PIH.CHAIN.TASK_DUPLICATE`; unexpected facts use
`PIH.CHAIN.ACTIVATION_UNEXPECTED`. |
| `AuditEvidenceIdentifiers` | invalid Python source; undeclared/mismatched marker; ID syntax/range; namespace not permitted for module scope; range conflict; duplicate owner; exact protected unowned function warning. Evidence duplicates use `PIH.EVIDENCE.ID_DUPLICATE`. |
| `ValidateChecksumManifest` | invalid root and intrinsic entry path use `PIH.PATH.*`; duplicate valid entry path uses `PIH.CHECKSUM.ENTRY_DUPLICATE`; missing valid entry uses `FILE_MISSING`; valid-file digest mismatch uses `HASH_MISMATCH`. Symlink, escape, exact case, and not-file remain the corresponding `PIH.PATH.*` condition. |
| `ValidateSkillResources` | first applies and propagates the complete `ValidateResourceManifest` `PIH.RESOURCE.*` findings, including forbidden overlay; only after a valid manifest pair does it emit duplicate skill ID, missing/wrong-kind entry, incomplete closure, unsupported `(skill_id, behavior_version)` pair, or unknown/incompatible authorization policy. Skill duplicates use `PIH.SKILL.DUPLICATE_ID`. |

When several independent fields are invalid and construction can continue safely,
all applicable issues are emitted and sorted. When a parent object cannot be
constructed, dependent relational/filesystem checks are suppressed. No action
emits both a generic duplicate code and its capability-specific duplicate code
for the same pair.

## Subject and path

`subject_id` is the most specific stable represented identity. `path` is
`DiagnosticPath | None`: a neutral canonical root-relative POSIX lexical
location when the finding concerns one. It may identify a regular-file resource,
a directory, or an ownership-scope prefix and does not claim existence or file
kind. Validators convert an already valid `ResourcePath` or
`OwnershipScopePath` to the same lexical diagnostic spelling without weakening
either specialized source type. A directory-tree ownership finding therefore
retains its machine-readable scope path rather than being mislabeled as a
regular-file resource or omitted. Neither field is constructed from human prose.
`related_ids` names other stable participants and is unique and sorted. A path
is not used as durable identity when a subject ID exists; both may be present.

## Duplicate behavior

The machine duplicate key is

```text
(severity, code, subject_id, path, related_ids)
```

where `None` is a distinct value and `related_ids` is its canonical tuple. An
action emits at most one issue for each machine duplicate key. If two detection
routes reach the same key, they are coalesced before result construction and one
stable generic message is selected by the owning action. Two messages with the
same machine key are not separately observable issues. Distinct related-ID sets
are distinct findings.

## Deterministic ordering

Issues are sorted by the following total key:

1. severity rank: `ERROR = 0`, `WARNING = 1`, `INFO = 2`;
2. `code` by exact ASCII bytes;
3. `subject_id`, with `None` before any string;
4. diagnostic `path`, with `None` before any string, using exact UTF-8 bytes of
   the NFC canonical `DiagnosticPath`;
5. `related_ids` lexicographically;
6. `message` by Unicode scalar value only as a final deterministic tie-breaker.

The duplicate key normally makes step 6 unnecessary. Filesystem traversal,
mapping insertion order, hash iteration, locale, current working directory, and
operating-system case rules cannot affect output ordering.

Resource references sort by `resource_id`; manifest/checksum paths sort by
canonical path; ownership roles sort by `(role, agent)`; evidence occurrences
sort by `(evidence_id, path, line)`; task facts sort by task ID. Input presentation
order is preserved only for checkpoint options because it is human decision
content.

## Empty and invalid-input semantics

A validator with no findings returns `ValidationResult(1, "PASS", ())`. An
expected-invalid external input returns a `FAIL` result and no partially trusted
primary object or derived facts. A nonempty all-info result is `PASS`; warnings
produce `WARN`; any error produces `FAIL`.

Internal programming errors are not `ValidationIssue`s. They raise a documented
exception and must not be converted into an empty or partial `PASS`. I/O changes
after resource selection are reported as an implementation/runtime failure,
unless the action can deterministically classify the changed supplied input
under an existing issue code.

## Claim boundary

`PASS` and `WARN` are software-structural result states only. They grant no human
acceptance, task authorization, successor activation, command execution,
numerical verification, scientific validation, uncertainty quantification,
package readiness, release status, or publication permission.
