# Separate synthetic topological phase sweeps

## Status and boundary

This is calculated non-DFT synthetic numerical-verification evidence authorized
by `RM-PERIODIC-2D-NONDFT-STUDY-HC06`. Qi--Wu--Zhang, flux-$1/3$ Hofstadter,
and Haldane remain separate finite Bloch operators with separate energy units.
The sweep does not represent a material phase diagram or scientific validation.

## Method

A $51^2$ torus mesh is used for each parameter sample. The primary route uses
normalized eigenvector links; the independent verifier reconstructs every
sample using projector Bargmann loops. Analytic expectations are imposed away
from declared Qi--Wu--Zhang and Haldane phase boundaries. The Hofstadter sweep
is a numerical continuation rather than an analytic transition theorem.

## Calculated results

- **Qi--Wu--Zhang:** the retained Chern sectors change at the analytic
  boundaries $m=-2,0,2$. The sampled brackets are $[-2,-1.9]$,
  $[-0.1,0]$, and $[1.9,2]$ with the implemented mesh convention.
- **Haldane:** the analytic boundaries are
  $M=\pm3\sqrt{3}t_2\sin\phi\simeq\pm0.7794$. The sampled changes are bracketed
  by $[-0.8,-0.75]$ and $[0.75,0.8]$.
- **Hofstadter:** the retained lower-band Chern integer changes from $-1$ to
  zero between superlattice amplitudes $\Delta=1.8$ and $2.0$. From
  $\Delta=2$ through the sampled atomic continuation at $\Delta=12$, no
  further retained-band Chern change occurs. The smallest sampled retained gap
  is $0.0711$ model units at $\Delta=2$.

![Separate topological parameter sweeps.](topological-phase-sweep-summary.png)

The sweep therefore supplies a numerical basis for using $\Delta=4$ as the
Hofstadter trivial control: it lies in the sampled zero-Chern sector connected
to the large-superlattice regime. This is not an exact analytic critical value.

## Verification

From `python/`:

```bash
uv run python \
  ../calculations/research-monograph/periodic-2d/verify_topological_phase_sweep.py \
  ../calculations/research-monograph/periodic-2d/topological-phase-sweep-result.json
```

The verifier reports
`periodic_2d_topological_phase_sweep_verification=PASS`.
