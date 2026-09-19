# Bulk-Silicon Direct Bootstrap Execution Observations

**Evidence status:** Provisional calculated and finite-setting numerical-verification
evidence from the identified direct bootstrap execution and provisional geometry.
This is not a canonical scientific `CampaignRun` or `ScientificWorkflowRun`,
accepted production convergence, numerical-verification acceptance, an
infinite-basis result, effective-mass convergence, EOS acceptance, scientific
validation, or uncertainty quantification. See the maintained [bootstrap
disposition](bootstrap-execution-disposition.md) and [read-only direct-results
audit](direct-results-audit.md).

The human authorized Option A only at boundary commit
`64de888ad54c1385941a0485433974342380094d`. The direct bootstrap runner,
governed by the development harness before the deterministic scientific
Campaign architecture existed, executed once
from 2026-08-13 13:14:44 UTC through 13:15:30 UTC. All 9 SCFs and 9 linked NSCFs
returned zero and emitted one `JOB DONE.` marker. No retry occurred.

Raw outputs and restart trees remain external under campaign descriptor
`ksdft2effmass-runs/bulk-silicon-production-convergence-20260813T021128Z`.
[`execution-provenance.json`](execution-provenance.json) retains their compact
identities and observations. [`finite-setting-analysis.json`](finite-setting-analysis.json)
applies only the predefined criteria. The later direct-results audit independently
verified all 41 retained output/receipt identities, all 18 input copies, all nine
case extractions, all eight comparisons, and all 18 scratch-tree metadata summaries.
No primary-case rerun is required merely to reproduce the execution through the
scientific harness.

## Finite-setting observations

| Comparison | $|\Delta E|$ (Ry/atom) | $|\Delta P|$ (kbar) | Max $|\Delta\sigma|$ (kbar) | Max aligned band 4/5 change (meV) | Max gap-probe change (meV) | All predefined criteria |
|---|---:|---:|---:|---:|---:|---|
| C30→C36 | $9.90\times10^{-5}$ | 0.31 | 0.31 | 1.0 | 1.2 | No |
| C36→C42 | $1.8535\times10^{-5}$ | 0.19 | 0.19 | 0.2 | 0.2 | No |
| C42→C48 | $2.835\times10^{-6}$ | 0.01 | 0.01 | 0.0 | 0.0 | Yes |
| C48→C54 | $4.435\times10^{-6}$ | 0.01 | 0.01 | 0.0 | 0.0 | Yes |
| C54→C60 | $2.110\times10^{-6}$ | 0.02 | 0.02 | 0.1 | 0.1 | Yes |
| K6→K8 (C48) | $2.980\times10^{-6}$ | 0.01 | 0.01 | 0.1 | 0.1 | Yes |
| K8 (C48)→K10 | $1.15\times10^{-7}$ | 0.00 | 0.00 | 0.0 | 0.0 | Yes |
| K10→K12 | 0.0 | 0.00 | 0.00 | 0.1 | 0.1 | Yes |

Band values are retained from QE output printed to 0.0001 eV. Comparisons below
that printed resolution cannot be inferred. These rows demonstrate stability
between finite tested settings only; they do not bound $|q_j-q_\infty|$.

No $E_*$ or $K_*$ is selected by this analysis. The four-corner interaction
inputs remain parameterized and were not executed because the primary campaign
authorization did not select settings or authorize follow-on calculations.

## Resources and warning

The campaign used 46 seconds by UTC timestamps; the sum of per-invocation wall
times was retained in the provenance record. Peak recorded maximum resident set
size was 81,936,384 bytes and final campaign storage was 161,744 KiB, within the
approved ceilings.

Every invocation emitted exactly:

```text
Note: The following floating-point exceptions are signalling: IEEE_INVALID_FLAG IEEE_DIVIDE_BY_ZERO IEEE_OVERFLOW_FLAG IEEE_UNDERFLOW_FLAG
```

This recurring report remains unresolved and unclassified. Exit status zero and
`JOB DONE.` do not establish that it is harmless.
