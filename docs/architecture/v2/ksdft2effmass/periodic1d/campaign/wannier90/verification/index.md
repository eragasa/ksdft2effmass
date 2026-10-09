# `periodic1d.campaign.wannier90.verification`

## Responsibility

Owns the numerically independent Wilson-loop reconstruction. It uses local polar-factor, loop-product, gauge-transform, eigenphase, and circular-assignment implementations rather than production Wilson Actions.

## Implemented classes

- [`Periodic1DWannier90WilsonVerificationRequest`](Periodic1DWannier90WilsonVerificationRequest/index.md)
- [`Periodic1DWannier90WilsonGroupVerificationResult`](Periodic1DWannier90WilsonGroupVerificationResult/index.md)
- [`Periodic1DWannier90WilsonVerificationResult`](Periodic1DWannier90WilsonVerificationResult/index.md)
- [`Periodic1DWannier90WilsonVerifier`](Periodic1DWannier90WilsonVerifier/index.md)

## Boundaries and evidence

The defining source is `python/src/ksdft2effmass/periodic1d/campaign/wannier90/verification.py`. Canonical tests are under `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/`; the [family dossier](../index.md) lists exact pytest owners, supported imports, Sphinx mapping, retained identities, and claim limitations. Passing evidence establishes software behavior only, not execution provenance, physical adequacy, scientific validation, UQ, or acceptance.
