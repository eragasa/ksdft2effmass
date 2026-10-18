# Isotropic 3-D hopping-support hierarchy

## Identity and status

This package is the architecture home for the second stage of the selected sequence.

- Family ID: `ksdft2effmass.campaign.model-adequacy.periodic3d.isotropic-hopping-support-hierarchy`.
- Intended source: `experiments/model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/`.
- Development task: `docs/tasks/dev/experiments/isotropic3d/`.
- Exact protocol: not yet frozen.
- Current status: active design task with no source or result.

## Architecture bundle

The package pages record the three-dimensional isotropic method at family granularity and
defer algorithm detail to future modules and classes.

- [Science](science.md).
- [Numerics](numerics.md).
- [Implementation](implementation.md).
- [Schematics](schematics.md).

## Scientific role

The experiment introduces a third periodic coordinate while preserving declared cubic
axis-permutation symmetry.

- The parent is a controlled simple-cubic scalar synthetic model.
- One scalar orbital per cell avoids alignment and multiband confounders.
- Candidate classes add complete cubic signed-permutation orbits.
- The result remains distinct from both anisotropic 3-D and bulk silicon.

## Current gates

The exact scientific and numerical controls must be authored before source modules or
classes are selected.

- Freeze the direct and reciprocal lattice convention.
- Freeze the analytic parent and orbit inventory.
- Freeze support classes, samples, weights, channels, domain, metric, and thresholds.
- Freeze certificate and conservative-arithmetic premises.
- Define strict schemas, independent verification, and evidence policy.
