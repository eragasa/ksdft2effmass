# C6-B20-W21 refitted native-shell witness follow-on

Status:
`post-hoc-refitted-ws-producer-checked-development-not-independently-verified`.

This authorized no-calculator follow-on asks whether the nearly one-dimensional loss
curve from literal native Wigner--Seitz shell deletion was caused by the absence of
refittable parameters. It remains in the fixed authenticated rank-10 Wannier basis and
does not introduce Slater--Koster or atomic-orbital semantics.

For each proper support `H-shell-00` through `H-shell-16`, every complete retained shell
has one real scale parameter:

\[
H_{\boldsymbol\alpha}(R)=\alpha_s H_W(R),\qquad 0\leq\alpha_s\leq2,
\]

where the same scale applies to all effective representatives in shell \(s\), including
both \(R\) and \(-R\). Blocks outside the declared support remain zero. The full
`H-shell-17` source remains an excluded exact control.

The producer used 17 spectral/operator scalarization weights and three deterministic
starts with bounded L-BFGS-B and analytic binary64 gradients. The resulting search is
constructive only: a retained parameter vector is an explicit witness, but failure to
find one is not a global infeasibility certificate. Ordered spectral losses are
nonsmooth at exact crossings or degeneracies.

## Headline result

The refitted witnesses no longer lie on the literal-truncation line. Each support
produces a visible spectral/operator tradeoff arc, and the union of those arcs defines a
genuinely two-threshold minimum-support surface over the sampled converged witnesses.
At several illustrative thresholds, refitting reduces the minimum observed support:

| \((\tau_1,\tau_2)\) | literal witness | fitted witness |
|---|---:|---:|
| \((1.0,1.0)\) | H-shell-02, 19 | H-shell-01, 13 |
| \((0.5,0.5)\) | H-shell-03, 43 | H-shell-03, 43 |
| \((0.1,0.15)\) | H-shell-07, 135 | H-shell-05, 79 |
| \((0.05,0.1)\) | H-shell-09, 177 | H-shell-07, 135 |
| \((0.02,0.04)\) | H-shell-11, 225 | H-shell-10, 201 |
| \((0.01,0.02)\) | H-shell-13, 313 | H-shell-13, 313 |
| \((0.002,0.006)\) | H-shell-14, 353 | H-shell-14, 353 |
| \((0.001,0.002)\) | H-shell-16, 371 | H-shell-16, 371 |
| \((0.0004,0.001)\) | none | none found |

These thresholds are illustrative post-hoc readings, not acceptance limits. “None
found” means only that no converged witness from this bounded search satisfies the
pair.

The tightest observed tradeoff remains on `H-shell-16`: its operator-oriented witness
attains approximately \((4.04\times10^{-4},1.394\times10^{-3})\), while its
spectral-oriented witness attains approximately
\((2.98\times10^{-4},1.745\times10^{-3})\). This is now a genuine same-support
spectral/operator tradeoff rather than a single literal deletion point.

## Retained artifacts

- [`request.json`](request.json): frozen scientific and optimization selections;
- [`run_analysis.py`](run_analysis.py): authenticated producer;
- [`result.json`](result.json): evaluated parameter vectors, losses, optimizer records,
  support summaries, and producer checks;
- [`render_surface_v2.py`](render_surface_v2.py): final headline renderer;
- [`witness-surface-v2.json`](witness-surface-v2.json): exact threshold-cell surface,
  deterministic witness selection, and illustrative witnesses;
- [`figures-v2/`](figures-v2/): final PDF/PNG surface and checksum manifest; and
- [`executions/`](executions/): no-overwrite execution records.

The initial [`render_surface.py`](render_surface.py), [`witness-surface.json`](witness-surface.json),
and [`figures/`](figures/) are retained as a superseded rendering attempt. The final
`figures-v2` surface removes cell-edge overplotting without changing witness selection.

## Interpretation rule

The headline surface uses only the 444 retained records with
`optimizer_success == true`. Nonconverged terminal iterates in `result.json` are not
used by the surface, even though their finite parameter vectors can be evaluated. The
surface therefore makes no claim that every attainable fitted witness or every global
Pareto point was found.

No QE or Wannier90 execution was performed. This follow-on does not validate the source
as an adequate silicon Hamiltonian, consume the frozen 402-point confirmation values,
or provide publication-qualified independent reconstruction.
