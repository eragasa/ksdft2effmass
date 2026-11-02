# FCC/diamond bounded refinement

Status: **replaceable three-mesh diagnostics; not silicon validation or qualified
scientific evidence**.

The numerical JSON outputs are intentionally excluded from source integration. The
bounded action ladder uses construction meshes `8^3`, `16^3`, and `32^3`, with separately
shifted evaluation meshes `17^3`, `33^3`, and `65^3`. The matrix-free implementation
evaluates complete physical-metric shells without materializing a dense global
cell--orbital operator.

The historical `N32` verification reported `passes: true`, maximum stored identity defect
`1.4534197211617388e-14`, and unchanged pointwise first-passing decision sets on both
successive refinements. Several outcomes remained unresolved at the unchanged shell cap.
The reported synthetic diamond-basis isolation gap is not a silicon material band gap.
These are replaceable historical observations, not retained evidence or a formal
convergence disposition.

Reproduce the bounded action ladder with:

```bash
python/.venv/bin/python calculations/periodic3d_rank2_fcc_diamond/band_equivalence_hopping_locality/run_refinement_01.py
python/.venv/bin/python calculations/periodic3d_rank2_fcc_diamond/band_equivalence_hopping_locality/run_refinement_02.py
```
