# POLICY-CONSTITUTION-1 — Stable repository constitution revision

Status: closed as human-accepted `PASS` through resolved `POLICY-CONSTITUTION-1-HC01`; no successor or execution activated

## Authority and objective

The human instruction dated 2026-08-04 authorizes a policy-documentation-only
revision that makes root `AGENTS.md` a stable repository constitution. The
revision removes mutable task snapshots and duplicated procedure, defines clear
authority precedence and proportional process classes, and preserves scientific,
mathematical, provenance, execution, branch, release, and human-authority
safeguards.

## Process classification

This is policy and public-control-contract documentation work. It changes no
scientific contract, public software API, schema, fixture, dependency, production
source, or test. A task-ownership manifest and separate writer roles are not
required because one bounded writer owns the documentation changes and one
independent reviewer performs a consolidated read-only review.

## Authorized paths

- `AGENTS.md`
- directly conflicting maintained control-plane or skill documentation
- this bounded task record
- `.pi/checkpoints/POLICY-CONSTITUTION-1-HC01-final-acceptance.json`

Historical evidence, closed H0/H1 artifacts, P1 evidence, harness implementation,
scientific source and tests, schemas, fixtures, dependencies, and lock files are
excluded.

## Required flow

1. revise the policy documentation;
2. validate state-reconstruction, precedence, process classes, conditional
   ownership/evidence/Rust/documentation rules, checkpoint compatibility, links,
   chain/checkpoint validity, unrelated-work preservation, and whitespace;
3. obtain one consolidated independent read-only policy/integration review;
4. permit at most one consolidated correction pass;
5. run final verification;
6. commit and push the validated pending acceptance boundary to `dev`; and
7. stop at `POLICY-CONSTITUTION-1-HC01` without activating a successor.

## Validation and consolidated review

The checkpoint validator, chain/checkpoint JSON validation, referenced-path
check, `git diff --check`, and warnings-as-errors Sphinx build passed. One
consolidated independent read-only policy/integration review returned `PASS`
with no material findings. No correction pass was needed. Final verification
passed; this record is part of the pending acceptance boundary.

## Acceptance and closeout

The human PI accepted Option A through
`.pi/checkpoints/POLICY-CONSTITUTION-1-HC01-final-acceptance.json` on 2026-08-04.
Deterministic closeout validation passed, and this policy task is closed as
human-accepted `PASS`. The acceptance closes only this policy revision. It did
not activate H3, H2, H4, H5, P2, harness implementation, external or release
execution, numerical work, or scientific execution.
