# Bulk-silicon controlled-reduction research protocol

The current methodology protocol is
[`controlled-reduction-protocol-post-s110.tex`](controlled-reduction-protocol-post-s110.tex),
SHA-256 `3ec2902a94ebe78eba1e223a0ee4ef99075f4bd86238398b67d370fa88224653`.
It retains the full untruncated Wannier operator as the fixed source for controlled
reduction, records the failed S110 ten-orbital alignment gate, and defines the
post-S110 continuation ladder. It treats withheld direct-parent values as a hidden
evaluation oracle rather than an operational reduction gate.

[`controlled-reduction-protocol.tex`](controlled-reduction-protocol.tex) is retained
byte-for-byte at SHA-256
`80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380` because completed
S90, S100, S105, and S110 evidence binds that exact identity. It remains the authority
for those completed stages but is superseded for post-S110 decisions.

[`research-protocol.tex`](research-protocol.tex) is retained byte-for-byte at SHA-256
`230aa0cebb37cf28a2e2e7cdcf1186d5ded98971217be3bbb8beadc2879d9dad` because earlier
completed preflights and retained evidence bind that exact path and identity. It records
the prior linear parent-fidelity-gated protocol and is not the current authority for the
reduction diagnostic sequence.

The current protocol requires:

- native convergence and structural eligibility before fixing the full operator;
- separate parent-to-source, spatial-truncation, parameterization, and end-to-end error
  channels;
- operational diagnostics that do not require withheld parent values;
- explicit labeling of the revealed 408-point set as development-oracle evidence;
- freezing reductions, diagnostic rules, calibration, fits, and predicted hidden errors
  before observing the 402-point confirmation values;
- prospective confirmation of whether frozen diagnostics predict hidden error without
  refitting; and
- separately authorized post-S110 continuation in increasing implementation difficulty:
  reusable Slater--Koster foundations, spectral-only feasibility, a global-unitary
  rank-10 operator study, a separately defined rank-9 projected source, and finally a
  new Slater--Koster-compatible Wannier source.

Stopping the Slater--Koster reduction branch remains the default under the failed
TB-anchored alignment contract. Level 1 reusable foundations have been
[implemented with synthetic software verification only](../analysis/c6-b20-w21-slater-koster-definition-fit/level-1-foundation-disposition.md);
this does not activate Level 2 or produce a reduction. The ladder is not an automatic
workflow. Spectral-only work cannot claim an operator residual, rank-9 work introduces
a distinct target-space error, a new Wannier source requires fresh bounded calculator
authorizations, and singular-value regularization is limited to labeled sensitivity
analysis.

No protocol file authorizes a calculator invocation.
