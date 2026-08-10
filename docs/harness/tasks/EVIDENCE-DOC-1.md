<!-- Generated from SQLite control state; do not edit. -->
# Class-owned evidence documentation convention

[Task index](index.md) · [Previous](./E.md) · [Next](./F.md)

## Status

`human_accepted_pass`: closed as human-accepted `PASS` through resolved `EVIDENCE-DOC-1-HC03` Option A on 2026-08-04

## Objective

The human PI authorized a repository-wide documentation grammar for class-owned software-verification, numerical-verification, and future scientific-validation evidence. After the bounded `CpnToken` pilot and the `FiringRequest` remand, resolved `EVIDENCE-DOC-1-HC02` Option B authorizes applying that grammar to all 32 maintained class-owned modules in the P1 CPN workflow test directory. It does not reopen or alter the accepted scientific or software meaning of P1, P1-HC01, P1-HC02, or P1-HC03.

## Parent and prerequisites

None.

## Authority references

- .pi/chains/backend-neutral-kohn-sham-qe.chain.json
- .pi/evidence/class-owned-evidence-convention/task-ownership.json
- docs/verification/testing-and-evidence.rst
- harness/archive/task-control-v1/tasks/EVIDENCE-DOC-1.md

## Authorized scope

- harden the existing documentation/test-evidence skill routing and reusable references;
- synchronize `docs/verification/testing-and-evidence.rst` and concise repository routing policy;
- add structural documentation validation without claiming semantic review authority;
- migrate every maintained P1 class-owned and artifact-owned evidence module, including semantic test names, exact module/test/helper grammar, and complete old/new node traceability, while preserving assertions, fixtures, parameterization, evidence IDs, and collection count;
- record complete pytest node-ID migration traceability;
- inventory software-verification, numerical-verification, artifact-owned, and protected historical modules;
- compare `NV-G-001` through `NV-G-009` with the convention without modifying that accepted historical module;
- update affected current ownership/control-plane records and checksums;
- run the requested deterministic validation and independent review.
- production source, schema, fixture, dependency, tolerance, assertion, or scientific-meaning changes;
- invention of scientific-validation or UQ markers or evidence-ID families;
- migration of closed operator-record evidence or evidence modules outside the maintained P1 class-owned and artifact-owned surfaces;
- modification of accepted checkpoint decisions;
- P2--P11 launch or production/scientific execution.

## Completion criteria

- The controlling chain names `.pi/evidence/class-owned-evidence-convention/task-ownership.json`. Separate implementation/control-plane, test, and documentation writers own non-overlapping paths; the integration reviewer is read-only. The required completion validator is:
- ```bash
python .pi/evidence/class-owned-evidence-convention/validate.py
```
- Passing structural validation does not prove oracle independence, mathematical correctness, scientific validity, tolerance adequacy, or uncertainty-treatment adequacy. Those are review questions.

## Exclusions

- P1 remains closed as human-accepted `PASS` through `P1-HC03`; this maintenance
task is not P2 and is not a scientific-program successor. EVIDENCE-DOC-1 is
closed as human-accepted `PASS` through resolved `EVIDENCE-DOC-1-HC03` Option A.
No successor was launched. P2--P11 and all production/scientific execution
remain blocked and unauthorized.

## Historical source

`harness/archive/task-control-v1/tasks/EVIDENCE-DOC-1.md` (`sha256:ab8d74c41051f21aeb98aae4a481261a957286791bd309f63657f4d15c097570`)
