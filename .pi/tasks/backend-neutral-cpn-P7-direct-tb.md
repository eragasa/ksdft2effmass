# P7 — Direct spectral/TB fan-out subnet

Status: blocked by accepted P3, P4, and P6

## Objective

Implement the CPN fan-out from an accepted neutral `PeriodicElectronicStructureDataset` parent to direct spectral/TB request and result tokens, with explicit training/withheld data, provenance, failure, retry, and acceptance states.

The route remains direct spectral DFT-to-TB fitting, not operator fitting. It never parses QE or reconstructs an operator from eigenvalues. Comparison eligibility retains parent/specification/representation metadata. Preserves G.

Completion requires implementation, tests, documentation, independent review, parent verification, and human acceptance.