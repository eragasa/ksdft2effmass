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

## Protected-branch continuation

GitHub rejected the direct non-force update because the required `Python 3.14` status
check was absent. The operator then explicitly authorized pushing the recovery branch,
creating pull request #7, and adding a real Python 3.14 GitHub Actions check. The
operator required calculation-heavy tests to be marked expensive and omitted from the
bounded hosted check. This authorizes the external GitHub-hosted CI execution for that
check; it does not authorize any scientific, Quantum ESPRESSO, Wannier90, cluster, or
cloud calculation.

The hosted check runs formatting, Ruff, production-source mypy, the Sphinx build, and
pytest with `-m "not expensive"`. The retained periodic-2D Stage B and Stage C workflow
suite is explicitly marked `expensive`; it remains covered by the complete local
preflight result and is reported as deselected, not passing, in hosted CI. The three
external-QEXSD cases retain their explicit skips and are not promoted into passing
evidence.

## Completion condition

Completion requires the exact pull-request tip to pass the required `Python 3.14`
check, merge to `refs/heads/main` without force, and remote identity verification. The
recovery branch was pushed only to satisfy the authorized protected-branch workflow;
no other branch, tag, release, package, or publication action is authorized.
