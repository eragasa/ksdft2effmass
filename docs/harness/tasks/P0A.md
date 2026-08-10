<!-- Generated from SQLite control state; do not edit. -->
# P0A — SNAKES/MyST packaging and documentation configuration

[Task index](index.md) · [Previous](./P0.md) · [Next](./P1.md)

## Status

`human_accepted_pass`: closed; human-accepted `PASS` through resolved `P0A-HC01` on 2026-08-03

## Objective

Adopt only the accepted dependency declarations and documentation configuration,
retain exact lock artifacts and hashes, add an accurate third-party notice, and
verify installation and maintained documentation behavior without implementing
the production CPN runtime.

## Parent and prerequisites

- Depends on: `P0`

## Authority references

- .pi/chains/backend-neutral-kohn-sham-qe.chain.json
- .pi/checkpoints/P0-HC01-packaging-license-and-configuration.json
- .pi/evidence/backend-neutral-cpn-P0A-packaging-configuration
- docs
- harness/archive/task-control-v1/tasks/P0A.md
- python/.venv
- python/build

## Authorized scope

- add `SNAKES>=0.9.33,<0.10` only to an optional `workflow` extra;
- keep SNAKES outside core and development-only dependency sets;
- add `myst-parser>=5.1,<6` to the documentation extra;
- constrain the documentation environment to `Sphinx>=8,<10`;
- refresh the established lockfile while preserving exact resolved artifacts and
- keep system Graphviz optional and outside Python wheel metadata;
- add a third-party dependency notice identifying SNAKES, its copyright holder,
- retain the observed fact that the distributed SNAKES license file contains
- define explicit MyST source collection and navigation behavior without
- correct or explicitly exclude existing directory links and duplicate RST/MyST
- add only focused installation/configuration verification needed for this task.

## Completion criteria

- dependency extras contain exactly the authorized ranges and placement;
- the lock records exact selected artifacts and hashes;
- clean installation/import probes cover the core installation, `workflow`
- the third-party notice matches retained upstream package evidence and does not
- explicit MyST collection/navigation behavior is documented;
- the selected maintained documentation build passes Sphinx with warnings as
- affected link and duplicate-navigation checks pass;
- focused formatter, linter, package-build, and import checks pass;
- no production CPN/scientific source or test implementation is introduced;
- independent read-only license/packaging, documentation, and integration
- parent verification confirms scope containment and checkpoint state;
- human final acceptance closes P0A before any later task may launch.
- The human PI selected Option A at `P0A-HC01` on 2026-08-03 and accepted P0A as
`PASS` without corrective work. The dependency placement, lockfile,
documentation collection policy, third-party notice, redistribution boundary,
validation evidence, and recorded non-blocking residual limitations are
human-accepted.
- P0A is closed. Its checkpoint resolution did not launch P1. The same human
message separately authorized P1 activation only after P0A closeout validation
passed; that activation is recorded independently in the P1 task and chain
records. No production CPN implementation, SNAKES adapter, persistence,
workflow execution, or scientific execution was produced by P0A.

## Exclusions

- vendor or embed SNAKES source;
- copy SNAKES implementation code into project-owned modules;
- modify or redistribute a SNAKES fork;
- bundle SNAKES into a standalone executable, application bundle, or container
- imply that SNAKES is covered by the project's Apache-2.0 license.
- SNAKES remains replaceable behind a project-owned boundary. Project records,
schemas, identifiers, persistence, provenance, retry semantics, and canonical
ordering remain backend-neutral. Pickle is prohibited for authoritative
persistence. Arbitrary Python expressions and untrusted guard text must not be
evaluated. Pure project-owned guards remain policy; SNAKES is not a security
sandbox. `StateGraph` supports only bounded reachability enumeration. Graphviz
output remains optional, derived, and nonauthoritative.
- P0A must not implement the production CPN runtime, public CPN contract, marking
persistence, scientific token payloads, backend integration, or another CPN
backend. It must not change scientific operator behavior or launch QE, ABINIT,
Wannier90, scheduler, remote, or other scientific calculations.

## Historical source

`harness/archive/task-control-v1/tasks/P0A.md` (`sha256:6477dbb4715637c557388f3ce97f5a3772d1a0c003ff2c92b13b515d099c8a5e`)
