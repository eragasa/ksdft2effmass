# Human-in-the-loop publication review protocol

## Purpose

This directory owns the reusable process for human-in-the-loop review of
publication working files in this repository. The process makes review inputs,
roles, findings, decisions, revisions, and closure auditable without treating
software agents or mechanical checks as substitutes for qualified human
judgment.

A review campaign applies the protocol to one exact publication candidate. A
campaign record belongs with that publication; it does not belong in this
reusable protocol directory.

## Status and authority

[`v0.1/`](v0.1/README.md) is the proposed version 0.1 protocol. It becomes the
governing protocol for a campaign only when that campaign names the protocol
version and exact Git revision it uses.

The protocol governs publication-review records only. It does not redefine
scientific specifications, calculation acceptance, proof status, software
verification, scientific validation, uncertainty quantification, submission,
publication, release, or human authorization. Those remain with their existing
owners.

A completed campaign means that the declared review process finished for the
bound candidate. It does not by itself mean that the publication is correct,
validated, accepted, publishable, submitted, or released.

## Versions

| Version | Status | Notes |
|---|---|---|
| [`v0.1`](v0.1/README.md) | proposed | Initial reusable protocol and campaign templates; no completed campaign yet |

A later version receives a new directory. Existing campaign bindings continue
to name the version and Git revision they actually used.

## Reusable surfaces

- [`v0.1/`](v0.1/README.md) contains the versioned protocol, component rules,
  and templates.
- [`v0.1/templates/candidate.md`](v0.1/templates/candidate.md) binds a campaign
  to exact source and rendered artifacts.
- [`v0.1/templates/packet.md`](v0.1/templates/packet.md) records one bounded
  review packet.
- [`v0.1/templates/finding.md`](v0.1/templates/finding.md) records an
  evidence-backed finding and its disposition.
- [`v0.1/templates/decision.md`](v0.1/templates/decision.md) records a genuine
  human-owned choice without disguising it as technical review.
- [`v0.1/templates/closure.md`](v0.1/templates/closure.md) records
  whole-publication closure without implying publication acceptance.

Templates state required information. Campaigns may add publication-specific
fields, but they must not remove required fields or weaken the protocol's human
gates.

## Repeatability boundary

The process is repeatable because each campaign records the same required
inputs, transitions, review passes, decision points, and outputs. Human
scientific and editorial judgments are not expected to be deterministic.
Different qualified reviewers may reach different conclusions; the campaign
must preserve the disagreement, evidence, and resolution rather than erase it.

## First application

The initial planned application is
[`RM-REVIEW-001`](../research-monograph/reviews/RM-REVIEW-001/README.md). Its
planning records do not claim that review has started or that any monograph
content has passed human review.
