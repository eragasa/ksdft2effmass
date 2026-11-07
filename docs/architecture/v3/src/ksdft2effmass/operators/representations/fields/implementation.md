# Implementation

`MatrixFieldABC` owns the common read-only interface and explicitly typed exact-comparison
method. `SquareMatrixFieldABC` derives the common dimension. The remaining ABCs are
semantic shape/role refinements without additional state.

The five final leaves are frozen/slotted dataclasses with custom constructors. Momentum
leaves accept only `FiniteMomentumMeshDomain`; the Fourier-block leaf accepts only
`FiniteTranslationDomain`. Three private functions centralize exact carrier checks and
array ownership/shape validation. Public names are listed explicitly in `__all__`.
