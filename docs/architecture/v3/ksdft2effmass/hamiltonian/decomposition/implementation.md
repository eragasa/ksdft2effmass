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
`analysis.operators.KineticPotentialDecompositionAnalyzer`. The verifier independently
reconstructs the reference and shifted decompositions and the four retained
model-class fits; it does not call that analyzer. The visualizer renders the declared
shift and unexplained fit norms to immutable PNG bytes and closes the Matplotlib figure.

## PIAB1D composition boundary

The implemented Hamiltonian class is dimension-independent. Installed source contains
no `Piab1dHamiltonianDecomposition` subtype or PIAB1D-specific decomposition runner.
The PIAB1D successor obtains its retained matrix from `Piab1dAnalyzer` and passes that
matrix and the declared shift directly to
`KineticPotentialDecompositionAnalyzer` during `run_01_calculation.py`.

The typed `KineticPotentialDecompositionResult` is stored once inside
`Piab1dCalculationResult`. Independent reconstruction belongs to
`Piab1dKineticPotentialDecompositionReferenceAnalyzer`; authenticated rendering belongs
to the decomposition figure action in `model_systems.piab1d.visualizations`. The calculation
script therefore contains no reusable decomposition kernel, verifier, visualizer,
Workflow, adapter class, or command-line parser.

The superseded calculation-local decomposition producer and its dedicated CLI test have
been removed from the maintained tip. Retained results, provenance paths, and checksum
entries remain historical records. Their references to removed producer paths identify
exact repository history and are not rewritten as successor provenance.

## Tests

Focused tests establish:

- execution on a two-dimensional input, demonstrating absence of a PIAB1D dimension
  specialization;
- PIAB1D declared-shift model-class norm parity;
- fail-fast rejection of a nonsymmetric shift;
- rejection of Boolean numeric controls; and
- deliberate export of `HamiltonianDecomposition` from the Hamiltonian domain.

Passing these tests establishes software and bounded numerical behavior only. It does
not validate a physical Hamiltonian decomposition or an inferred model class.
