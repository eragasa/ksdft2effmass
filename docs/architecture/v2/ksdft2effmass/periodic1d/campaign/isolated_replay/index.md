# `periodic1d.campaign.isolated_replay`

## Purpose and status

This is the canonical target page for the implemented row-023 isolated-band replay
adoption behavior. The source remains temporarily in the legacy underscored campaign
namespace until row 058 moves the campaign family without an alias. The module decodes
one retained sidecar, authenticates its frozen inputs, and adopts its numerical content
through explicit parent, retention, representation, and effective-model objects.

## Public inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `Periodic1DReplaySourceCorrelation` | Evidence DataObject | Bind input, retained result, producer, replay producer, and exact replay identities |
| `Periodic1DRangeEffectiveModelArtifacts` | Evidence DataObject | Keep truncated and fitted coefficient inventories separate for one range |
| `Periodic1DIsolatedBandReplayArtifacts` | Retained-evidence aggregate | Exact source objects, sidecar bytes, frame, projector identity, and coefficient inventories |
| `Periodic1DIsolatedBandParentDiscretization` | Numerical evidence | Finite represented parent versus separately identified finite reference |
| `Periodic1DRangeEffectiveModelAdoption` | Reduction-route aggregate | Distinct truncation and fit Actions, comparisons, and allowances |
| `Periodic1DIsolatedBandScientificAdoptionRequest` | Action request | Exact authenticated sources and optional energy allowance |
| `Periodic1DIsolatedBandScientificAdoptionResult` | Action result | Full untruncated-parent to finite-parent to retained/effective graph |
| `Periodic1DIsolatedBandReplayArtifactDecoder` | Decoder Action | Closed JSON decoding and source/content authentication |
| `Periodic1DIsolatedBandScientificAdoption` | Scientific-adoption Action | Construct the typed scientific graph without rerunning the parent calculation |

## Class navigation

- [`Periodic1DReplaySourceCorrelation`](Periodic1DReplaySourceCorrelation/index.md)
- [`Periodic1DRangeEffectiveModelArtifacts`](Periodic1DRangeEffectiveModelArtifacts/index.md)
- [`Periodic1DIsolatedBandReplayArtifacts`](Periodic1DIsolatedBandReplayArtifacts/index.md)
- [`Periodic1DIsolatedBandParentDiscretization`](Periodic1DIsolatedBandParentDiscretization/index.md)
- [`Periodic1DRangeEffectiveModelAdoption`](Periodic1DRangeEffectiveModelAdoption/index.md)
- [`Periodic1DIsolatedBandScientificAdoptionRequest`](Periodic1DIsolatedBandScientificAdoptionRequest/index.md)
- [`Periodic1DIsolatedBandScientificAdoptionResult`](Periodic1DIsolatedBandScientificAdoptionResult/index.md)
- [`Periodic1DIsolatedBandReplayArtifactDecoder`](Periodic1DIsolatedBandReplayArtifactDecoder/index.md)
- [`Periodic1DIsolatedBandScientificAdoption`](Periodic1DIsolatedBandScientificAdoption/index.md)

## Scientific graph and error separation

The untruncated Fourier toy parent, cutoff-11 finite Galerkin parent, rank-one retained
space, frame representation, exact finite-parent invariant restriction, complete
hopping representation, and truncated/fitted effective models remain different
objects. Cutoff-11 versus cutoff-15 evidence is a finite-discretization observation.
Fourier reconstruction and route comparison are numerical reproducibility evidence.
Neither is an untruncated-parent bound or scientific acceptance.

## Retained evidence

`calculations/research-monograph/periodic-1d/replay/isolated-band-v1/artifacts.json`
is the retained sidecar. Its README, protocol, `verify_replay.py`, and `SHA256SUMS`
define source hashes, construction order, independent checks, and claim boundaries.
The sidecar was produced by one separately authorized deterministic replay; this module
does not authorize or rerun it.

## Code, tests, and Sphinx

Current transitional source:
`python/src/ksdft2effmass/campaigns/periodic_1d/isolated_replay.py`.
Documented claim-bearing tests:
`python/tests/software_verification/ksdft2effmass/campaigns/periodic_1d/test__Periodic1DIsolatedBandScientificAdoption.py`.
Public Sphinx coverage: `doc/sphinx/api/research-monograph-campaigns.rst`.

Original local work under the repository license. Passing establishes authenticated
source correlation and bounded software/numerical reproducibility only—not material
relevance, convergence to the untruncated parent, validation, UQ, or acceptance.
