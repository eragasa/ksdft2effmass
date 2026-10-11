# `ksdft2effmass.periodic1d.multiband_alignment.verify`

## Purpose and status

Implemented independent reconstruction of M2 typed results.

## Public contract

- [`Periodic1DMultibandAlignmentVerificationResult`](Periodic1DMultibandAlignmentVerificationResult/index.md)
- [`Periodic1DMultibandAlignmentResultVerifier`](Periodic1DMultibandAlignmentResultVerifier/index.md)

The verifier rebuilds parent interpolation, eigensystems, transported frames, attacks,
pointwise/global alignment, projected matrices, Fourier blocks, Hermiticity, and all
range diagnostics without invoking the producer.

## Ownership and dependencies

The module verifies typed results; it does not decode untrusted JSON or decide
scientific acceptance.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/multiband_alignment/verify.py`.
Direct tests cover independent reconstruction, diagnostic and Hermiticity mutations,
producer-import separation, and retained contract tampering.

## Limitations

Producer and verifier share numerical libraries and conventions. The verifier supports
internal numerical consistency, not material validation.
