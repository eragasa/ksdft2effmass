# Class-owned evidence documentation convention

Status: closed as human-accepted `PASS` through resolved `EVIDENCE-DOC-1-HC03` Option A on 2026-08-04

## Authority and objective

The human PI authorized a repository-wide documentation grammar for class-owned software-verification, numerical-verification, and future scientific-validation evidence. After the bounded `CpnToken` pilot and the `FiringRequest` remand, resolved `EVIDENCE-DOC-1-HC02` Option B authorizes applying that grammar to all 32 maintained class-owned modules in the P1 CPN workflow test directory. It does not reopen or alter the accepted scientific or software meaning of P1, P1-HC01, P1-HC02, or P1-HC03.

## Scope

Authorized:

- harden the existing documentation/test-evidence skill routing and reusable references;
- synchronize `docs/verification/testing-and-evidence.rst` and concise repository routing policy;
- add structural documentation validation without claiming semantic review authority;
- migrate every maintained P1 class-owned and artifact-owned evidence module, including semantic test names, exact module/test/helper grammar, and complete old/new node traceability, while preserving assertions, fixtures, parameterization, evidence IDs, and collection count;
- record complete pytest node-ID migration traceability;
- inventory software-verification, numerical-verification, artifact-owned, and protected historical modules;
- compare `NV-G-001` through `NV-G-009` with the convention without modifying that accepted historical module;
- update affected current ownership/control-plane records and checksums;
- run the requested deterministic validation and independent review.

Excluded:

- production source, schema, fixture, dependency, tolerance, assertion, or scientific-meaning changes;
- invention of scientific-validation or UQ markers or evidence-ID families;
- migration of closed operator-record evidence or evidence modules outside the maintained P1 class-owned and artifact-owned surfaces;
- modification of accepted checkpoint decisions;
- P2--P11 launch or production/scientific execution.

## Ownership and completion

The controlling chain names `.pi/evidence/class-owned-evidence-convention/task-ownership.json`. Separate implementation/control-plane, test, and documentation writers own non-overlapping paths; the integration reviewer is read-only. The required completion validator is:

```bash
python .pi/evidence/class-owned-evidence-convention/validate.py
```

Passing structural validation does not prove oracle independence, mathematical correctness, scientific validity, tolerance adequacy, or uncertainty-treatment adequacy. Those are review questions.

## Implementation/control-plane progress

The implementation/control-plane writer added the shared convention reference,
routed the operator-record skill to it, preserved historical first-line evidence
owner declarations while adding `Evidence ID` field support to the reusable
audit, inventoried the maintained module surface, and recorded a read-only
`NV-G-001`--`NV-G-009` comparison. Following the test writer's complete-directory
migration, the structural completion validator requires all 32 manifest-
declared class modules, all 78 manifest-declared test functions, all 11 declared
helpers, and one complete 78-function node-ID map. The architecture-reviewed
follow-up also fixes the five artifact-owned destination filenames and requires
their ten evidence owners, differentiated artifact/boundary semantics, manifest
assignments, and old-to-new node mappings. The test writer completed that
synchronized rename and manifest migration; implementation/control-plane replay
paths, completeness records, mutation inventory, and structural validation now
use the current filenames. The prior per-module pilot maps and old P1 review
paths remain historical detail.
Structural tooling remains explicitly unable to establish oracle independence,
mathematical correctness, tolerance adequacy, scientific validity, UQ adequacy,
or final acceptance.

## Current implementation result

The existing `document-research-python` skill owns the reusable grammar through
`references/test-evidence-documentation.md`; `develop-operator-records` routes
operator-specific evidence to that shared reference. The grammar now owns exact
class filename/SUT agreement, descriptive artifact filenames, two-sided versus
directional boundary naming, exact approved Workflow/subnet segments, prohibited
generic names, synchronized rename traceability, and the structural/semantic
review boundary. All 32 class-owned modules in
`python/tests/software_verification/ksdft2effmass/workflows/cpn/` retain 78 stable
evidence IDs under semantic test names, with complete old/new function-node
traceability in `cpn-complete-directory-node-id-map.json`.

The approved artifact filenames are
`test__workflow_cpn_python_public_api.py`,
`test__workflow_cpn_v1_python_json_contract.py`,
`test__workflow_cpn_v1_json_fixtures_python_runtime_contract.py`,
`test__workflow_cpn_python_import_dependency_direction.py`, and
`test__workflow_cpn_python_snakes_and_deferred_engine_isolation.py`. The test
writer renamed and documented those files and synchronized its P1 manifest,
validator, and node mappings. The implementation/control-plane writer then
synchronized the completion validator, gate replay paths, current completeness
and mutation-audit records, and migration inventory. Documentation-writer updates to `docs/verification/cpn-contract.rst` and
`docs/verification/testing-and-evidence.rst` are synchronized with the current
filenames and convention. The two current checksum catalogs cover those pages,
the migrated class and artifact modules, and their current control-plane
records; obsolete integration filenames occur only in explicitly historical
reviews, baselines, or predecessor mappings. The architecture decision preserves `SV-CPN-028`
as one accepted conjunctive
nonnumeric Python/JSON boundary agreement: its local resolution, required-
definition, closed-enum, and representative-wire facets remain one requirement,
with no split and no new evidence IDs. Numeric agreement remains separately
owned by `SV-CPN-087` and `SV-CPN-088`.

The protected `NV-G-001`--`NV-G-009` module remains a read-only comparison
target.

This follow-up records deterministic structural conformance only. The persisted
final architecture/VVUQ and integration reviews both conclude PASS. Fresh parent
validation records 1012 full-suite Python tests passed, Sphinx 9.1.0 with `-W`
passed, ten contract replay tests passed, and 91 focused P1 tests passed. The
EVIDENCE-DOC-1 completion validator, P1 ownership validator, task-ownership
preflight, skill-capability validator, checkpoint validator, both checksum
catalogs, chain JSON parsing, and `git diff --check` also pass. The evidence audit
reports 403 owned IDs, zero errors, and the same 22 protected historical owner
warnings, which remain outside this task.

Implementation and independent review are complete. The human PI granted final
acceptance through `EVIDENCE-DOC-1-HC03` Option A. This acceptance closes only
the bounded maintenance task; it does not establish scientific validation, UQ,
tolerance adequacy, or Rust conformance and does not authorize a successor.

## State boundary

P1 remains closed as human-accepted `PASS` through `P1-HC03`; this maintenance
task is not P2 and is not a scientific-program successor. EVIDENCE-DOC-1 is
closed as human-accepted `PASS` through resolved `EVIDENCE-DOC-1-HC03` Option A.
No successor was launched. P2--P11 and all production/scientific execution
remain blocked and unauthorized.
