# Implementation

The target signature is:

```python
result = OrthogonalSubspaceComparator(request).compare()
```

The frozen comparator retains one request. `compare()` accepts no arguments,
materializes each projector through its owning subspace contract, subtracts
`candidate - reference`, and returns one correlated immutable result.

The request accepts the explicit union of `OrthogonalTrialSubspace` and
`OrthogonalSpectralSubspace`; no generic subspace protocol or abstract base is
introduced in this tranche.

Tests must cover each permitted nominal pairing, dimension rejection, sign-invariant
spectral columns, identical subspaces, and the fixed difference sign.
