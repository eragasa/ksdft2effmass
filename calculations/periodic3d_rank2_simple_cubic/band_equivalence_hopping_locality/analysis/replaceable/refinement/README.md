# Simple-cubic bounded refinement

Status: **replaceable three-mesh diagnostics; not qualified scientific evidence**.

The numerical JSON outputs are intentionally excluded from source integration. The
bounded action ladder uses construction meshes `8^3`, `16^3`, and `32^3`, with separately
shifted evaluation meshes `17^3`, `33^3`, and `65^3`. The matrix-free implementation uses
centered-mesh tensor FFTs and bounded Fourier evaluation and evaluates complete physical
shells without materializing a dense global cell--orbital operator.

The historical `N32` verification reported `passes: true`, maximum stored identity defect
`1.3252199345370914e-14`, and unchanged first-passing decision sets on both successive
refinements. The rotated endpoint remained unresolved at the unchanged shell cap. These
are replaceable historical observations, not retained evidence or a formal convergence
disposition.

Reproduce the bounded action ladder with:

```bash
python/.venv/bin/python calculations/periodic3d_rank2_simple_cubic/band_equivalence_hopping_locality/run_refinement_01.py
python/.venv/bin/python calculations/periodic3d_rank2_simple_cubic/band_equivalence_hopping_locality/run_refinement_02.py
```
