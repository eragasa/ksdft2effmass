# `ksdft2effmass.periodic2d.campaign`

## Purpose and status

This package owns the canonical two-dimensional isolated-band campaign records and
operations after phase-7 decomposition. Encoded documents remain distinct from
campaign definitions, represented operators, typed results, correlation, and
verification. Concrete campaign records are independent immutable composition roots;
the former dimension-only ``Periodic2DCampaign`` base is removed without an alias or
replacement protocol.

## Child map

- [One-band isolated campaign](nbands_1/index.md)
  - [Encoded documents](nbands_1/encoded_documents/index.md)

## Ownership boundary

Campaign records may retain project-specific exact wires, definitions, requests,
results, and evidence-correlation policy. They do not redefine general periodic models,
retained spaces, represented operators, or reusable lattice primitives.
