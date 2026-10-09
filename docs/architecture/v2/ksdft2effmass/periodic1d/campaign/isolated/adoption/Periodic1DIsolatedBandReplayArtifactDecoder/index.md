# `Periodic1DIsolatedBandReplayArtifactDecoder`

## Purpose and status

This implemented row-023 decoder Action consumes one closed replay-sidecar JSON payload
plus explicit frozen source bytes and exact typed campaign objects. It returns an
authenticated `Periodic1DIsolatedBandReplayArtifacts` or fails without partial adoption.

## Boundary and failures

The decoder applies the common strict campaign JSON boundary, exact schema/version and
inventory checks, canonical numeric construction, source SHA-256 correlation, exact
historical-result byte equality, frame/sewing reconstruction, and canonical array
content authentication. It performs no filesystem discovery, parent eigensolve,
scientific acceptance, or repair of changed inputs.

Changing an input byte, digest, dimension, representative inventory, or content array
fails explicitly. Source paths are supplied by the caller and are not scientific
identities.

## Evidence and limitations

The tampered-source test demonstrates fail-closed correlation. `verify_replay.py`
independently checks reconstructable numerical channels without rerunning the parent
calculation. Successful decoding establishes observed-content identity and exact source
correlation, not independently authenticated production provenance, validation, or UQ.
