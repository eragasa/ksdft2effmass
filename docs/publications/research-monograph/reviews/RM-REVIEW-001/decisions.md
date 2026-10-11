# RM-REVIEW-001 human decision register

## Status

Every decision below is `OPEN`. Recommendations are planning advice, not human
decisions. A named human decision owner must record the selected option and
rationale before the affected gate can close.

## RM-REVIEW-001-D01 — initial Appendix M scope

**Status:** `OPEN`

**Question:** Should the initial review candidate exclude the proposed Appendix
M or wait for a clean successor that includes it?

### Option A — review the committed A--L composition

- Benefit: the candidate can be frozen from an existing clean commit.
- Cost: the campaign will not review preliminary-silicon status material that
  may be intended for the current monograph.
- Consequence: adding Appendix M later requires a new candidate version,
  dependency impact review, and likely reopening `RM-P05`, `RM-P07`, and
  `RM-P10`.

### Option B — include Appendix M in a clean successor

- Benefit: the campaign reviews the intended current evidence-status narrative.
- Cost: candidate freeze waits until Appendix M and its composition, citations,
  evidence claims, and build are retained and independently checked.
- Consequence: no dirty or unretained Appendix M bytes may be treated as part of
  commit `2f30d7a3`.

**Recommendation:** Option B if Appendix M is intended to remain in the
monograph. Seal and validate it before freezing the review candidate rather than
reviewing a knowingly incomplete composition.

**Decision owner:** unassigned.

**Human selection and rationale:** pending.

## RM-REVIEW-001-D02 — one editorial tier or core-plus-appendix tiers

**Status:** `OPEN`

**Question:** Should every page receive the same narrative-polish standard, or
should the core narrative and technical appendices receive different declared
editorial treatment while remaining in one manuscript?

### Option A — one editorial standard

- Benefit: one uniform expectation is simple to state.
- Cost: it spends scarce human attention polishing technical reference material
  as if every appendix were part of the primary undergraduate progression.

### Option B — core narrative plus technical-reference tier

- Benefit: every page still receives correctness and evidence review, while
  undergraduate pacing and narrative intensity focus on the main text.
- Cost: the campaign must state which editorial expectations differ and verify
  that appendices remain navigable and correct.

**Recommendation:** Option B. Keep one source tree and one assembled manuscript,
but distinguish correctness/evidence requirements, which apply everywhere,
from primary-narrative pedagogy, which applies most strongly to the core.

**Decision owner:** unassigned.

**Human selection and rationale:** pending.

## RM-REVIEW-001-D03 — campaign definition of done

**Status:** `OPEN`

**Question:** Is the first campaign intended to establish an internally reviewed
working monograph or publication-ready copy?

### Option A — internally reviewed working monograph

- Benefit: matches the current pre-results evidence boundary and permits
  explicit proposed work and unresolved scientific questions.
- Cost: a later publication-readiness campaign remains necessary.

### Option B — publication-ready copy

- Benefit: aims directly at an external deliverable.
- Cost: requires a selected venue or form, external-review expectations,
  resolved scope, and evidence not currently represented as complete.

**Recommendation:** Option A. The first campaign should establish correctness,
coherence, provenance, bounded claims, and undergraduate accessibility without
misrepresenting incomplete material work as publication-ready evidence.

**Decision owner:** unassigned.

**Human selection and rationale:** pending.

## RM-REVIEW-001-D04 — human review panel and independence

**Status:** `OPEN`

**Question:** What minimum human panel is required before the campaign may
close?

### Option A — author-led review with ad hoc consultation

- Benefit: lower coordination cost.
- Cost: weak independence, higher risk of shared blind spots, and no guaranteed
  observation from the intended audience.

### Option B — role-based panel

Require at minimum:

- a lead editor;
- a primary reader for every page;
- an independent scientific reviewer for central physical claims;
- a mathematical/numerical reviewer for derivations and certificates; and
- an undergraduate audience reader for the foundational progression.

One person may fill multiple roles only when the overlap and loss of
independence are recorded.

- Benefit: the human-in-the-loop claim has concrete coverage and role meaning.
- Cost: greater scheduling and coordination effort.

**Recommendation:** Option B. If a required reviewer cannot be recruited, mark
the affected packet `REVIEW_INCONCLUSIVE` rather than weakening the gate after
the fact.

**Decision owner:** unassigned.

**Human selection and rationale:** pending.

## Assignment gate

After `D04` is recorded, add names, roles, independence notes, and packet
coverage to `packet-map.md`. Do not place private contact details in the
repository. Reviewer consent and any requested public attribution must be
handled explicitly.
