# Mathieu1D experiment removal readiness

## Decision

**Removed after separate authorization.** The 65-file source inventory was closed,
every source had a calculation-side destination or explicit provenance-only disposition,
maintained publication and documentation consumers used calculation-owned paths, and the
non-destructive checks below passed before removal.

The operator separately authorized the recommended exact removal in the active session.
Exactly the 65 manifest-bound files were removed at `2026-10-27T14:02:06Z`; no other
experiment or calculation file was removed. That authorization did not permit calculation-side predecessor-byte changes, scientific
execution, evidence replacement, sealing, release, or publication. A later authorization
covered direct recalculation, consumer replacement, and deletion of all calculation-side
predecessor run artifacts.

## Pre-removal package audit

Before experiment-donor removal, the calculation and experiment surfaces each contained
the same four predecessor run directories:

- `...v1.run-20261014T183028Z`;
- `...v1.run-20261014T183603Z`;
- `...v1.run-20261014T183721Z`; and
- `...v1.run-20261014T184707Z`.

For all eight pre-removal filesystem copies, the audit verified:

- the evidence-package identity equals the SHA-256 digest of `SHA256SUMS`;
- every checksum catalog has nine unique entries;
- every listed file matches its recorded digest; and
- each experiment run directory is byte-identical to its calculation destination.

The 44 run-directory files were read but not rewritten at that gate. They and the runs
README were later deleted from the live tree. Their exact Git recovery boundary is
[`legacy-run-retirement.md`](legacy-run-retirement.md).

## Predecessor recovery

The publication-facing run records historical predecessor revision
`9a65849d886d5be499b2664e2b653c3983fab06e`, path
`calculations/ICMSEP2026/conference/paper_1/isolated-band`, and Git tree
`418999a90efa3001d2e50a2e7912f126bc30903f`. Reading that Git object directly confirmed
the recorded tree and these four SHA-256 values:

| File | SHA-256 |
|---|---|
| `SHA256SUMS` | `64f16168fa05fefa902f8c2216b1e445c6a0ecd8e28dcebd75c73589833edf5f` |
| `input.json` | `62899d4cd550db9d0bd69a8d97149ccfea312c6b20be9c395e8765734693bf65` |
| `result.json` | `c7262e3527a58dfd8fe237fa495549c53a1a65f3e46a98ed6d40673f14b6a394` |
| `verification.json` | `9b37dc896a3a438a04dc19c46dd9d431230901ef82bfd9e7181ff5b7504b21a1` |

The predecessor was removed from the live tree by
`6c17150bce8bf339e9c818453a0ef0572d34e17a`. Restoration of that historical calculation
is neither required nor authorized by this audit.

## Verifier reconciliation

`calculations/mathieu1d/run_02_experiment_verification.py` checks the publication-facing
package identity, catalog entries, canonical JavaScript Object Notation (JSON), strict
schemas, recorded pass values, dependency revisions, and source manifest. It now also
reads the historical predecessor directly from its recorded full Git revision, verifies
the recorded Git tree identity, and hashes the original blob bytes for all four recorded
predecessor files.

The verifier passed without restoring the deleted predecessor directory and without
changing retained package bytes. It was later retired with the other calculation-side
legacy code after direct-successor parity; its exact source remains recoverable through
[`direct-successor-retirement.md`](direct-successor-retirement.md). The removed
experiment-side `verify_package.py` remains recoverable as a historical donor and is not
a maintained execution route.

## Development-environment reconciliation

The duplicate calculation-local `pyproject.toml` and `uv.lock` were removed. The
repository Python project is now the only live dependency authority, and the focused
live-revision test uses its reviewed Optimization and PhysKit revisions.

The removed experiment-side project and lock files are provenance-only donors in the
65-file migration manifest and remain recoverable from the baseline revision. The later
predecessor-run deletion did not change the repository dependency authority.

## Consumer migration

At the experiment-donor removal gate, the following maintained consumers had migrated
to `calculations/mathieu1d/`:

| Consumer | Completed disposition |
|---|---|
| `docs/publications/papers/Ragasa2026a/v1/experiment-references.json` | Publication-facing package, source manifest, and artifact paths redirected; artifact digests and evidence-package identity preserved. |
| `docs/publications/research-monograph/experiment-references.json` | The same authenticated calculation paths now serve the monograph. |
| `docs/publications/papers/Ragasa2026a/v1/manuscript.md` | Retained figure link redirected. |
| `docs/publications/papers/Ragasa2026a/v1/manuscript.tex` | Retained figure input redirected. |
| `docs/publications/research-monograph/appendices/G-periodic-reduction-experiments.tex` | Maintained family locator and retained figure input redirected. |
| `docs/publications/papers/experiment-to-paper-allocation.md` | Publication allocation redirected to the calculation owner. |
| `experiments/README.md` | Family index redirected to the calculation owner and marked migrated. |
| `calculations/README.md` | Donor path qualified as historical and bound to the recovery revision. |
| `docs/architecture/v2/ksdft2effmass/analysis/single-band-hopping-reduction.md` | Calculation owner identified as the maintained consumer. |
| `docs/architecture/v2/ksdft2effmass/calculation-campaign-identity-registry.md` | Maintained locator updated; the baseline schematic remains explicitly historical. |
| `docs/architecture/v2/ksdft2effmass/single-band-experiment-workflow-migration.md` | Maintained composition now starts at the calculation owner. |

At that removal gate, the two publication manifests were the only
`experiment-references.json` files consuming the family. Their redirected SHA-256
values were `72c779c62d62e4d4feda71fb816d31703ecdfca8177843ba38cab8b9c60ba484` for
Ragasa2026a version 1 and
`16135594fdc140b3302f91c79d7b36920bd0dc47f9e4a16257196c12bfb43cb8` for the research
monograph.

A later separately authorized direct-lifecycle migration recalculated the finite result,
independently verified its exact bytes, produced authenticated replacement figures and a
buildable report, and moved Ragasa2026a and the research monograph to that direct
execution. A subsequent authorization removed all four predecessor runs and their runs
README. No live publication manifest now binds a predecessor artifact.

## Git recovery references

Historical bytes are absent from the live tree. Recovery references are confined to the
migration manifest and the compact retirement ledgers. The predecessor run tree is bound
by [`legacy-run-retirement.md`](legacy-run-retirement.md); the experiment donor remains
recoverable from Git revision `c73aa96077ee03e1f7438ecbb44349b445a3eec8`.

## Non-destructive validation

The experiment-donor removal review established:

- the source filesystem and tracked-file set both contain exactly the 65 manifest paths,
  with no untracked file beneath the donor;
- all source and destination/disposition digests pass: 53 exact duplicates, 10 adapted
  or integrated successors, and two provenance-only environment donors;
- all eight retained package copies pass evidence-identity and checksum-catalog checks;
- both redirected publication manifests are canonical JSON, resolve every artifact, and
  preserve every artifact digest and the evidence-package identity;
- the Git-bound package verifier passes without restoring the predecessor;
- all 10 focused Mathieu1D tests and all 16 manuscript-auditor tests pass;
- strict mypy passes over the 10 Mathieu1D implementation and test files;
- Ruff and formatting checks pass over the same calculation package;
- the root dependency lock check passes;
- Sphinx builds with warnings treated as errors;
- the 496-page research monograph builds in scratch and loads the calculation-owned
  Mathieu1D figure; and
- repository search leaves only qualified migration, baseline, and immutable provenance
  occurrences of the experiment path.

The Ragasa2026a version-one manuscript also resolves and loads the redirected Mathieu1D
figure. Its complete scratch build remains blocked later by pre-existing absent
multiband, admissible-set, periodic-2D, and silicon-preview assets unrelated to this
migration. Five corresponding Markdown links were already broken. No missing asset was
fabricated or copied from an unauthenticated worktree.

## Removal record

The exact removal was bounded by the 65 source paths and SHA-256 digests in
[`experiment-migration-manifest.json`](experiment-migration-manifest.json). Immediately
before deletion, the filesystem set, tracked-file set, and manifest set were identical,
and the donor had no untracked files. Immediately after deletion, Git reported exactly
65 staged source deletions and the donor directory no longer existed.

Recovery authority for the experiment donor remains Git revision
`c73aa96077ee03e1f7438ecbb44349b445a3eec8`, source tree
`bf20cf55a06c9eaae72f34093b72da0ea00c9240`, and the manifest's per-file source digests.
The later calculation-side predecessor-run removal is separately bound to Git tree
`48ba8cff3a2567a4d955c30f0f4bc570dc425a74` in
[`legacy-run-retirement.md`](legacy-run-retirement.md). Neither removal changes or
strengthens any scientific claim.
