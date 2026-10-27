# Experiment-tree removal readiness

## Scope

This audit evaluated whether the final 35 tracked files under
`experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/` had
complete calculation-side ownership or explicit provenance-only dispositions. The audit
itself did not authorize deletion; the operator subsequently authorized the exact
35-file removal recorded below.

The removal predecessor is merge revision
`011eee90f7be30770dd5fb2db844fe35633755fc`. The original 40-file partition baseline is
`c49aaf816702c321cdd649e2567af70da57246fe`.

## File coverage

[`experiment-removal-manifest.json`](experiment-removal-manifest.json) binds every final
pre-deletion source path and SHA-256. Its closed partition is:

| Disposition | Count | Meaning |
|---|---:|---|
| `exact_duplicate` | 13 | Pre-deletion source and calculation-owned destination bytes were identical. |
| `superseded_predecessor` | 12 | The source was a digest-bound baseline predecessor; the calculation owner has an explicitly identified successor. |
| `adapted_predecessor` | 9 | The source was a non-maintained script donor with a calculation-owned effect adapter and recorded parity/recovery history. |
| `provenance_only` | 1 | The local `.gitignore` duplicated repository-root policy and remains Git-recoverable. |
| **Total** | **35** | Every final pre-deletion file had exactly one disposition. |

The three protocol files already moved byte-exactly into `protocol/`, and the two README
donors were removed only after integration. Together with these 35 entries, this closes
the original 40-file partition.

## Nested ownership and protocol authority

- [`nested-channel-crosswalk.md`](nested-channel-crosswalk.md) separately identifies the
  flat, nonflat, parent-family, truncation, refinement, diagnostic-packaging, rendering,
  and protocol channels, including their classes, serializers, schemas, effect adapters,
  artifacts, and retained-lifecycle gaps.
- [`protocol-authority-and-historical-donors.md`](protocol-authority-and-historical-donors.md)
  distinguishes the concise current boundary from the complete buildable prospective
  bundle and records conflict rules.
- The same document binds the removed M2 and research-monograph periodic-1D donor trees
  at revision `c5d34a93b4710a4a430738c404c775865d418d42`, their Git tree objects and selected
  artifact digests, plus the finite-angle regression revision. Those scientifically
  distinct donors are not merged into this family.

Open direct-lifecycle and reusable-source work does not require keeping obsolete
experiment-tree duplicates. It remains mandatory before proposing a retained execution.

## Consumer independence

Repository searches after recovery establish:

- no Ragasa2026a v3 Markdown or TeX source contains an `experiments/` input path;
- no Python, TOML, JSON, YAML, or test/runtime surface consumes the exact experiment
  path; and
- the only exact path references outside migration records and the source tree are:
  1. the presentation asset's historical copy-time locator; and
  2. two immutable Git locators for the removed finite-angle regression fixture.

These are documentary predecessor references, not build or runtime dependencies.

## Removal-readiness correction

Review found that recovery revision `011eee90...` had promoted a dirty scientific-story
PDF identical to the separately qualified presentation copy
`9e88e334c7b6c3ae25fbd264428d128d2ba17f16121ed8613c2412c886c1e9be`.
That contradicted the recorded separation between the presentation asset and the
maintained calculation figure. This branch restores:

- scientific-story PDF:
  `191d8fff0dbc777a6268c0e1e3dd481f8160da11bc9b5797510919ca9e57b2a8`;
- scientific-story PNG:
  `b323ab00db328a3e0ad4304781d9ac79f68396861b15e1e24dc183793fea05ce`;
- the corresponding pre-recovery calculation plotter.

The rejected dirty PDF and PNG remain exactly recoverable from `011eee90...`; the dirty
plotter has an exact recorded source hash and a recoverable calculation-path-adapted
candidate at that revision. All three have explicit source-only dispositions in
`recovered-development-source-manifest.json`.

## Validation

The non-destructive review completed these checks from the removal-readiness branch:

- removal-manifest path-set, source-hash, destination-hash, and disposition validation:
  35/35 files;
- recovered-source manifest validation: 55 exact, 23 adapted, and six source-only
  dispositions, including recovery-revision checks;
- historical donor digest verification: 12/12 selected M2 and monograph-composite files;
- focused calculation tests: 33 passed; four direct-invocation warnings reported the
  repository-specific `software_verification` marker as unregistered because the tests
  were invoked outside the `python/` pytest configuration;
- Ruff check and format check: 58 files passed;
- calculation-owner `compileall`: passed;
- Sphinx HTML build with warnings treated as errors: passed;
- calculation-owner local Markdown links: 81 checked;
- protocol bundle SHA-256 identities: unchanged;
- restored scientific-story scratch rendering: PNG byte-exact, PDF 150-dpi rendering
  exact, and PDF bytes exact after normalizing only `CreationDate`/`ModDate`; and
- `git diff --check`: passed.

## Authorized removal

The operator separately authorized the recommendation to delete exactly the 35 manifest
entries. At `2026-10-27T06:37:02Z`, a preflight required:

- the manifest source set to equal the complete tracked set beneath the authorized family
  path;
- the filesystem file set to equal that same 35-path set, so no untracked file could be
  removed accidentally; and
- every source SHA-256 to match the manifest before unlinking.

All conditions passed. Exactly those 35 files were removed, and the authorized family
path is absent. No other periodic-1D experiment family, calculation owner, retained run,
historical Git object, publication asset, or parent experiment directory was removed.
The deletion is recoverable from revision
`011eee90f7be30770dd5fb2db844fe35633755fc`. Its authorization did not include commit,
push, pull-request creation, or merge.

Post-removal validation established:

- all 35 deleted bytes remain digest-exact at the predecessor revision and all 34
  calculation destinations remain digest-exact;
- every deletion reported by Git remains beneath the one authorized family path;
- 34 focused calculation and experiment-convention tests passed;
- Ruff check/format over 58 calculation files, scratch-cache `compileall`, Sphinx with
  warnings as errors, JSON parsing, and `git diff --check` passed;
- 99 in-scope Markdown links passed; and
- consumer searches still found no Ragasa2026a, runtime, test, or configuration
  dependency on the deleted path.

A broader link scan of the modified repository-level `calculations/README.md` also
reported 19 pre-existing links to unrelated historical calculation trees removed before
this tranche. The two links changed here both resolve. Repairing those unrelated
historical locators is safe to defer and is not a blocker for this family removal.

## Technical conclusion

The bounded experiment-tree removal has no current technical blocker. Commit, push,
pull-request creation, and merge remain separate protected actions; the removal
authorization did not include them.

This conclusion does not authorize retained execution, sealing, release, or publication.
It does not establish scientific validation or convert development outputs into retained
evidence.
