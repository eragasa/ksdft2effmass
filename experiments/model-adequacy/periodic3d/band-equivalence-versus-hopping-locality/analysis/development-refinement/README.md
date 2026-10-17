# Simple-cubic bounded development refinement

Status: **replaceable three-mesh diagnostics; not qualified scientific evidence**.

The numerical JSON outputs are intentionally excluded from this source integration. The
summary below reports completed bounded local development runs; rerun the maintained
actions to recreate replaceable artifacts.

The unchanged simple-cubic definition has now been repeated at construction meshes
`8^3`, `16^3`, and `32^3`, with separately shifted evaluation meshes `17^3`, `33^3`, and
`65^3`. The matrix-free implementation consumes owner centered-mesh tensor FFTs and
tensor-product or bounded selected-mode Fourier evaluation, then evaluates KSD-owned
complete physical shells one at a time; it never materializes a dense global
cell--orbital operator or point-by-all-block phase matrix.

The `N32` verification record reports `passes: true` and maximum stored identity defect
`1.3252199345370914e-14`. All six first-passing decision sets remain unchanged on both
successive refinements. At `N32`, the largest interpolation Hamiltonian error is
`3.392451599378968e-15`, the smallest sampled external isolation gap is
`1.0579913866420914 E_ref`, and the largest flat-correlation quadrature defect is
`1.1102230246251565e-16`.

The local `N32` action completed in approximately 33 seconds with about 760 MB peak
memory in the measured development environment. The rotated endpoint still has unresolved
outcomes at the unchanged shell cap. A formal convergence disposition remains blocked on
the complete Paper 1 diagnostic-parity comparison and frozen channel-specific tolerances.
Reproduce with:

```bash
python/.venv/bin/python experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/run_first_refinement.py
python/.venv/bin/python experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/run_second_refinement.py
```
