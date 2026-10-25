# Graphene-inspired family bounded development refinement

Status: **replaceable three-mesh diagnostics; not graphene validation or qualified scientific evidence**.

The numerical JSON outputs are intentionally excluded from this source integration. The
summary below reports completed bounded local development runs; rerun the maintained
actions to recreate replaceable artifacts.

The unchanged three-case family has now been repeated at construction meshes `16 x 16`,
`32 x 32`, and `64 x 64`, with separately shifted evaluation meshes `33 x 33`,
`65 x 65`, and `129 x 129`. The matrix-free implementation consumes owner centered-mesh
tensor FFTs and tensor-product or bounded selected-mode Fourier evaluation, then streams
KSD-owned complete physical-metric shells.

The `N64` verification record reports `passes: true` and maximum stored identity defect
`1.9178913778897513e-14`. The previously observed matched-square shell change occurs only
between `N16` and `N32`; all 18 pointwise decision sets are unchanged between `N32` and
`N64`. At `N64`, every case's largest interpolation Hamiltonian error is below
`2.69e-15`. The largest flat-correlation quadrature defect is
`2.220446049250313e-16`.

The inspired parent remains a synthetic connectivity control. The complete Paper 1
software-level diagnostic-parity comparison is now closed. A formal family convergence
disposition still requires frozen channel-specific tolerances and review of unresolved
cap failures. Reproduce with:

```bash
python/.venv/bin/python calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/run_first_refinement.py
python/.venv/bin/python calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/run_second_refinement.py
```
