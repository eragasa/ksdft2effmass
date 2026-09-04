# Harness compiler implementation

## Status and identity

**Status: administratively closed and human accepted.** The v2 owner is
`ksdft2effmass.harness`; the managed Task is
`migration.v2.harness.compiler`. The accepted bounded result uses the full aggregate,
contract-first design and source-level evidence Option A. This acceptance applies only
to the implemented software contract; it grants no protected execution, scientific
acceptance, successor activation, publication, or release authority.

## V1 source responsibilities

Canonical Task JSON, Task selection, development decisions and legacy checkpoints,
generic resource records, Pi agent definitions, and maintained Python evidence source
bytes remain owned by their existing decoders and nominal records. Generated SQL,
databases, projected task graphs, and documentation are not compiler inputs.

## Target concern and exclusions

The target is one explicit repository loader, one closed source snapshot, one pure
compiler, and one immutable complete selected-source `HarnessState`. Completeness
means required source-family presence, not downstream semantic validation.
Configuration, authority,
validation, persistence, projection, installed-agent observations, scientific
Workflow state, retry, repair, and execution remain separate.

## Containment decomposition

The Task owns this cohesive compiler slice. It introduces no implementation-phase
child registry or second Task topology.

## Planning cascade

Administrative closeout clears the managed selection. Automatic succession stays
disabled; no sibling or successor is activated by compilation, verification, review,
or acceptance.

## Implementation approach

`HarnessSourceFamilyContract` carries plural configured roots and explicit sorted
source paths. `HarnessLegacyDecisionBinding` supplies non-inferred one-way checkpoint
adaptation identities. `HarnessRepositoryLoader` performs bounded no-follow reads and
stable metadata/path-closure checks. `HarnessCompiler` performs no I/O and builds the
existing Task registry and selection, existing decision values, and capability,
resource, and evidence catalogs. Under authorized evidence Option A, evidence reuses
exact `PythonModuleSource` paths/bytes and source identities only. Downstream Python
conformance exclusively owns parsing, evidence owners, evidence IDs, and claim
boundaries. Agent decoding receives an injected `PiHarnessConfiguration`. A
compiler-owned strictly typed canonical serializer derives all public aggregate
identities without the generic erased `_contract` encoder.

## Prerequisite results

The accepted Task-model and configuration implementations and the current Option-A
human selection are the applicable implementation inputs. This implementation does
not infer prerequisite satisfaction from Task status.

## Conditional human decisions

The plural-root, explicit legacy-decision binding, current `PythonModuleSource`, and
injected Pi-configuration corrections were resolved during implementation. No further
material human-owned choice is selected here.

## Verification

Focused maintained tests provide software verification of complete selected-source
state construction, exact identity binding, actual state provenance, required-family
and format admission, explicit legacy decisions, component-wise path security, and
fail-closed family mismatch. Changed-surface Ruff and mypy, Python evidence
conformance, 3,270 passing broader software-verification tests with three explicit
external-artifact skips, Sphinx warnings-as-errors, Harness validation, projection
sync/check, diff checks, and corrected independent review passed before closeout.
These results establish the bounded software contract, not scientific validation or
protected-execution authority. Final human acceptance is supplied separately by the
recorded closeout authorization.

## Cutover, retirement, and rollback

The new public import surface is additive. It does not restore the retired
`PythonTestEvidenceSource`, replace existing source owners, persist state, or change a
projection consumer. Any future replacement or retirement requires a separately
authorized Task and applicable compatibility analysis; canonical source records remain
authoritative.

## Residual limitations

Version 1 adds no state wire/schema, persistence, validator, projector, CLI, automatic
repair, external-effect operation, or scientific aggregate. Evidence loading preserves
exact selected paths, bytes, and source identities but does not parse evidence owners,
evidence IDs, or claim boundaries and makes no evidence-semantic validation claim.
Filesystem hardening currently relies on POSIX descriptor-relative operations,
including `O_NOFOLLOW`; the broader supported-filesystem matrix remains deferred.
