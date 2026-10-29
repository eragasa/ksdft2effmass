# Numerical conventions

## Candidate and loss coordinates

The candidate parameter order is energy-shift ratio followed by positive traceless
splitting scale. The loss energy scale is a positive scalar in the unitless parent-energy
unit. For each construction momentum, the candidate retains the reference trace,
applies the declared energy shift, and scales the traceless reference component.

Spectral loss is the root mean square ordered-eigenvalue discrepancy. Operator loss is
the root mean square Frobenius discrepancy after one selected global real rotation. Both
are divided by the declared energy scale and use the construction mesh to define the
admissible sublevel sets. The disjoint evaluation mesh is diagnostic-only and cannot
select an angle, witness, or disposition.

## Quadratics and separation

Squared losses are retained as centered positive-definite two-dimensional quadratics.
A compatible result requires the declared witness to satisfy both thresholds for one
angle component. A separated result uses splitting-axis ellipsoid extrema and records
both a conservative lower bound and an attained upper bound in Euclidean parameter
coordinates. It is certified separated only when the lower bound exceeds the declared
separation resolution; otherwise the outcome is unresolved.

Error maxima are not added. Pointwise residual identities may telescope, but maxima from
interpolation, truncation, cyclic conversion, or total consequence remain separately
named diagnostics.

## Locality channels

The construction mesh is centered and even. Cyclic-to-ordinary conversion removes only
the negative-Nyquist representative and records its normalized removed-block power.
Deliberate finite-range truncation then acts on the ordinary model and records the
ordinary omitted-block L2 norm. These channels have different meanings and are never
pooled.

All retained values are finite binary64 values. The independent reconstruction shares
NumPy binary64 arithmetic and is not an exact or physical oracle. SHA-256 establishes
byte identity only.
