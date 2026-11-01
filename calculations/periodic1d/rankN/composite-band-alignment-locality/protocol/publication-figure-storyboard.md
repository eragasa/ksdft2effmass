# Rank-N publication-figure storyboard

## Status

This storyboard is an iterative presentation layer over the integrity-admitted
16-case development cache. The plotted values are calculated results, not synthetic
illustrations. They remain **unsealed** and are not independently verified in full.
Cache admission establishes canonical-byte integrity and inventory completeness; it
does not establish scientific correctness or publication acceptance.

The storyboard does not replace the fixed nine-view development renderer. It selects a
more compact narrative for protocol review while retaining the nine development views
as the detailed diagnostic record.

## Narrative sequence

| Figure | Scientific question | Intended placement |
|---|---|---|
| `01-alignment-information-hierarchy` | Which alignment families recover the reference frame, restore short-range hopping diagnostics, and reduce the finite-support spectral consequence? | Main text |
| `02-rank-depth-scaling` | How do the attacked representation, restricted global fit, and pointwise control vary over the frozen rank/depth grid? | Main text |
| `03-locality-and-support-consequences` | At the fixed interior anchor, how do unchanged Fourier coefficients and retained-support consequences respond to alignment? | Main text |
| `04-separated-error-channels` | Are interpolation, deliberate truncation, and total spectral consequence kept distinct rather than presented as an additive scalar budget? | Main text or methods |
| `05-claim-operands-and-unresolved-boundary` | Which frozen threshold operands are available, and which missing represented-operator operand prevents a complete claim disposition? | Main text |
| `06-numerical-controls` | Do refinement, qualification, residual decomposition, sampled Pareto counts, and pointwise/oracle agreement support numerical review? | Supplement or methods |

## Encoding rules

- PDF is the vector publication master; PNG is a 600-dpi review rendering.
- Rank uses marker shape and circuit depth uses color where individual cases are shown.
- Gauge families use a fixed black/blue/green/orange palette.
- Logarithmic panels use a display floor of `1e-18` only for axis placement.
- Exact zeros are marked explicitly and are not relabelled as `1e-18` results.
- Lines across sampled support cutoffs connect declared finite calculations and are
  guides to the eye; no continuum support interpolant is claimed.
- Hopping-tail panels diagnose unchanged coefficients. Retained-support panels apply an
  irreversible support-truncation policy. Equal integer cutoffs do not make those
  inventories interchangeable.
- Error channels remain separate. The pointwise residual fields add, but separately
  maximized norms need not form an additive scalar error budget.
- Green cell borders in the claim figure mean that the displayed frozen inequality is
  met. They do not assign the complete locality-extension claim because the frozen
  global represented-operator operand is not retained.

## Reproduction

From `python/`:

```bash
uv run python \
  ../calculations/periodic1d/rankN/composite-band-alignment-locality/protocol/render_publication_storyboard.py
```

The renderer reads only:

```text
results/development-cache/
```

and writes the closed design inventory under:

```text
protocol/figures/storyboard/
```

Changing this presentation layer does not require rerunning the scientific producer.
Any future publication renderer must preserve the admitted-cache provenance, evidence
status, missing-operand disclosure, and exact-zero semantics.
