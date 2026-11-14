# Technical report

The narrative-focused second version is maintained under [`v2/`](v2/). It uses the
conventional introduction/background/methodology/results/discussion structure and
centers the bounded internal Wannier-reduction findings rather than the full calculation
status history.

[`technical-report.tex`](technical-report.tex) is the calculation-facing status and
design report for the bulk-silicon parent and reduction program. Its bibliography is
maintained in [`references.bib`](references.bib). The report is publication-independent
and may be cited by Paper D without transferring calculation identity.

Build outside the source tree with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-si-bulk-technical-report technical-report.tex
```

The selected compiled `technical-report.pdf` is retained as a review snapshot. It is
not retained calculation evidence, scientific validation, or a publication; LaTeX
auxiliary products remain untracked.

The detailed production-parent audit remains in
[`docs/computational/bulk-silicon-production-convergence-design.md`](../../../../docs/computational/bulk-silicon-production-convergence-design.md).
The separate external empirical development control and its source boundary are under
[`analysis/controls/vogl-sp3s-star/`](../analysis/controls/vogl-sp3s-star/). The report
does not duplicate retained result payloads, ingested source bytes, or historical
provenance bytes.

The selected C6-B20-W21 gauge-alignment/locality section includes the complete retained
nine-figure package from the authorized producer-only development run. A separate
post-hoc two-tolerance section adds the literal minimum-support witness surface
$W(\tau_1,\tau_2)$ and a follow-on fitted surface $W_\alpha(\tau_1,\tau_2)$ with one
bounded scale per retained native Wigner--Seitz shell, without introducing a
Slater--Koster model. The latter exposes same-support spectral/operator tradeoff arcs
that literal deletion cannot. A subsequent Wannier-only fidelity ladder freezes three
witnesses and compares fitted-408 errors with exact Parseval operator losses, independent
dense spectral meshes, and source-relative gap, valley, Hessian, and mass diagnostics.
A comprehensive non-SOC band-edge amendment adds full electron mass tensors, Gamma
valence-cluster integrity, high-symmetry direct-gap and bandwidth checks, and a
polar-transported three-band quadratic valence Hamiltonian. It explicitly rejects
independently ordered hole-band Hessians at the near-degenerate source edge and does not
claim physical SOC heavy-hole, light-hole, or split-off parameters. Separate RMS and
maximum-error diagnostic maps remain retained in the original
calculation owner but are supplementary. The figures
consume the checksum-bound authenticated producer result directly and are labeled
`producer-checked-development-analysis-not-independently-verified`. The support-error
panel uses the additive discrete Pareto amendment, which explicitly marks observed
non-dominated complete-shell supports rather than merely relabeling raw curves as a
frontier. The conditional LaTeX inclusion still renders an explicit pending notice if
any retained figure is absent; it never substitutes synthetic numerical data.
