# Provisional S1 Gamma-centered K10 cutoff confirmation preflight

This directory retains compact **preflight only** material for the second stage of
fresh setting confirmation on the exact 758-byte provisional S1 structure, SHA-256
`d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`.

The axis uses Gamma-centered K10 and wavefunction cutoffs 30, 36, 42, 48, 54, and
60 Ry with an 8:1 density-cutoff ratio. The just-completed S1 K10/C42 occurrence is
reused by exact authenticated identity; the five new inputs are C30, C36, C48, C54,
and C60. The calculation-owned rule selects the smallest sampled cutoff whose
absolute total-energy difference from C60 is at most `1.0 meV/atom`.

[`campaign-preflight.json`](campaign-preflight.json) binds the exact structure,
reused C42 evidence, executable, pseudopotential, settings, new input identities,
order, and resource limits. Preparation performed no calculator execution.

## Authorization and execution state

The operator authorized exactly five sequential `pw.x` invocations in order C30, C36,
C48, C54, C60, with one process per occurrence, `600 s` timeout per occurrence, at
most `2 GiB` retained per occurrence, zero retries, and stop on the first failure. All
five succeeded and no retry occurred. As instructed, C42 was reused and not rerun.
Compact evidence is under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-k10-cutoff-confirmation/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-k10-cutoff-confirmation/).

The sampled calculation-owned rule again selects 42/336 Ry. Together with the
separately confirmed K10 result this defines a candidate stable pair awaiting explicit
scientific disposition. It does not automatically create a downstream parent SCF.
