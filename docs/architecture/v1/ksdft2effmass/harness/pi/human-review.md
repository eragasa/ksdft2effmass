# Human-review objects in v1

## Boundary

`ksdft2effmass.harness.pi` exposes immutable explicit-input records for preparing one
bounded review packet and representing one decision already made by a human. These
objects do not conduct a review, interpret natural language, authenticate authority,
persist state, modify Git or checkpoints, activate work, or establish scientific
validity.

The public objects are:

- `HumanReviewTarget`;
- `HumanReviewObservation`;
- `HumanReviewFinding`;
- `HumanReviewPacket`;
- `HumanReviewPreparer`;
- `HumanReviewDecision`; and
- `HumanReviewDecisionRecorder`.

They are runtime DataObjects, ResultObjects, and ActionObjects. They are not members of
the generic serialized wire-record union and define no persistence contract.

## Review target

`HumanReviewTarget` identifies exactly one bounded review subject:

| Field | Contract |
|---|---|
| `review_id` | Stable Harness identifier |
| `revision` | Exact lowercase 40-character Git object name supplied by the caller |
| `represented_subject` | Nonempty human-readable subject |
| `paths` | Nonempty ordered tuple of unique normalized repository-relative paths |
| `evidence_class` | `software_verification`, `numerical_verification`, `scientific_validation`, `uncertainty_quantification`, or `not_applicable` |
| `contract_references` | Ordered unique repository-relative contract paths |

Construction validates lexical values only. It does not inspect Git or the filesystem.

## Observations and candidate findings

`HumanReviewObservation` records one deterministic observation. Its status is
`passed`, `failed`, `indeterminate`, or `not_run`. It retains an identifier, check
name, substantive summary, optional target path, and optional detail. An observation
is not a human judgment and does not by itself establish numerical or scientific
correctness.

`HumanReviewFinding` records one candidate issue for human disposition. Severity is
`blocker`, `high`, `medium`, `low`, or `advisory`. A finding retains its identifier,
statement, optional target path, unique supporting-observation identifiers, and one
nonempty unresolved limitation. Packet preparation does not accept the finding or
recommend a disposition.

## Packet preparation

`HumanReviewPreparer.execute` receives one target and explicit tuples of observations,
findings, and limitations. It:

1. rejects duplicate observation or finding identifiers;
2. requires observation and finding paths to belong to the target;
3. requires every supporting observation reference to resolve;
4. sorts observations and findings by identifier and limitations lexically; and
5. returns one immutable `HumanReviewPacket`.

The packet status is `blocked_by_failed_observation` when any observation failed;
otherwise it is `ready_for_human_review`. `indeterminate` and `not_run` do not become
`failed` implicitly. Packet status is preparation state, not human acceptance.

`HumanReviewPacket` retains the exact target, canonical observations, canonical
findings, canonical limitations, and derived status. It stores no recommendation,
correction authorization, persistence handle, or workflow state.

## Decision representation

`HumanReviewDecisionRecorder.execute` accepts an already prepared packet, the exact
human response, an explicit normalized disposition, and explicit authorized scope. It
first verifies that the packet equals the canonical result of
`HumanReviewPreparer`.

The dispositions are:

| Disposition | Scope rule |
|---|---|
| `accepted` | Scope must be empty; packet must be ready |
| `bounded_correction` | At least one unique nonempty scope statement is required |
| `deferred` | Scope must be empty |
| `rejected` | Scope must be empty |

The resulting immutable `HumanReviewDecision` preserves the complete packet and exact
human response. A ready packet may be accepted while advisory findings or limitations
remain. A packet blocked by a failed observation cannot be accepted.

The recorder performs no text-to-disposition inference, filesystem access, Git
operation, checkpoint mutation, subprocess execution, clock access, networking,
database persistence, correction, or successor activation. The caller remains
responsible for establishing that the response and disposition have appropriate human
authority.

## Claim boundary

These objects provide deterministic software representation only. They do not replace
the direct human decision, resolve an existing checkpoint automatically, authorize a
protected action, classify scientific evidence, or provide final human acceptance.
