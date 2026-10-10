# `Periodic1DMultibandAlignmentCalculator`

## Purpose

Stateless Action that executes the deterministic M2 frame, alignment, and locality
protocol.

## Public operation

`execute(definition)` requires the exact M2 definition and returns a correlated
`Periodic1DMultibandAlignmentCalculationResult`. It interpolates/diagonalizes the
parent, transports rank-two frames, applies the attack, computes pointwise and global
alignments, projects represented operators, Fourier transforms three gauge channels,
and evaluates each range on training/evaluation meshes. Class-specific detail is split
into [implementation](implementation/index.md),
[mathematics](implementation/mathematics/index.md), and
[testing](implementation/testing/index.md).

## Mathematical ownership

Private methods own finite protocol policy: external-gap minimum, raw eigenspaces,
attack rotations, path rotation, aggregate global rotation, recovery/frame/operator
defects, and range assembly. Reusable transport, projection, Fourier, truncation, and
Hermiticity algorithms remain delegated.

## State-space contract

Projector comparisons are invariant. Matrix/operator comparisons occur only after the
frames identify the same rank-two represented space. Pointwise and global unitary
families remain separate.

## Evidence and limitations

Tests cover channel separation, determinism, independent reconstruction, and tamper
response. The one-global-unitary channel is not a general momentum-dependent alignment
optimizer, and no material claim follows.
