---
document_id: ksdft2effmass.harness.003.001.001
task_id: null
parent: ksdft2effmass.harness.003.001.000
status: proposed_inactive
sphinx: excluded
---

# Human Review Packet and Decision Workflow

> **Long-term proposal remains inactive.** The bounded packet-preparation API
> documented by the [initial round](ksdft2effmass.harness.003.001.000.md) is now
> implemented. This page still authorizes no expanded packet contract, storage
> format, CLI, decision record, checkpoint, runtime workflow, telemetry collection,
> correction, or successor activation.

## Purpose

Current human review occurs conversationally, often one source or test module at a
time. The relevant contract, diff, validation observations, and claim limitations
must be reconstructed manually. Large agent reports overload the review surface,
while human comments must be translated manually into bounded correction prompts.
Informal review is difficult to measure, resume, or compare, and it is easy to
conflate review, correction authorization, and final acceptance.

The proposed objective is:

> Provide a deterministic, one-item-at-a-time human-review workflow that prepares
> bounded review material, records the human response verbatim, authorizes only
> explicit correction scope, and keeps final task acceptance separate.

## Scope and terminology

| Term | Meaning |
|---|---|
| Human review | Human inspection and disposition of one bounded item |
| Review packet | Derived ordered collection of review items |
| Review item | One source, test, artifact, schema family, document, or decision surface |
| Review decision | Verbatim human disposition of one item |
| Correction authorization | Explicit bounded scope resulting from a correction request |
| Review completion | Every required item has a terminal disposition |
| Final acceptance | Separate human decision concerning the completed task or capability |

**Human review is not automatically final acceptance.** A reviewer approving one
file does not accept the entire task, scientific result, release, or successor
activation.

## Proposed DataObjects

The request, item, decision, progress, and summary shapes below remain candidate
immutable public contracts. The candidate expanded packet shape is not the current
implemented packet contract. Field names and types remain subject to a later accepted
architecture decision.

### `HumanReviewRequest`

```python
@dataclass(frozen=True, slots=True)
class HumanReviewRequest:
    review_id: str
    task_id: str
    starting_revision: str
    candidate_revision: str
    review_kind: HumanReviewKind
    paths: tuple[str, ...]
    authoritative_paths: tuple[str, ...]
```

The request would identify one review and task, bind immutable starting and
candidate Git revisions, preserve explicit ordered review paths, and name explicit
authoritative references. It would grant no repository discovery or mutation
authority.

### `HumanReviewItem`

```python
@dataclass(frozen=True, slots=True)
class HumanReviewItem:
    item_id: str
    path: str
    represented_surface: str
    change_summary: str
    contract_summary: str
    diff_text: str
    validation_observations: tuple[str, ...]
    claim_limitations: tuple[str, ...]
```

An item would be bounded and human-readable. It would contain only the material
needed to review one represented surface and would not embed an unbounded repository
diff or complete command log. Omitted or truncated material would be explicit.

### `HumanReviewPacket`

The following is a proposed future expansion, not the implemented first-slice
`HumanReviewPacket`. Adopting it would require a separately accepted public-contract
change.

```python
@dataclass(frozen=True, slots=True)
class HumanReviewPacket:
    review_id: str
    task_id: str
    starting_revision: str
    candidate_revision: str
    items: tuple[HumanReviewItem, ...]
```

Packet item ordering would be deterministic. The packet would be reconstructable
from immutable revisions, explicit paths, and declared authoritative inputs rather
than from ambient repository discovery.

### `HumanReviewDecision`

```python
@dataclass(frozen=True, slots=True)
class HumanReviewDecision:
    review_id: str
    item_id: str
    human_response: str
    disposition: HumanReviewDisposition
    correction_scope: str | None
    recorded_at: str
```

`human_response` would be preserved verbatim. Candidate dispositions are:

```text
APPROVE_ITEM
REQUEST_CORRECTION
QUESTION
DEFER_ITEM
REJECT_ITEM
```

There is deliberately no generic `PASS` disposition that could be mistaken for
whole-task acceptance. A later contract must define timestamp authority and
representation before `recorded_at` can become a public field.

### `HumanReviewProgressResult`

This proposed immutable ResultObject would report completed item IDs, pending item
IDs, the current item ID, whether correction is pending, whether review is complete,
and deterministically ordered structured conflicts.

### `HumanReviewSummary`

This proposed immutable ResultObject would contain the review identity, reviewed
revisions, ordered decisions, approved items, corrected items, deferred or rejected
items, unresolved questions, review-completion state, and an explicit statement that
final acceptance remains separate.

ResultObjects are semantically DataObjects and require no nominal base class solely
to express that role.

## Proposed ActionObjects

### `PrepareHumanReview`

A proposed stateless ActionObject would:

- receive explicit request inputs;
- observe only explicit revisions and paths through an authorized local adapter;
- create deterministically ordered review items;
- summarize relevant contracts and validation observations;
- bound diff size;
- record omitted or truncated material explicitly;
- avoid deciding whether a change is correct;
- avoid contacting subagents; and
- perform no repository mutation.

### `RecordHumanReviewDecision`

A proposed stateless ActionObject would accept one packet and one human decision,
verify matching review and item identities, preserve the human response verbatim,
validate disposition and correction-scope consistency, and return updated immutable
progress. It would not interpret ambiguous human prose, edit source, activate a
writer, resolve a checkpoint, or accept the full task. Human-intent interpretation,
when needed, remains a separate human-facing skill or root responsibility.

### `SummarizeHumanReview`

A proposed stateless ActionObject would combine the packet and recorded decisions,
detect missing or duplicate decisions, and return deterministic review status. It
would not convert approval of one or all items into task acceptance.

## One-item-at-a-time interaction

The maintained interface would present exactly one pending item at a time:

```text
Human review: item 4 of 7

Path:
python/tests/.../test__ExternalExecutionResult.py

Represented surface:
ExternalExecutionResult

Change:
Separated result behavior from the internal outcome alias.

Contract:
The public result owns immutable completed-execution state.
The internal alias remains unexported.

Validation:
97 focused cases passed.

Claim boundary:
Software verification only.

Disposition:
A. Approve this item
B. Request correction
C. Ask a question
D. Defer this item
E. Reject this item
```

The interface would wait for a human response before advancing and would not display
all review items simultaneously by default.

## Review modes

| Review kind | Primary human concern |
|---|---|
| `SOURCE_MODULE` | Public behavior, ownership, clarity, invariants |
| `CLASS_OWNED_TEST` | SUT, surface, oracle, cohesion, evidence limits |
| `ARTIFACT_OWNED_TEST` | Cross-surface agreement and integration ownership |
| `PUBLIC_API` | Exported names, defining modules, compatibility |
| `SCHEMA_AND_FIXTURE` | Wire contract and valid/invalid family agreement |
| `DOCUMENTATION` | Accuracy, authority, implemented/proposed distinction |
| `ARCHITECTURE_DECISION` | Alternatives, consequences, unresolved choices |
| `NUMERICAL_EVIDENCE` | Mathematics, units, scale, reference, tolerance |
| `SCIENTIFIC_VALIDATION_PROTOCOL` | Physical claim, reference evidence, adequacy |
| `UNCERTAINTY_QUANTIFICATION_PROTOCOL` | Uncertain inputs, propagation, reported uncertainty |

Each mode requires a distinct checklist. One universal checklist is not sufficient.

## Correction workflow

The proposed sequence is:

1. The human selects `REQUEST_CORRECTION`.
2. The human response is stored verbatim.
3. Bounded correction scope is recorded.
4. The correction becomes a separately authorized writer request.
5. Only explicitly named paths may change.
6. Focused validation is rerun.
7. The same item returns with old and corrected revisions.
8. The previous human decision remains preserved.
9. The human reviews the corrected item.
10. Review then proceeds to the next item.

A correction request would not automatically create a broad task. Example scope:

```text
Correct only python/src/example/result.py and its class-owned test module.
Preserve the public constructor and serialized field names. Run only the focused
result tests and return this review item against the corrected revision.
```

## Durable storage proposal

A first authorized implementation could use:

```text
.pi/human-reviews/<review-id>/
├── request.json
├── packet.json
├── decisions.json
└── summary.json
```

| Artifact | Authority |
|---|---|
| Request | Durable review scope |
| Packet | Derived review material |
| Decisions | Human-authoritative item dispositions |
| Summary | Derived review status |

Packets should remain reconstructable from immutable revisions, and giant copied
diffs should not be retained unnecessarily. Human decisions must preserve exact
text. Future SQLite storage may index events and decisions, but SQLite must not
replace the durable human-authority record without a separately accepted persistence
contract. This proposal does not design a SQLite schema or authorize these paths.

## Relationship to checkpoints

Review decisions concern individual items. Checkpoint decisions resolve genuine
human choices or final task acceptance. `ResolveCheckpointDecision` transforms an
already interpreted checkpoint decision; it does not interpret review prose.
Review-item approval must not silently resolve a checkpoint. A completed review may
become an input to a later acceptance checkpoint, but cannot substitute for it.

## Relationship to agents

The root or an authorized local adapter would prepare a packet. Durable writer agents
could receive explicit correction scope. Reviewer agents do not substitute for human
review, no subagent may present itself as the human, and human review does not require
multiple independent agent reviewers. The workflow should reduce giant final review
reports rather than introduce another reviewer layer.

## Telemetry integration

This proposal is related to the maintained
[harness telemetry research proposal](../research/agentic-development-case-study/agenticdevelopment_casestudy.00.md).
A future authorized integration could emit:

```text
HUMAN_REVIEW_STARTED
HUMAN_REVIEW_ITEM_PRESENTED
HUMAN_REVIEW_DECISION_RECORDED
HUMAN_REVIEW_QUESTION_ASKED
HUMAN_CORRECTION_REQUESTED
HUMAN_REVIEW_ITEM_APPROVED
HUMAN_REVIEW_COMPLETED
```

Candidate measurements are review time per item, question count, correction-request
count, decision reversals, files and logical surfaces reviewed, human-review surface,
implementation-review time, process-artifact-review time, and time from review
completion to final acceptance. Telemetry measures process behavior and does not
establish correctness. No telemetry event or metric is implemented here.

## Minimal pilot

A future pilot would:

> Review one class-owned test module, one item at a time.

It would use one explicit starting revision and one explicit candidate revision,
contain one test module, identify one public SUT, show a bounded diff and focused test
observations, state the evidence-class limitation, record one human disposition,
authorize at most one bounded correction, and stop without final task acceptance.

## Deferred work

The following remain explicitly deferred:

- Python implementation;
- CLI implementation;
- interactive terminal UI;
- web UI;
- SQLite storage;
- Pi runtime hooks;
- automatic agent dispatch;
- automatic source correction;
- automatic acceptance;
- complete-repository review;
- scientific review automation;
- external execution; and
- release integration.

## Risks and limitations

Review packets may omit important context, and summaries may bias human judgment.
Overly small items may fragment coherent behavior, while overly large items may
recreate information overload. Repeated human review may become ceremony. Derived
validation observations may be stale, and human approval may be mistaken for
scientific validation. Verbatim human decisions may contain sensitive content. Git
revisions do not capture uncommitted external state.

## Acceptance questions for a later architecture decision

Before implementation, a human-owned architecture decision must resolve:

1. Which review DataObjects belong to the generic extractable layer?
2. Which local adapter may observe Git diffs and repository files?
3. Should human decisions be serialized through the generic wire contract?
4. Which review artifacts are committed and which remain local runtime state?
5. How are sensitive human comments handled?
6. What maximum review-item size is appropriate?
7. Does correction authorization require a formal task record?
8. How does final acceptance consume a completed review summary?
9. What telemetry is collected during review?
10. Which single class-owned module should be the pilot?

These questions remain unanswered. This proposal must not silently choose among
them.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Program:** [Human review interface](ksdft2effmass.harness.003.000.000.md)
- **Parent:** [Initial human-review interface round](ksdft2effmass.harness.003.001.000.md)
- **Previous:** [Initial human-review interface round](ksdft2effmass.harness.003.001.000.md)
- **Next:** [Historical documentation index](ksdft2effmass.harness.090.000.000.md)
