<!-- Generated from SQLite control state; do not edit. -->
# Periodic electronic-structure record extraction

[Task index](index.md) · [Previous](./bulk-silicon.artifacts.qe.inventory.md) · [Next](./bulk-silicon.simulation.qe.reference.md)

## Status

`active`: Explicitly activated after human acceptance of bulk-silicon.artifacts.qe.inventory. The first bounded implementation is limited to the observed compact QEXSD source silicon.save/data-file-schema.xml and must present a proposed minimal record boundary before implementation. Automatic successor activation remains disabled; no other Task is active.

## Objective

Determine and implement the minimal periodic electronic-structure records supported by observed QE tutorial artifacts and accepted scientific conventions.

## Parent and prerequisites

- Depends on: `bulk-silicon.artifacts.qe.inventory`

## Authority references

- calculations/bulk-silicon/qe-example01-si-scf-davidson/artifact-inventory.json
- calculations/bulk-silicon/qe-example01-si-scf-davidson/artifact-inventory.md
- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Use only the observed compact QEXSD source silicon.save/data-file-schema.xml for the first bounded implementation.
- Extract lattice vectors and units; reciprocal-lattice vectors and units; atomic species and positions; k-points and weights; Kohn-Sham eigenvalues and occupations; total energy; FFT-grid metadata; exit status; creator and QEXSD version; and source-artifact identity.
- Keep mechanical QEXSD parsing separate from immutable semantic record construction.
- Make units, indexing, source conventions, and provenance explicit; represent absent energy reference, spin convention, gauge information, basis information, and physical interpretation as unavailable rather than inferred.

## Completion criteria

- Every extracted field has an identified source, unit, convention, and provenance.
- Parsing and semantic adaptation have focused software-verification evidence.
- Unsupported and unavailable information remains explicit.
- Any public record contract has synchronized schema, fixture, runtime, and documentation surfaces.

## Exclusions

- Do not parse wfc*.dat, charge-density.dat, stdout iteration history, band-calculation outputs, HDF5, Wannier90 artifacts, another backend, or any artifact other than the observed data-file-schema.xml in the first bounded implementation.
- No universal DFT API or unsupported backend-neutral field is introduced.
- Kohn–Sham eigenvalues are not treated as a unique represented operator or complete many-body spectrum.
- No hidden unit, basis, gauge, geometry, energy-zero, spin, or physical-interpretation transformation is permitted.
- Software verification does not establish scientific validation.

## Historical source

No archived source.
