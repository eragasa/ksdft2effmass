# C6-B20-W21 spatial-truncation disposition

This directory records the separately authorized no-calculator S105 disposition after
the complete S90/S100 shell study.

## Recommendation and decision

Retain the **full-support shell** as the controlled operator:

- shell: `H-shell-17`;
- radius: `16.857151341 Å`;
- included representatives: 383;
- excluded representatives: 0; and
- disposition: `H_T = H_W`; no spatial truncation is accepted.

S90 froze the shell family and diagnostic rules but did not freeze a numeric nontrivial
operator-error acceptance threshold. S100 then exposed nonmonotone trade-offs. For
example, `H-shell-15` has more favorable gap and primary-mass changes than
`H-shell-16`, while `H-shell-16` has the smaller direct operator error. Creating a
threshold after observing those values would turn one favorable point into a post-hoc
acceptance rule.

The pre-existing 1 meV and 0.5% numerical-convergence tolerances are not repurposed as
spatial-reduction criteria. They govern the parent numerical/discretization channel;
spatial truncation is a separate model-reduction channel.

Full support is the only evaluated shell with exact zero tail, direct operator,
ordered-spectrum, gap, valley-location, and primary-mass differences from the S30
source. The other 17 shells remain descriptive development evidence; this disposition
does not claim that they are physically invalid.

## Downstream consequence

For the selected controlled chain,

\[
H_T = H_W,
\qquad
H_W-H_T=0.
\]

The separately authorized
[S110 attempt](../c6-b20-w21-slater-koster-definition-fit/) subsequently stopped at its
mandatory common-space alignment gate: the projected ten-orbital `sp3s*` frame is rank
deficient at two C6 points. No model was fit. Unless a new separately frozen `H_T` is
authorized, any finite-range restriction introduced by a future `H_SK` would belong to
the parameterization error `H_T-H_SK`, not to the spatial-truncation channel.

No Slater--Koster basis, parameter map, shell map, fitting objective, optimizer, or
validation partition is selected here. No 408-point or 402-point parent values were
consumed.

## Artifacts

| Artifact | SHA-256 |
|---|---|
| disposition implementation | `6613d234b7e084baede6d9cfef9d34be7e14360b23ccc296e6adacfe24f422e0` |
| disposition result | `519adfcf1101f7caa7916e04f3bf37879f4ad82b0f30e4ef38adc39770224f68` |

No calculator was invoked.
