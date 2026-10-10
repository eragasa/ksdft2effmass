# `Periodic1DAdmissibleSetLocalityResult`

## Purpose and contract

Immutable locality summary for one declared M3 hopping range. It binds exact nonnegative
`maximum_range` and finite nonnegative omitted-block $\ell^2$ norms for reference,
attacked, and selected candidate channels.

The values use the M2 parent energy unit implicitly through the correlated result;
they are not combined with dimensionless spectral/operator losses. Aggregate
construction enforces exact range sequence and numerical correlation with the M2/M3
transforms.

## Interpretation

This record provides finite-range context for one evaluated candidate. It is not a
localization theorem or range-selection policy.
