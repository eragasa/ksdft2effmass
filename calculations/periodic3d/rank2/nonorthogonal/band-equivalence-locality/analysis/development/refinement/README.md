# Silicon-inspired family bounded development refinement

Status: **replaceable three-mesh diagnostics; not silicon validation or qualified scientific evidence**.

The numerical JSON outputs are intentionally excluded from this source integration. The
summary below reports completed bounded local development runs; rerun the maintained
actions to recreate replaceable artifacts.

The unchanged three-case family has now been repeated at construction meshes `8^3`,
`16^3`, and `32^3`, with separately shifted evaluation meshes `17^3`, `33^3`, and
`65^3`. The matrix-free implementation consumes owner centered-mesh tensor FFTs and
tensor-product or bounded selected-mode Fourier evaluation, then evaluates KSD-owned
complete physical-metric shells one at a time.

The `N32` verification record reports `passes: true` and maximum stored identity defect
`1.4534197211617388e-14`. All 18 pointwise first-passing decision sets remain unchanged on
both successive refinements. At `N32`, every case's largest interpolation Hamiltonian
error is below `3.94e-15`; the silicon-inspired parent's smallest sampled external
isolation gap is `2.005725708052135 E_ref`. This is not a silicon material band gap.
The largest flat-correlation quadrature defect is `4.440892098500626e-16`.

The local `N32` action completed in approximately 80 seconds with about 740 MB peak
memory in the measured development environment. Several outcomes remain unresolved at
the unchanged shell cap. The complete Paper 1 software-level diagnostic-parity
comparison is now closed; a formal convergence disposition remains blocked on frozen
tolerances and cap-policy review. Reproduce
with:

```bash
python/.venv/bin/python calculations/periodic3d/rank2/nonorthogonal/band-equivalence-locality/run_first_refinement.py
python/.venv/bin/python calculations/periodic3d/rank2/nonorthogonal/band-equivalence-locality/run_second_refinement.py
```
