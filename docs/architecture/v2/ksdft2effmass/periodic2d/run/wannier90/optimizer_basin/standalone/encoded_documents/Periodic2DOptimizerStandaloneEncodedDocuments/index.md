# `Periodic2DOptimizerStandaloneEncodedDocuments`

## Classification

`Periodic2DOptimizerStandaloneEncodedDocuments` is a frozen, slotted encoded-document
DataObject for crosswalk row `PERIODIC-XWALK-055`. It replaces the misleading former
`Periodic2DOptimizerStandaloneCampaignModel` name without a compatibility alias.

It is **not** a physical model, mathematical operator, finite representation, retained
space or operator, represented operator, effective model, initial-gauge model, optimizer,
basin classifier, provenance record, convergence result, validation result, or
acceptance decision.

## Exact state

| Field | Contract |
|---|---|
| `proposal_payload` | Exact nonempty built-in `bytes` for `standalone-study-proposal.json` |
| `initial_gauges_payload` | Exact nonempty built-in `bytes` for `standalone-initial-gauges.json` |
| `result_payload` | Exact nonempty built-in `bytes` for `standalone-result.json` |

No field owns a repository path. Verification receives an absolute `repository_root`
through its request and confines compact-source reads to that root.

## Retained identities

The maintained files are under
`calculations/research-monograph/periodic-2d-optimizer-basin/`:

| File | SHA-256 |
|---|---|
| `standalone-study-proposal.json` | `d260475252b420d151ebfd7e276e170c1d069e4bbc7ad974d21e911dd6db3485` |
| `standalone-initial-gauges.json` | `34ebdb57dbcdb3cb72bb3fbc602a12b3c05b58534d1c028047578afceb1a8f4b` |
| `standalone-result.json` | `add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a` |
| `extract_standalone_results.py` | `c30612ccd886f140fe429f04233b6312601859d8a09328c71312e1fc204fe5c3` |

SHA-256 establishes content identity only. It does not establish historical execution,
author identity, native-file presence, provenance, semantic correctness, scientific
validity, uncertainty, or acceptance.

## Verified bounded behavior

A request-scoped verifier authenticates all three encapsulated wires and the directly
declared maintained extractor. It adapts consumed fields to closed immutable records and
independently reconstructs endpoint transitions, spread algebra, terminal diagnostic
classes, summary counts, group membership, best endpoints, ordered basin
representatives, threshold-qualified members, spread-eligible rejected comparisons,
derived start-block presence, density-threshold sensitivity, post-hoc controls, and the
exact negative claim boundary.
See the [frozen field contract](../../verification-contract.md),
[schematic](../../schematic.md), [numerical contract](../../numeric.md), and
[scientific claim boundary](../../scientific.md).

The historical result wire contains bare positive `Infinity` only at the complete
indexed paths of two extended-real fields for rejected basin-equivalence candidates. The
bounded adapter rejects extra nesting, missing indices, look-alike ancestors, duplicate
keys, `NaN`, `-Infinity`, and nonfinite values everywhere else. Proposal and gauge wires
use shared strict JSON decoding.

## Evidence

### Routine class-owned evidence

- `test__Periodic2DOptimizerStandaloneEncodedDocuments.py`
- `test__Periodic2DOptimizerStandaloneCampaignContracts.py`
- `test__Periodic2DOptimizerStandaloneActionOwnership.py`
- `test__Periodic2DOptimizerStandaloneDocumentDecoder.py`

These tests establish intrinsic byte ownership, immutability, request/result validation,
Action decomposition, documentation, and the bounded historical-wire exception. They do
not authenticate retained files.

### Artifact-owned evidence

- `test__integration__periodic_2d_optimizer_standalone_artifacts.py`
- `test__integration__periodic_2d_optimizer_standalone_fail_closed.py`

These tests bind maintained bytes and checksum-catalog identities, exercise the portable
reconstruction, and demonstrate sensitivity to forged declarations, repository mismatch,
coordinated byte changes, aggregate corruption, basin-member reassignment, and
claim-boundary corruption. Passing
establishes bounded software and numerical behavior only.

## Supported imports

The same defining class is available from four reviewed facades:

- `ksdft2effmass.periodic2d`;
- `ksdft2effmass.periodic2d.run.wannier90`;
- `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin`; and
- `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone`.

The retired model-named class and retained-model module remain absent; no alias or
forwarding module is provided.

## Limitations

The 16 starts are deterministic finite-design controls, not random population samples or
an exhaustive global search. Observed basin membership is an operational numerical
quotient under retained thresholds, not proof of distinct stationary points. The
verifier does not read external native run roots, rerun Wannier90, prove global or
general optimizer convergence, combine error classes, establish scientific validation,
quantify physical uncertainty, or record acceptance.
