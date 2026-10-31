# Accepted-S1 first pw2wannier90 conversion preflight

This directory retains the dry-run preflight for the first rank-10 interface conversion
candidate. It binds the verified `silicon.nnkp` topology to the authenticated Davidson
NSCF saved state.

The exact converter declaration uses:

- prefix `system` and staged outdir `./tmp/`;
- seed `silicon`;
- scalar non-spin component `none`;
- standalone mode;
- AMN and MMN enabled;
- UNK and SPN disabled; and
- required outputs `silicon.amn`, `silicon.mmn`, and `silicon.eig`.

The maintained ProjectKoios `QePw2Wannier90Runner` rendered
[`pw2wannier90.in`](pw2wannier90.in) in dry-run mode. The parent manifest authenticates
67 saved-state files totalling 18,799,008 bytes. The NNKP has SHA-256
`4dd17877e0f3bc0b19a0f74ce539a91bd8ceb1c66a18d3f733f08e5d8ce07014`.
The exact bound decision document is retained as
[`wannier-interface-decision.txt`](wannier-interface-decision.txt), SHA-256
`76b53356bb8aff1bfc7915900a7e8a3b4bab5bb724bb4a43bbb34e85dd01a152`.
No calculator was executed.

UNK output is outside the maintained converter interface. The separately authenticated
QE wavefunction inventory remains the native coefficient evidence required by the
component-operator profile; it is not replaced by AMN/MMN/EIG.

As in the preprocessing preflight, a local runtime alias maps the retained tranche's
former PhysKit converter class name to the installed public converter singleton.
Neither dependency was modified.

## Authorization state

Status: **authorization consumed by one occurrence**.

Exactly one single-process `pw2wannier90.x` invocation was performed with zero retries.
It returned zero, printed `JOB DONE`, and produced finite, shape-consistent AMN/MMN/EIG
artifacts correlated with the Davidson QEXSD and NNKP neighbor inventory. Compact
evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-sp3sstar/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-sp3sstar/).

This does not authorize Wannier90 localization or any retry.
