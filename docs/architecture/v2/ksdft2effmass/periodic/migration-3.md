# Migration phase 3: encoded campaign documents

## Status

**In progress.** Rows 037--049 are implemented through
`work/periodic-wannier90-encoded-documents`. The periodic-1D campaign remains under
development, so its calculation-directory verifier adapters and checksum catalog
evolve with the public campaign API.

## Purpose

Correct software names and ownership for records that preserve encoded campaign input,
result, or auxiliary documents. This phase is a terminology and ownership migration,
not a scientific-retention implementation.

## Included crosswalk entries

Phase 3 implements `PERIODIC-XWALK-037` through `PERIODIC-XWALK-057` from
[`current-to-target-class-crosswalk.md`](current-to-target-class-crosswalk.md).

## Crosswalk implementation checklist

A box is checked only after the source disposition, affected imports and exports,
tests, documentation, and preservation checks for that exact migration unit are
complete. Renaming a definition without migrating every consumer does not complete an
entry.

### Pure periodic1d document containers

- [x] `PERIODIC-XWALK-037`: replace
  `Periodic1DIsolatedBandCampaignModel` with
  `Periodic1DIsolatedBandEncodedDocuments`.
- [x] `PERIODIC-XWALK-038`: replace `Periodic1DCompositeCampaignModel` with
  `Periodic1DCompositeEncodedDocuments`.
- [x] `PERIODIC-XWALK-039`: replace `Periodic1DStressCampaignModel` with
  `Periodic1DReductionChallengeEncodedDocuments`. The target name describes challenges
  to the nominal reduction assumptions and does not denote mechanical stress.

### Compound periodic1d integration documents

- [x] `PERIODIC-XWALK-040`: split `Periodic1DWannier90IntegrationModel` into
  `Periodic1DWannier90EncodedDocuments` and the existing typed native-artifact-group
  ownership.

### Path-bearing periodic1d defect bundles

- [x] `PERIODIC-XWALK-041`: replace `BlindAlignmentCampaignModel` with
  `BlindAlignmentEncodedDocuments` and move `repository_root` to a campaign request.
- [x] `PERIODIC-XWALK-042`: replace `ContinuumRefinementCampaignModel` with
  `ContinuumRefinementEncodedDocuments` and move `repository_root` to a campaign
  request.
- [x] `PERIODIC-XWALK-043`: replace `FiniteRankOracleCampaignModel` with
  `FiniteRankOracleEncodedDocuments` and move `repository_root` to a campaign request.
- [x] `PERIODIC-XWALK-044`: replace `RouteReconciliationCampaignModel` with
  `RouteReconciliationEncodedDocuments` and move `repository_root` to a campaign
  request.

### Periodic1d encoded result documents

- [x] `PERIODIC-XWALK-045`: replace `Periodic1DRetainedResultDocument`,
  `Periodic1DRetainedResultKind`, and `Periodic1DRetainedResultJsonSerializer` with
  `Periodic1DEncodedResultDocument`, `Periodic1DEncodedResultKind`, and
  `Periodic1DEncodedResultJsonSerializer`.

### Periodic2d document containers

- [x] `PERIODIC-XWALK-046`: replace
  `Periodic2DIsolatedBandCampaignModel` with
  `Periodic2DIsolatedBandEncodedDocuments`.
- [x] `PERIODIC-XWALK-047`: replace `Periodic2DCompositeCampaignModel` with
  `Periodic2DCompositeEncodedDocuments`.
- [x] `PERIODIC-XWALK-048`: replace `Periodic2DTopologicalCampaignModel` with
  `Periodic2DTopologicalEncodedDocuments`.
- [x] `PERIODIC-XWALK-049`: replace
  `Periodic2DTopologicalPhaseSweepCampaignModel` with
  `Periodic2DTopologicalPhaseSweepEncodedDocuments`.
- [ ] `PERIODIC-XWALK-050`: replace
  `Periodic2DWannier90BalancedCampaignModel` with
  `Periodic2DWannier90BalancedEncodedDocuments`.
- [ ] `PERIODIC-XWALK-051`: replace `Periodic2DWannier90StudyCampaignModel` with
  `Periodic2DWannier90StudyEncodedDocuments`.
- [ ] `PERIODIC-XWALK-052`: replace `Periodic2DOptimizerBasinCampaignModel` with
  `Periodic2DOptimizerBasinEncodedDocuments`.
- [ ] `PERIODIC-XWALK-053`: replace
  `Periodic2DOptimizerReanalysisCampaignModel` with
  `Periodic2DOptimizerReanalysisEncodedDocuments`.
- [ ] `PERIODIC-XWALK-054`: replace
  `Periodic2DOptimizerRegressionCampaignModel` with
  `Periodic2DOptimizerRegressionEncodedDocuments`.
- [ ] `PERIODIC-XWALK-055`: replace
  `Periodic2DOptimizerStandaloneCampaignModel` with
  `Periodic2DOptimizerStandaloneEncodedDocuments`.

### Existing result-document owners

- [ ] `PERIODIC-XWALK-056`: verify
  `Periodic2DIsolatedBandResultDocument` remains an encoded result document under the
  canonical campaign owner and correct any misleading module or import ownership.
- [ ] `PERIODIC-XWALK-057`: verify or move each existing defect result-document owner
  without changing payloads:
  - [ ] `ContinuumRefinementCampaignResultDocument`;
  - [ ] `FiniteRankOracleCampaignResultDocument`; and
  - [ ] `RouteReconciliationCampaignResultDocument`.

### Cross-cutting synchronization

- [ ] Remove former payload-only class definitions, imports, exports, aliases, and
  forwarding modules.
- [ ] Update every consuming campaign, request, serializer, correlator, verifier,
  Workflow, test, and Sphinx page.
- [ ] Verify exact field-byte equality and SHA-256 identity for every renamed owner.
- [ ] Confirm calculation payloads, reports, and provenance are unchanged and each
  `SHA256SUMS` catalog validates after any in-development adapter update.
- [ ] Run the phase completion gate and record any unavailable check.

## Source slices

### 3.1 Pure encoded-document containers

Rename every `...CampaignModel` whose owned scientific state consists only of exact
payload bytes to `...EncodedDocuments`.

- Move 1D records out of `model/retained/` into campaign-owned document modules under
  the existing `ksdft2effmass.campaigns.periodic_1d` namespace.
- Move 2D records out of `model/retained/` into document modules below
  `ksdft2effmass.periodic2d.campaign`.
- Update concrete campaigns, requests, serializers, verifiers, exports, tests, and
  Sphinx pages to consume the renamed record.
- Remove the old class definitions and imports without compatibility aliases or
  forwarding modules.

The 1D namespace does not migrate to `ksdft2effmass.periodic1d` in this slice; that is
phase 5.

### 3.2 Compound Wannier90 bundle

Split `Periodic1DWannier90IntegrationModel` into encoded-document ownership and its
existing typed native-artifact groups. The encoded owner stores the same composite
input and result bytes and result-kind identity. Native artifact records retain their
existing path, digest, role, and grouping semantics.

### 3.3 Encoded result-document terminology

Rename archival uses:

- `Periodic1DRetainedResultDocument` to `Periodic1DEncodedResultDocument`;
- `Periodic1DRetainedResultKind` to `Periodic1DEncodedResultKind`; and
- `Periodic1DRetainedResultJsonSerializer` to
  `Periodic1DEncodedResultJsonSerializer`.

Names such as `Periodic1DRetainedLocalizationResult` remain unchanged because they
describe selected-space scientific content rather than archival persistence. The currently named stress document owner becomes
`Periodic1DReductionChallengeEncodedDocuments`; the complete campaign-family rename is
owned by row 060 rather than this document-only slice.
`Periodic2DIsolatedBandResultDocument` and defect result-document records already state
document ownership and require only relocation or import correction where applicable.

### 3.4 Path-bearing defect source bundles

Split each defect-campaign `...CampaignModel` that combines input/result bytes with
`repository_root`:

- the new `...EncodedDocuments` DataObject owns exact bytes only; and
- an existing or dedicated campaign request owns repository location and filesystem
  access.

This split must not move filesystem behavior into the encoded DataObject or create a
generic repository manager.

## Preservation contract

For every renamed, relocated, or split record:

- payload fields remain exact `bytes` and are never decoded and re-encoded merely for
  migration;
- payload byte sequences and SHA-256 identities remain unchanged;
- experiment identifiers, result kinds, provenance strings, and repository-relative
  paths remain unchanged;
- calculation input, result, report, and figure payloads remain unchanged;
- in-development verifier adapters may migrate with the public API, and their
  `SHA256SUMS` entries are updated in the same change so the complete catalog validates;
- serializers reconstruct the same typed semantic content;
- wrong runtime types remain rejected rather than coerced;
- no class gains `PeriodicModel` inheritance because of its former location; and
- no old name remains through alias, re-export, forwarding module, or deprecated route.

## Excluded work

Phase 3 does not:

- implement a retention construction, retained space, or retained operator;
- migrate scientific parent, defect, or effective models;
- change calculation, correlation, verification, or acceptance policy;
- rerun a retained calculation or native external program;
- alter a numerical value, tolerance, schema version, or wire format; or
- remove `Periodic2DCampaign`.

## Completion gate

Phase 3 is complete only when:

1. rows 037--057 have implemented terminal dispositions;
2. source, public exports, tests, Sphinx pages, and architecture prose use encoded
   document terminology consistently;
3. a source scan finds no former payload-only `...CampaignModel` definition or import;
4. fixture tests establish exact field-byte and digest preservation through renamed
   owners;
5. retained verifier CLIs and affected campaign software and numerical tests pass
   without modifying retained payloads; and
6. formatting, Ruff, source and targeted-test mypy, Sphinx warnings-as-errors,
   documentation links, and `git diff --check` pass or an unavailable gate is reported.
