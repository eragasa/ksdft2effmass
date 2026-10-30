# Review of the five old experiment files

## What this review covers

Five files remained under
`experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/` when
this review began. The review checked whether each file had a clear home under the
calculation folder. The review itself did not authorize deletion; the operator later
authorized the exact five-file removal recorded below.

The source revision is `81f7c09a5edc50be698bd3a5f047438cd61d4eca`.
Exact paths and hashes are stored in
[`experiment-removal-manifest.json`](experiment-removal-manifest.json).

## Where the five files go

| Old file | Current treatment |
|---|---|
| `experimental-protocol.tex` | Copied byte-for-byte to `protocol/experimental-protocol.tex`. |
| `run_development.py` | Replaced by the calculation-side script of the same name. Only the code owner and output directory differ. |
| `verify_d1_p0_g0_controls.py` | Replaced by `verify_analytic_controls.py`. The Python content is identical after removing the old shebang line. |
| `README.md` | Incorporated into the plain-language calculation README, protocol README, and migration records. |
| `.gitignore` | Replaced by rules for the calculation's current `results/` directory and standard Python caches. |

The old development runner imported a package that no longer exists. The last complete
copy of that package is at revision
`25161d7f55c708a464c18ea8d5d0fd6152ff86a6`, Git tree
`94f2f042322aa69969448ca77b8d47c163edef70`. It was removed in
`c5d34a93b4710a4a430738c404c775865d418d42`. At the time of this removal-readiness
review, the calculation's `workflow/` directory was the migration successor. Four of its
eleven Python files were byte-identical to that historical package; the other seven were
recorded as later successors in
[`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md). The directory
is now read-only historical provenance; maintained behavior belongs to
`ksdft2effmass.periodic1d.higher_rank_alignment` and canonical upstream owners.

## Documentation users

The following maintained documents now point to the calculation folder:

- the repository experiment and calculation indexes;
- the experiment-to-paper allocation table;
- the Ragasa2026c calculation-plan link;
- the Ragasa2026c finite-grid formula-check source link; and
- the proposed implementation-contract location in the architecture plan.

Repository searches found no Python, JSON, TOML, YAML, test, or build configuration that
uses the old experiment path. The only remaining exact old-path text outside the source
folder and this calculation's migration records is the repository calculation index,
where it is explicitly identified as the five-file historical donor pending removal.

## Checks completed

- The copied calculation plan has the same SHA-256 as the old file:
  `160b61b2c2dc87e7628524c710c779f8e3b2c547f0a2d228615300aa06bdce0b`.
- The 26-page plan built successfully in a scratch directory.
- The development runners have identical Python syntax trees after normalizing only the
  import owner and output directory.
- The two formula-check scripts are identical after removing the old shebang and produced
  byte-identical output on a 200-interval test grid.
- Twenty-nine focused calculation and ownership tests passed.
- Ruff checking and formatting passed for 31 calculation files.
- `compileall` passed with bytecode written to scratch storage.
- Sphinx built successfully with warnings treated as errors.
- All five manifest source hashes, destination hashes, and the historical implementation
  Git tree were verified.
- Forty-four in-scope Markdown links passed.
- Consumer searches found no maintained runtime or publication input that depends on the
  old path.

## What remains unfinished

The current development calculation does not yet have a stable typed result format, an
independent check of the complete result, authenticated plotted values, or a retained
run. Those are required before retained evidence can be proposed, but they do not require
keeping obsolete duplicate scripts and documentation in the experiment folder.

## Authorized removal

The operator separately authorized deletion of exactly the five manifest-listed files.
At `2026-10-27T12:05:11Z`, a preflight proved that:

- the manifest listed every tracked file under the old family path;
- the filesystem contained no additional untracked file under that path; and
- all five source hashes matched.

Exactly those five files were deleted. No other experiment or calculation family was
removed. The deleted bytes remain recoverable from
`81f7c09a5edc50be698bd3a5f047438cd61d4eca`.

Post-removal checks confirmed that all five predecessor hashes and current destination
hashes still match, all 44 in-scope links resolve, Sphinx builds with warnings treated as
errors, Ruff and `compileall` pass, and no runtime, test, build, configuration, or
publication input uses the deleted path. The first post-removal test command exceeded its
300-second command window after five tests; no test failure was reported. A clean rerun
completed all 29 tests successfully in 146.41 seconds.

## Conclusion

The bounded five-file removal is complete in the worktree with no current technical
blocker. Commit, push, merge, scientific execution, release, and publication remain
separate protected actions. This work does not establish scientific validation.
