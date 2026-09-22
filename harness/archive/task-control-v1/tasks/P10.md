# P10 — Synthetic composed workflow verification

Status: blocked by accepted P6, P7, P8, P9, and required metrics

## Objective

Verify composed CPN semantics with synthetic requests/results: multisets, independent fan-out, provenance-compatible joins, pure guards, failure/recovery, explicit retry authorization, repeated convergence iterations, durable marking round trips, terminal failed-attempt history with new-identity retries, recoverable blocked branches, explicitly finalized blocked outcomes, scope-explicit accepted/rejected outcomes, and restart from persisted project state.

The evidence is software verification and applicable numerical verification only. It does not run QE/Wannier90, establish G02, scientific validation, UQ, or Rust conformance. It contributes to G01b after its own review and acceptance.

Completion requires tests/evidence, documentation, independent review, parent verification, and human acceptance.