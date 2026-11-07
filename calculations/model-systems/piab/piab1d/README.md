# PIAB1D calculation crosswalk

This normalized path indexes existing PIAB1D records without copying or rewriting them.

| Record | Status | Authoritative locator |
|---|---|---|
| Appendix D finite-representation diagnostics | Calculated retained package | `calculations/research-monograph/particle-in-box/` |
| Timestamped campaign attempt | Failed before result serialization | `calculations/research-monograph/campaigns/piab1d/runs/20260922T213932Z/` |

The corresponding maintained experiment path is
`experiments/model-systems/piab/piab1d/`.

New PIAB1D runs, after an immutable experiment version and evidence policy are frozen,
will use `runs/<run-id>/`. The historical package remains authoritative until a
separately reviewed provenance migration.
