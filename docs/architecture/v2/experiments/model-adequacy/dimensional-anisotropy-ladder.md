# Dimensionality and anisotropy model-adequacy ladder

## Purpose

This page records the human-selected order for controlled hopping-support experiments.

- Stage 1 is isotropic 2-D.
- Stage 2 is isotropic 3-D.
- Stage 3 is anisotropic 2-D.
- Stage 4 is anisotropic 3-D.
- Each stage has an independent family, version, run, evidence, and interpretation identity.

## Stage 1

Isotropic 2-D supplies the square-symmetric starting point.

- Family ID: `ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy`.
- Architecture: [isotropic 2-D package](periodic2d/hopping-shell-hierarchy/index.md).
- Task: [isotropic 2-D development](../../../../tasks/dev/experiments/isotropic2d/index.md).
- Status: maintained prospective protocol with selected controls; no implementation,
  immutable version, or result.

## Stage 2

Isotropic 3-D introduces a third periodic coordinate while preserving axis-permutation
symmetry.

- Family ID: `ksdft2effmass.campaign.model-adequacy.periodic3d.isotropic-hopping-support-hierarchy`.
- Architecture: [isotropic 3-D package](periodic3d/isotropic-hopping-support-hierarchy/index.md).
- Task: [isotropic 3-D development](../../../../tasks/dev/experiments/isotropic3d/index.md).
- Status: selected family and active design task; no frozen protocol or result.

## Stage 3

Anisotropic 2-D removes axis-permutation equivalence while remaining in the already
exercised dimension.

- Family ID: `ksdft2effmass.campaign.model-adequacy.periodic2d.anisotropic-hopping-support-hierarchy`.
- Architecture: [anisotropic 2-D package](periodic2d/anisotropic-hopping-support-hierarchy/index.md).
- Task: not yet opened.
- Status: selected family boundary; no exact protocol or result.

## Stage 4

Anisotropic 3-D combines the dimensional and anisotropy stresses after they have been
isolated separately.

- Family ID: `ksdft2effmass.campaign.model-adequacy.periodic3d.anisotropic-hopping-support-hierarchy`.
- Architecture: [anisotropic 3-D package](periodic3d/anisotropic-hopping-support-hierarchy/index.md).
- Maintained proposal: `calculations/periodic3d/rank1/anisotropic-hopping-support-hierarchy/`.
- Status: exact pre-version proposal and exploratory design record; implementation deferred.

## Terminology

The sequence uses discrete lattice and model symmetry rather than continuous rotational
symmetry.

- `Isotropic` means the child preserves its declared square or cubic axis permutations.
- `Anisotropic` means the child removes axis-permutation equivalence.
- Both may retain declared sign or inversion symmetry.
- Neither term implies a specific material.

## Sequencing rationale

The order changes one architecture stress at a time.

- Isotropic 3-D isolates dimensional extension.
- Anisotropic 2-D isolates symmetry removal.
- Anisotropic 3-D combines both only after the isolated stages.
- The order exposes hidden dimension and symmetry assumptions.
- The order does not make the four outcomes directly subtractable.

## Stage gate

An earlier stage must establish a reviewed architecture and scientific protocol before
implementation advances to the next stage.

- Bind parent, lattice, symmetry, basis, gauge, energy reference, and units.
- Bind maximal coordinates and nested support classes.
- Freeze objective-construction, evaluation, and locality roles.
- Freeze channels, domain, metric, thresholds, resolution, and certificate premises.
- Define strict schemas and independent verification.
- Pin exact dependency and adapter identities.
- Record bounded interpretation and evidence policy.

## Post-sequence generalization

General full-rank 2-D and 3-D lattice-vector capabilities are considered only after the
four concrete stages reveal stable shared behavior.

- Architecture: [general-lattice-vector extension](../../ksdft2effmass/analysis/model_adequacy/general-lattice-vector-extension.md).
- Preserve direct basis, reciprocal dual, Gram metric, orientation, units, rank, and conditioning policy.
- Keep embedded-plane 2-D distinct from periodic 3-D.
- Select concrete finite oblique and triclinic verification cases before claiming general support.
- Assign no experiment-family identity until a concrete scientific question is selected.

## Ownership

The sequence does not authorize premature common software.

- PhysKit owns reusable lattice primitives.
- Numerical owners own reviewed unit-free kernels.
- KSD experiments own geometry meaning, support policy, channels, thresholds, evidence, and interpretation.
- No generic result hierarchy, shell builder, solver facade, or disposition enum is selected.

## Material interpretation

The four stages are synthetic or retained-toy studies rather than versions of a silicon
experiment.

- No stage validates bulk silicon.
- No stage supplies diamond-lattice orbital or valley structure.
- A future silicon study requires a distinct family and exact material provenance.
- Synthetic results do not transfer to a material-reference family.
