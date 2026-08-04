# H1-HC01 Option-B diagnostic-path correction trace

## Authority and original finding

The human PI resolved `H1-HC01` as Option B on 2026-08-04. The complete human
response is preserved verbatim in
`.pi/checkpoints/H1-HC01-harness-contract.json`; that checkpoint remains the
authority for wording and scope.

The finding was that the proposed contract used
`ValidationIssue.path: ResourcePath | None`, while
`ValidateOwnershipManifest` must report findings about
`OwnershipScopePath` values that can denote directory-tree scopes. A directory
scope is not necessarily a regular-file resource. The diagnostic contract could
therefore either misrepresent the location or omit it.

No retained initial or correction review file was rewritten. This trace is an
additive record of the human finding and the single authorized correction.

## Exactly one bounded correction

The corrected version-1 proposal introduces one common semantic primitive:

```text
DiagnosticPath
```

Its Python representation is an immutable built-in `str`. It is nonempty,
NFC-normalized, root-relative POSIX lexical syntax with no absolute form, empty
segment, `.` or `..`, repeated separator, trailing slash, control character,
backslash, Windows drive/drive-relative/device/UNC syntax, normalization on
input, or case folding. Comparison is exact and case-sensitive. It may identify
a regular file, a directory, or an ownership-scope prefix. It is purely lexical
in a serialized diagnostic and claims neither existence nor regular-file kind.

The intended Rust mapping is the validated newtype:

```text
DiagnosticPath(String)
```

The only field correction is:

```text
ValidationIssue.path: ResourcePath | None
```

becoming:

```text
ValidationIssue.path: DiagnosticPath | None
```

`ResourcePath` remains the specialized regular-file path used by resource
records. `OwnershipScopePath` remains the specialized file/directory-tree path
used by ownership records. Neither semantic type is weakened or replaced.

## Interface and version accounting

`DiagnosticPath` is a semantic primitive, not a DataObject, ResultObject,
ActionObject, error, record-kind value, or separately dispositioned candidate.
The H1 counts therefore remain 36 included interfaces and 39 candidate
dispositions. Because H2 and H3 remain unimplemented and final H1 acceptance is
pending, the correction establishes the proposed version-1 contract; it does not
migrate an accepted implementation or advance a version value.

## Reconciled planning obligations

H3 must define `ValidationIssue.path` as `DiagnosticPath | null`, provide valid
fixtures for a regular-file spelling, directory-tree scope spelling, and `null`,
and provide invalid fixtures for absolute, traversal, non-NFC, malformed,
control, repeated/trailing-separator, and Windows/platform-specific forms. Its
canonical JSON vectors must be usable for later Python/Rust agreement checks.

H2 class-owned `ValidationIssue` evidence must exercise all three valid forms and
all rejection families. H2 artifact-owned evidence must prove specialized path
meanings remain intact, issue ordering uses the diagnostic path, H3 schema and
fixture agreement holds, and canonical JSON agrees with the intended Rust
`DiagnosticPath(String)` round trip.

## Scope fence retained

No H2 Python, H3 resource/schema/fixture, local integration, orchestration,
subprocess, Git mutation, plugin, registry, dispatch, Graphify, scientific,
numerical-validation, UQ, package, or successor work is part of this correction.
No accepted serialization, integer, checksum, overlay, evidence-kind,
`ProjectProfile`, or generic/local decision is reopened.
