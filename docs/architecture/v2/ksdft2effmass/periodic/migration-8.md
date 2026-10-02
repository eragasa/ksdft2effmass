# Migration phase 8: campaign architecture correction

## Status

**Proposed.** `Periodic2DCampaign` remains a provisional dimension-only base inherited
by ten concrete campaign records.

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

The correction must explicitly check:

- dataclass field order and generated constructors;
- equality and hashing behavior;
- slots and instance layout;
- method-resolution order;
- import cycles and public exports;
- exact concrete class identities; and
- tests or documentation that use `isinstance(..., Periodic2DCampaign)`.

No compatibility alias or empty replacement base remains after removal.

## Excluded work

Phase 8 does not merge campaign calculations, create common serializers or verifiers,
change numerical policy, or declare campaigns compatible merely because they are 2D.

## Completion gate

- A source scan finds no `Periodic2DCampaign` definition, import, export, inheritance,
  or runtime check.
- All ten former subclasses retain their concrete behavior and public supported routes.
- Campaign-to-model dependency direction is verified without reverse imports.
- No 1D or 3D campaign base is introduced.
- Focused inheritance/API tests, the affected suite, typing, Ruff, formatting, Sphinx,
  links, and diff checks pass.
