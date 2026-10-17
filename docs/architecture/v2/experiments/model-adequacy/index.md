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
- [Band-equivalence dimensional extension](band-equivalence-dimensional-extension.md).
- [Band-equivalence test and diagnostic parity](band-equivalence-test-and-diagnostic-parity.md).

## Child map

The current architecture covers controlled periodic 2-D and 3-D families.

- [Orthogonal periodic 2-D experiments](periodic2d/index.md).
- [Non-orthogonal periodic 2-D experiments](periodic2d_nonorthog/index.md).
- [Orthogonal periodic 3-D experiments](periodic3d/index.md).
- [Non-orthogonal periodic 3-D experiments](periodic3d_nonorthog/index.md).
- Periodic 1-D maintained experiments have not yet migrated into this architecture mirror.
- Dimension-specific 2-D and 3-D band-equivalence/locality children now have prospective
  protocols and matching architecture bundles.

## Current status

The selected 2-D/3-D sequence remains pre-version work.

- Isotropic 2-D hopping-shell adequacy has a maintained prospective protocol, active
  development task, and legacy HSH design bundle.
- Isotropic 3-D hopping support has an active development task but no frozen protocol.
- Square-lattice, graphene-inspired honeycomb, simple-cubic, and silicon-inspired
  diamond band-equivalence/locality families now have bounded three-level matrix-free
  tensor actions that produce independently verified, strict-schema-validated canonical
  documents. Replaceable numerical artifacts are not retained in this source tranche.
  The families remain pre-version, lack a complete diagnostic-parity and convergence
  disposition, and are outside retained evidence.
- Separate 2-D rhombic and 3-D Bain deformation families now have publication-independent
  protocols, bounded frozen-parent M0 diagnostics, and separately labeled M1/M2 smoke
  actions. Their canonical result documents now have distinct strict packaged M0/M1/M2
  schemas. Typed input/verification binding, independent artifact verification,
  convergence, and retained evidence remain open.
- Anisotropic 2-D has a selected identity but no opened task or protocol.
- Anisotropic 3-D has a preserved exact proposal and exploratory threshold-design record.
- None has an immutable version or retained result.

## Limitations

Legacy prospective HSH pages remain under the installed-package architecture as design
inputs until concrete composition is fully re-homed.

- Their old `python/src/ksdft2effmass` mapping is not implementation authority.
- New concrete architecture is owned by this experiment mirror.
- Reusable extraction requires later cross-owner review.
