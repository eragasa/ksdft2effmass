# `QePwEvidenceAdapter`

## Ownership

`QePwEvidenceAdapter` is KSD's effect-free anti-corruption action between the
local Quantum ESPRESSO `pw.x` process boundary and Project Koios Simulations
execution observations. It does not represent or admit `bands.x` execution.
Project Koios Simulations owns the calculator-neutral observation, exact stream
content identities, explicit process-entry and termination facts, monotonic duration,
and canonical `execution.json` bytes. KSD owns preparation, workspace snapshots,
Workflow identities, later diagnostic/native-output correlation, and scientific
interpretation.

## Inputs and output

The adapter consumes two cohesive immutable objects:

- the exact `LocalQePreparedExecution`; and
- the exact `LocalQeCapturedProcess` produced for that preparation.

It does not accept detached paths, stream bytes, duration, or termination scalars as
public action arguments. Those values remain owned by the preparation and capture
objects. `QeNormalProcessExit` retains the provider-owned `CalculatorExitCode`, whose
`CalculatorExitDisposition` is the only success/failure surface used by KSD logic.
The raw numeric value remains exact provenance and legacy-wire data; KSD does not
branch on unexplained numeric exit codes. After exact lineage and snapshot checks, the
adapter invokes the provider's `CalculatorExecutionObservationAssembler` and returns
`QePwObservation`. The binding retains all three exact instances
directly without performing publication.

## Execution-record publication

`LocalQePreparedExecution` owns one exact
`LocalQeExecutionRecordDestination`, containing the portable destination and confined
absolute path. No global destination constant or detached path argument is used.
`QePwEvidencePublisher` consumes only the observation binding, obtains the
provider-owned canonical bytes and the prepared destination from those objects, and
publishes with exclusive no-follow temporary creation plus same-directory no-replace
hard linking. It synchronizes the file and directory, independently reopens and hashes
the destination without following symbolic links, and closes a post-publication
workspace snapshot.

Success returns `QePwPublishedEvidence`, retaining the exact nominal publisher
identity, observation binding, prepared destination instance, SHA-256 content identity,
publication snapshot manifest, and exact manifest entry. Publication precedes
diagnostic classification, native-output collection, and KSD terminal publication.

## Final result assembly

After terminal publication, effect-free `QePwResultAssembler` validates the exact
`QePwPublishedEvidence`, diagnostic report, native-output manifest, calculator
outcome, terminal record, and published terminal artifact before returning
`QePwResult` directly. It verifies preparation and predecessor sources, stream
content identities, snapshot lineage, provider-record manifest identity, terminal
wire content, and destination ownership. No public correlated-evidence intermediate
or second result adapter is introduced. The terminal record is the private
`qe-local-terminal-record-v2` wire and explicitly references the provider execution
record content, manifest entry, publication snapshot, diagnostic report, and native
output manifest.

## Failure behavior

The adapter returns one typed failure for:

- preparation/process lineage mismatch;
- process/snapshot lineage mismatch; or
- rejection by the provider observation contract.

The adapter, publisher, and assembler use the shared `QePwEvidenceFailureCode`
taxonomy. A failure contains
no partial successful binding. Publication-specific values distinguish invalid or
pre-existing destinations, limit exhaustion, publication failure, durability
uncertainty, and post-publication identity mismatch; assembly-specific values identify
diagnostic, native-output, outcome, or terminal mismatch. Sanitized failure
text does not replace typed identities or become scientific evidence.

## Claim boundary

The adapter performs no filesystem access, process entry, publication, diagnostic
classification, retry, authority grant, convergence decision, or scientific
acceptance. The publisher performs only the bounded record-publication effect and
establishes no calculator or scientific meaning. Final `QePwResult` assembly is now
reachable for `pw.x`; replacement of its legacy evidence payload remains gated by the
replacement persistence wire.
