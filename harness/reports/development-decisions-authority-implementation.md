# Development decisions and optional authority implementation

## Status

**Software implementation result.** Commit candidate based on activation record
`migration.v2.harness.decisions-authority.implementation-activation` implements the
accepted `DevelopmentDecision` and default-unsigned, explicitly per-Task opt-in
signature-verification contracts. It creates no private key, signature, credential,
real authority artifact, protected execution, publication, release, or automatic
successor activation.

## Implemented surfaces

- immutable DevelopmentDecision, option, and exact source-provenance records;
- strict canonical serialization and one-way exact-byte legacy adaptation;
- all 28 retained checkpoint records adapt without loss or invented authority identity;
- immutable Task signature configuration with a deterministic unsigned default;
- optional Ed25519 verification through the `authority-signatures` extra pinned to
  `cryptography==50.0.0`;
- strict trust, signed-snapshot, ledger-closure, reconstruction receipt/context, and
  exact operation-authorization records and actions;
- six closed Draft 2020-12 JSON schemas, public imports, API documentation, fixtures,
  and maintained software-verification evidence.

The unsigned path does not import cryptography. A Task configured as `required` fails
closed when the optional capability or valid signed context is unavailable. Signed
contexts bind their records to the independently verified head-snapshot payload.

## Verification

The following checks passed on 2026-08-19:

- focused authority and public-import software verification: `32 passed`;
- Ruff over the complete Python tree;
- mypy over 146 source files;
- six authority schemas against the Draft 2020-12 metaschema;
- Sphinx HTML build with warnings as errors;
- Harness projection synchronization and drift check;
- Harness validation: Python conformance, resources, Task graph, checkpoints, skills,
  and control state; and
- `git diff --check`.

A complete pytest run produced `3091 passed, 3 failed`. The three failures are existing
stale-fixture references outside this Task: two tests name removed historical Task
files and one skill-capability fixture names another removed historical Task file. No
authority or decision test failed.

Independent final review found no blocker or high-severity finding after correction.

## Residual boundary

The complete shared `HarnessState`, compiler, and aggregate cross-record validator do
not yet exist. Their integration remains owned by the separately declared
`migration.v2.harness.compiler` and `migration.v2.harness.validation` Tasks. This
implementation does not invent those deferred public fields or activate either Task.
