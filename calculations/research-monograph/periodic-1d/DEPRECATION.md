# Appendix G historical adapter deprecation

The executable Python files in this directory are frozen historical calculation and
verification artifacts. They remain authenticated by `SHA256SUMS` and by hashes
embedded in retained result and execution records.

They are **deprecated for new execution and new software integration**. Deprecation
does not alter their retained evidentiary meaning, authorize their deletion, or permit
rewriting them as compatibility shims.

New software must use the public owners under:

- `ksdft2effmass.analysis.model_systems.periodic_1d`;
- `ksdft2effmass.solid_state`;
- `ksdft2effmass.analysis`;
- `ksdft2effmass.integration.wannier90`; and
- `ksdft2effmass.campaigns.research_monograph.periodic_1d` when the versioned campaign
  boundary is available.

Any future command-line adapter must be versioned separately from these historical
files and contain typed argument/path adaptation only. It must not claim byte identity
with a retained historical runner unless an independent compatibility check establishes
that exact claim.

No retained Appendix G result, verifier, execution record, or native artifact is
superseded by this notice. No calculation is authorized by it.
