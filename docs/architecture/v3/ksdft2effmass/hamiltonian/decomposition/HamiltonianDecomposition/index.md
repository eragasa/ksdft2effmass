# `HamiltonianDecomposition`

## Status

Implemented concrete public class in
`python/src/ksdft2effmass/hamiltonian/decomposition.py`.

## Responsibility

`HamiltonianDecomposition` composes three concrete collaborators and exposes one
researcher-facing operation. It is not an abstract base class and defines no extension
registry.

```python
result = HamiltonianDecomposition(
    reduced_hamiltonian,
    shift,
    absolute_tolerance=2.0e-14,
    visualization_dpi=180,
).execute()
```

Execution is equivalent to:

```python
calculation = self.o_runner.run()
verification = self.o_verifier.verify(calculation)
if not verification.passed:
    raise ValueError(...)
visualization = self.o_visualizer.visualize(calculation, verification)
return HamiltonianDecompositionResult(
    calculation=calculation,
    verification=verification,
    visualization=visualization,
)
```

## Invariants

- Calculation completes before verification.
- Verification reconstructs decisive identities without calling the runner.
- Failed verification cannot produce a visualization or successful correlated result.
- Visualization consumes the calculated and verified records.
- `ReducedHamiltonian` binds the reduced matrix, an abstract spectral subspace, and a
  parent-coordinate Hamiltonian embedding before decomposition. The PIAB1D concrete
  subspace owns its orthonormal basis and derives its projector.
- Its retained matrix and the shift are finite, square, shape-compatible,
  unit-compatible, and real symmetric within the declared absolute tolerance.
- Matrix dimension comes from the inputs and is not specialized to PIAB1D.
- Boolean numeric controls and numeric strings are rejected.

## Public import

```python
from ksdft2effmass.hamiltonian import HamiltonianDecomposition
```

No collaborator is re-exported from `ksdft2effmass.hamiltonian`.

## Claim boundary

The result establishes calculation and independent numerical checks under the declared
finite inputs and tolerances. It does not identify a unique physical potential or
establish scientific acceptance, material validation, publication, or release status.
