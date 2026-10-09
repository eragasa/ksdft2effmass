# `BlindAlignmentEvaluationResult`

## Purpose and status

Record distinct post hoc map, shift, extraction, model, and spectral errors.

This implemented row-062 immutable DataObject is defined by
`ksdft2effmass.periodic1d.campaign.alignment.blind.evaluation.BlindAlignmentEvaluationResult`.

## Contract and ownership

Documented public fields or operations: `identifier`; `phase_quotiented_alignment_frobenius_defect`; `energy_shift_error`; `extraction_frobenius_defect`; `extraction_relative_frobenius_defect`; `planted_onsite_model_class_residual`; `extracted_onsite_model_class_residual`; `active_spectral_maximum_absolute_defect`; `active_lowest_state_fidelity`; `active_lowest_eigenspace_dimension`; `active_lowest_eigenspace_projector_defect`; `alignment_map_sha256`; `extracted_operator_sha256`.

Intrinsic immutable invariants remain with DataObjects. Request-dependent source
authentication, construction, inference, evaluation, correlation, and verification
remain with their named Actions. Exact primitive types, explicit identities, ordered
inventories, finite binary64/complex128 values, and declared represented spaces fail
closed. Names, dimensions, ranks, spectra, paths, filenames, and digests do not infer
scientific identity, compatibility, gauge, provenance, or meaning.

Dense operations, where applicable, use quadratic storage and up to cubic time in the
represented dimension; no arbitrary size cap is imposed and allocation may raise
`MemoryError`.

## Scientific boundary and evidence

This class alone does not establish calculator execution, physical-model adequacy,
convergence, transferability, scientific validation, uncertainty quantification, or
acceptance. See the [module dossier](../index.md) and [family dossier](../../index.md)
for source, test, Sphinx, retained-provenance, and limitation mappings.

Original local work under the repository license.
