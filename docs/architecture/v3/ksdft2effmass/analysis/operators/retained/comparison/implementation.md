# Implementation

The target signature is:

```python
result = RealSymmetricRetainedOperatorComparator(request).compare()
```

The frozen comparator retains one immutable request. `compare()` takes no arguments,
forms `candidate - reference`, splits the difference into diagonal and off-diagonal
matrices, and returns one result correlated to the same request.

The module may depend on NumPy and operator quantity records. It does not depend on
subspace construction, eigensolvers, model systems, matrix-norm policy, serializers,
or outward composition.

Tests must establish the sign convention, exact diagonal/off-diagonal reconstruction,
shape/unit/symmetry rejection, immutable request correlation, and zero comparison.
