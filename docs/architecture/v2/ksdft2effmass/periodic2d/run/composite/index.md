# `ksdft2effmass.periodic2d.run.composite`

## Purpose and migration status

This package owns the preserved composite periodic-2D campaign record, its exact
encoded documents, correlation, and independent verification surfaces. These
responsibilities remain distinct.

Crosswalk row 047 reconciles the encoded input/result pair. Row 068 completes the
wider decomposition into typed input, provenance, result document, calculation,
correlation, and independent verification owners. Each operation is instantiated per
request; the campaign is an independent immutable composition root.

## Child map

- [Encoded documents](encoded_documents/index.md)
  - [`Periodic2DCompositeEncodedDocuments`](encoded_documents/Periodic2DCompositeEncodedDocuments/index.md)

## Supported imports and evidence

The reviewed facade `ksdft2effmass.periodic2d.run.composite` exposes the campaign,
encoded documents, and correlation/verification contracts. Calculation owners remain
in the defining `calculate` module. Exact campaign behavior is exercised by
`python/tests/ksdft2effmass/periodic2d/run/composite/test__Periodic2DCompositeCampaign.py`;
class-owned and retained-artifact nodes are declared in the mirrored
`resources/implementation-verification-ownership.json`. The public Sphinx mapping is
`doc/sphinx/api/ksdft2effmass/periodic2d/run/composite.rst`.

## Claim boundary

Passing establishes strict adaptation and independent reconstruction of represented
space, gap, projection, gauge, topology, hopping, localization, and exact-wire
observations. Smooth/rough frame coordinates, projector bytes, and some reciprocal
matrices remain unavailable and are not inferred. Encoded content and digest identity
do not establish a mathematical retained space/operator, physical convergence,
scientific validation, uncertainty quantification, or acceptance.
