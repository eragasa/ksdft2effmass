# `ksdft2effmass.analysis`

## Purpose and status

`ksdft2effmass.analysis` owns reusable interpretation of already represented numerical
objects. It does not own experiment composition, filesystem persistence, retained-
evidence policy, or execution authority. Domain-neutral rendering mechanics remain
under `ksdft2effmass.visualizations`; a cohesive analysis child may own its typed
authenticated projection and family-specific figure composition.

## Child map

- [`operators`](operators/index.md) — reusable represented-operator analyses.
- [`subspaces`](subspaces/index.md) — reusable comparisons and analyses of typed
  subspaces.
- [`model_adequacy`](model_adequacy/index.md) — finite represented-model adequacy
  analyses, including the installed multidimensional rank-two
  [band-equivalence/locality lifecycle](model_adequacy/band_equivalence_locality/index.md).

## Ownership boundary

A reusable analysis must implement one cohesive mathematical operation. A list of
analyses chosen for one PIAB1D or QHO1D experiment remains with that experiment or
calculation owner. Similar scripts do not authorize a library orchestrator.

## Dependency rules

`analysis` may consume `operators` and model-independent typed records. The reverse
dependency is forbidden. Calculation and experiment packages may consume `analysis`;
`analysis` must not import them.

## Evidence and limitations

Implemented leaves have focused software-verification evidence only. Canonical bytes,
digests, passing tests, independent finite comparisons, and authenticated rendering do
not establish continuum convergence, uncertainty quantification, material validity,
retained-evidence admission, or publication acceptance.
