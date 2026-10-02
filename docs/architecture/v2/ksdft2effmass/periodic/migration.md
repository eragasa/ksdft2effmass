# Migration to the general periodic framework

## Current and target surfaces

The current repository contains several historically independent periodic surfaces:

| Current surface | Current role | Target disposition |
|---|---|---|
| `ksdft2effmass.periodic` | Implemented nominal scientific-model root and toy-catalog contract plus transitional compatibility exports | Migrate concrete models into the nominal branches, then retire the compatibility inventory through reviewed source migration |
| `ksdft2effmass.campaigns.periodic_1d` | Extracted one-dimensional models, retained campaigns, defects, serializers, and Workflows | Separate scientific models from executable campaigns and migrate canonical new work toward `periodic1d` |
| `ksdft2effmass.periodic2d` | Canonical two-dimensional represented mechanics and retained campaigns | Preserve current capability work while separating model and campaign ownership |
| `analysis.model_systems.periodic_1d` and `analysis.model_systems.periodic2d` | Reusable represented numerical constructions | Retain or migrate according to demonstrated ownership; move reusable cross-project mathematics to PhysKit only under an accepted contract |
| Retained `calculations/research-monograph/periodic-1d` and `periodic-2d` paths | Historical evidence and provenance | Preserve paths and bytes |

The committed `Periodic2DCampaign` class predates the accepted model/campaign
separation. It is provisional architecture: it must not be copied into periodic1d or
periodic3d as the scientific hierarchy. A later forward correction will either remove
it or place it under a demonstrated executable campaign owner after the scientific
model hierarchy and consumer are defined. Existing concrete campaign behavior remains
unchanged until that correction is implemented and verified.

## Migration phases

1. **Architecture freeze.** Maintain this directory as the target and reconcile
   conflicting architecture prose by links rather than duplicate definitions.
2. **Nominal scientific foundation (implemented).** The dimension-enforced
   `PeriodicModel` hierarchy, model-role identity, defect bases, and immutable toy-model
   catalog contract are public without campaign behavior or retained-wire state.
3. **One-dimensional adoption.** Migrate demonstrated 1D toy and defect models while
   preserving Appendix G contracts and retained evidence.
4. **Two-dimensional adoption.** Migrate current periodic2d toy and represented-model
   owners, then define the graphene material-reference boundary. The periodic2d parity
   gate remains applicable.
5. **Three-dimensional adoption.** Define bulk-silicon material-reference ownership
   before adding silicon defect models. Do not infer 3D numerical contracts from 1D or
   2D by notation alone.
6. **Catalog execution.** Register the migrated models in an explicit catalog and add
   one campaign that consumes an exact immutable catalog snapshot.
7. **Comparison families.** Add compatibility-gated comparison quantities and typed
   unavailable outcomes before attempting all-model reports.
8. **Campaign migration.** Separate immutable campaign definitions, executable
   Actions or Workflows, results, correlation, and independent verification.
9. **Defect progression.** Continue dimension-specific defect campaigns only after
   their parent model, represented-space, and comparison prerequisites pass the
   applicable gates.

## Gate matrix

| Capability | 1D | 2D | 3D |
|---|---|---|---|
| Scientific model hierarchy | Foundation implemented; concrete migration proposed | Foundation implemented; concrete migration proposed | Foundation implemented; no concrete models |
| Toy-model inventory | Existing models; catalog registration pending | Existing models; catalog registration pending | No registered models |
| Defect-model hierarchy | Nominal base implemented; existing campaign-specific defects not migrated | Nominal base implemented; new concrete work gated by periodic2d parity | Nominal base implemented; no concrete models |
| Material-reference family | No family selected | Graphene target selected; specification absent | Bulk silicon target selected; existing project evidence requires integration |
| Catalog campaign | Not implemented | Not implemented | Not implemented |
| Cross-model comparison | Existing local comparisons only | Existing local common-space comparison only | Not implemented |

“Proposed” and “not implemented” are architecture status labels, not failed scientific
results. Existing calculated evidence retains its original status.

## Migration invariants

- Do not rewrite retained payloads, checksums, experiment identifiers, or provenance
  paths solely for source reorganization.
- Do not add empty 3D implementations to create apparent symmetry.
- Do not treat graphene or silicon material-reference labels as validation.
- Do not generalize operator subtraction across unidentified state spaces.
- Do not combine parent-model, numerical, and reduction errors.
- Do not introduce a generic method base that erases concrete request inputs.
- Use forward commits; do not rewrite the existing periodic2d branch history.

## Completion boundary

Architecture migration is complete only when source, typing, tests, public exports,
Sphinx documentation, applicable specifications, and retained adapters agree. Passing
that software gate does not authorize or establish production calculations,
scientific validation, uncertainty quantification, publication, or release.
