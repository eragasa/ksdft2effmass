# Repository test-evidence conformance control-plane implementation

Status: **milestones 1–6 implemented; raw maintained-test migration pending**

Baseline revision: `13c814ce53cab46b1d1a2cebab091c8a88bd33d4`

The current human instruction activated `TEST-EVIDENCE-CONVENTIONS-2` for all
current maintained Python test modules. The controlling chain and validated
ownership manifest are `.pi/chains/test-evidence-repository-conformance.chain.json`
and `task-ownership.json` in this directory. Its ownership preflight must name the
non-default chain explicitly:

```text
python .pi/task-ownership/validate_task_ownership.py \
  --chain .pi/chains/test-evidence-repository-conformance.chain.json \
  --task TEST-EVIDENCE-CONVENTIONS-2
```

## Captured baseline

- maintained test root: `python/tests`;
- top-level maintained test modules: **182**;
- expanded pytest nodes: **2383**;
- every module has explicit class-owned or artifact-owned classification, evidence
  class, content SHA-256, and migration status in `maintained-test-inventory.json`;
- every current module is deliberately `not_yet_conforming` until its controlled
  migration and semantic review are complete.

## Implemented controls

- preserved `protocol` for genuine Python protocol operations while rejecting vague
  facets such as `protocol__behavior`;
- added controlled deterministic findings and false-positive guards for vague facets,
  mixed enum construction/name lookup, mixed unknown/wrong-type partitions, circular
  enum lookup oracles, blanket E501 suppression, doubled/placeholder prose, and
  undeclared equality/frozen completeness claims;
- synchronized canonical and live `develop-python-test-evidence` skill resources;
- added a generic maintained-test inventory schema and controlled recurrence fixtures;
- added the local fail-closed completion command
  `python harness/local/validation/validate_repository_test_evidence.py`;
- routed all identified Python test writers and the evidence reviewer through the
  shared skill and repository gate; and
- retained the structural/semantic claim boundary explicitly.

## Current gate result

The completion gate currently returns the expected `FAIL` with exactly 182
`TE.REPOSITORY_STATUS` findings while reporting 182 discovered modules and 2383
collected nodes. This is a successful fail-closed baseline result, not task
completion. Migration must update content identities and statuses only after each
module passes structural validation and independent semantic review. No raw
`python/tests` module was changed in this implementation slice.
