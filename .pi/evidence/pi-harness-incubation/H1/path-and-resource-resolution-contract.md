# H1 path and resource-resolution contract

Status: proposed for `H1-HC01`; no resolver or resource tree is implemented.

## Three distinct path categories

### Serialized resource path

A `ResourcePath` is portable manifest data, not a workstation path. It is a
nonempty NFC-normalized Unicode string of POSIX segments separated by one `/`.
It is always relative to an explicitly supplied root.

Version 1 requires:

- no leading or trailing `/`;
- no empty, `.` or `..` segment;
- no repeated separator;
- no backslash;
- no NUL, C0/C1 control, Unicode line/paragraph separator, or unpaired surrogate;
- no Windows drive prefix, drive-relative syntax, device prefix, or UNC syntax;
- NFC normalization on input; non-NFC text is rejected rather than rewritten;
- exact case-sensitive comparison, independent of host filesystem behavior.

Unicode filenames are permitted only in NFC form. Percent encoding, URI
interpretation, tilde expansion, environment expansion, globbing, and shell
interpolation do not occur. The empty path and a path denoting the root itself
are invalid. Version 1 resources are regular files, not directories.

### Serialized ownership-scope path

An `OwnershipScopePath` uses the same NFC Unicode, POSIX separator, relative,
segment, control-character, Windows-syntax, and case-sensitive rules as a
`ResourcePath`, but its `OwnershipScope.scope_kind` explicitly declares either
one `file` or one `directory_tree`. The string never ends in `/`. A directory-tree
scope contains its named path plus exact descendants beginning `path + "/"`;
plain string prefix without that separator never establishes containment. Scope
overlap is symmetric containment of either declared path. Runtime binding uses
both lexical and resolved confinement and rejects symlink escape. Ownership
scopes are repository path declarations, never resource-manifest identities.

### Runtime filesystem root

A runtime root is a caller-supplied `pathlib.Path`, never serialized in a
resource record. It must be absolute, exist, and identify a directory. The action
computes its canonical resolved location once for confinement. No action obtains
a root from `Path.cwd()`, Git, a parent-directory search, `.pi`, environment
variables, user configuration, or package-resource fallback.

A caller may explicitly supply:

- one generic root and its generic manifest;
- optionally one local root and its local manifest.

The profile names the expected manifest identities, not workstation root text.
The caller is responsible for choosing roots; the resolver verifies their
manifest/content contract.

### Resolved filesystem path

A resolved path is the runtime-only result of joining a validated
`ResourcePath` to the corresponding explicit root. It must exist, be a regular
file, have exact component spelling, contain no symlink component below the
root, and remain below the canonical root after resolution. It is returned as a
`pathlib.Path` and is never durable identity or serialized output.

## Lexical and resolved confinement

Validation occurs in this order:

1. validate the serialized path grammar;
2. validate the explicit root;
3. join the lexical segments without normalization that could hide invalid
   segments;
4. compare every actual directory-entry component with exact case;
5. reject any symlink component, including a symlink final file;
6. resolve the candidate and require `resolved.relative_to(resolved_root)` to
   succeed;
7. require a regular file;
8. hash exact bytes and compare `ArtifactIdentity`.

Both lexical and resolved confinement are mandatory. Resolved confinement alone
does not make `..` acceptable. Symlinks are rejected rather than followed even
when they resolve within the root; this avoids selected-content changes and
cross-platform ambiguity. The explicitly supplied root itself may be a
caller-selected symlink path only if its canonical target is stable for the
entire call; resources below it still may not contain symlinks. A root that
changes during resolution is an internal/runtime failure, never a pass.

Missing files produce `PIH.PATH.MISSING`; an existing non-file produces
`PIH.PATH.NOT_FILE`; exact-case mismatch produces `PIH.PATH.CASE_MISMATCH` even
on a case-insensitive filesystem. All reporting uses the serialized path, not an
absolute workstation path, unless a caller separately records the runtime root
outside the generic wire result.

## Manifest selection and overlay behavior

### Inputs

`ResolveResource` receives explicitly:

```text
resource_id
generic_root
generic_manifest
generic_manifest_identity
local_root or None
local_manifest or None
local_manifest_identity or None
ProjectProfile
```

The profile's generic manifest ID and version must equal the supplied generic
manifest, and SHA-256 of that manifest's RFC 8785 canonical JSON plus LF must
equal the separately supplied `generic_manifest_identity`. If the profile's local
manifest ID and version are both `null`, all three local inputs must be absent.
Otherwise both profile fields and all three local inputs are required,
ID/version/canonical-byte identity must match, and the local manifest must declare
`extends_manifest_id` equal to the generic identity. Keeping content identity as
an action input avoids a circular local-manifest/profile hash dependency.

### Version-1 overlay policy

The sole v1 policy is `extend_only`:

- generic resources are selected only from the generic root;
- local-only resources are selected only from the local root;
- a local manifest may depend on generic resources;
- a generic manifest may not depend on local resources;
- a local manifest may not reuse or replace a generic `resource_id`;
- a local manifest may not reuse a generic serialized path;
- duplicate IDs or paths are errors even when content hashes are equal;
- there is therefore no winner-by-precedence rule and no shadow replacement.

“Generic before local” is validation/dependency order, not overwrite
precedence. A future replace-capable overlay would be contract-breaking for v1
and requires an explicit new policy/version and human decision.

### Dependency and compatibility behavior

Every selected reference must exist in the validated manifest pair. Dependencies
are complete, acyclic, and selected by stable ID. Missing dependencies produce
`PIH.RESOURCE.MISSING_DEPENDENCY`. Unsupported resource kind or format version
produces the corresponding resource issue before file access. A local dependency
may target either layer; a generic dependency may target only generic.

Profile, manifest, resource-format, and skill-behavior compatibility are checked
independently. An incompatible version fails; it is not silently upgraded,
downgraded, or fetched. There is no network or ambient global fallback. A
fallback can exist only as another explicit caller-supplied manifest/root under a
future accepted policy; no such v1 policy is included.

### Identity and selected content

`manifest_id` is opaque identity and `manifest_version` is its resource-contract
revision. The profile binds ID and version; the action's explicit identity argument binds
SHA-256 of canonical manifest JSON bytes, preventing silent same-ID/version
content drift without embedding a circular manifest hash in the profile.
Each resource reference owns the expected exact file-byte identity. Selection
succeeds only when the selected file hash matches that identity.

A hash mismatch produces no selected path/reference. Content identity implies
byte equality only. Media type, resource kind, format version, and behavior
version remain separate represented facts; matching bytes do not prove that two
resources are behaviorally or semantically interchangeable.

## Deterministic failure behavior

Manifest/identity/version errors are reported before path and filesystem errors;
path grammar errors precede existence and hash checks. Within each stage,
resources and issues use the common deterministic ordering. A duplicate or
ambiguous identity prevents selection rather than choosing the first entry.

The resolver has read-only filesystem side effects: metadata inspection and
byte hashing under supplied roots. It performs no writes, installation, import,
execution, dispatch, network access, Git lookup, package discovery, cache
mutation, or cleanup.

## Workstation independence and validation modes

Serialized paths and wire results never include an absolute workstation root.
Clean-revision validation records the revision and explicit roots externally to
the generic records. An optional local pre-commit check is a separate invocation
against an explicitly supplied worktree and cannot replace clean-revision
validation. Personal, meeting, conference, paper, notebook, or concurrently
edited working files are not manifests, overlays, fallback resources, or
validator inputs unless a later explicit task contract intentionally and
lawfully declares them; H1 declares none.
