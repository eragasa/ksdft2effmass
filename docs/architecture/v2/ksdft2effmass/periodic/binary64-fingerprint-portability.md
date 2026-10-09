# Binary64 fingerprints and portable numerical verification

## Status and scope

This decision governs maintained package verification of retained periodic campaign
results. It does not rewrite historical version-one artifacts, checksum manifests, or
calculation protocols, and it does not authorize regenerating a retained result.

## Problem

Several retained records contain SHA-256 fingerprints of arrays produced with binary64
transcendental functions or eigensolvers. The retained provenance identifies Python and
NumPy, but not the operating system, architecture, libm, or BLAS/LAPACK implementation.
A Linux CI reconstruction can therefore satisfy every reviewed numerical tolerance yet
produce different low-order bits and a different array digest from the macOS generation
runtime.

Treating those digests as portable numerical oracles incorrectly conflates two claims:

- exact identity of bytes produced by one generation runtime; and
- numerical agreement of independently reconstructed represented quantities.

## Decision

The maintained package keeps byte identity and numerical verification as separate
channels.

- File, source, runner, implementation, and whole-artifact SHA-256 values continue to
  require exact equality where the identified bytes are available.
- A retained matrix fingerprint continues to identify the exact generation-time
  binary64 bytes and must remain a lowercase 64-character SHA-256 value.
- Independent matrix reconstruction is evaluated through the record's existing
  structural checks, compact witnesses, and reviewed numerical tolerances.
- A reconstructed matrix fingerprint is validated as a well-formed identity but is not
  required to equal the generation-time fingerprint across numerical runtimes.
- Historical calculation scripts and version-one artifacts remain unchanged. Their
  existing checksum manifests continue to authenticate their exact contents.
- Future bitwise-replay claims must additionally bind the operating system,
  architecture, Python, NumPy, BLAS/LAPACK, and relevant math runtime. Without that
  environment identity, only tolerance-based numerical replay may be claimed.

This does not authorize changing a retained value or tolerance to obtain a pass. A
numerical mismatch outside the frozen tolerance remains a verification failure.

## CI consequence

The bounded CI checkout supplies full Git history because oracle-disposition evidence
uses `git show` to authenticate named reviewed revisions. Shallow checkout failure is an
evidence-environment defect, not an oracle disposition.

Before a pull request is opened, its exact bounded CI command and history assumptions
must be reproduced or explicitly reported as unavailable. Passing narrower local suites
is not equivalent to passing the pull-request gate.

## Claim boundary

A passing portable reconstruction establishes bounded software and numerical
consistency for the declared synthetic finite representations. It does not establish
bitwise replay, execution provenance, parent-model convergence, physical adequacy,
scientific validation, uncertainty quantification, transferability, or acceptance.
