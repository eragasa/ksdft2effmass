# Deferred harness improvement — explicit current phase and reconstructable history

Status: deferred; inactive

Activation: not authorized

Implementation: none

## Observation

Current chain records use a one-element `chain` array whose entry is replaced as the active phase changes. This is an internally consistent current-state projection, and existing records are not malformed merely because they replace that projection. The field name and array shape can nevertheless imply a retained ordered sequence, while chronology is actually distributed across authoritative task records, checkpoints, activation and decision records, retained evidence, and Git history.

Current chain behavior and schemas remain authoritative. This record does not reinterpret current state or authorize migration.

## Prospective design

A future, separately activated design task may evaluate an explicit current-state shape such as:

```json
"current_phase": {
  "phase": "P2-bounded-actions-test-evidence-correction",
  "message": "...",
  "entered_at": "...",
  "authority": "..."
}
```

The preferred investigation is a deterministic timeline-reconstruction action that derives ordered history from authoritative durable task, checkpoint, activation, decision, evidence, and—where necessary—Git records. It should not automatically duplicate all events into the chain record. An append-only `phase_history` may be considered only if deterministic reconstruction is insufficient, and it must not become a second conflicting source of truth.

## Unresolved design questions

1. Should `chain` become `current_phase`, or remain temporarily through a versioned compatibility mapping?
2. Which record owns authoritative phase-entry and phase-exit timestamps?
3. Which authority records why a phase changed?
4. Can existing durable records reconstruct a complete deterministic ordered timeline?
5. How should simultaneous sibling tasks or independently active programs be represented?
6. Should chain records own operational state only while tasks and checkpoints own history?
7. What migration and version boundary is required for existing consumers?
8. How should legacy records remain readable without rewriting historical evidence?
9. What future SQLite representation could preserve current state, events, authority, and provenance without duplicating truth?
10. Which behavior is generic to `ksdft2effmass.harness.pi`, and which interpretation belongs in `ksdft2effmass.harness.pi.local`?

These questions are not accepted decisions.

## Scope and activation boundary

No current chain record, chain schema, validator, runtime consumer, harness Python source, test, documentation navigation, dependency, lockfile, checkpoint, P2 record, H5 state, or P3–P11 state is changed or authorized by this record. No SQLite work, replay, implementation, task activation, or external/scientific execution is authorized.

Future work requires separate explicit human activation, bounded ownership, compatibility analysis, and applicable validation. This prospective infrastructure improvement makes no numerical-verification, scientific-validation, uncertainty-quantification, physical-correctness, or human-acceptance claim.
