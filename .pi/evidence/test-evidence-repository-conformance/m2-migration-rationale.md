# M2 migration rationale

M2 migrates all 32 class-owned CPN object modules, all five artifact-owned Workflow CPN integration modules, and the supporting CPN `conftest.py` under `AUTHORIZED_TEST_EVIDENCE_WRITE`.

The baseline collected 91 nodes. Every baseline node is mapped one-to-one in `m2-node-migration-map.json` by its preserved authoritative evidence ID. Renames replace superseded headings and vague `contract` facets with concrete constructor, field, method, and artifact surfaces.

The 132 genuinely new nodes in `m2-new-split-nodes.json` arise from deterministic semantic corrections:

- explicit parameter IDs replace hidden case loops;
- accepted-state, wrong-semantic-type, and malformed-value partitions have separate owners;
- `evaluate_value` and `evaluate_guard` have separate method evidence;
- fixed schema entry points, definition inventories, enum agreements, numeric bounds, strict JSON behavior, fixture classifications, and runtime relational outcomes have cohesive artifact owners;
- public API evidence uses a fixed literal 49-name oracle rather than self-inspection; and
- new owners use the previously unused sequential evidence IDs `SV-CPN-089` through `SV-CPN-173`.

Assertions, fixtures, synthetic values, exception types/messages/codes, public imports, and version-1 public contracts were retained. No production source, public schema, fixture, dependency, specification, or historical evidence was changed.
