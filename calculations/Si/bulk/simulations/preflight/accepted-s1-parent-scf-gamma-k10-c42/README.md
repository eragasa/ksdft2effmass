# Accepted S1 parent-SCF preflight

This directory retains compact preflight material for the new parent SCF emitted by
acceptance of [`accepted-stable-pair.json`](../../accepted-stable-pair.json).

The occurrence uses exact accepted S1, Gamma-centered K10, 42/336 Ry, fixed
occupations, PBE, and the authenticated SSSP 1.3.0 efficiency Si pseudopotential. Its
saved state is intended to become the source for a separately authorized downstream
NSCF.

The rendered `pw.in` is byte-identical to the earlier K10/C42 confirmation input
because the physical settings are identical. The occurrence itself must nevertheless
be new: it requires a new execution record and new saved-state lineage. No confirmation
saved state will be relabelled or reused as the parent.

## Authorization and execution state

The operator authorized exactly one `pw.x` invocation, one process, `600 s` timeout,
`2 GiB` maximum retained bytes, zero retries, and stop on failure. The occurrence
returned zero and converged; no retry occurred. Compact evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-parent-scf-gamma-k10-c42/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-parent-scf-gamma-k10-c42/).

This establishes process and saved-state facts only; it does not authorize the NSCF or
any Wannier90 stage.
