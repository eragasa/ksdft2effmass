# `ksdft2effmass.periodic2d.run.wannier90.study`

## Purpose and migration status

This package owns the retained periodic-2D Wannier90 sensitivity-study campaign record,
its exact encoded input and result, and an independent portable verification surface.
These responsibilities remain separate from native execution and scientific acceptance.

Crosswalk row 051 reconciles the encoded document pair. The input encodes a reference
case and bounded study axes for reciprocal mesh, plane-wave cutoff, and auxiliary
embedding. Row 071 completes request-scoped portable reconstruction while keeping
native formats and artifacts integration-owned. The byte container does not interpret
those axes, authenticate case completion, or establish convergence. Rows 052–055 and
072 independently own optimizer-family documents and operations.

## Child map

- [Encoded documents](encoded_documents/index.md)
  - [`Periodic2DWannier90StudyEncodedDocuments`](encoded_documents/Periodic2DWannier90StudyEncodedDocuments/index.md)

## Supported imports and evidence

The reviewed facade exposes only `Periodic2DWannier90StudyCampaign` and
`Periodic2DWannier90StudyEncodedDocuments`; verification contracts remain in `verify`.
The exact campaign node is
`python/tests/ksdft2effmass/periodic2d/run/wannier90/study/test__Periodic2DWannier90StudyCampaign.py`,
with retained-artifact nodes in the mirrored software-verification manifest. Sphinx maps
the family in `doc/sphinx/api/ksdft2effmass/periodic2d/run/wannier90-study.rst`.

## Claim boundary

Passing establishes portable reconstruction over declared finite study axes. Encoded
case declarations and observations remain distinct from native artifacts, execution
provenance, convergence evidence, qualified oracles, and scientific conclusions. A
reported completed case is not accepted merely because its bytes and digest are
preserved; no native artifact is accessed and Wannier90 is not rerun.
