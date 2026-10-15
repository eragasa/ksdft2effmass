# Model-adequacy experiment architecture

## Purpose

This subtree mirrors experiments that compare declared model-adequacy channels in one
identified candidate-parameter space.

- Shared evidence meanings come from the KSD [admissible-set contract](../../ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md).
- Concrete parameters, channels, thresholds, metric choices, certificate-method bindings, experiment data and retained evidence instantiating owner-defined premises, evidence wrappers, premise-failure policy, dispositions, and interpretations remain experiment-owned.
- No shared Python result type or solver facade is selected here.

## Architecture bundle

The package-level pages define only behavior common to the model-adequacy experiment
family.

- [Science](science.md).
- [Numerics](numerics.md).
- [Implementation](implementation.md).
- [Schematics](schematics.md).
- [Dimensionality and anisotropy ladder](dimensional-anisotropy-ladder.md).

## Child map

The current architecture covers controlled periodic 2-D and 3-D families.

- [Periodic 2-D experiments](periodic2d/index.md).
- [Periodic 3-D experiments](periodic3d/index.md).
- Periodic 1-D maintained experiments have not yet migrated into this architecture mirror.

## Current status

The selected 2-D/3-D sequence remains pre-version work.

- Isotropic 2-D has a maintained prospective protocol, active development task, and
  legacy HSH design bundle.
- Isotropic 3-D has an active development task but no frozen protocol.
- Anisotropic 2-D has a selected identity but no opened task or protocol.
- Anisotropic 3-D has a preserved exact proposal and exploratory threshold-design record.
- None has an immutable version or retained result.

## Limitations

Legacy prospective HSH pages remain under the installed-package architecture as design
inputs until concrete composition is fully re-homed.

- Their old `python/src/ksdft2effmass` mapping is not implementation authority.
- New concrete architecture is owned by this experiment mirror.
- Reusable extraction requires later cross-owner review.
