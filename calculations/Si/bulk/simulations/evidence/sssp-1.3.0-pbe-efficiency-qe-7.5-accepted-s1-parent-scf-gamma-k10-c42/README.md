# Accepted-S1 parent SCF evidence

This directory retains compact evidence from the separately authorized parent SCF on
the exact accepted structure/settings pair:

- structure: `Si.PrimitiveUnitCell.RightHanded.RelaxedS1`;
- structure SHA-256:
  `d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`;
- Gamma-centered mesh: K10;
- wavefunction/density cutoffs: 42/336 Ry;
- pseudopotential: SSSP 1.3.0 PBE efficiency Si USPP;
- invocation count: one;
- retries: zero;
- return code: zero; and
- electronic convergence: reported in five iterations.

The native input is byte-identical to the earlier K10/C42 confirmation input, but this
is a distinct occurrence with its own authorization, execution record, output, QEXSD,
and saved-state lineage. The confirmation saved state was not reused.

The complete saved state remains under the authenticated external root:

`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-parent-scf-gamma-k10-c42-20261031T070321Z`

[`result/saved-state-manifest.json`](result/saved-state-manifest.json) records 50 saved
state files totalling 6,720,372 bytes. The maintained ProjectKoios handoff manifest is
retained as
[`result/scf-saved-state-manifest.json`](result/scf-saved-state-manifest.json), SHA-256
`2b80acf2bc53dcbc5c667d50c4747036704a640c86cdf5902a98e998e21aefb9`, and was
verified against the external `run/tmp` root. The retained QEXSD has SHA-256
`3409a838a50e296d52b8ac70d74a1788b1ecf5fc3d4ccbccce17cfe6d3b83bd5`.
The full external artifact inventory contains 71 files totalling 8,220,835 bytes.

QE again emitted the four retained IEEE flag classes after successful completion.
They remain diagnostics because the process completed, reported convergence, and
produced finite observations and a readable saved state.

This occurrence establishes the accepted parent SCF and saved-state source only. It
does not authorize an NSCF, Wannier90 preprocessing, `pw2wannier90.x`, or localization.
