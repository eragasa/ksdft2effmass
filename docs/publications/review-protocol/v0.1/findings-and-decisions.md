# Findings, outcomes, and human decisions

## Finding dispositions

Every retained finding has exactly one disposition:

- `MUST_FIX` — an evidence-backed defect prevents the declared scope from
  meeting its definition of done;
- `HUMAN_DECISION_REQUIRED` — materially different defensible choices remain at
  a human-owned boundary;
- `SAFE_TO_DEFER` — a real issue does not block the declared scope and has a
  stated consequence and revisit condition;
- `NO_ACTION_REQUIRED` — the concern is resolved, stale, unsupported, purely
  informational, or outside scope.

Do not expose numeric severity, traffic-light color, or unexplained reviewer
shorthand as the campaign's disposition.

## Technical outcomes

Every packet synthesis and the final technical synthesis has exactly one
outcome:

- `CHANGES_REQUIRED` — at least one `MUST_FIX` finding remains;
- `REVIEW_INCONCLUSIVE` — missing, conflicting, or unavailable evidence
  prevents a reliable bounded conclusion;
- `NO_BLOCKING_FINDINGS` — the bounded technical review found no current
  blocker.

Derive the outcome from current evidence:

1. if any `MUST_FIX` finding remains, use `CHANGES_REQUIRED`;
2. otherwise, if missing, unavailable, or conflicting evidence prevents a
   reliable bounded conclusion, use `REVIEW_INCONCLUSIVE`; and
3. otherwise, use `NO_BLOCKING_FINDINGS`.

These outcomes do not alter scientific evidence status. In particular,
`NO_BLOCKING_FINDINGS` does not mean scientifically validated, accepted,
publishable, or authorized for submission.

## Finding record

Every finding records:

```text
Disposition: <one finding disposition>
Problem: <plain-language problem>
Evidence: <exact source, page, record, command, or contradiction>
Consequence: <effect if unchanged>
Next action: <correction, decision, revisit condition, or none>
```

It also records campaign, packet, candidate version, stable finding identifier,
review pass, author, dates, affected dependencies, and closure evidence. Use the
versioned [`finding template`](templates/finding.md).

Changing a finding's disposition does not erase its prior disposition. Record
the change and supporting evidence.

## Human decisions

A human-decision record states:

- the exact question;
- identified decision owner;
- available options and trade-offs;
- agent or reviewer recommendation with reasons;
- selected option and human rationale;
- affected findings and sources; and
- whether a later decision supersedes it.

A deterministic correction is not reclassified as a human decision merely to
transfer technical responsibility to the operator. Conversely, an agent may
recommend but may not select among genuine human-owned alternatives.

Use the versioned [`decision template`](templates/decision.md).

## Decision and closure rule

A packet cannot close while an applicable `HUMAN_DECISION_REQUIRED` finding
lacks a recorded human selection. Deferral is allowed only when new evidence
supports reclassification as `SAFE_TO_DEFER` with a consequence and revisit
condition, or when a recorded scope decision removes the matter from the
campaign.

No response is not a decision. Reviewer disagreement remains visible until a
named decision owner records a resolution or the packet remains inconclusive.
