# M2 calculator testing

`TestPeriodic1DMultibandAlignmentCalculator` verifies that projector/spectrum,
pointwise frame, global frame, represented operator, and locality channels remain
separate. It checks fresh-execution determinism and independent reconstruction, then
mutates alignment diagnostics, Hermiticity, frozen controls, numeric Boolean inputs, and
result-threshold correlation.

The retained standalone import test verifies independence from producer modules. Shared
NumPy/SciPy and scientific conventions remain a known limitation.
