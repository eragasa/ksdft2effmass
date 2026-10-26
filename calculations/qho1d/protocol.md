# QHO1D direct spatial-truncation protocol

## Question

For the nondimensional oscillator with `hbar = mass = omega = 1`, compare the
real-line analytical number-state model, a finite homogeneous-Dirichlet centered-
difference model, and the exact retained ladder-basis Hamiltonian after placing the two
finite matrices in common retained coordinates.

## Authored sweep

The calculation evaluates the ordered Cartesian product:

- box half-widths: `4.0`, `6.0`, `8.0`;
- requested grid spacings: `0.2`, `0.1`, `0.05`; and
- retained dimensions: `2`, `4`, `6`.

The state-resolved rendering uses `(b, h, K) = (8.0, 0.05, 6)` and displays the first
four states. These controls are authored in `run_01_calculation.py` and serialized into
each execution through `Qho1dConfiguration`.

## Calculation

For each case, production analysis:

1. samples analytical Hermite states on ordered interior coordinates;
2. scales samples by the square root of the realized spacing;
3. applies symmetric Gram inverse-square-root orthonormalization;
4. constructs the injection `J` from retained coordinates to the finite grid;
5. forms `J.T @ H_h @ J - D_K`;
6. groups finite geometry, sampled-state alignment, common-coordinate Hamiltonian
   comparison, and full-space residual values into separate typed sections; and
7. retains the selected finite eigensolution and analytical samples once.

All arrays and quantities use the shared typed JSON codec. QHO1D owns no JSON array
transport and does not call `.tolist()`.

## Adjacent-grid analysis

`Qho1dCrossGridAnalyzer` may derive a separate typed analysis from a direct result. At
fixed box half-width and retained dimension, it subtracts adjacent coarse/fine
pulled-back Hamiltonians and evaluates the canonical PhysKit Frobenius norm. The
pulled-back matrices act in the same retained number-state coordinates even though
the parent finite-grid matrices act in different spatial spaces.

`Qho1dCrossGridVerifier` checks the derived controls, represented dimensions, and norm
directly from the authoritative case matrices. The existing retained execution is not
rewritten to embed this later analysis. The diagnostic measures adjacent finite-
representation change; it is not a continuum error estimate or convergence rate.

## Independent verification

Verification does not invoke `Qho1dAnalyzer` or `Qho1dComparator`. It reconstructs:

- Hermite functions through `scipy.special.eval_hermite`;
- the centered-difference kinetic and harmonic-potential matrix directly in NumPy;
- the sampled Gram matrix and symmetric orthonormalization;
- the common-coordinate operators and all scalar diagnostics; and
- the selected finite eigensolution with explicit sign alignment.

The verifier derives and hashes the exact visualization projection before composing
operation-named spatial-representation, sampled-state-alignment,
Hamiltonian-comparison, residual, state-comparison, and visualization-projection
verification values. The semantic-section execution retains 468 comparisons across
those six components.

## Rendering

Rendering requires a passing verification bound to the exact result and projection
SHA-256 identities. It publishes exactly three validated PNG files:

- `qho1d-eigenstates.png`;
- `qho1d-eigenstate-distortion.png`; and
- `qho1d-diagnostics.png`.

## Claim boundary

The protocol separates finite represented operators from the continuum differential
operator. The current discrepancy combines finite-box closure, boundary-adjacent rows,
interior discretization, sampled-state Gram correction, projection, and binary64
arithmetic. No single channel is represented as a continuum error bar.
