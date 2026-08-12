<!-- Generated from SQLite control state; do not edit. -->
# Periodic electronic-structure record extraction

[Task index](index.md) · [Previous](./bulk-silicon.artifacts.qe.inventory.md) · [Next](./bulk-silicon.simulation.qe.band-reference.md)

## Status

`closed_human_accepted_pass`: Human-accepted PASS for the limited claim that the observed QE 7.2 QEXSD artifact was faithfully transformed through separated Quantum ESPRESSO I/O, periodic-geometry, Kohn–Sham, and plane-wave-record domains with explicit units, coordinate conventions, reciprocal scaling, provenance, and unavailable metadata. Acceptance does not establish numerical convergence beyond the retained tutorial observation, physical validation, transferability to other QE calculations, completeness of the plane-wave basis description, suitability for Wannier or effective-mass analysis, or scientific acceptance of downstream results. Automatic successor activation remains disabled; no successor is active.

## Objective

Determine and implement the minimal plane-wave Kohn-Sham calculation record supported by the observed QE tutorial QEXSD artifact, with QEXSD I/O, periodic geometry, representation-neutral Kohn-Sham semantics, and plane-wave ownership separated.

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
- Make unit system, physical dimension, concrete unit, coordinate convention, scale convention, indexing, source conventions, and provenance explicit; represent absent energy reference, spin convention, gauge information, basis information, and physical interpretation as unavailable rather than inferred.
- Implement the dependency direction io.quantum_espresso.qexsd -> ksdft.pw -> {ksdft, periodic}, with no Quantum ESPRESSO or QEXSD imports from domain packages.

## Completion criteria

- Every extracted field has an identified source, unit, convention, and provenance.
- Parsing and semantic adaptation have focused software-verification evidence.
- Unsupported and unavailable information remains explicit.
- Any public record contract has synchronized schema, fixture, runtime, and documentation surfaces.
- Direct and physical reciprocal lattices satisfy A B^T = 2*pi I under the documented deterministic floating-point criterion.
- Old pre-acceptance periodic record imports and compatibility aliases are absent.

## Exclusions

- Do not parse wfc*.dat, charge-density.dat, stdout iteration history, band-calculation outputs, HDF5, Wannier90 artifacts, another backend, or any artifact other than the observed data-file-schema.xml in the first bounded implementation.
- No universal DFT API or unsupported backend-neutral field is introduced.
- Kohn–Sham eigenvalues are not treated as a unique represented operator or complete many-body spectrum.
- No hidden unit, basis, gauge, geometry, energy-zero, spin, or physical-interpretation transformation is permitted.
- Software verification does not establish scientific validation.

## Historical source

No archived source.
