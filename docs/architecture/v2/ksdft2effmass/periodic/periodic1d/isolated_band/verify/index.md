# `ksdft2effmass.periodic1d.isolated_band.verify`

## Purpose and status

Implemented independent numerical reconstruction for M1 typed results.

## Public contract

- [`Periodic1DIsolatedBandVerificationResult`](Periodic1DIsolatedBandVerificationResult/index.md)
- [`Periodic1DIsolatedBandResultVerifier`](Periodic1DIsolatedBandResultVerifier/index.md)

The verifier reconstructs parent spectra, selected-band samples, direct Fourier blocks,
interpolation, and every range diagnostic without invoking the producer Action.

## Ownership and dependencies

This module owns typed-result verification. It does not decode untrusted JSON, mutate
retained evidence, execute external calculators, or make a scientific acceptance
decision.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/isolated_band/verify.py`.
Direct evidence includes independent reconstruction, tampered convergence detection,
and the retained-verifier producer-import test.

## Limitations

The verifier shares NumPy/SciPy, floating-point, eigensolver, unit, and representation
conventions with the producer. It is independent of the producer Action, not an
independent physical oracle.
