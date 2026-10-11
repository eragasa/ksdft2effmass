# Lifecycle and roles

## Human roles

Every role is filled by an identified human or agent for each packet. One human
may fill more than one role, but the campaign records that fact. A claim of
independent review requires a different qualified human from the author or
producer of the reviewed claim.

**Lead editor**
: Owns the intended argument, scope, structure, and integration of accepted
  revisions. The lead editor does not acquire authority over scientific or
  computational records owned elsewhere.

**Primary reader**
: Reads the complete packet and confirms that its findings cover the material
  actually read.

**Scientific reviewer**
: Reviews physical interpretation, assumptions, literature support, novelty
  boundaries, and the distinction between synthetic and material evidence.

**Mathematical and numerical reviewer**
: Reviews derivations, domains, state-space identifications, estimates,
  certificates, numerical reasoning, and declared tolerances.

**Audience reader**
: Judges whether the material is understandable to the declared audience. An
  undergraduate audience reader is not asked to certify specialist correctness.

**Human decision owner**
: Selects among genuine alternatives at an explicitly assigned boundary.

## Agent roles

**Review orchestrator**
: Prepares packets, inventories claims, checks evidence, synthesizes findings,
  recommends dispositions, tracks gates, and reports uncertainty.

**Mechanical verifier**
: Runs deterministic builds, linters, source-graph checks, citation checks,
  provenance checks, and other declared commands.

An agent may not satisfy any human role, close a human gate, infer acceptance
from silence, or represent its own recommendation as a human decision.

## Campaign lifecycle

Campaign lifecycle is separate from finding disposition and technical outcome.
The allowed states are:

- `PLANNING` — scope, roles, and candidate are not yet frozen;
- `CANDIDATE_FROZEN` — initial immutable candidate and protocol binding exist;
- `PACKET_REVIEW_ACTIVE` — one or more packets are undergoing human review;
- `REVISION_ACTIVE` — agreed revisions are being prepared and checked;
- `CLOSURE_REVIEW` — packet gates are complete and whole-publication synthesis
  is active;
- `CLOSED` — the final candidate and closure record satisfy this protocol;
- `SUPERSEDED` — a later campaign replaces this one without rewriting it.

The normal transition is:

```text
PLANNING
  -> CANDIDATE_FROZEN
  -> PACKET_REVIEW_ACTIVE
  <-> REVISION_ACTIVE
  -> CLOSURE_REVIEW
  -> CLOSED
```

A campaign may return from `CLOSURE_REVIEW` to `REVISION_ACTIVE`. A closed
campaign is never edited to cover a new candidate; a new campaign supersedes it.

## Packet lifecycle

Packet states are:

- `PLANNED`;
- `BRIEF_READY`;
- `HUMAN_READING`;
- `FINDINGS_SYNTHESIS`;
- `REVISION`;
- `OUTCOME_CONFIRMATION`;
- `CLOSED`;
- `REOPENED`.

A packet cannot enter `HUMAN_READING` without the required brief, exact candidate
version, rendered page range, and role assignments. It cannot enter `CLOSED`
solely on an agent report.

## Human-in-the-loop packet cycle

Each packet follows this order:

1. The agent prepares the brief and provisional claim inventory.
2. A human primary reader reads the complete packet and records annotations.
3. Assigned human specialists complete their passes.
4. The agent checks evidence, deduplicates findings, recommends dispositions,
   and identifies conflicts or unavailable evidence.
5. Human decision owners resolve `HUMAN_DECISION_REQUIRED` findings or leave
   the packet open.
6. The agent prepares only agreed deterministic corrections and
   decision-conforming revisions.
7. Mechanical checks run against the revision candidate.
8. Humans inspect the relevant redline and answer concrete outcome questions.
9. The orchestrator records the packet outcome and either closes or reopens the
   packet.

Packet closure requires the primary reader's coverage confirmation and human
confirmation of any revised scientific interpretation or audience outcome.

## Human record boundaries

The campaign records a stable reviewer identity, role, coverage, date, and any
relevant independence limitation. It does not store private contact details,
credentials, or restricted personal information. Public attribution and any
external reviewer communication require the reviewer's consent and applicable
project authority.
