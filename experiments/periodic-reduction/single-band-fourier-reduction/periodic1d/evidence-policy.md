# Retained-evidence and failure policy

A successful retained run directory contains canonical `input.json`, `result.json`,
`verification.json`, exact `provenance.json`, `report.md`, publication-ready figure
data and image, `source.sha256`, and `SHA256SUMS`. The run identity names one execution
of immutable version `v1`. The evidence-package identity is
`sha256:<SHA-256(SHA256SUMS bytes)>`; it does not include `SHA256SUMS` itself and is
therefore non-recursive.

Canonical JSON is UTF-8, sorted by key, compact, finite, and terminated by exactly one
line feed. Documents must validate against their version-bound schemas with unknown
properties rejected. Evidence consumers must verify file digests before interpreting
values.

`provenance.json` binds the repository base revision, dirty-worktree source manifest,
exact dependency revisions, runtime, local-only execution boundary, and exact
historical predecessor revision/path/tree/file digests. A dirty worktree is not
misrepresented as the base commit; `source.sha256` identifies every in-scope source
file used by the run. The immutable version-one dependency pair remains in the
experiment-owned project and lock records. Repository-level development dependencies
may advance after the run; package verification must not reinterpret those later pins
as execution provenance.

Any execution, serialization, strict-schema validation, digest, or independent
verification failure prevents a success disposition. Failed attempts may be retained
only in separately identified directories with the failure and incomplete outputs made
explicit. Publication manifests may cite only a successful run whose byte identities
and independent verification pass. No retained outcome selects a scientifically
adequate range, certifies continuum isolation, validates a material, or supplies
uncertainty quantification.
