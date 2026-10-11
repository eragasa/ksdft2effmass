# RM-REVIEW-001 — first human-in-the-loop monograph review

## Campaign state

**State:** `PLANNING`

No publication candidate is frozen, no human reviewer has been assigned, no
packet has entered human reading, and no review outcome exists. This directory
is a review plan, not evidence that the monograph has been reviewed.

## Purpose

This campaign will apply the reusable human-in-the-loop publication-review
protocol to the research monograph in bounded packets. It is intended to make a
large technical manuscript reviewable without allowing automated checks,
software-agent recommendations, or human silence to stand in for qualified
human judgment.

The proposed first outcome is an internally reviewed working monograph with an
explicit evidence boundary. Publication readiness, submission, scientific
validation, and release remain separate later decisions.

## Protocol binding

- Proposed protocol: [`v0.1`](../../../review-protocol/v0.1/README.md)
- Protocol Git revision: **pending**
- Binding state: **not bound**

The campaign cannot enter `CANDIDATE_FROZEN` until the protocol and campaign
plan exist at exact retained Git revisions.

## Candidate planning

[`candidate.md`](candidate.md) records commit `2f30d7a3` as a possible baseline,
not as a frozen candidate. That revision composes Appendices A--L and does not
contain the currently proposed Appendix M in its manuscript composition. The
human decision about Appendix M must precede candidate freeze.

## Packet plan

[`packet-map.md`](packet-map.md) divides the manuscript into ten bounded review
packets and records cross-packet dependencies. The packets separate:

1. computational foundations;
2. periodic geometry, discretization, and projection;
3. periodic reduction and evidence vocabulary;
4. model adequacy and certificates;
5. the bulk-silicon program;
6. the doped-silicon program;
7. the proof program and global claims; and
8. three appendix groups.

Every substantive page must receive an identified human primary reader. Each
applicable specialist pass must have a named qualified human or remain
`REVIEW_INCONCLUSIVE`.

## Human gates

The campaign requires humans to:

- confirm the intended candidate, audience, and definition of done;
- read every substantive page assigned to them;
- review specialist claims within their recorded qualifications;
- resolve genuine scientific, structural, and editorial choices;
- inspect relevant revision redlines;
- confirm observable scientific-interpretation and audience outcomes;
- conduct a final sequential whole-manuscript read; and
- decide separately whether any later submission or publication action is
  appropriate.

A human is not asked to approve unfamiliar technical details without evidence.
The review orchestrator must provide a recommendation, its basis, uncertainty,
and a concrete question.

## Agent and mechanical support

Agents may prepare packet briefs, inventory claims, trace evidence, compare
cross-references, test bounded calculations, synthesize findings, propose
corrections, and run deterministic checks. Agents may not fill human roles,
close human gates, accept claims by silence, or infer publication authority.

## Planning records

- [`candidate.md`](candidate.md) — proposed baseline and unresolved freeze gate;
- [`packet-map.md`](packet-map.md) — packet boundaries and dependencies;
- [`claim-ledger.md`](claim-ledger.md) — preliminary central-claim inventory;
- [`decisions.md`](decisions.md) — open human-owned planning decisions;
- [`packets/README.md`](packets/README.md) — packet-record creation and naming;
- [`closure.md`](closure.md) — inactive closure gate and eventual required
  evidence.

## Immediate next gate

Before review begins, identified humans must record decisions about:

1. whether Appendix M enters the initial candidate;
2. whether the core narrative and technical appendices receive distinct
   editorial treatment within one retained manuscript;
3. the campaign's definition of done;
4. the named lead editor, primary readers, specialists, and undergraduate
   audience reader; and
5. the exact clean candidate commit and rendered artifact.

Until then, all packet states remain `PLANNED`.
