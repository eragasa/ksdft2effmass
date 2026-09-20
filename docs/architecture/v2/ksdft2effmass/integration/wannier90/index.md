# Wannier90 integration

`ksdft2effmass.integration.wannier90` owns deterministic anti-corruption adapters for
native Wannier90 artifacts. The current boundary authenticates explicitly named,
caller-supplied bytes by size and SHA-256 and parses `.nnkp`, `.eig`, `.amn`, `.mmn`,
`_u.mat`, `_hr.dat`, and `.wout` bytes into immutable typed records. Authentication
and parsing remain separate Actions.

The package does not:

- execute Wannier90;
- implement localization, disentanglement, or spread optimization;
- discover native files or symbolic run roots;
- discover a manifest or choose which artifact inventory is authoritative;
- interpret authenticated `.win`, `.chk`, log, or other unsupported payloads;
- apply an `_hr.dat` degeneracy/interpolation convention; or
- claim numerical agreement or scientific validation.

The Appendix G campaign adapter extracts its expected artifact inventory from the
retained result document. Its native-artifact Workflow requires the caller to supply
all named bytes, authenticates the complete inventory, parses the seven supported
scientific text formats, checks shared k-point/band/Wannier dimensions, and correlates
parsed final centers and Wannier count with the retained result. It does not execute
Wannier90 or infer Wilson phases from native gauge matrices. Downstream interpolation
or alignment still requires an explicit owning convention.
