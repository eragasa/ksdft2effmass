# Implementation

The target signature is:

```python
result = RealSymmetricReferenceResidualAnalyzer(request).analyze()
```

The frozen analyzer retains one immutable request. `analyze()` accepts no arguments,
forms the action residual, and returns a result retaining the same request.

The module may depend on NumPy and operator-owned quantity and trial-subspace records.
It does not depend on eigensolvers, operator reduction, comparison, norm analysis,
model systems, or outward composition.

Tests must establish the residual sign and shape, exact zero examples, nonzero examples,
unit and dimension rejection, and the pullback identity when composed independently
with operator reduction and retained comparison.
