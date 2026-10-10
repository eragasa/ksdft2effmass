# `ksdft2effmass.periodic1d.admissible_sets.verify`

## Purpose and status

Implemented independent reconstruction of M3 typed results and decisive certificate
premises.

## Public contract

- [`Periodic1DConstrainedAdmissibleSetVerificationResult`](Periodic1DConstrainedAdmissibleSetVerificationResult/index.md)
- [`Periodic1DConstrainedAdmissibleSetResultVerifier`](Periodic1DConstrainedAdmissibleSetResultVerifier/index.md)

The verifier reconstructs M2/M3 paths, all candidate losses, three evaluation roles,
quadratic centers/matrices/minima, common witnesses, unclipped-set premises, locality,
and the splitting-axis lower bound.

## Ownership and dependencies

This module verifies typed results. The standalone script owns strict untrusted-wire,
manifest, configuration, and source-correlation checks. Neither route performs
scientific acceptance.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/admissible_sets/verify.py`.
Direct adversarial evidence covers evaluation-role mutation, quadratic premise
mutation, source-manifest miscorrelation, nonpositive tolerances, and other wire
contract attacks.

## Limitations

The verifier shares numerical libraries and conventions with the producer and validates
only the frozen continuous parameter rectangle and finite global-angle family.
