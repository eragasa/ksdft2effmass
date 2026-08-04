# P9 — Wannier90 execution and result-adaptation subnet

Status: blocked by accepted P2, P3, and P8

## Objective

Implement verified Wannier90 capabilities and two-phase preprocessing/localization/interpolation request, result, failure, retry, adaptation, and acceptance transitions.

`wannier90.x -pp`, localization/interpolation, and optional `postw90.x` are distinct capabilities. Guards perform no execution or I/O. Results retain common-parent lineage and validation state needed by later Wannier-TB construction and comparison. No real execution without the production checkpoint.

Completion requires implementation, tests, documentation, independent review, parent verification, and human acceptance.