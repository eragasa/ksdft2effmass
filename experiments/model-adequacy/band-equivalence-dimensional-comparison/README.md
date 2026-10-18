# Band-equivalence dimensional comparison

This directory is the thin cross-protocol composition root for comparing identically
defined diagnostics from the four Paper 2 band-equivalence-versus-hopping-locality
families. It does not own or replace their geometry, parent, mesh, shell, tolerance,
convergence, run, or evidence identities.

The comparison consumes:

- `periodic2d/band-equivalence-versus-hopping-locality/`;
- `periodic2d_nonorthog/band-equivalence-versus-hopping-locality/`;
- `periodic3d/band-equivalence-versus-hopping-locality/`; and
- `periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`.

The authoritative shared diagnostic requirements remain in
[`../band-equivalence-test-and-diagnostic-parity.md`](../band-equivalence-test-and-diagnostic-parity.md).
The exact comparison rules are stated in
[`comparison-protocol.md`](comparison-protocol.md).

Run the bounded local development composition from the repository root with:

```console
PYTHONPATH=python/src python/.venv/bin/python \
  experiments/model-adequacy/band-equivalence-dimensional-comparison/plot_development.py
```

The sampled shell--scale decision landscapes use a separate composition entry point:

```console
PYTHONPATH=python/src python/.venv/bin/python \
  experiments/model-adequacy/band-equivalence-dimensional-comparison/plot_shell_scale_decision_landscapes.py
```

Both commands write replaceable PNG and PDF outputs under `analysis/development/`.
These outputs establish neither a continuum Pareto frontier, scientific acceptance, nor
retained evidence. No production Quantum ESPRESSO or Wannier90 execution is involved.
