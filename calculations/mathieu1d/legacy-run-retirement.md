# Mathieu1D legacy-run retirement

## Scope and authorization

The operator explicitly authorized removal of every live predecessor artifact under
`calculations/mathieu1d/runs/` after the direct Mathieu1D calculation, independent
verification, authenticated figures, technical report, and publication consumers had
been replaced. Exactly 45 tracked files are in scope. No direct-execution byte is in
scope.

The predecessor artifacts are removed from the live tree. They are not supported data,
runtime inputs, compatibility contracts, publication inputs, or retained repository
artifacts. The obsolete `calculations/mathieu1d/.gitattributes` rule that applied only
to removed `runs/**/figure-data.csv` paths was removed as part of the authorized live-
reference cleanup. Its recovery blob is
`a45ed9633fde1ceb22be04ae71a2eb43aa2b3fa7`, and its SHA-256 is
`10bd9cd47645107ff0bc44c492a352601dfcf5b98f010ef1e1e05abc61a4906d`.

## Git recovery boundary

The removed bytes remain recoverable only from existing Git history:

- recovery revision: `2ea109d5165366bc507d8900cf85a67de1a2bf73`;
- removed path: `calculations/mathieu1d/runs/`;
- removed tree: `48ba8cff3a2567a4d955c30f0f4bc570dc425a74`;
- tracked file count: 45;
- sorted path inventory SHA-256: `821527b467e0982fafb8e9b0016ff0111bda775b06e2b6986addf7a391bfac69`;
- sorted `git ls-tree -r` inventory SHA-256:
  `92147fbefa1a1cfb85778e00a044c68f19a501427edeb62bc02ac2b901a7ee73`.

The four removed child trees were:

| Historical execution suffix | Git tree |
|---|---|
| `...run-20261014T183028Z` | `f5075ffa24d25a47e5cbfad1dc2d8d52309c7185` |
| `...run-20261014T183603Z` | `5ef0ae9e5e035b003179f95990779624b025a456` |
| `...run-20261014T183721Z` | `7863c3b7db5d1fa7923899ef3542364788c7f940` |
| `...run-20261014T184707Z` | `d6c73e2822dbf4d4bebc6923db7fcb0250e4314a` |

Recovery, if ever separately authorized, is possible without rewriting history:

```console
git archive 2ea109d5165366bc507d8900cf85a67de1a2bf73 \
  calculations/mathieu1d/runs/
```

These Git references establish byte recovery only. They do not preserve a live contract
or establish scientific validity.

## Direct replacement

The only live Mathieu1D execution is
`calculations/mathieu1d/executions/direct-finite-reduction-n64/`. It was calculated by
the direct typed implementation and remains explicitly unsealed.

| Direct artifact | SHA-256 |
|---|---|
| `inputs/configuration.json` | `cc1b1c2d61f764315700bd60f178c0bf013255821630dd11e9f52c42c914ca54` |
| `results/result.json` | `83d25e824a0aedf085e77e86a998c02a17d4a51c320375b0bfb395986dae3fe6` |
| `verification/verification.json` | `61553c16636efc39452706006dc480b827c2f2d04f3e318e02e3c2eec4f24664` |
| `figures/mathieu1d-publication-summary.png` | `243722cfd538943dce572b32b1104e587371d88b59d13181c369ccfdac7d6c6c` |
| `technical_report/technical-report.pdf` | `ee5fde28270bc183df18175f8abd3b916a74351993ee44af639c4076abfd7416` |

Ragasa2026a and the research monograph consume only these direct artifacts. The direct
figure is generated from verifier-authenticated data recalculated by the new source; no
removed predecessor dataset is a rendering input.
