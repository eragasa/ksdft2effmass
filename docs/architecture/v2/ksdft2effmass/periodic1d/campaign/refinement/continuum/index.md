# `ksdft2effmass.periodic1d.campaign.refinement.continuum`

## Purpose and status

This implemented canonical package owns the periodic-1D separated
continuum-refinement campaign. Row 063 moved the implementation to
`ksdft2effmass.periodic1d.campaign.refinement.continuum` without a compatibility
alias, wire change, or dependency on the former underscored campaign route.

The campaign varies continuum mesh, continuum domain, lattice supercell, lattice scale,
and profile family as separate axes. The package name does not make encoded bytes,
repository paths, a parent lattice operator, a parabolic continuum approximation,
represented spectra, frozen criteria, or retained conclusions interchangeable.

## Public facade

The reviewed current facade exports exactly:

- `ContinuumRefinementCampaign`;
- `ContinuumRefinementCampaignResultDocument`; and
- `ContinuumRefinementEncodedDocuments`.

Lower-level input, verification, workflow, and numerical-operation types remain
available from defining implementation modules and are not flattened into the leaf
facade.

## Child map

| Child | Responsibility | Canonical page |
|---|---|---|
| `campaign` | Facade calculation, retained correlation, and independent-verification entry points | [Campaign](campaign/index.md) |
| `encoded_documents` | Exact input and retained-result bytes, excluding repository location | [Encoded documents](encoded_documents/index.md) |
| `result_documents` | Exact encoded result wire and derived content identity | [Result documents](result_documents/index.md) |
| `workflow` | Closed input contracts, authenticated parent loading, distinct numerical Actions, result assembly, and serialization | [Workflow owners](workflow/index.md) |
| `verification` | Verification request/result contracts and independent numerical reconstruction | [Verification owners](verification/index.md) |

The [numerical-techniques and scientific-reasoning narrative](numerical-techniques-and-scientific-reasoning.md)
explains the represented parent and comparator, lattice scaling, Fourier conventions,
profile normalizations, five independent refinement operations, diagnostics, frozen
decision logic, retained finite observations, independent reconstruction, error
accounting, literature relationship, and scientific non-claims.

## Ownership and dependency boundary

Encoded documents own bytes only. Retained correlation receives an explicit absolute
repository-root method argument because it performs authenticated source access and
recalculation. Independent verification owns the absolute root in
`ContinuumRefinementVerificationRequest`; constructing that request performs no
filesystem access. Neither boundary derives provenance from a path or digest.

## Row-063 dossier

- **Supported imports:** the leaf facade exports only
  `ContinuumRefinementCampaign`, `ContinuumRefinementCampaignResultDocument`, and
  `ContinuumRefinementEncodedDocuments`; the `refinement` parent facade exports that
  same reviewed set. Lower-level owners remain available only from their defining
  modules.
- **Sphinx mapping:** `doc/sphinx/api/ksdft2effmass/periodic1d/campaign/continuum-refinement.rst`
  documents every defining module and states the finite scientific boundary.
- **Provenance:** retained artifacts remain under
  `calculations/research-monograph/impurity-defect-1d-continuum-refinement/`; migration
  changes no retained bytes and performs no calculator execution.
- **Tests-as-evidence:** canonical facade, former-route removal, import independence,
  exact encoded-document identities, and result-document identity are bound by
  `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/`.
  The mirrored ownership manifest is in that directory's `resources/` child.
- **Claim boundary:** exact bytes and passing reconstructions establish bounded
  software/numerical consistency only. They do not prove asymptotic convergence,
  physical adequacy, material validation, transferability, uncertainty
  quantification, or acceptance.

Rows 042 and 057 retain the encoded-pair and result-document evidence inherited by
this family. Row 063 additionally establishes canonical source ownership and former
route removal. The retained calculation is consumed read-only; this dossier does not
rerun it or authenticate undeclared transitive sources.

Original local work under the repository license.
