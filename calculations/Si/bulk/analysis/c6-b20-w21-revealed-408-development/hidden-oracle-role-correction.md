# Hidden-oracle role correction

The initial S40 result correctly calculated the revealed 408-point parent discrepancies,
but incorrectly treated the frozen parent-fidelity criteria as operational gates that
stopped controlled reduction. That disposition conflated information available only in
the controlled study with diagnostics available during real reduction.

The original result is retained unchanged as
[`development-result-initial-linear-gate-disposition.json`](development-result-initial-linear-gate-disposition.json),
SHA-256
`fbd9ab474328323f43d03754d01a0a9be115ea30739c1a4ac65ca47767d99459`.

The corrected result changes no spectrum, gap, valley, curvature, mass, or residual
value. It reclassifies the revealed-parent comparisons as development-oracle labels:

- they may limit claims about physical fidelity to the Kohn--Sham parent;
- they are not deployable reduction diagnostics;
- they do not change provider eligibility or S30 structural eligibility; and
- they do not block a separately declared controlled reduction from the fixed full
  untruncated Wannier operator.

Reduction definitions, operational diagnostic rules, calibration, fits, and predicted
hidden errors must be frozen before the 402-point confirmation-parent values are
observed. The correction invokes no calculator and does not reveal those values.
