# TEST-EVIDENCE-CONVENTIONS-2 — Prevent recurring mixed-surface and generated-prose defects in Python test evidence

Status: `closed` as human-authorized PASS after final deterministic stabilization

```text
bounded_implemented_capability: module-local named literal pytest.param inventory resolution
remaining_backlog: activated_by_current_human_instruction
activation_authorized_for_remaining_backlog: true
implementation_authorized_for_remaining_backlog: true
controlling_chain: .pi/chains/test-evidence-repository-conformance.chain.json
ownership_manifest: .pi/evidence/test-evidence-repository-conformance/task-ownership.json
```

The current human instructions that all current tests must conform and to “fix this”
activate the remaining deterministic controls, the repository-wide inventory and
fail-closed gate, test-writer routing, and controlled migration of maintained Python
tests. The accepted generic convention remains authoritative where this older backlog
wording conflicts with it: `protocol` remains valid for genuine Python protocol
operations and is rejected only when semantically misused as a vague surface.
Production source, dependencies, scientific meaning, protected execution, release,
and publication remain unauthorized.

The concise proposal record is
[`../evidence/harness-backlog/TEST-EVIDENCE-CONVENTIONS-2.json`](../evidence/harness-backlog/TEST-EVIDENCE-CONVENTIONS-2.json).

The required ownership preflight for this non-default chain is:

```text
python .pi/task-ownership/validate_task_ownership.py \
  --chain .pi/chains/test-evidence-repository-conformance.chain.json \
  --task TEST-EVIDENCE-CONVENTIONS-2
```

The shorter ``--task``-only command selects the repository default chain and is not the
preflight for this task.

## Purpose and authority boundary

The current human instruction activates the remaining reusable controls plus one
project-local repository inventory and completion gate. The controlling chain and
validated ownership manifest above supply writer/reviewer separation and mutation
scope. Implementation is staged: control surfaces and the fail-closed baseline gate
precede controlled raw-test migration. The task remains unrelated to production or
scientific execution and does not activate or accept P2, P3, or another scientific
workflow.

## Recurring defects

The human P2 module audit repeatedly found:

1. vague surfaces such as `test_protocol__behavior__...`, `test_behavior__...`,
   and `test_contract__...`; genuine Python protocol operations remain valid;
2. one owner combining `EnumType(value)` (`__call__`) with `EnumType[name]`
   (`__getitem__`);
3. unknown valid-type values and wrong-semantic-type values combined because
   both happen to raise the same Python exception;
4. successful lookup using the circular oracle `SUT.__members__[name]` instead
   of an independently specified literal member;
5. blanket file-level suppression such as `# ruff: noqa: E501`;
6. doubled punctuation and generic generated prose;
7. irrelevant enum, dataclass, tuple, or action scope copied between modules;
8. “complete represented state” equality claims that vary only one field;
9. all-fields-frozen claims that exercise only one field;
10. missing field-by-partition coverage for repeated intrinsic validation; and
11. structural-validator PASS reported as if it established semantic correctness.

## Observed workflow friction

The P2 file-by-file audit also exposed coordination costs that are distinct from
test defects. The contemporaneous observation record is
[`../evidence/backend-neutral-cpn-P2-tools-provenance/p2-test-evidence-friction-observations.md`](../evidence/backend-neutral-cpn-P2-tools-provenance/p2-test-evidence-friction-observations.md).

Controls that protect an accepted boundary should remain explicit: primary
ownership, complete historical-node migration, production-source nonmutation,
semantic review, and durable queue state. Candidate accidental friction includes:

1. exact structural-opening requirements conflicting with ordinary formatter or
   lint line limits;
2. repeated manual assembly of the same scoped structural, collection, pytest,
   coverage, Ruff, mypy, regression, nonmutation, and Git checks;
3. manual synchronization of queue, task, chain, ownership, migration, progress,
   completion, and parent-verification records;
4. separate static-parameter and pytest-collected counts that require manual
   reconciliation;
5. aggregate consistency rules implemented through several ad hoc commands
   rather than one scoped entry point;
6. low-information coverage output for declarative enum classes with no
   executable method body;
7. an intentionally exact migration schema that requires rationale to be stored
   in a separate companion record; and
8. repeated nonactionable virtual-environment warning noise in command output.

These observations do not authorize weakening a completion gate. A future
implementation should automate evidence production and reconciliation while
retaining the underlying control and its claim boundary.

## Candidate workflow automation

If separately activated, evaluate:

- generated scoped command manifests derived from explicit ownership records;
- one result containing both structural counts and actual pytest collection;
- deterministic synchronization checks for queue/task/chain/evidence state;
- one scoped aggregate consistency command for a supplied maintained surface;
- explicit `not_applicable` diagnostic coverage for declarations with no
  executable body;
- a validated migration-rationale companion format; and
- validator/formatter interoperability fixtures, including long artifact names.

## Activated deterministic rules

### Concrete public surfaces

Reject known vague facet segments `behavior`, `contract`, `general`, and `misc`.
Preserve `protocol` as the accepted surface for genuine Python protocol operations,
but reject a vague spelling such as `test_protocol__behavior__...`. Accept explicit
surfaces such as `constructor`, `field`, `property`, `method__call`,
`method__getitem`, `method__eq`, `method__hash`, `method__repr`,
`method__execute`, and `method__deserialize`. This is not a universal closed list:
explicit public method and protocol facets remain extensible.

### Mixed enum lookup ownership

Detect one test function containing both value construction and name lookup,
including equivalent forms of `SUT(value)` and `SUT[name]`. Emit a structured
finding requiring separate owners unless an explicit accepted exception exists.

### Mixed invalid partitions

Detect one owner combining an unknown value of the accepted semantic type with
a wrong-semantic-type value. Identical incidental exception types do not make
those input partitions semantically identical.

### Circular enum oracles

Flag successful lookup whose expected member is derived exclusively from
`SUT.__members__[name]` and reused to check the same lookup behavior. Recommend
literal expected enum members. Continue allowing `__members__` inspection for
exact vocabulary, declaration-order, count, and alias evidence.

### Blanket suppression

Reject maintained evidence modules containing file-level
`# ruff: noqa: E501` unless a narrow accepted exception is documented. Do not
prohibit targeted, justified suppressions unrelated to formatting.

### Prose defects

Detect at least doubled terminal punctuation, missing required module headings,
missing evidence fields, known placeholder language, and module scope naming
object categories absent from the module. Mechanical checks cannot establish
complete prose-semantic accuracy.

### Equality completeness

When prose claims complete represented state, every public field, or
field-complete equality, require a structured field inventory showing that each
represented field is independently varied. If AST analysis is unreliable, emit
an advisory rather than a false deterministic PASS.

### Frozen-field completeness

When prose claims all fields are frozen, require semantic cases for every
declared public field or an explicit accepted alternative.

### Structural claim boundary

Every validator result must state that structural PASS does not establish:

- semantic cohesion;
- oracle independence;
- field completeness unless explicitly checked;
- numerical verification;
- scientific validation;
- UQ;
- provenance truth; or
- human acceptance.

## Proposed fixture families

Future fixtures should include paired valid and invalid examples for:

- concrete method surface / vague protocol surface;
- separate `__call__` and `__getitem__` / combined lookup owner;
- independent literal enum oracle / circular `__members__` oracle;
- separate unknown-value and wrong-type evidence / combined invalid partitions;
- ordinarily formatted module / blanket E501 suppression;
- field-complete equality / false complete-equality claim;
- field-complete frozen evidence / incomplete frozen-field claim; and
- specific evidence prose / generic generated prose.

Each invalid fixture should fail for one primary reason whenever practical.

## Advisory and human-review boundary

Deterministic tooling cannot fully determine whether:

- two partitions are semantically or scientifically cohesive;
- an oracle is genuinely independent;
- every relevant invariant has been identified;
- a test is proportionate;
- lifecycle prose is scientifically accurate; or
- a numerical tolerance is adequate.

These remain human-review responsibilities. Advisory findings should be labeled
as advisory and must not be converted into unsupported deterministic PASS claims.

## Relationship to P2

`P2-A02` supplies accepted examples of corrected enum and record evidence.
`P2-A03` exposed the same recurring pre-convention patterns and aggregate-check
friction. `P2-A04` supplies additional enum-ownership and declarative-coverage
observations. The current file-by-file human P2 audit remains authoritative.

This activated task does not retroactively rewrite historical reports, change an
already recorded P2 audit decision, or itself activate/accept P2. Current maintained
test modules are nevertheless required to migrate under this task; historical node
identity and evidence identifiers remain preserved through explicit one-to-one maps.

## Completion shape

Completion requires synchronized generic/live skill resources, controlled validator
fixtures with false-positive guards, an exact repository inventory, a fail-closed local
completion gate, migration of every current maintained module, focused software gates,
one consolidated independent review, and correction of any accepted bounded finding.
Structural PASS remains separate from semantic review and human acceptance.
