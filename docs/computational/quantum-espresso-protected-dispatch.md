# Quantum ESPRESSO protected local dispatch

## Status and scope

This procedure records the provisional trusted-host architecture selected for the
initial local Quantum ESPRESSO campaign. It does not grant execution authority and is
not an execution record.

The manifest CLI remains plan-only. Its non-plan path must stay blocked. A manifest,
development-decision identity, checksum, successful preflight, or historical run does
not substitute for a current one-dispatch grant and verified authority snapshot.

## Boundary ownership

An application-owned trusted host is responsible for obtaining and authenticating the
external authority source. It supplies already verified, immutable typed values to
`QuantumEspressoProtectedDispatchWorkflow`. The Workflow correlates those values and
owns reservation, claim, immediate reauthorization, durable dispatch entry, and the
single executor call. It does not authenticate raw transport data, issue a grant,
discover authority, retry, or broaden scope.

The host must supply all of the following explicitly:

- the exact dated-v2 `QuantumEspressoExecution` plan;
- an exact predecessor-revision read request and matching `WorkflowRuntimeBundle`;
- the selected `TaskActivation`;
- unused preparation and reserved claim authority views produced by the trusted
  boundary;
- distinct lifecycle revision, commit, reservation, claim, and dispatch identities;
- one configured `WorkflowRunRepository`, serializer, and authorizer; and
- the exact version-bound diagnostic catalog.

Authority values must not be reconstructed from manifest references. Raw JSON with
matching identities is not authenticated authority.

## Read-only operator preflight

Before requesting protected execution, the trusted host may call
`QuantumEspressoProtectedDispatchWorkflow.preflight` with the complete typed request.
Preflight:

1. loads the exact predecessor revision;
2. requires replay equality;
3. checks manifest, activation, grant, and lifecycle correlation;
4. evaluates the supplied preparation and claim authority views;
5. constructs the matching local executor in memory; and
6. returns a closed readiness result.

Preflight performs no Workflow commit, reservation, claim, dispatch entry, workspace
creation, staging, process entry, or retry. `ready` means only that the supplied state
passed these software checks at preflight time. It is not authority, a promise that a
later execution will proceed, evidence of calculator success, or scientific
acceptance.

## Protected execution

A separate explicit call to `QuantumEspressoProtectedDispatchWorkflow.execute` repeats
persisted assembly and delegates to the generic control lifecycle. The lifecycle must
still win each current authorization and persistence boundary. Any stale, revoked,
mismatched, losing, duplicate, or indeterminate condition fails closed at its owning
stage.

After a confirmed dispatch, Workflow control must reconcile the exact dispatch-entry
receipt and runtime envelope before admitting the immutable result, native-output
manifest identities, terminal attempt, obligation disposition, and result-producing
CPN firing in one replay-equal successor commit. A process exit or executor return by
itself must not advance the marking.

Each retry or new attempt requires new activation, operation, request, attempt,
obligation, dispatch, and grant identities. The host must never reuse a previous grant
or infer permission from an earlier successful run.

## Operator stop conditions

Do not call protected execution when any of these conditions holds:

- the grant or verified snapshot was not obtained through the trusted host boundary;
- preflight is not `ready`;
- the authority source, trust configuration, freshness, revocation closure, or exact
  scope cannot be established;
- the predecessor revision or runtime bundle changed after review;
- executable, input, pseudopotential, resources, destination, or diagnostic catalog
  differ from the reviewed plan; or
- explicit authorization for the reported real QE execution and resource use is
  absent.

The current implementation supplies no generic command-line decoder for authority
records and no authority database or signing protocol. Those remain deferred unless
unattended or distributed execution establishes a concrete need.
