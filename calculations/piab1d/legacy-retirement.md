# PIAB1D legacy retirement

## Scope and authorization

The operator explicitly authorized a QHO1D-style compatibility audit and deletion of the
PIAB1D predecessor after the direct typed lifecycle replaced its maintained calculation,
verification, visualization, and report behavior.

The retirement removes exactly 62 tracked files:

- 44 flat calculation, custom-verifier, plot, checksum, calculation-local analysis, and
  duplicate development-report files;
- eight installed predecessor files from `model_systems/piab1d/study/` and the now
  orphaned generic `model_systems/study/` package; and
- ten predecessor tests and test-ownership records.

The exact sorted inventory is retained in `legacy-retirement-paths.txt`. Direct scripts,
the direct execution, maintained technical report, protocol, Appendix D drafts, and
Architecture v3 documentation are outside the deletion scope.

## Compatibility audit

The audit found no remaining supported Python consumer of the predecessor wire or
`study/` API outside its own tests and package-root re-exports. Those exports, tests, and
the orphaned generic study base were removed together. The Sphinx campaign boundary now
links the direct contracts rather than indexing removed classes.

The Appendix D Markdown and LaTeX sources were migrated from flat figures to the
authenticated direct-execution figure inventory. The protocol evidence table now points
to the typed direct result, byte-owning verification, and development-provenance record.
The maintained technical-report ladder generator now admits the direct result only after
checking its retained typed verification and subject digest. The duplicate development
report source and assets had already been promoted as byte-identical copies into
`technical_report/` before that maintained report evolved and the duplicate was removed.

A clean temporary direct run reproduced the retained result and verification bytes
exactly and reproduced all 13 PNG bytes. The rendering manifest retains its original
execution-time source digests and was not rewritten after later renderer consolidation.
Focused PIAB1D, QHO1D-removal, and Mathieu1D tests, package-wheel tests, strict typing,
Ruff, and Sphinx with warnings as errors passed after removal. These checks establish
software compatibility only.

## Recovery authority

Every removed byte remains recoverable from revision
`2ea109d5165366bc507d8900cf85a67de1a2bf73`.

| Recovery property | Value |
|---|---|
| File count | 62 |
| Sorted path-inventory SHA-256 | `66a1feef783ec19e3d4c4a170f5a8469d67ff944912df5dd4dc88a906587bccf` |
| Sorted path-and-content-digest SHA-256 | `ce325e8d6a5d4ae831dbfd20ac3a98b9ee6a3bacf852a1fb32034379dbdf1c3c` |
| Duplicate development-report tree | `9737c0ba0c6ca3d6f9ba0d3fef783f803d922774` |
| Calculation-local analysis tree | `173d4c7bce130be3654051cee1b5c28dbc541fd9` |
| Installed PIAB1D `study/` tree | `887bbc03b524be67fe0a4e78db97300017ceccdd` |
| Orphaned generic `model_systems/study/` tree | `eb75ee2772611de88e969a64d919a90e438d213b` |
| PIAB1D predecessor-test tree | `74ac3f83ffefcb1702396f5267892b6e6c222550` |
| Historical `SHA256SUMS` blob | `63a44785cc9669f932de043915d335a86d1042cf` |

For example, one removed source file can be recovered without restoring the predecessor:

```console
git show 2ea109d5165366bc507d8900cf85a67de1a2bf73:python/src/ksdft2effmass/model_systems/piab1d/study/records.py
```

The historical checksum catalog was composite rather than a single-tip checksum
contract. Thirty-one entries matched the pre-retirement live tree, four named later
versions of live paths, and four named already removed producer scripts. All eight stale
or absent rows reproduce their recorded hashes at revision
`daf3e3fa175955babbe7cca0530412bc6700d6f4`.

These locators establish recovery only. They do not reactivate a supported API, restore
a live wire contract, or establish scientific validity.

## Direct replacement

The maintained surface is:

```text
calculations/piab1d/run_01_calculation.py
  → run_02_verification.py
  → run_03_render.py
```

The sole retained execution is
`calculations/piab1d/executions/direct-core-n8-m3/`. Its result, 79-comparison independent
verification, authenticated 13-figure inventory, and development-provenance record remain
unchanged and explicitly unsealed. `technical_report/` retains the maintained report and
local copies of its required assets.

The Appendix D Markdown and LaTeX drafts now reference authenticated direct-execution
figures. The protocol maps its evidence table to the direct result, verification, and
development-provenance records.
