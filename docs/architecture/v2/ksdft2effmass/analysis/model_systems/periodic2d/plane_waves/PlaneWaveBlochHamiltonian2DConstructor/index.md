# `PlaneWaveBlochHamiltonian2DConstructor`

## Purpose and status

This implemented row-033 Action constructs a finite two-dimensional spinless scalar
plane-wave Bloch matrix from an exact request.

## Algorithm and conventions

The Action first checks column-basis duality `A^T B = 2*pi*I`. It then assembles
$H_{n'n}(\kappa)=E_K|B(\kappa+n)|^2\delta_{n'n}+V_{n'-n}$ in declared
`p`-outer, `q`-inner order. Missing transfers are exact zero. Reduced coordinates are
mapped by the reciprocal primitive matrix before evaluating kinetic energy.

Inline comments preserve the direct/reciprocal convention, transfer sign/order, and
exact-zero boundary. The Action performs no eigensolve, band selection, gauge alignment,
truncation comparison, or scientific acceptance.

Software and numerical tests establish ordering, analytic entries, exact request
retention, immutability, and duality failures. They do not establish cutoff convergence,
physical adequacy, validation, or UQ.
