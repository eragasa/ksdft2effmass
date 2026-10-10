# M1 calculator testing

The direct owner is
`TestPeriodic1DIsolatedBandCalculator`. The primary execution oracle checks exact role
separation. Fresh-execution serialization checks binary64 determinism. Independent
reconstruction checks every parent, Fourier, and range channel. A mutated convergence
observation must fail verification. Unit and Boolean attacks exercise the public control
boundary.

These tests establish software and finite numerical behavior; they do not establish
physical isolation, continuum convergence, or material validation.
