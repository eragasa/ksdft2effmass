# `Periodic1DMultibandAlignmentResultVerifier`

## Purpose

Stateless Action that independently reconstructs the typed M2 calculation.

## Operation

`execute(calculation)` rebuilds parent matrices, eigensystems, transported frames,
attack rotations, pointwise/global alignment, projected represented operators, Fourier
blocks, Hermiticity, truncations, and range spectral errors. It returns
`Periodic1DMultibandAlignmentVerificationResult` and never calls the M2 producer.

## Decisive private methods

The verifier owns direct finite implementations of parent interpolation, eigensystem
ordering, polar transport, attack construction, alignment, projection, Fourier
transformation, Hermiticity, interpolation, and projector/frame/spectral defects.

## Evidence and limitations

Tests cover successful reconstruction and mutations of alignment, Hermiticity, and wire
controls. The verifier shares NumPy/SciPy and conventions with the producer; it is not an
independent physical oracle or general gauge optimizer.
