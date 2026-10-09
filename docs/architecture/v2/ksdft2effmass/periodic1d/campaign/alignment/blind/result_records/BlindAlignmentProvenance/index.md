# `BlindAlignmentProvenance`

## Purpose and status

Represent retained version-one execution provenance.

This implemented row-062 immutable DataObject is defined by
`ksdft2effmass.periodic1d.campaign.alignment.blind.result_records.BlindAlignmentProvenance`.

## Contract and ownership

Documented public fields or operations: `input_path`; `input_sha256`; `script_path`; `script_sha256`; `python_version`; `numpy_version`.

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
