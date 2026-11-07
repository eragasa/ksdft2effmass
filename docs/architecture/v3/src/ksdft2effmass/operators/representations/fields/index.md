# `ksdft2effmass.operators.representations.fields`

## Source

`python/src/ksdft2effmass/operators/representations/fields.py`

## Responsibility

The module owns the semantic matrix-field interface hierarchy and five immutable
NumPy-backed leaves. The hierarchy separates square and rectangular shape contracts from
operator, projector, gauge, frame, and Fourier-block intent.

## Abstract interfaces

- [`MatrixFieldABC`](MatrixFieldABC/index.md)
- [`SquareMatrixFieldABC`](SquareMatrixFieldABC/index.md)
- [`OperatorFieldABC`](OperatorFieldABC/index.md)
- [`ProjectorFieldABC`](ProjectorFieldABC/index.md)
- [`GaugeFieldABC`](GaugeFieldABC/index.md)
- [`RectangularMatrixFieldABC`](RectangularMatrixFieldABC/index.md)
- [`FrameFieldABC`](FrameFieldABC/index.md)
- [`FourierBlockFieldABC`](FourierBlockFieldABC/index.md)

## Private validators

- [`_require_momentum_domain`](_require_momentum_domain/index.md)
- [`_require_translation_domain`](_require_translation_domain/index.md)
- [`_immutable_field_values`](_immutable_field_values/index.md)

## Concrete leaves

- [`NumpyOperatorField`](NumpyOperatorField/index.md)
- [`NumpyProjectorField`](NumpyProjectorField/index.md)
- [`NumpyGaugeField`](NumpyGaugeField/index.md)
- [`NumpyFrameField`](NumpyFrameField/index.md)
- [`NumpyFourierBlockField`](NumpyFourierBlockField/index.md)

## Pages

- [Scientific interpretation](scientific.md)
- [Numerical behavior](numerics.md)
- [Implementation](implementation.md)
- [Schematic](schematics.md)
