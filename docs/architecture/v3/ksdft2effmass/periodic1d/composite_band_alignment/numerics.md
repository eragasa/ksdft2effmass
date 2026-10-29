# Composite-band alignment numerical contract

The parent uses exact integer numerators divided by 100. Construction uses 64 centered
half-open reciprocal points; evaluation uses 257 exact-rational staggered points shifted
by `1/65` of one evaluation step. The inventories are exactly disjoint.

PhysKit owns dense complex-Hermitian eigensystems and canonical column phases.
Optimization owns batched complex-unitary Procrustes selection. Rank cutoffs are
`max(1e-14, 1e-12 sigma_max)` and rank deficiency fails closed. KSD owns polar frame
transport, represented-operator composition, centered finite Fourier transforms, block
cyclic-to-ordinary conversion, separated interpolation/truncation/total Hamiltonian and spectral errors, and independent recomputation. The verifier tolerances are
software comparison controls, not physical error bars.