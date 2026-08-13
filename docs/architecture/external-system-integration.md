# External-System Integration

External scientific artifacts are not repository resources and are not committed.
Git-tracked records identify them through portable logical stores rather than
user-specific absolute paths.

## `user_opt` store

The `user_opt` store resolves explicitly to `~/opt`:

1. expand the current user's home directory;
2. append `opt`;
3. canonicalize the root with physical-path resolution;
4. reject a symlink at the declared root;
5. join a normalized relative path that has no empty, `.` or `..` component;
6. canonicalize the candidate's existing parent and file;
7. require the result to be strictly contained beneath the canonical root; and
8. reject a symlink at the artifact and any symlink found in its declared
   installed directory tree.

A lexical prefix check alone is insufficient. Failure of canonicalization,
containment, regular-file identity, or the expected digest stops preflight or
execution.

The selected production-Si reference is:

```json
{
  "store": "user_opt",
  "relative_path": "pseudodojo/1.0/pbe/nc-sr-04-standard/Si/Si.upf",
  "version": "1.0",
  "sha256": "39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282"
}
```

It resolves locally to
`~/opt/pseudodojo/1.0/pbe/nc-sr-04-standard/Si/Si.upf`. The installed
`manifest.json` and compressed source remain beside it. A run-local copy may be
made under an authorized campaign workspace, but that copy is derived execution
input and never authority.

The store contract establishes path resolution and artifact identity only. It
does not establish license permission, redistribution authority, executable
readability, numerical convergence, or scientific validation.
