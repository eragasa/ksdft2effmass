# `ksdft2effmass.periodic2d.run.topological`

## Purpose and migration status

This package owns the preserved periodic-2D topological campaign record, its exact
encoded documents, and independent correlation and verification surfaces. These
responsibilities remain distinct.

Crosswalk row 048 reconciles the encoded input/result pair. Row 049 separately covers
the phase-sweep document pair, and row 069 completes typed topological calculation,
correlation, and independent verification without promoting encoded expected values to
qualified oracles.

## Child map

- [Encoded documents](encoded_documents/index.md)
  - [`Periodic2DTopologicalEncodedDocuments`](encoded_documents/Periodic2DTopologicalEncodedDocuments/index.md)
- [Topological phase-sweep campaign](phase_sweep/index.md)
  - [Encoded documents](phase_sweep/encoded_documents/index.md)
  - [`Periodic2DTopologicalPhaseSweepEncodedDocuments`](phase_sweep/encoded_documents/Periodic2DTopologicalPhaseSweepEncodedDocuments/index.md)

## Supported imports and evidence

The reviewed facade `ksdft2effmass.periodic2d.run.topological` exposes the campaign and
encoded documents. Calculation, correlation, and verification owners remain in their
defining modules. The exact campaign node is
`python/tests/ksdft2effmass/periodic2d/run/topological/test__Periodic2DTopologicalCampaign.py`;
the mirrored software-verification manifest binds class-owned and retained-artifact
nodes. Sphinx documents the family in
`doc/sphinx/api/ksdft2effmass/periodic2d/run/topological.rst`.

## Claim boundary

Independent reconstruction establishes bounded consistency for retained Chern, Wilson,
gap, and gauge-attack observations. Encoded expected observations remain campaign
content rather than independently qualified numerical oracles. Passing and content
identity do not establish a physical model identity, a general topology result,
convergence, scientific validation, uncertainty quantification, or acceptance.
