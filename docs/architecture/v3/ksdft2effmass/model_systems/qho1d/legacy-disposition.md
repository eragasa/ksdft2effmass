# Legacy QHO1D removal record

## Decision

The JSON-authored QHO1D predecessor was removed from the current tree after completion
of the direct typed calculate → verify → render migration. The removal was explicitly
authorized on 2026-10-26. It does not delete Git history, rewrite a retained direct
execution, seal evidence, establish scientific validation, publish a result, or create
a release.

The direct owner is now the only maintained QHO1D calculation surface:

```text
calculations/qho1d/run_01_calculation.py
  → run_02_verification.py
  → run_03_render.py
```

## Removed surface

The authorized removal covered:

- `calculations/qho1d/input.json`;
- `calculations/qho1d/dev_analysis.py`;
- `calculations/qho1d/dev_verification.py`;
- `calculations/qho1d/dev_plots.py`;
- `calculations/qho1d/analysis/development/`;
- `calculations/qho1d/development_report/`;
- `python/src/ksdft2effmass/model_systems/qho1d/study/`;
- the associated QHO1D root re-exports;
- the `campaigns.research_monograph` `HarmonicOscillator...` aliases;
- predecessor-only tests, test-ownership entries, and API documentation; and
- the unused QHO1D values in the shared historical study-identity enums.

The adjacent-grid coarse/fine Frobenius diagnostic was the only predecessor scientific
analysis selected for migration. Its maintained typed owner is `Qho1dCrossGridAnalyzer`,
with derivation checks owned by `Qho1dCrossGridVerifier`.

## Recovery locator

Commit `7e3331eb3addd8034cdf97cc2a65e64c4f74ac67` is the last complete committed tree
containing the predecessor and report. The following Git tree object identities locate
the complete removed directories at that commit:

| Removed directory | Git tree object |
|---|---|
| `calculations/qho1d/development_report/` | `0d6d1cc64c1b818302fde92049159f79ba092c6e` |
| `calculations/qho1d/analysis/development/` | `96233b34ccba706a9f89dca87a9282a3cd836e0a` |
| `python/src/ksdft2effmass/model_systems/qho1d/study/` | `6ebba155937e4a20e380865210a859dc63d001f8` |
| `python/tests/ksdft2effmass/model_systems/qho1d/study/` | `3273437a4f9b50617d0ae12f1afe158702c1ad7e` |

Principal exact-byte identities at that commit were:

| Removed path | SHA-256 |
|---|---|
| `calculations/qho1d/input.json` | `93d8d987bc18320402eb0a2beabde829a51a5f43f6aefdf291cfcf9fea03b9d9` |
| `calculations/qho1d/dev_analysis.py` | `def531aa1ad7c74e5879c7f476808ef9a04b813cc95041d3677e9c4805363913` |
| `calculations/qho1d/dev_verification.py` | `c164e92477147be955d36d91bfa9eafef030cd46063e5a8255f4ca9fed625fc6` |
| `calculations/qho1d/dev_plots.py` | `c6ea9c676100181080daabfe4cd782cbd39759c6bc27cf90436b86e3c06219d6` |
| `development_report/README.md` | `ae911d6ec0f2affde6f8321de43f24afd68fe9bfe420420c8ae798b4fd36d472` |
| `development_report/development_report.tex` | `11fa387a02342c1035cc051de15c5cb44501dadeab84202a9834b2417d2de9b5` |
| `development_report/development_report.pdf` | `b4bf3897aef9a9c5a2d57f4fa42eebe5a27afabe4485b56a43b8ae44903e232d` |
| `development_report/qho1d-eigenstates.png` | `d016e16a6ecc2eea216a8e329347f1c878febb7839c096384e2009c5cb328ca7` |
| `development_report/qho1d-eigenstate-distortion.png` | `792b8a6b80806f62efd1b6f18562d7fa21d9b76792b15c97725e744076508a66` |
| `development_report/qho1d-diagnostics.png` | `5476634b34c30a67244a7f541484465d11bc748dbfafc311cf2c28a2346ed58a` |
| `development_report/references.bib` | `bf2abdb9d3814ef8076abc30182bd1305a202e2b06194f71847871ef452b353a` |

These identities permit audit and byte recovery from Git. They do not make the removed
surface supported or restore its APIs.

## Historical report qualification

The removed report source embedded result SHA-256
`e22e83398b7f77d1ad3717e6789da30847092af5eebf5af4ebe9c7f7d57ac25d`, while its
README associated the report-local figures with result SHA-256
`1bc17c2911ede0d679af080442a7331a18972213f9ad464a4f6fb6937d2f961a`.
The latter ignored local result passed the predecessor verifier during the removal
audit. The report was therefore an unsealed historical review snapshot with an
unresolved internal result-correlation mismatch, not exact retained evidence.

## Retained direct artifacts

The earlier direct execution
`calculations/qho1d/executions/direct-spatial-truncation-3x3x3/` remains because the
research monograph consumes its authenticated figures and exact result and verification
identities. Flat direct-result decoding and three-component direct-verification decoding
also remain so that this artifact stays byte-exact, decodable, and renderable.

Those retained direct contracts are not the removed JSON-authored `study/` predecessor.
The maintained technical report uses the semantic-section execution
`direct-spatial-truncation-3x3x3-sections/`.

Execution-bound report snapshots created before this removal may mention the former
`development_report/` path. They remain unchanged because their byte identities are
already recorded; this page is the additive qualification.
