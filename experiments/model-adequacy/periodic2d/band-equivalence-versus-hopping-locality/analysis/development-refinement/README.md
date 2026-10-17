# Square-lattice bounded development refinement

Status: **replaceable three-mesh diagnostics; not qualified scientific evidence**.

The numerical JSON outputs are intentionally excluded from this source integration. The
summary below reports completed bounded local development runs; rerun the maintained
actions to recreate replaceable artifacts.

The unchanged square-family definition has now been repeated at construction meshes
`16 x 16`, `32 x 32`, and `64 x 64`, with separately shifted evaluation meshes
`33 x 33`, `65 x 65`, and `129 x 129`. The matrix-free implementation consumes owner
centered-mesh tensor FFTs and tensor-product or bounded selected-mode Fourier evaluation,
then streams KSD-owned complete physical shells; it never materializes the full
cell--orbital operator.

The `N64` verification record reports `passes: true` and maximum stored identity defect
`1.869365566450181e-14`. All six first-passing decision sets remain unchanged on both
successive refinements. At `N64`, the largest interpolation Hamiltonian error is
`2.397161524971329e-15`, the smallest sampled external isolation gap is
`1.056979659142123 E_ref`, and the largest flat-correlation quadrature defect is
`4.440892098500626e-16`.

These observations provide the required third mesh level, but a formal family convergence
disposition still requires the complete Paper 1 diagnostic-parity comparison and frozen
channel-specific tolerances. Reproduce the two refinement points from the repository root:

```bash
python/.venv/bin/python experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/run_first_refinement.py
python/.venv/bin/python experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/run_second_refinement.py
```
