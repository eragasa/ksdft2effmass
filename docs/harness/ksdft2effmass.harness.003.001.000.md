---
document_id: ksdft2effmass.harness.003.001.000
task_id: null
parent: ksdft2effmass.harness.003.000.000
status: proposed
sphinx: excluded
---

# Initial human-review interface round

> **Proposed and inactive.** This filesystem-first pilot is not implemented and
> authorizes no review execution, correction, checkpoint decision, or successor.

The proposed pilot formalizes the existing one-module-at-a-time human audit process.
Its default unit is one coherent source module, one class-owned test module, or one
artifact-owned integration module. The purpose is to stabilize a compact review
contract before deciding whether normalized SQLite storage is appropriate.

## Proposed review unit

One review unit contains:

- a review identifier;
- the exact repository revision;
- explicitly supplied source and test paths;
- the represented public object or artifact;
- the applicable contract and evidence class;
- deterministic checks actually run;
- structured observations;
- human findings;
- unresolved limitations;
- the human disposition; and
- any separately authorized correction.

## Proposed workflow

1. Select one coherent source module, class-owned test module, or artifact-owned
   integration module.
2. Capture the exact revision and explicit paths.
3. Run only applicable deterministic inspection Actions.
4. Produce one compact review packet.
5. Present source, tests, observations, and limitations to the human.
6. Record the human’s critique and disposition verbatim.
7. Stop unless correction or continuation is separately authorized.

## Rejected behavior

The pilot explicitly rejects:

- repository-wide review sweeps as the default unit;
- automatic PASS from coverage, Ruff, mypy, or pytest alone;
- repeated reviewer spawning;
- review voting;
- replay loops;
- hidden path discovery;
- hard-coded test counts;
- automatic checkpoint resolution;
- automatic successor activation; and
- scientific-validation or uncertainty-quantification claims when those evidence
  classes do not apply.

## Candidate deterministic interfaces

Future design may consider these names, but this proposal implements none of them:

```text
HumanReviewTarget
HumanReviewObservation
HumanReviewFinding
HumanReviewPacket
HumanReviewDecision
PrepareHumanReviewPacket
RecordHumanReviewDecision
```

Targets, observations, and findings would be immutable DataObjects. Packets and
decisions would be immutable ResultObjects where their represented meaning warrants
that role. Preparation and recording operations would be stateless ActionObjects
with explicit inputs and effects. No nominal base class should be introduced solely
to label these roles.

## Candidate telemetry

A future authorized pilot could measure:

- elapsed review time;
- deterministic command count;
- LLM review assignment count;
- duplicate review count;
- files inspected;
- findings by severity;
- correction cycles;
- human reversals or remands;
- review-packet size;
- process-ceremony fraction; and
- control-plane amplification.

These are proposed measurements, not implemented metrics. They do not independently
establish review quality, scientific validity, or human acceptance.

## Authority and stop boundary

Deterministic observations remain distinct from LLM critique and human decisions.
Only the human may dispose of findings or authorize correction and continuation.
Duplicate reviews are not independent evidence. The pilot stops after recording the
human response unless separate authority permits another action.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [Human review interface](ksdft2effmass.harness.003.000.000.md)
- **Previous:** [Human review interface](ksdft2effmass.harness.003.000.000.md)
- **Next:** [Historical documentation index](ksdft2effmass.harness.090.000.000.md)
