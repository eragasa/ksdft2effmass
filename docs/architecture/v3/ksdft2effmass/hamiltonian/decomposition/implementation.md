# Implementation

## Source structure

```text
python/src/ksdft2effmass/hamiltonian/
├── __init__.py
└── decomposition.py
```

`__init__.py` imports and exports only `HamiltonianDecomposition`.
`operators/hamiltonians.py` owns `Hamiltonian`, its exact
`HermitianHamiltonian` refinement, and `ReducedHamiltonian`; `operators/subspaces.py`
owns the abstract `SpectralSubspace` boundary and concrete orthogonal implementation.
`decomposition.py` consumes the reduced subtype and owns the concrete facade, runner,
verifier, visualizer, verification record,
visualization record, and correlated result. The module does not depend on a
registry, service locator, abstract factory, or generic study container.

## Concrete composition

`HamiltonianDecomposition` validates the public numeric controls and constructs three
concrete collaborators. Its `execute()` method:

1. calls `o_runner.run()`;
2. passes the calculation result to `o_verifier.verify(...)`;
3. fails closed when verification does not pass;
4. passes calculation and verification to `o_visualizer.visualize(...)`; and
5. returns one correlated `HamiltonianDecompositionResult`.

The runner uses the established
`analysis.operators.DecompositionIdentifiabilityAnalyzer`. The verifier independently
reconstructs the reference and shifted decompositions and the four retained
model-class fits; it does not call that analyzer. The visualizer renders the declared
shift and unexplained fit norms to immutable PNG bytes and closes the Matplotlib figure.

## First caller and migration boundary

The implemented class is dimension-independent. PIAB1D is the first concrete caller,
not a specialization. Installed source contains no `Piab1dHamiltonianDecomposition`,
PIAB1D runner, PIAB1D verifier, or PIAB1D visualizer. PIAB1D supplies its represented
Hamiltonian and shift to the same class used by any other supported caller.

`Piab1dResidualStudyResult.reduced_hamiltonian` is one `ReducedHamiltonian` binding
the reduced matrix, PIAB1D's concrete orthogonal spectral subspace, and a typed
parent-coordinate Hamiltonian embedding. The concrete subspace owns the basis and
derives the projector.
`calculations/piab1d/hamiltonian_decomposition.py` is the first
thin migration entry point. It evaluates the typed PIAB1D study in memory, passes that
object and the declared shift to `HamiltonianDecomposition`, and invokes `run()`,
`verify()`, and `visualize()` in order. It does not parse the historical retained result
to recover the Hamiltonian. It defines no
Workflow, adapter class, PIAB1D decomposition subclass, runner, verifier, or visualizer.
It writes only a caller-selected verified PNG with no-overwrite behavior.

Historical `identifiability.py`, `run_identifiability.py`, retained results, provenance
paths, and checksum entries remain unchanged. The successor entry point does not assert
that the historical flat artifacts form one execution package.

## Tests

Focused tests establish:

- execution on a two-dimensional input, demonstrating absence of a PIAB1D dimension
  specialization;
- PIAB1D declared-shift model-class norm parity;
- fail-fast rejection of a nonsymmetric shift;
- rejection of Boolean numeric controls; and
- package export of only `HamiltonianDecomposition`.

Passing these tests establishes software and bounded numerical behavior only. It does
not validate a physical Hamiltonian decomposition or an inferred model class.
