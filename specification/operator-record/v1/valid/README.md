# Valid fixtures

- `minimal.json`: one-dimensional finite operator record with a zero real matrix.
- `complex-hermitian.json`: two-dimensional complex Hermitian matrix. A
  conforming deserializer must accept it, and Hermiticity analysis with zero
  tolerance must accept it.
- `complex-nonhermitian.json`: structurally valid two-dimensional complex matrix
  that is intentionally not Hermitian. A conforming deserializer must accept it;
  Hermiticity analysis must report the nonzero residual through public analyzer
  behavior.
