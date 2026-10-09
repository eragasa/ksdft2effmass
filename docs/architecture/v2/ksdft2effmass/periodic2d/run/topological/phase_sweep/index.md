# `ksdft2effmass.periodic2d.run.topological.phase_sweep`

## Purpose and migration status

This package owns the preserved periodic-2D topological phase-sweep campaign record,
its exact encoded documents, and independent correlation and verification surfaces.
These responsibilities remain distinct.

Crosswalk row 049 reconciles the encoded input/result pair. The parameter axes encoded
in the input, unavailable or omitted outcomes, retained observations, and independent
verification are not collapsed into the byte-container owner. Row 070 completes typed
calculation, correlation, and verification ownership while preserving unavailable
transition-point outcomes.

## Child map

- [Encoded documents](encoded_documents/index.md)
  - [`Periodic2DTopologicalPhaseSweepEncodedDocuments`](encoded_documents/Periodic2DTopologicalPhaseSweepEncodedDocuments/index.md)

## Supported imports and evidence

The reviewed phase-sweep facade exposes the campaign and encoded documents; calculation,
correlation, and verification owners remain in their defining modules. The exact
campaign node is
`python/tests/ksdft2effmass/periodic2d/run/topological/phase_sweep/test__Periodic2DTopologicalPhaseSweepCampaign.py`;
the mirrored software-verification manifest binds class-owned and retained-artifact
nodes. Sphinx documents the family in
`doc/sphinx/api/ksdft2effmass/periodic2d/run/topological-phase-sweep.rst`.

## Claim boundary

Passing establishes bounded reconstruction over the declared axes and available
samples. Analytic outcomes at declared transition points remain explicit unavailable
values and are not imputed from neighboring samples. Encoded content does not establish
a general phase diagram, model adequacy, convergence, validation, uncertainty
quantification, or acceptance; expected observations are not qualified oracles.
