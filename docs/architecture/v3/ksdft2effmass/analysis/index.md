# `ksdft2effmass.analysis`

## Purpose and status

`ksdft2effmass.analysis` owns reusable interpretation of already represented numerical
objects. It does not own physical model construction, experiment composition, files,
JSON, plotting, or execution authority.

## Child map

- [`operators`](operators/index.md) — reusable represented-operator analyses.
- [`subspaces`](subspaces/index.md) — reusable comparisons and analyses of typed
  subspaces.

## Ownership boundary

A reusable analysis must implement one cohesive mathematical operation. A list of
analyses chosen for one PIAB1D or QHO1D experiment remains with that experiment or
calculation owner. Similar scripts do not authorize a library orchestrator.

## Dependency rules

`analysis` may consume `operators` and model-independent typed records. The reverse
dependency is forbidden. Calculation and experiment packages may consume `analysis`;
`analysis` must not import them.

## Evidence and limitations

The proposed reduction leaves are documentation-first and have no implemented or
exported source contracts yet.
