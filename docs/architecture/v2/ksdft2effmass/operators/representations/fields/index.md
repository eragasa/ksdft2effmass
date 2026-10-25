# `ksdft2effmass.operators.representations.fields` module

## Purpose and status

This implemented Phase 1 module defines the narrow matrix-field ABC hierarchy and its
NumPy-backed leaves. The abstract interfaces specify domain correlation and matrix shape.
Concrete names declare intended semantic roles without promoting arrays to mathematical
proofs.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerics](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Abstract contract inventory

```text
MatrixFieldABC
├── SquareMatrixFieldABC
│   ├── OperatorFieldABC
│   ├── ProjectorFieldABC
│   └── GaugeFieldABC
├── RectangularMatrixFieldABC
│   └── FrameFieldABC
└── FourierBlockFieldABC
```

Class pages:

- [`MatrixFieldABC`](MatrixFieldABC/index.md)
- [`SquareMatrixFieldABC`](SquareMatrixFieldABC/index.md)
- [`OperatorFieldABC`](OperatorFieldABC/index.md)
- [`ProjectorFieldABC`](ProjectorFieldABC/index.md)
- [`GaugeFieldABC`](GaugeFieldABC/index.md)
- [`RectangularMatrixFieldABC`](RectangularMatrixFieldABC/index.md)
- [`FrameFieldABC`](FrameFieldABC/index.md)
- [`FourierBlockFieldABC`](FourierBlockFieldABC/index.md)

`MatrixFieldABC` exposes `domain`, immutable `values`, and positive source and target
dimensions. `SquareMatrixFieldABC` additionally exposes the common `dimension`.

## Concrete leaf inventory

| Leaf | Domain | Array shape | Intended role only |
|---|---|---|---|
| [`NumpyOperatorField`](NumpyOperatorField/index.md) | `FiniteMomentumMeshDomain` | `(points, n, n)` | operator |
| [`NumpyProjectorField`](NumpyProjectorField/index.md) | `FiniteMomentumMeshDomain` | `(points, n, n)` | projector |
| [`NumpyGaugeField`](NumpyGaugeField/index.md) | `FiniteMomentumMeshDomain` | `(points, n, n)` | internal gauge |
| [`NumpyFrameField`](NumpyFrameField/index.md) | `FiniteMomentumMeshDomain` | `(points, target, source)` | frame |
| [`NumpyFourierBlockField`](NumpyFourierBlockField/index.md) | `FiniteTranslationDomain` | `(translations, n, n)` | Fourier blocks |

Provisional imports come from the defining module:

```python
from ksdft2effmass.operators.representations.fields import (
    NumpyFrameField,
    NumpyOperatorField,
)
```

## Storage and ordering

Every leaf requires an exact finite NumPy array with exact native `complex128` dtype.
The first axis is correlated positionally with the declared domain order. Momentum fields
therefore use the mesh owner's flattened point count; Fourier blocks use the exact
translation inventory order.

Matrix rows are target coordinates and columns are source coordinates. For a frame,
columns represent source coordinates in the retained space and rows represent target
coordinates in the ambient space.

Concrete leaves copy caller arrays into immutable bytes-backed, C-contiguous storage.
Caller mutation cannot alter stored values, and NumPy cannot re-enable the stored array's
write flag. No separate caller-supplied dimensions are accepted; dimensions are derived
from validated shape.

## Invariants and failure behavior

All leaves require:

- the exact domain leaf appropriate to their role;
- exactly three array axes;
- first-axis length equal to domain cardinality;
- positive source and target dimensions;
- square trailing axes for square-field leaves;
- exact `complex128` dtype; and
- finite real and imaginary components.

Wrong domain, container, or dtype raises `TypeError`. Shape, correlation, or finiteness
failure raises `ValueError`.

## Mathematical-property boundary

The following implications are deliberately invalid:

- `NumpyOperatorField` does not imply Hermiticity;
- `NumpyProjectorField` does not imply self-adjointness or idempotency;
- `NumpyGaugeField` does not imply realness, orthogonality, unitarity, or determinant
  class;
- `NumpyFrameField` does not imply isometry, rank, sewing, or periodicity; and
- `NumpyFourierBlockField` does not imply Hermitian pairing, inversion closure, support
  completeness, or reconstruction correctness.

Those are later evidence contracts evaluated over an explicitly identified field and
domain.

## Dependencies and collaborators

The module uses:

- domain contracts from [`../domains/index.md`](../domains/index.md);
- NumPy array operations;
- `projectkoios.numerics.numpy.typing.Complex128Array`; and
- the Numerics immutable-array owner.

It imports no analysis, campaign, schema, serializer, Workflow, or formal code.

## Code mapping

- Source: `python/src/ksdft2effmass/operators/representations/fields.py`
- Package page: [`../index.md`](../index.md)

## Test mapping

- class-matched `test__Numpy...Field.py` modules under
  `python/tests/software_verification/ksdft2effmass/operators/representations/`;
- `test__RepresentationIdentity__dependency_boundary.py`.

Tests cover semantic-role interfaces, accepted non-Hermitian/nonprojector/nonunitary data,
rectangular orientation, domain correlation, shape, dtype, finiteness, exact value
equality, caller-copy isolation, and immutable bytes backing. They do not test the Python
language's generic frozen-dataclass mechanism.

## Sphinx mapping

No Sphinx API page or supported root export is selected in Phase 1.

## Evidence and limitations

Passing tests establishes storage, shape, domain, and intended-role software behavior
only. It does not establish any mathematical property named above, numerical convergence,
physical interpretation, formal proof, or scientific validation.
