# Adapted-script parity audit

## Scope

This audit compares the nine executable donors under
`experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/analysis/`
with their calculation-owned counterparts. It establishes bounded software and artifact
parity for migration. It does not establish continuum convergence, scientific
validation, retained evidence, or publication acceptance.

Source hashes are bound to experiment baseline
`c49aaf816702c321cdd649e2567af70da57246fe`. Destination hashes are the bytes reviewed
on branch `work/periodic1d-band-equivalence-owner` after canonical owner-path commit
`dfa9923bc6e0c93e5c8bd03127468a67458246e1`.

## Script identities

| Experiment-relative donor | Source SHA-256 | Calculation-relative counterpart | Counterpart SHA-256 |
|---|---|---|---|
| `analysis/analyze.py` | `316537795cba86f638edc173e02062ba318392216862ae1c020365d2d0e954b1` | `run_flat_development.py` | `9f66d625e9ad3a31f1f1ab565954f9ed6884a8950ce0c283db5d86b35389fc65` |
| `analysis/analyze_nonflat.py` | `b32e43ba25a9cdcbde7656a4d0ab5de74a83e69a95ba241e8bcb375777df8434` | `run_nonflat_development.py` | `699a37c08cd98cfc01b277b13afaf675fd8953d7b40a4133b4042e52bb5955ea` |
| `analysis/analyze_parent_family.py` | `d523b7dbb49db7fc7d8d5963c34fbd8dccb764263da51ca3781a8fea3a62ce8c` | `run_parent_family_development.py` | `146fa10e193b954af55f7ac2f39308681089202fdc763393efa36945e514c0af` |
| `analysis/analyze_truncation.py` | `728788701a0b8e8e02c22e2212ed8a2327b0c4f46bdf2e15d71bcce8d5f52091` | `run_truncation_development.py` | `617e6e6ae5461fab7412d60c85b24adb48a11e828f2e85adba8d064c2f52461f` |
| `analysis/plot.py` | `37e12d242c6db5e64dcc2c6701cbfa5e0f6d60e9dc341d436eb90f51ac0f0c83` | `analysis/development/plot.py` | `32bdbdb08bfcb374c50f21d1f5a4be585ac03803cdb2cb62cc3fb82235846351` |
| `analysis/plot_nonflat.py` | `fc3bd2db69fe373714f98a6deb0f539616964a4ccee1a9495a836b2e8921f88e` | `analysis/development/plot_nonflat.py` | `215fe86666f5d4424838c7d74887fc260660451a903a6077910410bf26e443ee` |
| `analysis/plot_parent_family.py` | `b4d0b146eb0d400b9c0ad28075c65dbb5a8bd8e66c1c885ee317cc939c512bee` | `analysis/development/plot_parent_family.py` | `bf8bb4d3f8f0af6d2a405844bf7ab25434328475188b0a186d9fbf8aef6724a0` |
| `analysis/plot_scientific_story.py` | `38cc2c224b512296fef9ed838f50b0fb5286ee66787ee1452edf4bd7be85965a` | `analysis/development/plot_scientific_story.py` | `50201f4af29319ad2989157b84d0599e22b8fb24143380e083185acc37656431` |
| `analysis/plot_truncation.py` | `c31057999d984f4227b2cc90b2d20a5b040bfe75f748d71dfdcecd3d450114e5` | `analysis/development/plot_truncation.py` | `2e7d287b9803921969f9f99a57a2a5faca2d85bb1c7f33995460b092e2ad262f` |

## Difference classification

A normalized Python-AST comparison passed for all nine pairs. The normalization:

1. treats the removed installed donor import
   `ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.periodic1d` and the
   calculation-local `workflow` import as the same scientific-owner boundary;
2. ignores top-level assignments whose only purpose is routing inputs, results, and
   figures between the former experiment layout and the calculation layout;
3. canonicalizes path-root expressions while preserving every filename; and
4. sorts top-level imports before comparison.

After those transformations, each pair has an exact AST match. No difference remains in
numeric constants, mesh sizes, amplitude nodes, thresholds, loop structure, calculations,
CSV fields, plotting marks, labels, scales, or output filenames. The four analysis
counterparts differ only in import ownership and filesystem routing. The five plotting
counterparts differ only in filesystem routing.

The experiment analysis scripts are not a maintained executable route: they import an
installed package that no longer exists. Their role is predecessor recovery and parity,
not continued operation. The calculation counterparts remain development adapters and
are not the final Architecture v3 direct lifecycle.

## Scratch execution

The calculation directory was copied to isolated scratch and all nine counterparts were
executed there. No tracked input, result, or figure was overwritten. The environment was:

- CPython 3.14.6;
- NumPy 2.5.1;
- SciPy 1.18.0;
- Matplotlib 3.11.1; and
- Ghostscript 10.04.0 for PDF raster comparison.

The four calculation actions reproduced all 13 tracked CSV result files byte-for-byte.
Their SHA-256 values therefore equal the source and calculation values recorded in
[`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md).

The five plotting actions reproduced all five tracked PNG files byte-for-byte. The five
PDF files differed in raw bytes only at their single Matplotlib `/CreationDate` metadata
entry: after replacing that entry with one common token, each regenerated PDF was
byte-identical to its tracked counterpart. Independently, Ghostscript rendering at 150
dpi produced byte-identical one-page PNGs for each tracked/regenerated PDF pair.

The normalized PDF SHA-256 values were:

| Figure PDF | Creation-date-normalized SHA-256 |
|---|---|
| `band-equivalence-locality-scientific-story.pdf` | `5448829fe4ebec1eef463197cf226e206f4e3e411cddda8a27487c070b42ba7f` |
| `band-equivalence-versus-hopping-locality.pdf` | `6f8c86ee14be2b5fdca801687c913911d365dabd8411a93c8b0849cc02ef7a50` |
| `nonflat-four-state-exploratory.pdf` | `ac7072da9792a501fd76662e0958d29cdfa90920e41ceeb0eb8886b99793519c` |
| `parent-family-robustness-exploratory.pdf` | `1166201966d5603d3883fd58a9fb1200e27f293e1c2c7caf104c4a998b211846` |
| `truncation-band-consequences.pdf` | `a02edc7081c76cd513ac0761c3877f03c31c003506ba33a264c37985af2d1eb3` |

The focused calculation test suite also passed: 18 tests. These checks establish parity
with the tracked development surfaces under the stated runtime. They do not make the
internal development disposition labels scientific convergence claims.

## Disposition

The nine experiment scripts may be removed when the remaining documentation, protocol,
and consumer migrations close and deletion is separately authorized. Their source paths
and SHA-256 values remain recoverable from the baseline revision and this audit. The
calculation-side `workflow/` extraction and direct typed calculate → independently verify
→ render lifecycle remain separate open work.
