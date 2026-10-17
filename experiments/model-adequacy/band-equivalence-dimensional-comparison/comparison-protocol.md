# Cross-protocol tolerance-requirement comparison

## Purpose

This pre-version development protocol compares two identically defined operator-mismatch
requirements across the four independently interpreted Paper 2 dimensional families. It
is a cross-protocol synthesis, not a fifth dimensional experiment family.

## Inputs

The composition evaluates the explicit bounded development request from each of four
independent family protocols and consumes the resulting typed diagnostics directly.

| Input protocol | Maintained source |
|---|---|
| Orthogonal square 2-D | [`../periodic2d/band-equivalence-versus-hopping-locality/`](../periodic2d/band-equivalence-versus-hopping-locality/) |
| Nonorthogonal triangular/honeycomb 2-D | [`../periodic2d_nonorthog/band-equivalence-versus-hopping-locality/`](../periodic2d_nonorthog/band-equivalence-versus-hopping-locality/) |
| Orthogonal simple-cubic 3-D | [`../periodic3d/band-equivalence-versus-hopping-locality/`](../periodic3d/band-equivalence-versus-hopping-locality/) |
| Nonorthogonal FCC/diamond 3-D | [`../periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](../periodic3d_nonorthog/band-equivalence-versus-hopping-locality/) |

Each input retains its own family identity, geometry, parent cases, construction and
evaluation meshes, amplitude and parent-scale samples, shell cap, and tail-error
tolerances. No dimensional result is substituted for another, and no tolerance or
convergence outcome is transferred between protocols.

## Displayed quantities

For every sampled point at which restricted alignment is applicable, the map displays:

1. the minimum restricted operator threshold after positive splitting-scale
   optimization, normalized by $\sqrt{\kappa}$; and
2. the exact-spectrum joint operator threshold at unit splitting scale, normalized by
   $E_{\mathrm{ref}}$.

Faint lines connect sampled amplitudes at fixed family case and parent scale. The diamond
for each family is the componentwise maximum over all of its sampled points and cases.
Consequently, a candidate pair of family-specific acceptance limits would have to lie at
or above that diamond to accept the complete sampled family. The two coordinates of a
diamond need not originate from the same sampled point.

![Cross-family development tolerance-requirement map.](analysis/development/tolerance-requirement-map.png)

## Companion shell--scale decision landscapes

The companion calculation uses each case's maximum declared parent scale and gauge
amplitude. For every complete metric shell under the declared cap, it samples 17
uniformly spaced coordinates on

$$
\lambda(u)=(1-u)\lambda_*+u,\qquad 0\le u\le1,
$$

where $\lambda_*$ is the nonnegative restricted-alignment scale. It minimizes the
three-component vector

$$
(N_{\mathrm{blocks}},\ \varepsilon_H,\ \varepsilon_E),
$$

with Hamiltonian error normalized by $\sqrt2E_{\mathrm{ref}}$ and sorted-band error by
$E_{\mathrm{ref}}$. A calculated vertex is nondominated only when no other calculated
vertex weakly improves all three components and strictly improves at least one. Unlike
the componentwise family diamond above, every such vertex is one attainable sampled
decision. The triangular surface visualization joins adjacent cells in the discrete
shell--scale grid; it supplies no interpolation, convexity, or continuum-frontier claim.

## Interpretation boundary

This is a requirement map, not an acceptance plot. No shaded pass region or decision
boundary is drawn because no family-specific scientific acceptance limits are justified
and frozen. Choosing limits from the displayed outcomes merely to obtain a pass would be
post hoc. Software verification establishes reconstruction and plotting behavior only;
it does not establish scientific adequacy, numerical convergence, material validity, or
retained-evidence status.

The displayed output is replaceable bounded synthetic development output. It must be
regenerated after any input-family protocol change and must not be cited as a qualified
scientific result.
