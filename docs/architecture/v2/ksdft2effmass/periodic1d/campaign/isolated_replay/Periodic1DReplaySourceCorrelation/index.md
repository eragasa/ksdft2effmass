# `Periodic1DReplaySourceCorrelation`

## Purpose and status

This implemented row-023 evidence DataObject binds canonical SHA-256 identities for the
frozen input, retained historical result, historical producer, replay producer, and
replayed result.

## Contract

All five identities are lowercase 64-character SHA-256 strings. The explicit
`exact_result_bytes_match` flag must be a built-in Boolean and true; replayed and
historical result digests must be identical. Digests identify observed immutable bytes,
not paths, scientific objects, or independently authenticated production lineage.

## Evidence map and claim boundary

The decoder constructs this record from caller-supplied bytes. Claim-bearing test
`TestPeriodic1DIsolatedBandScientificAdoption::test_method__execute__authenticates_replay_and_constructs_hierarchy`
checks the retained identities; the tampered-source test checks failure before adoption.
The retained README and protocol describe the authorized replay.

Successful construction establishes exact result-byte correlation only. It does not
validate the calculation, parent model, numerical convergence, scientific conclusion,
or uncertainty estimate.
