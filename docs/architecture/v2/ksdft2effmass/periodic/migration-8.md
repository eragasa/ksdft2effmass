# Migration phase 8: campaign architecture correction

## Status

**Implemented.** The dimension-only `Periodic2DCampaign` definition, module, imports,
facade exports, and inheritance are removed after all ten concrete campaigns became
independent immutable composition roots.

## Purpose

Remove campaign inheritance that implies no useful shared executable contract and
complete the one-way dependency from campaigns to scientific models and results.

## Included crosswalk entry

Phase 8 completes `PERIODIC-XWALK-073` after phases 3, 4, and 7 have removed its
accidental model/document coupling.

## Required correction

1. Remove `Periodic2DCampaign` inheritance from each concrete 2D campaign.
2. Preserve each concrete campaign's immutable fields, equality, hashing, slots,
   constructor behavior, execution routes, and public supported identity.
3. Delete the dimension-only base and its public export after no consumer remains.
4. Do not introduce `Periodic1DCampaign`, `Periodic3DCampaign`, a structural campaign
   protocol, or a generic campaign Workflow as replacement symmetry.
5. Keep campaign definitions, calculation requests, correlation, verification,
   serializers, and acceptance policy with their concrete domain owners.
6. Ensure campaigns consume nominal models, retained scientific objects, represented
   operators, or encoded documents through explicit typed fields.

## Inheritance audit

The correction preserves each frozen slotted dataclass's single exact document field,
generated constructor, equality, hashing, public identity, and campaign-specific
methods. Their direct base is now exactly `object`. No operation used inherited state;
the removed base supplied only a constant spatial-dimension property. Facade imports
load without cycles, and the former defining module fails to import.

`python/tests/software_verification/ksdft2effmass/periodic2d/campaign/test__Periodic2DCampaign.py`
checks both facade absences, defining-module absence, and direct bases for all ten
concrete campaign classes. No compatibility alias, empty replacement base, 1D/3D
counterpart, protocol, registry, or generic Workflow remains.

## Excluded work

Phase 8 does not merge campaign calculations, create common serializers or verifiers,
change numerical policy, or declare campaigns compatible merely because they are 2D.

## Completion evidence

- A source scan finds no `Periodic2DCampaign` definition, import, export, inheritance,
  or runtime check in production source.
- All ten former subclasses retain concrete public routes and now instantiate
  correlation/verifier Actions per request rather than as replaceable class attributes.
- The former `campaign/base.py` and its Sphinx page are deleted; maintained API text
  documents independent composition roots.
- Focused campaign/API coverage passes (`226 passed`), strict mypy passes for all
  147 scoped source/test files, and scoped Ruff format/check passes.
- Strict Sphinx, architecture-link, broader regression, and final diff gates are rerun
  after the synchronized crosswalk edits.

Passing these software checks establishes only the architecture correction. It does not
establish compatibility among campaigns, scientific validation, convergence,
uncertainty quantification, or acceptance.
