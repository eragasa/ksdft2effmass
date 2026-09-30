# Main recovery promotion authorization

## Status

Resolved human authorization for one protected branch update.

## Human instruction

The operator instructed:

> Adopt recovery/calculations-working-state-20260927 at f74084aa wholesale as the
> new main, after the preflight audit, and push it without force.

The preflight found one provenance-schema verification failure caused by the absent
optional RFC 3339 validator. The operator selected correction before promotion and
then explicitly selected the dependency-based correction. That correction is commit
`cb7f41b5` and adds `rfc3339-validator>=0.1.4` to the development dependency set and
resolved lockfile.

## Authorized branch operation

The authorized operation is a non-force fast-forward of `origin/main`, whose audited
starting identity is `ea21ec3dc7da39125dff90a7613c704e930787a2`, to the current tip
of `recovery/calculations-working-state-20260927` after this authorization record is
committed. The promoted history includes `f74084aa416664612b2a0bdcc446f8d63d8c111d`,
the selected wholesale recovery boundary, the deterministic provenance-format
dependency correction, and this durable authorization record.

This authorization does not permit force-pushing, history rewriting, tag creation,
release creation, package publication, DOI changes, or any other remote branch
update. The push must stop if `origin/main` no longer equals the audited starting
identity or if the update is not a fast-forward.

## Preflight evidence

The audited recovery boundary was a clean fast-forward descendant of `origin/main`.
The dry-run push required no force. Current-tree secret-pattern checks found no
private-key, GitHub-token, or AWS-access-key pattern. Ruff and formatting passed.
The complete Python test suite passed with `4319 passed, 3 skipped`; the skips require
external Quantum ESPRESSO QEXSD artifacts and are not promoted into passing evidence.
The focused provenance contract suite passed with `160 passed`. The three retained
external-artifact skips establish no external-artifact verification.

The historical comparison from the old `main` contains five pre-existing trailing
whitespace findings and historical SQLite blobs up to approximately 8 MB. The current
tree does not retain the Harness SQLite state file; the largest current tracked file
observed by the audit is approximately 3 MB. These historical facts are accepted as
part of the operator's wholesale recovery-history selection and are not represented
as software-verification failures of the current tree.

## Completion condition

Completion requires pushing the exact authorization-record tip to `refs/heads/main`
without force, fetching or querying the remote afterward, and verifying that the
remote `main` identity exactly equals the local promoted identity. The existing
recovery branch may remain separately configured; this operation does not push it.
