# M1 implementation

## Algorithm

`Periodic1DIsolatedBandCalculator.execute()` performs the following ordered actions:

1. validate the exact frozen definition type;
2. construct the finite plane-wave reference and convergence sweep;
3. construct finite-difference convergence observations against that reference;
4. evaluate the selected scalar band on training and staggered evaluation meshes;
5. create scalar reciprocal-operator samples from training values;
6. compute the complete discrete Fourier hopping representation;
7. verify complete-model Hermiticity;
8. for each declared range, construct mediated truncation and direct fit;
9. calculate training, evaluation, Parseval, route, and band-shape diagnostics; and
10. construct one immutable correlated result.

## Representation choices

The result retains typed quantity objects rather than unlabelled arrays. Coordinates,
reciprocal period, energy unit, representative ordering, and training/evaluation roles
are preserved through construction. Result post-initialization rejects cross-wired
objects even when their numerical arrays have compatible shapes.

## Serialization

`Periodic1DIsolatedBandResultJsonSerializer` emits schema
`ksdft2effmass.periodic1d.isolated-band-calculation-result.v1`. Keys are sorted,
separators are canonical, nonfinite JSON values are forbidden, complex entries are
encoded as `[real, imaginary]`, and exactly one terminal newline is emitted.

## Independent reconstruction

`Periodic1DIsolatedBandResultVerifier` reconstructs parent spectra, selected-band
samples, direct Fourier blocks, and every retained range diagnostic. It does not call
the producer Action. The standalone retained script adds strict JSON decoding and
package-level provenance checks, but shares NumPy/SciPy and scientific conventions.

## Code mapping

| Stage | Source owner |
|---|---|
| Controls | `periodic1d/isolated_band/definition.py` |
| Producer | `periodic1d/isolated_band/calculate.py` |
| Correlated result | `periodic1d/isolated_band/results.py` |
| Wire format | `periodic1d/isolated_band/serialization.py` |
| Library reconstruction | `periodic1d/isolated_band/verify.py` |
| Retained orchestration | `calculations/ICMSEP2026/conference/paper_1/isolated-band/` |

## External boundary

M1 performs no filesystem write in its domain objects and no external execution. File
creation belongs to retained calculation scripts; Quantum ESPRESSO and Wannier90 are
outside the package.
