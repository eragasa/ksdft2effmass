# PAW and pseudopotential capabilities

PAW, norm-conserving pseudopotentials, and ultrasoft pseudopotentials are core-
treatment choices, not backend identities. The neutral periodic specification
records the required formalism and provenance; a concrete backend reports
whether it can satisfy that request. No generic `PAWCalculator` superclass is
approved.

## PAW representations

The PAW transformation is

$$
|\psi_{n\mathbf k}\rangle
=
\hat{\mathcal T}|\widetilde{\psi}_{n\mathbf k}\rangle.
$$

Auxiliary smooth Bloch states and reconstructed all-electron Bloch states are
distinct. They are also distinct from projector coefficients, augmentation
information, Wannier overlap matrices, and Wannier projection matrices. Every
future wavefunction-like artifact must declare its representation; unlike
representations must not be compared as though they were identical.

Prospective artifact categories such as `AUXILIARY_PSEUDO`, `PAW_RECONSTRUCTED`, `PROJECTOR_COEFFICIENTS`, `WANNIER_OVERLAP_MATRICES`, `WANNIER_PROJECTION_MATRICES`, and `NOT_AVAILABLE` are architecture concepts only. The first two are wavefunction representations; the projector/Wannier entries are product roles; `NOT_AVAILABLE` is an availability state. A future contract may store those as separate fields. No generic wavefunction DataObject is implemented.

## Paired-backend matching

Future QE–ABINIT numerical comparisons classify pseudopotentials as:

- `EXACT_ARTIFACT`: the same checksummed artifact is officially supported by
  both backends with the same semantics;
- `COMMON_GENERATION_LINEAGE`: backend-specific artifacts share generator,
  generation inputs, XC functional, valence configuration, relativistic
  treatment, and core model;
- `MATCHED_PHYSICAL_SPECIFICATION`: explicitly matched physical
  characteristics without identical generation;
- `UNMATCHED`: pseudopotential differences materially confound comparison.

The same element, XC functional, or broad PAW/norm-conserving label does not
establish identity. No pseudopotential family is selected by the current
architecture pass. Selection remains a later human scientific decision.

See the authoritative [periodic integration architecture](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/architecture/periodic-electronic-structure-integration.md).
