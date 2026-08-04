# H1 bounded correction round 2

The correction-1 reviews are retained unchanged. This second and final bounded
contract correction responds to their semantic findings; it does not claim
human acceptance.

## Corrections

1. Removed generic local issue-code registration. Version-1
   `ValidationIssue` accepts only the closed generic registry; project-local
   diagnostics remain outside generic `ValidationResult` unless a future
   contract explicitly adds them.
2. Limited every serialized general integer to $2^{53}-1$ (and evidence widths
   accordingly) so RFC 8785/ECMAScript-number canonicalization preserves exact
   Python/Rust integer values.
3. Added the public closed `WireRecordKind` enum, public closed
   `HarnessWireRecord` typing union, and nonserialized public
   `HarnessInternalError` with exact Python/Rust representation. Defined the
   Rust constructor-error mapping and all action signatures.
4. Replaced insufficient protected-evidence IDs with complete
   module-scope-to-marker/allowed-namespace rules and exact protected unowned
   `(module_path, test_function)` pairs. Defined namespace string generation.
5. Split task prerequisites from external prerequisites and supplied both the
   complete known external-condition set and its satisfied subset to chain
   evaluation. Generic code never infers meaning from opaque colon text.
6. Added a complete action-to-code ownership/precedence table, including
   suppression of generic/capability duplicate codes and filesystem versus
   checksum conditions.
7. Reconciled every Rust identifier/path table mapping to the exact validated
   newtypes and defined the internal/constructor error structures.
8. Added the exact unresolved/resolved checkpoint field-state table and UTC time
   syntax requirement.
9. Removed unattested `ArtifactIdentity.media_type`; resource interpretation
   remains separate in `ResourceReference.resource_kind`. Removed unattested
   checksum catalog ID/version/root-role fields; the runtime root is an explicit
   action argument.
10. Expanded field-level consumer traceability for every operation-specific
    result and public support type, and replaced prospective evidence citations
    with current validator/skill/checksum/checkpoint/chain consumers where
    applicable.

## Architecture-review preflight note

The correction-1 architecture agent reported that the production ownership
preflight did not name H1. That check is intentionally not applicable: H1 is a
non-production contract-evidence task, creates no implementation/resource root,
and the repository production-task preflight applies before production
implementation begins. H1's user instruction explicitly requires read-only
semantic reviews but prohibits creating H3/H2 manifests or agent records.
Future H3, H2, and H4 remain blocked and each plan entry requires its own
validated manifest before launch. This note does not waive any future production
preflight.

## Remaining human authority

The entire corrected contract remains proposed. `H1-HC01` retains the human
choice to accept, accept with bounded corrections, reject/reopen, or defer. No
successor or implementation is activated by these corrections.
