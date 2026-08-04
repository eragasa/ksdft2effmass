# H0 — Harness inventory and ownership classification

Status: active read-only preflight; activated from authoritative accepted P1 closeout; H1--H5 and P2--P11 remain blocked

## Project

PI Harness Incubation and Extraction Readiness (`pi-harness-incubation`). This project is separate from the backend-neutral CPN P0--P11 chain.

## Objective

Inventory the current repository harness/control-plane surface and classify every component as exactly one of:

- `EXTRACTABLE`;
- `SPLIT_GENERIC_AND_LOCAL`;
- `KEEP_PROJECT_LOCAL`;
- `RETIRE_AS_DUPLICATE`;
- `DEFER`.

H0 establishes evidence for a later human decision; it does not treat the prospective architecture under `docs/harness/` as implemented functionality.

## Authorized read-only scope

Inspect and inventory:

- repository-local skills and references;
- deterministic scripts and validators;
- schemas, templates, manifests, and profiles;
- task, checkpoint, chain, evidence, checksum, and Git decision-boundary mechanics;
- task/test ownership and evidence-ID rules;
- software- and numerical-verification conventions;
- documentation and Sphinx/MyST collection policy;
- package/path assumptions, current consumers, and duplicated responsibilities.

H0 may write only its task/checkpoint/control records and retained inventory/review evidence under `.pi/evidence/pi-harness-incubation/H0/`. Inspection of source, tests, specifications, documentation, skills, and runtime state is read-only.

## Required outputs

- complete component inventory with one classification per component;
- generic/local source-of-truth map;
- consumer and duplicated-responsibility map;
- prospective-versus-implemented path/interface report;
- conflict and project-leakage findings;
- H1 contract-scope and migration-constraint proposal;
- deterministic inventory validator and checksums;
- independent task-decomposition, architecture/VVUQ, documentation, and integration reviews;
- genuine `H0-HC01` human checkpoint approving or correcting the inventory, classifications, generic/local boundary, source-of-truth map, H1 scope, and migration constraints.

## Prohibited work

H0 performs no Python harness implementation, source movement, skill retirement, validator replacement, package extraction/publication, P2 work, CPN behavior change, schema/fixture/test mutation, external-tool execution, or scientific execution. It must not create `python/src/ksdft2effmass/harness/pi/`, `python/src/ksdft2effmass/harness/pi/local/`, `harness/pi/`, or `harness/local/` as implementation/resource trees.

## VVUQ boundary

H0 produces control-plane and software-inventory evidence. Numerical verification applies only to a future actual numerical algorithm. Scientific validation and uncertainty quantification are not applicable.

## Completion and stop

H0 is complete only when its inventory and reviews pass deterministic validation and the pending `H0-HC01` checkpoint is committed and pushed. H0 then blocks for the human. H1 must not activate before accepted H0, and P2 must remain blocked.
