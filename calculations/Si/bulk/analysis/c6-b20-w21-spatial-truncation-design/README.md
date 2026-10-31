# `C6-B20-W21` controlled spatial-truncation design

## Purpose

This authorized S90 no-calculator stage freezes the spatial-truncation family and its
operational diagnostics for the full untruncated `C6-B20-W21` Wannier Hamiltonian. It
does not evaluate or select a truncation, fit a Slater--Koster model, invoke a
calculator, or observe the 402-point confirmation-parent values.

The fixed reduction source is the exact S30 full operator. S40 direct-parent differences
are development-oracle labels: they limit physical-fidelity claims but do not define the
truncation masks or serve as deployable diagnostics.

## Truncation family

The design retains all 18 complete physical-radius shells already authenticated by S30:

- shell `H-shell-00` is the onsite-only control;
- shells are nested and include every effective representative in each physical-radius
  group;
- every mask must preserve complete \(R\leftrightarrow -R\) closure;
- shell `H-shell-17` contains all 383 effective representatives and is the full-support
  control; and
- no radius is selected by S90.

S30 had already produced descriptive locality values. To avoid retrospective pruning,
S90 retains every shell rather than selecting a favorable subset. Shell admission
reproduces S30's structural rule—Cartesian radii rounded to nine decimal places in
angstrom before grouping—while the shell ordinal and cumulative representative count
provide deterministic correlation.

## Operational diagnostics frozen for S100

For every shell, S100 must retain:

1. representative counts, negative-pair closure, Hermiticity, and full-support recovery;
2. the excluded-block spectral triangle bound \(B_H\), which is a uniform operator-error
   upper bound;
3. the Frobenius tail \(F_H\), which is an RMS/Parseval measure and not a uniform bound;
4. direct full-to-truncated operator spectral and Frobenius differences on the fixed
   Gamma-origin `21 x 21 x 21` grid;
5. ordered-spectrum errors over all ten bands, the lowest conduction band, and the
   full-source edge window;
6. gap, signed Delta-valley location and energy, curvature, effective-mass, and
   curvature-stencil changes relative to the full operator; and
7. monotone larger-shell envelopes so that a nonmonotone favorable shell cannot be
   selected in isolation.

These are controlled \(H_W\)-to-\(H_{\mathrm{truncated}}\) diagnostics. They are not
errors relative to the hidden Kohn--Sham parent.

## Selection and oracle boundary

S100 must report the complete family and may not change masks, refit a model, or accept a
radius. The separately authorized [S100 evaluation](../c6-b20-w21-spatial-truncation-evaluation/)
has now reported every frozen shell without selecting one. The separately authorized
[S105 disposition](../c6-b20-w21-spatial-truncation-disposition/) retained full support,
so `H_T = H_W`; it did not accept a nontrivial shell. Any future nontrivial selection
requires a new separate record using only declared construction authority and without
relabeling parent numerical tolerances as reduction tolerances.

Before the 402-point parent values can be observed, the campaign must freeze selected
truncation candidates, diagnostic rules, any calibration using the revealed 408-point
development oracle, the Slater--Koster definition and fit roles, and predicted hidden
errors. S90 consumes no 402-point parent values.

## Artifacts

[`prepare_design.py`](prepare_design.py) authenticates the current controlled-reduction
protocol, the S30 implementation and result, and the S40 hidden-oracle correction. It
writes [`truncation-design.json`](truncation-design.json) with KSD's
`TypedJsonMappingSerializer`.

| Artifact | SHA-256 |
|---|---|
| S90 design implementation | `687ed568e392ea1c3ac333c543313cc57206d5a92903b7e3e015b5103224cc1d` |
| Frozen truncation design | `6b9863271ba8241881d62435a7c8307d3431ffe59bfdcce5d96525fe86fcb531` |

No calculator invocation or later-stage authorization follows from this design.
