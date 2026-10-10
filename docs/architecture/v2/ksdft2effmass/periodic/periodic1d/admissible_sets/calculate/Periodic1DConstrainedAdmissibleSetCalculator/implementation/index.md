# M3 calculator implementation

`execute()` composes M2 and never subclasses it. It builds finite training/evaluation
paths, derives exact angle-resolved squared-loss quadratics over the continuous
parameter rectangle,
and then evaluates compatible and separated cases under predeclared thresholds.

`_compatible_case` requires the prospective witness. `_separated_case` constructs
boundary points and an analytic lower bound; failed finite search alone is insufficient.
`_evaluate` binds one exact role to one parameter/angle and retains locality.
`_quadratic`, `_domain_minimum_squared_loss`, `_feasible_angles`, and `_axis_extreme`
own the decisive proof geometry.

No method reads sensitivity results or alters frozen controls after evaluation.
