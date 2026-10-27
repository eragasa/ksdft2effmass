# Periodic-1D rank-two band-equivalence and locality calculation

**Status:** migration-in-progress development calculation; no retained run or evidence
package exists at this location.

This calculation is the publication-independent numerical owner intended for the active
rank-two calculation used by `Ragasa2026a` version 3. It studies a synthetic
one-dimensional four-state finite-range Bloch parent, its isolated two-band retained
space, smooth momentum-dependent real rotations, and the resulting distinction between
band equivalence and hopping locality.

This is not a Mathieu model, a material model, a production calculation, or scientific
validation. The retained Mathieu1D scalar precursor remains separately owned by
[`calculations/mathieu1d/`](../../../mathieu1d/README.md).

## Current ownership boundary

Calculation-specific definitions, calculations, records, serialization, and independent
reconstruction checks are owned by [`workflow/`](workflow/). Generic matrix-field,
Fourier, optimization, and physical record capabilities remain with their canonical
reusable library owners.

The publication-independent experiment specification remains at:

```text
experiments/model-adequacy/periodic1d/
  band-equivalence-versus-hopping-locality/
```

Its calculation-specific workflow, tests, development producers, tables, plotting code,
and figures have moved into this calculation root. Reusable numerical capabilities
remain in `python/src` or their external owner packages.
Historical M1--M3 and scalar Fourier-reduction packages retain their existing paths and
identities; this directory does not copy, rename, or upgrade them.

## Layout

- [`protocol.md`](protocol.md) records the calculation boundary and migration rules.
- [`workflow/`](workflow/) owns the calculation-specific implementation.
- The root `run_*_development.py` files are thin workflow entrypoints.
- [`tests/`](tests/) owns calculation-workflow software verification.
- [`simulations/`](simulations/README.md) owns the current inputs and tabular development
  results; versioned stages remain open.
- [`analysis/`](analysis/README.md) owns extracted development plotting, narrative, and
  figures; independent versioned analysis verification remains open.
- [`technical-report/`](technical-report/README.md) owns the calculation-facing technical
  report split into reviewable sections.

No stage script is added until that stage has an implemented input/output contract. No
new numerical result is claimed by creating this directory.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Flat-parent baseline | Development producer, result/verification records, refinement tables, and plots exist. |
| Nonflat four-state realization | Separate development definition, producer, verifier, records, tables, and plots exist. |
| Parent-family robustness | Separate development composition and plots exist; it is explanatory, not a retained experiment. |
| Truncation consequences | Separate development definition, producer, records, tables, and plots exist. |
| Momentum and amplitude refinement | Development diagnostics exist; the proposed amplitude ladder does not satisfy the declared interpolation target. |
| `workflow/` | Calculation-local definitions, producers, records, serialization, schemas, and verification to extract to reviewed source owners. |
| Experiment migration source | 40 tracked files under `experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/`: protocol, analysis scripts, tables, narratives, figures, and path contracts; every file must receive a destination or provenance-only disposition. |
| Historical M2 and monograph composite work | Gauge/alignment/hopping donors at the exact historical revision; not this family identity. |
