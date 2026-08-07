# TEST-EVIDENCE-CONVENTIONS-2 — Prevent recurring mixed-surface and generated-prose defects in Python test evidence

Status: `proposed_inactive` except for one bounded implemented capability

```text
bounded_implemented_capability: module-local named literal pytest.param inventory resolution
remaining_backlog: proposed_inactive
activation_authorized_for_remaining_backlog: false
implementation_authorized_for_remaining_backlog: false
```

The current human instruction titled **TEST-EVIDENCE-CONVENTIONS-2 — Bounded
named-parameter-inventory validator correction** authorizes only that capability. It
does not activate the other deterministic rules or workflow-automation proposals
below, and it does not activate P2-A09.

The concise proposal record is
[`../evidence/harness-backlog/TEST-EVIDENCE-CONVENTIONS-2.json`](../evidence/harness-backlog/TEST-EVIDENCE-CONVENTIONS-2.json).

## Purpose and authority boundary

Except for the bounded named-inventory capability recorded above, this inactive
backlog item records possible future improvements to the reusable Python test-evidence
capability. The bounded slice changes only static module-local named-inventory
resolution and its canonical/live convention text; it does not activate another rule,
workflow automation, or the P2 audit.

A separately recorded human activation is still required before any further change to:

- `harness/pi/skills/develop-python-test-evidence/`;
- `harness/pi/validation/validate_python_test_evidence.py`;
- `harness/pi/fixtures/python-test-evidence/`; or
- the corresponding live local route.

This proposal is not a prerequisite for P2, P3, or any scientific workflow. It
has no writers, reviewers, activation record, completion evidence, or checkpoint.

## Recurring defects

The human P2 module audit repeatedly found:

1. vague surfaces such as `test_protocol__...`, `test_behavior__...`, and
   `test_contract__...`;
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

## Candidate deterministic rules

### Concrete public surfaces

Reject known vague first surface segments:

```text
protocol
behavior
contract
general
misc
```

Accept explicit surfaces such as `constructor`, `field`, `property`,
`method__call`, `method__getitem`, `method__eq`, `method__hash`,
`method__repr`, `method__execute`, `method__serialize`, and
`method__deserialize`. This must not become a universal closed list: explicit
public method surfaces remain extensible.

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

This proposal, apart from the bounded implemented named-inventory capability:

- does not retroactively invalidate cleared items;
- does not change P2 criteria during the active audit;
- does not modify any current P2 test or evidence decision;
- does not activate, advance, or clear any P2 audit item; and
- may be implemented further only after separate human activation.

## Proposed future completion shape

If activated later, implementation should update the generic skill, validator,
and focused fixture family together; add deterministic tests for every new
finding; distinguish errors from advisories; preserve the structural claim
boundary; and obtain separate authorization before synchronizing any live local
route. Those are planning notes, not present authority.
