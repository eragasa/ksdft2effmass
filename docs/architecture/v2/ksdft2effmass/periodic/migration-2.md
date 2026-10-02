# Migration phase 2: current-to-target class crosswalk

## Status

**Implemented on `work/periodic2d-parity` in `ad41d3d1`.** The crosswalk remains an
active migration record until the complete program passes its final source audit.

## Purpose

Classify boundary-defining current types by represented meaning rather than historical
name or package location. The classification prevents payload containers from becoming
scientific models and prevents matrix records from silently becoming retained spaces
or operators.

## Delivered boundary

[`current-to-target-class-crosswalk.md`](current-to-target-class-crosswalk.md) provides
73 ordered migration entries covering:

- nominal and concrete scientific-model candidates;
- retention definitions and missing retained-space/operator ownership;
- represented operators;
- effective-model candidates;
- encoded campaign documents;
- campaign definitions, requests, and results; and
- supporting Actions, serializers, comparison owners, and verifiers.

Each entry records current meaning, target category, disposition, and applicable
preservation constraint or blocker.

## Important findings

- No current class completely owns a manuscript-level retained subspace or exact
  retained operator.
- Payload-only `...CampaignModel` records are encoded campaign documents.
- `BlockHoppingModel1D` is used in both exact-representation and approximation contexts,
  so its construction route cannot be inferred from coefficient data alone.
- `Periodic1DGaussianOnsiteDefectModel` is a perturbation definition without a parent.
- The concrete `periodic2d.defects.Periodic2DDefectModel` collides with the nominal
  defect-base name.
- The dimension-only `Periodic2DCampaign` base has no justified cross-dimensional
  counterpart.

## Excluded work

Phase 2 changed no Python source, import route, payload, manuscript, calculation, or
scientific result. Crosswalk target names are migration dispositions, not compatibility
aliases.

## Retirement

After every row has a terminal implemented disposition and the final audit passes, the
crosswalk is marked completed in one commit. A following commit removes it from active
navigation and records only its immutable Git locator in [`archives.md`](archives.md).
