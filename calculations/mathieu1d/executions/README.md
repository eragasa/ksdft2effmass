# Mathieu1D direct executions

This directory owns executions of the direct typed
`mathieu1d-finite-reduction` lifecycle. The predecessor `runs/` tree has been removed;
[`../legacy-run-retirement.md`](../legacy-run-retirement.md) records its Git recovery
boundary without retaining any predecessor artifact in the live tree.

## Retained execution

[`direct-finite-reduction-n64/`](direct-finite-reduction-n64/) is a retained **unsealed**
local deterministic execution produced by:

```console
uv run --project python python calculations/mathieu1d/run_01_calculation.py
uv run --project python python calculations/mathieu1d/run_02_verification.py
MPLBACKEND=Agg uv run --project python python calculations/mathieu1d/run_03_render.py
```

The scripts refuse to overwrite any completed stage. The execution records dirty-
worktree qualification at committed base
`2ea109d5165366bc507d8900cf85a67de1a2bf73` and contains exact typed configuration,
result, independent verification, authenticated rendering, two PNG figures, and a
buildable technical-report snapshot.

| artifact | SHA-256 |
|---|---|
| `inputs/configuration.json` | `cc1b1c2d61f764315700bd60f178c0bf013255821630dd11e9f52c42c914ca54` |
| `results/result.json` | `83d25e824a0aedf085e77e86a998c02a17d4a51c320375b0bfb395986dae3fe6` |
| `verification/verification.json` | `61553c16636efc39452706006dc480b827c2f2d04f3e318e02e3c2eec4f24664` |
| `figures/mathieu1d-finite-reduction.png` | `de0ae08bd6e4c16afee074b14a73be2a7efbfa133044fc08ee75492238886b7e` |
| `figures/mathieu1d-publication-summary.png` | `243722cfd538943dce572b32b1104e587371d88b59d13181c369ccfdac7d6c6c` |
| `figures/rendering.json` | `05f02f3a07d8514df581b8380b47a8b259aec9df5184359ec586e850c496f97b` |
| `technical_report/technical-report.pdf` | `ee5fde28270bc183df18175f8abd3b916a74351993ee44af639c4076abfd7416` |

These hashes establish byte references only. The execution does not establish continuum
convergence, uncertainty quantification, material validity, publication acceptance,
evidence sealing, or release.
