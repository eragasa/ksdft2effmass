# Numerical contract

For operator `H`, trial injection `J`, and retained reference `D`, the analyzer
constructs

$$
R_{J,D}=HJ-JD.
$$

`H` has shape `N` by `N`, `J` has shape `N` by `K`, `D` has shape `K` by `K`, and the
residual has shape `N` by `K`. `H`, `D`, and the residual share one unit; `J` is
unitless.

When independently composed with trial reduction and retained comparison,

$$
J^{\mathsf T}R_{J,D}
=J^{\mathsf T}HJ-D.
$$

The analyzer does not form the right-hand comparison itself and does not select a norm.
An experiment may apply `RepresentedMatrixNormAnalyzer` to the residual and must state
any normalization.
