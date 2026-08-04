# P8 — Wannier specification and QE-to-Wannier90 bridge

Status: blocked by accepted P3, P4, P5, and P6

## Objective

Implement Wannier specification tokens, Stage-03 uniform-grid NSCF child request/result lineage, and the QE-to-Wannier bridge artifact contract.

The child carries the accepted G02 SCF parent manifest. `.nnkp`, `.amn`, `.mmn`, `.eig`, and approved optional artifacts remain typed external references. QE and Wannier90 remain separate capabilities/backends. No real run occurs without the production checkpoint. Preserves H bridge content.

Completion requires implementation, tests, documentation, independent review, parent verification, and human acceptance.