# Representations and synthetic setup

Operator analysis begins with a mathematical operator and its finite matrix
representation. This page defines that distinction and constructs the synthetic
records used by the subsequent functionality pages.

## Mathematical object and stored matrix

Let $\hat H$ be a mathematical operator acting on an identified
$N$-dimensional state space. In the ordered orthonormal basis
$\mathcal B=(|b_0\rangle,\ldots,|b_{N-1}\rangle)$, its stored matrix is

$$
H_{ij}=\langle b_i|\hat H|b_j\rangle,
\qquad
\mathbf H\in\mathbb C^{N\times N}.
$$

The symbols are:

- $\hat H$: the mathematical operator;
- $\mathbf H$: its finite matrix representation in $\mathcal B$;
- $H_{ij}$: the matrix entry in row $i$ and column $j$;
- $|b_i\rangle$ and $|b_j\rangle$: ordered basis states;
- $\langle b_i|$: the conjugate-transpose dual of $|b_i\rangle$;
- $i,j\in\{0,\ldots,N-1\}$: zero-based matrix indices;
- $N$: the represented state-space dimension; and
- $\mathbb C^{N\times N}$: the set of complex $N$-by-$N$ matrices.

In software, `state_space.dimension`, `len(basis.ordering)`, and both dimensions
of `record.matrix` must all equal $N$. The label `basis.ordering[i]` identifies
the basis state associated with row and column $i$.

## Basis dependence

A unitary basis transformation changes the matrix coordinates according to

$$
\mathbf H'=\mathbf U^{\dagger}\mathbf H\mathbf U,
\qquad
\mathbf U^{\dagger}\mathbf U=\mathbf I_N.
$$

The additional symbols are:

- $\mathbf U\in\mathbb C^{N\times N}$: a unitary basis-transformation matrix;
- $\mathbf U^{\dagger}$: the conjugate transpose of $\mathbf U$;
- $\mathbf H'$: the representation of the same mathematical operator in the
  transformed basis; and
- $\mathbf I_N$: the $N$-dimensional identity matrix.

Entrywise subtraction is coordinate dependent. Equal dimensions, equal spectra, or
matching basis names do not construct $\mathbf U$ and do not prove basis or gauge
alignment.

## Construct synthetic records

The following is an **illustrative example using synthetic test data**. Keep the
`reference` and `candidate` variables available while following the remaining pages.
The example does not represent a calculated physical result.

```python
import numpy as np

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    OperatorRecord,
    StateSpace,
)

state_space = StateSpace("synthetic-space", "finite synthetic", 2)
basis = Basis(
    "synthetic-basis",
    "orthonormal synthetic",
    ("b0", "b1"),
    True,
)
geometry = Geometry(
    "synthetic-system",
    ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    "finite synthetic",
    "Cartesian row lattice vectors",
    "dimensionless",
)
energy_reference = EnergyReference("explicit synthetic zero", "eV")

reference = OperatorRecord(
    identifier="reference",
    operator_kind="finite_test_hamiltonian",
    matrix=np.array([[1.0, 0.2j], [-0.2j, 2.0]], dtype=np.complex128),
    state_space=state_space,
    basis=basis,
    geometry=geometry,
    energy_reference=energy_reference,
    provenance={"source": "illustrative synthetic example"},
)

candidate = OperatorRecord(
    identifier="candidate",
    operator_kind="finite_test_hamiltonian",
    matrix=np.array([[1.125, 0.2j], [-0.2j, 1.75]], dtype=np.complex128),
    state_space=state_space,
    basis=basis,
    geometry=geometry,
    energy_reference=energy_reference,
    provenance={"source": "illustrative synthetic example"},
)
```

The matrices use electronvolts because `energy_reference.unit` is `"eV"`.
The row lattice vectors use the exact `"dimensionless"` length-unit label because
this is synthetic test data. Neither label triggers unit conversion.

Next, evaluate the records with [Hermiticity analysis](hermiticity.md).
Return to the [operator-analysis overview](index.md).
