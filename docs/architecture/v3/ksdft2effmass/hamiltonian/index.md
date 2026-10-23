# `ksdft2effmass.hamiltonian`

## Purpose and status

This implemented package owns researcher-facing operations on an already represented
Hamiltonian. Its first bounded operation is decomposition.

Source package: `python/src/ksdft2effmass/hamiltonian/`.

## Public surface

`python/src/ksdft2effmass/hamiltonian/__init__.py` exports exactly one symbol:

```python
from .decomposition import HamiltonianDecomposition

__all__ = ["HamiltonianDecomposition"]
```

The runner, verifier, visualizer, and result records are implementation collaborators
in `decomposition.py`. They are not re-exported by the package.

## Source mapping

`decomposition.py` contains the concrete decomposition facade and its internal stage
collaborators. Its mirrored design is documented beneath `decomposition/`.

## Ownership boundary

The package does not define a new generic operator record, state space, physical model,
Hamiltonian constructor, eigensolver, calculation campaign, execution package, or
publication status. Those remain with their existing owners.

Model-specific code supplies a typed `ReducedHamiltonian` and a declared decomposition
shift. `HamiltonianDecomposition` coordinates reusable calculation, verification, and
visualization; it does not infer physical meaning from a matrix alone.

## Evidence

Focused tests establish the implemented software composition and the retained PIAB1D
model-class norm values. They do not establish scientific validation, uncertainty
quantification, human acceptance, publication, or release status.
