# `ksdft2effmass.periodic2d.campaign.nbands_1`

## Purpose and migration status

This package owns the isolated one-band periodic-2D campaign definition, exact encoded
documents, calculation, correlation, serialization, and independent verification
surfaces. These responsibilities remain separate.

Crosswalk row 046 reconciles the encoded input/result pair. Row 056 reconciles the
encoded result-document owner under `result_documents` without changing its public name
or payload contract. Row 067 completes the wider decomposition into strict definition
and provenance, calculation, correlation, and independent verification Requests,
Results, and Actions. The campaign record is an independent immutable composition root
rather than an instance of a generic dimension-only campaign base.

## Child map

- [Encoded documents](encoded_documents/index.md)
  - [`Periodic2DIsolatedBandEncodedDocuments`](encoded_documents/Periodic2DIsolatedBandEncodedDocuments/index.md)
- [Result documents](result_documents/index.md)
  - [`Periodic2DIsolatedBandResultDocument`](result_documents/Periodic2DIsolatedBandResultDocument/index.md)

## Supported imports and evidence

The reviewed facade is `ksdft2effmass.periodic2d.campaign.nbands_1`. Lower-level
implementation owners remain in their defining `definition`, `calculate`, `correlate`,
`result_documents`, `serialization`, and `verify` modules. Exact class and retained-wire
evidence is collected by:

- `python/tests/ksdft2effmass/periodic2d/campaign/nbands_1/test__Periodic2DIsolatedBandCampaign.py`;
- the software-verification modules declared in
  `python/tests/software_verification/ksdft2effmass/periodic2d/campaign/nbands_1/resources/implementation-verification-ownership.json`; and
- `doc/sphinx/api/ksdft2effmass/periodic2d/campaign/nbands_1/serialization.rst`
  plus the campaign API page in `research-monograph-campaigns.rst`.

The retained provenance and exact encoded documents authenticate only the declared
content and implemented reconstruction. Authenticated frame/projector coordinates are
unavailable, so observations are not promoted to a mathematical retained space or
retained operator.

## Claim boundary

Passing establishes closed-schema adaptation, request-scoped execution, content
correlation, and independent software/numerical reconstruction for the retained finite
campaign. It does not establish historical execution, parent-model convergence,
retained-space identity, provenance beyond authenticated declarations, physical
adequacy, scientific validation, uncertainty quantification, or acceptance.
