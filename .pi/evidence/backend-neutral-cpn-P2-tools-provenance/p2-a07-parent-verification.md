# P2-A07 parent verification

Status: **PASS — P2-A07 audited_and_cleared; P2-A08 next and not started**

Original P2-A07 starting revision: `c95534d3ade91cd62702a9b0a0e5aae95973107a`.
Post-audit correction starting revision: `e0cd54aba28e73b1075e437ec9216cf3880cb50d`,
with `HEAD == origin/dev` and a clean working tree after fetching `origin/dev`.
P2-A07 was reopened only for the remaining controlled-import oracle correction;
P2-A08 remained inactive and `TEST-EVIDENCE-CONVENTIONS-2` remained
`proposed_inactive`.

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
and fixed per-file absolute module mappings match exactly. The post-audit correction
replaced the insufficient dangerous-observation inequality. Each absolute provenance,
`from . import records`, and level-two relative controlled import must now equal its
exact `StaticImportDependency`; the first must equal the absolute-internal
classification, and the latter two must each equal the ambiguous-relative
classification. Controlled mutation confirms that silently discarding either unusual
relative form fails `SV-PROV-070`. The existing exact undeclared absolute-module oracle
remains unchanged. No architecture word is searched in arbitrary source text.

The module contains two test functions/evidence owners, one ID-free helper, and two
collected cases. Its two changed pytest nodes have a complete one-to-one migration.

Deterministic results:

- structural validation: PASS with zero findings;
- collection: 2 tests;
- focused module: 2 passed;
- complete provenance integration family: 144 passed;
- Ruff format/lint and focused mypy: PASS;
- exact source inventory, internal adjacency, absolute imports, and exact controlled
  extraction/classification: PASS;
- silent-discard confirmation for module-less and higher-level relatives: both correctly
  fail;
- evidence uniqueness and unchanged complete node migration: PASS;
- P2 ownership, completion, and checkpoint validators: PASS.

The one targeted read-only reviewer run
`8bce7075-3fc7-4124-9dd0-b28a57730667` inspected only the import-dependency module
and the production modules needed to check its oracles. It returned PASS with no
findings and made no mutations. A subsequent human audit identified the weak
controlled-import inequality; the exact human-directed correction was applied without
an additional general review or replay cycle.

Production provenance source and exports, schemas and fixtures, dependencies and
lockfiles, the other four integration modules, historical evidence, harness resources,
and protected inactive-backlog files remain unchanged.

The queue retains `active_item: null`, marks P2-A07 `audited_and_cleared`, and names
P2-A08 as next without starting it. P2 remains open and unaccepted. P3, H5, protected
execution, publication, and release remain inactive.
