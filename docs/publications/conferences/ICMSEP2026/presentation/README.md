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

## Build

Build with BibLaTeX/Biber through `latexmk`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error presentation.tex
```

The references frame is unnumbered and can remain as a backup slide. The numbered deck
keeps the full motivation-to-diagnostic mapping and the four bounded result groups rather
than enforcing a fixed slide count; presenters can select or skip detail slides to match
the assigned conference time.
