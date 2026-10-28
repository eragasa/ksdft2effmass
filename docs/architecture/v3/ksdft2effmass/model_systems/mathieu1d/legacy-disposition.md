# Legacy Mathieu1D disposition

## Decision

The workflow-shaped Mathieu1D predecessor was removed after the direct typed
calculate → independently verify → authenticated render lifecycle replaced it. The
direct owner is the only maintained Mathieu1D calculation surface:

```text
calculations/mathieu1d/run_01_calculation.py
  → run_02_verification.py
  → run_03_render.py
```

The removal does not rewrite Git history, seal the retained execution, establish
continuum convergence or uncertainty, validate a material model, publish a result, or
create a release.

## Removed surface

The completed retirement covers four related surfaces:

1. the 65-file experiment donor under
   `experiments/periodic-reduction/single-band-fourier-reduction/`;
2. the calculation-local producer, package verifier,
   `single_band_fourier_reduction` package, and associated tests;
3. the installed `ksdft2effmass.model_systems.mathieu1d.study` package and predecessor
   exports; and
4. four predecessor run directories, the version-one input and schemas, and the
   run-specific attribute rule.

No removed class, wire decoder, schema, run artifact, or calculation-local module is a
supported runtime or publication input.

## Recovery authority

The detailed calculation records remain the exact-byte recovery annexes:

| Removed surface | Recovery record | Principal locator |
|---|---|---|
| Experiment donor | [`experiment-migration-crosswalk.md`](../../../../../../calculations/mathieu1d/experiment-migration-crosswalk.md) | revision `c73aa96077ee03e1f7438ecbb44349b445a3eec8`, tree `bf20cf55a06c9eaae72f34093b72da0ea00c9240` |
| Calculation-local code and tests | [`direct-successor-retirement.md`](../../../../../../calculations/mathieu1d/direct-successor-retirement.md) | revision `2ea109d5165366bc507d8900cf85a67de1a2bf73`, source tree `ea991f6d12cd17b5a3abec30bcbcd821d8e84f61` |
| Installed `study/` package | [`installed-successor-retirement.md`](../../../../../../calculations/mathieu1d/installed-successor-retirement.md) | revision `2ea109d5165366bc507d8900cf85a67de1a2bf73`, tree `7e9c91b7b95255b3f7c647c57b7b37562dc0d59e` |
| Predecessor executions | [`legacy-run-retirement.md`](../../../../../../calculations/mathieu1d/legacy-run-retirement.md) | revision `2ea109d5165366bc507d8900cf85a67de1a2bf73`, tree `48ba8cff3a2567a4d955c30f0f4bc570dc425a74` |
| Version-one input and schemas | [`legacy-contract-retirement.md`](../../../../../../calculations/mathieu1d/legacy-contract-retirement.md) | input blob `a59b30283dda8c44362889ad8bb6880184413401`, schemas tree `203f631200b8d2b6fbc91f2b1c0e4d1e79f4eba7` |

These identities permit audit and byte recovery. They do not reactivate the removed
surface or establish scientific validity.

## Machine-readable disposition

`calculations/mathieu1d/experiment-migration-manifest.json` preserves the original donor
to calculation-side crosswalk. A destination removed after that migration retains its
historical path and digest together with an explicit `destination_disposition`. The
manifest therefore distinguishes byte correspondence at the donor-removal gate from
current live ownership.

The direct lifecycle is not a compatibility revision of the predecessor wire. Its typed
configuration, result, verification, and visualization records are separate contracts.

## Retained direct execution

The sole live execution is
`calculations/mathieu1d/executions/direct-finite-reduction-n64/`. It remains explicitly
unsealed and records a dirty-worktree qualification.

| Direct artifact | SHA-256 |
|---|---|
| Configuration | `cc1b1c2d61f764315700bd60f178c0bf013255821630dd11e9f52c42c914ca54` |
| Result | `83d25e824a0aedf085e77e86a998c02a17d4a51c320375b0bfb395986dae3fe6` |
| Verification | `61553c16636efc39452706006dc480b827c2f2d04f3e318e02e3c2eec4f24664` |
| Publication figure | `243722cfd538943dce572b32b1104e587371d88b59d13181c369ccfdac7d6c6c` |
| Technical-report PDF | `ee5fde28270bc183df18175f8abd3b916a74351993ee44af639c4076abfd7416` |

Execution-time source digests remain historical facts and are not rewritten after later
source documentation or behavior-preserving renderer consolidation. The maintained
source reproduces the retained result, verification aggregate, visualization projection,
and both PNG files byte for byte.
