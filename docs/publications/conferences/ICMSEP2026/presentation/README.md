# ICMSEP 2026 presentation

`presentation.tex` is the 16:9 conference deck. It leads with the project's intended
Si/Si:P workflow: construct compatible Wannier representations, reconcile their state
spaces and gauges, and subtract the aligned operators to obtain a substitutional-
phosphorus perturbation for a reduced model. It then synthesizes four currently
available bounded result groups that establish controls needed by that workflow:

1. exact rank-two 1-D band-equivalence/range inflation;
2. scalar 2-D spectral-to-TB and interpolation controls;
3. rank-three gauge/locality and Wannier90 bridge controls; and
4. the read-only silicon tutorial component-truncation result.

Charcoal and blue content denotes retained bounded evidence. Red content denotes
prospective work or an unexecuted extension. DLSU green supplies the presentation
hierarchy rather than carrying a scientific evidence status. The deck does not present
the planned 2-D/3-D, non-orthogonal, higher-rank, or production-silicon studies as
completed.

## Visual identity and asset provenance

The deck was styled from the official DLSU Brand Kit page consulted on 2026-10-16:
<https://old.dlsu.edu.ph/offices/asist/dlsu-brand-kit/>. It uses a white/neutral content
field, DLSU green hierarchy, restrained evidence colors, and a 16:9 layout intended to
keep equations, tables, and scientific figures readable.

The locally retained logo files are:

| Local asset | Official source and local treatment | SHA-256 |
|---|---|---|
| `assets/dlsu-wordmark-green.png` | Top horizontal lockup cropped from the official Brand Kit image titled “Canva Brandkit Green Logo,” [`4.png`](https://old.dlsu.edu.ph/wp-content/uploads/2024/02/4.png); downscaled to 1200 px wide without recoloring | `77a5774a26133a6477c5ae0959733d0f7870b6daca8392338e0ce789aaa48876` |
| `assets/dlsu-wordmark-white.png` | Exact copy of the transparent white DLSU header lockup served on the same official page, [`dlsu-logo-white.png`](https://old.dlsu.edu.ph/wp-content/uploads/2017/10/dlsu-logo-white.png) | `1ca774000494c4b26013f9ea776d4932b4e25f099070c3f522de27b31e2c399a` |

Access limitations matter. The page's Canva brand-template link returned HTTP 404 even
in the authenticated browser session. The page's **Color** accordion rendered an empty
media area, so no unseen palette values are asserted here. The visible **Fonts** pane
specified Garamond for the title and Frutiger for subtitles/headings (including the
visible 42 pt bold title and 36 pt bold subtitle/heading roles). Because Frutiger was not
available as a redistributable TeX font, the deck uses EB Garamond for the presentation
title and TeX Gyre Heros as a conservative sans-serif substitute for Frutiger. Font sizes
were adapted to Beamer and scientific-content density rather than copied literally from
the Canva role sizes. The green used in the deck is RGB `(0, 129, 77)`, sampled from the
official transparent DLSU page-header wordmark. No obsolete departmental template was
used.

## Presentation-local scientific figures

Every figure consumed by `presentation.tex` is copied beneath `assets/`, so the deck
has no build-time dependency on calculation or experiment paths outside this directory.
These copies are presentation inputs, not independent scientific evidence; their claim
status remains that of the identified source calculation or development analysis.

| Local asset | Source path at copy time | SHA-256 |
|---|---|---|
| `assets/band-equivalence-locality-scientific-story.pdf` | `experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/analysis/band-equivalence-locality-scientific-story.pdf` | `9e88e334c7b6c3ae25fbd264428d128d2ba17f16121ed8613c2412c886c1e9be` |
| `assets/periodic-2d-summary.png` | `calculations/research-monograph/periodic-2d/summary.png` | `ba921830f01cd39908a5a84ac02546b8804cc2916fd937501ad8a8922b5c53b1` |
| `assets/periodic-2d-composite-summary.png` | `calculations/research-monograph/periodic-2d/composite-summary.png` | `8554a2ef16e833475149f12827fbd3d6c6386d85adc16e90b70b7f7bc44a3c57` |
| `assets/periodic-2d-wannier90-balanced-summary.png` | `calculations/research-monograph/periodic-2d/wannier90-balanced-summary.png` | `cad8e5de538761e8e03c6a456f0b0f4c03ec34c5b2f28265f104f03b1d54cbaf` |
| `assets/silicon-real-space-shell-block-norms.pdf` | `calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/real-space-shell-block-norms.pdf` | `8decd56396b97ab6ce02a2847092e3b901a590724955476feaa8396bacf62d25` |
| `assets/silicon-real-space-truncation-relative-error.pdf` | `calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/real-space-truncation-relative-error.pdf` | `2b16e3d4cb92719000d9d2014ca381dab9df7102492c792bdd4558c8d710325f` |

The five calculation-owned source files matched `origin/main` when copied. The
band-equivalence figure was copied from the dirty
`work/monograph-current-library-capabilities` worktree and therefore requires explicit
Git-state qualification: its copied digest is the value above, while the corresponding
`origin/main` byte identity was
`191d8fff0dbc777a6268c0e1e3dd481f8160da11bc9b5797510919ca9e57b2a8`.
The table's experiment path is therefore a historical copy-time locator, not a live
build dependency. The corresponding maintained development figure is now
`calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/analysis/development/figures/band-equivalence-locality-scientific-story.pdf`
with SHA-256
`191d8fff0dbc777a6268c0e1e3dd481f8160da11bc9b5797510919ca9e57b2a8`.
Neither identity establishes scientific validation or publication acceptance.

## Build

Build with BibLaTeX/Biber through `latexmk`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error presentation.tex
```

The references frame is unnumbered and can remain as a backup slide. The numbered deck
keeps the full motivation-to-diagnostic mapping and the four bounded result groups rather
than enforcing a fixed slide count; presenters can select or skip detail slides to match
the assigned conference time.
