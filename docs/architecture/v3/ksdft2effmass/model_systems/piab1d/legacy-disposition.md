# Legacy PIAB1D disposition

## Decision

The JSON-authored and Workflow-shaped PIAB1D predecessor was removed after the direct
typed calculate → independently verify → authenticated render lifecycle replaced its
maintained behavior. The direct owner is now the only maintained PIAB1D calculation
surface:

```text
calculations/piab1d/run_01_calculation.py
  → run_02_verification.py
  → run_03_render.py
```

The removal was explicitly authorized. It does not rewrite Git history, alter the direct
execution, seal evidence, establish continuum convergence or uncertainty, validate a
material model, publish a result, or create a release.

## Removed surface

The completed retirement covers:

- flat version-one inputs and results;
- custom historical calculation, verification, and plot scripts;
- flat historical figures and the obsolete composite checksum catalog;
- the calculation-local analysis package;
- the duplicate `development_report/` tree;
- `ksdft2effmass.model_systems.piab1d.study` and its package-root exports;
- the orphaned generic `ksdft2effmass.model_systems.study` package; and
- predecessor-only tests and test-ownership records.

No removed class, wire decoder, result, figure, checksum row, or calculation-local module
is a supported runtime or publication input.

## Recovery authority

The detailed recovery record is
[`calculations/piab1d/legacy-retirement.md`](../../../../../../calculations/piab1d/legacy-retirement.md),
and its exact 62-path inventory is retained beside it. The recovery revision is
`2ea109d5165366bc507d8900cf85a67de1a2bf73`.

| Removed directory or catalog | Git identity |
|---|---|
| Duplicate development report | tree `9737c0ba0c6ca3d6f9ba0d3fef783f803d922774` |
| Calculation-local analysis | tree `173d4c7bce130be3654051cee1b5c28dbc541fd9` |
| Installed PIAB1D `study/` | tree `887bbc03b524be67fe0a4e78db97300017ceccdd` |
| Generic `model_systems/study/` | tree `eb75ee2772611de88e969a64d919a90e438d213b` |
| PIAB1D predecessor tests | tree `74ac3f83ffefcb1702396f5267892b6e6c222550` |
| Historical `SHA256SUMS` | blob `63a44785cc9669f932de043915d335a86d1042cf` |

The sorted path inventory has SHA-256
`66a1feef783ec19e3d4c4a170f5a8469d67ff944912df5dd4dc88a906587bccf`;
the sorted path-and-content-digest inventory has SHA-256
`ce325e8d6a5d4ae831dbfd20ac3a98b9ee6a3bacf852a1fb32034379dbdf1c3c`.
These identities permit audit and byte recovery only.

## Historical checksum qualification

The removed `SHA256SUMS` was a composite historical catalog, not a checksum contract for
one repository tip. Before removal, 31 entries matched live paths, four referred to
subsequently changed live files, and four referred to already removed producer scripts.
All eight stale or absent entries reproduce their recorded hashes at revision
`daf3e3fa175955babbe7cca0530412bc6700d6f4`.

The catalog was removed rather than regenerated because rewriting it would falsely turn
a mixed historical record into current evidence.

## Retained direct execution and reports

The sole live execution is
`calculations/piab1d/executions/direct-core-n8-m3/`. It was generated from clean source
commit `c8d808c6b8959dec8338207dff0450ebacc31646` and remains explicitly unsealed.

| Direct artifact | SHA-256 |
|---|---|
| Result | `7941264158f6662da4d6b34236bcb300f82b41018f3398d719c936437f30d8bf` |
| Verification | `d64dfbb7910ad64ab8d3eb0ccc78b97ad9665293d71c35dcfb54e147fc3274fb` |
| Rendering manifest | `f16bc2b7573b4f73f9ccb266b07b50b18feae864cbed2024aa309c86d273d095` |

`technical_report/` remains the maintained calculation report. The Appendix D draft
sources now consume authenticated direct-execution figures. The retained Appendix D PDF
is a historical review snapshot, not a sealed calculation artifact.
