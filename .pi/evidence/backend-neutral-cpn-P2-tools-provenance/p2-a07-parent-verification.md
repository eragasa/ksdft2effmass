# P2-A07 parent verification

Status: **PASS — P2-A07 audited_and_cleared; P2-A08 next and not started**

Starting revision: `c95534d3ade91cd62702a9b0a0e5aae95973107a` with
`HEAD == origin/dev` and a clean working tree after fetching `origin/dev`.
P2-A06 was `audited_and_cleared`, `active_item` was null, P2-A07 was next, and
`TEST-EVIDENCE-CONVENTIONS-2` was `proposed_inactive`. Only P2-A07 was activated.

The corrected module remains artifact-owned software verification of the static import
graph of the provenance package. It preserves `SV-PROV-070` and `SV-PROV-071`
exactly once and adds no evidence ID. Its visible ID-free helper returns a `frozenset`
of frozen `StaticImportDependency` records retaining import form, complete AST module
or `None`, imported names, and exact relative level. It neither reduces absolute
modules to roots nor discards unusual relative forms.

The supplied absolute-import draft was verified against the production source at the
starting revision with no discrepancy. The exact source inventory contains
`__init__.py`, `actions.py`, `external_execution.py`, `external_tools.py`, `records.py`,
`serialization.py`, and `tool_observations.py`. The fixed level-one relative adjacency
and fixed per-file absolute module mappings match exactly. Controlled syntax examples
show that an absolute provenance import, `from . import records`, a level-two relative
import, and undeclared standard-library, project, scheduler, plugin, and third-party
imports remain visible and differ from the applicable exact oracle. No architecture
word is searched in arbitrary source text.

The module contains two test functions/evidence owners, one ID-free helper, and two
collected cases. Its two changed pytest nodes have a complete one-to-one migration.

Deterministic results:

- structural validation: PASS with zero findings;
- collection: 2 tests;
- focused module: 2 passed;
- complete provenance integration family: 144 passed;
- Ruff format/lint and focused mypy: PASS;
- exact source inventory, internal adjacency, absolute imports, and controlled dangerous
  forms: PASS;
- evidence uniqueness and complete node migration: PASS;
- P2 ownership, completion, and checkpoint validators: PASS.

The one targeted read-only reviewer run
`8bce7075-3fc7-4124-9dd0-b28a57730667` inspected only the import-dependency module
and the production modules needed to check its oracles. It returned PASS with no
findings and made no mutations. No correction pass or second review was required.

Production provenance source and exports, schemas and fixtures, dependencies and
lockfiles, the other four integration modules, historical evidence, harness resources,
and protected inactive-backlog files remain unchanged.

The queue retains `active_item: null`, marks P2-A07 `audited_and_cleared`, and names
P2-A08 as next without starting it. P2 remains open and unaccepted. P3, H5, protected
execution, publication, and release remain inactive.
