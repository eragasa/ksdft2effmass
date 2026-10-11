# Closure and retention

## Cross-packet review

After packet review, the campaign performs cross-cutting audits for:

- notation and definition consistency;
- logical and pedagogical dependency order;
- duplicate or contradictory claims;
- citation suitability and literature coverage;
- numerical, figure, and table provenance;
- scientific evidence status;
- current versus proposed software capability;
- abstract, introduction, and conclusion agreement; and
- unresolved human decisions.

At least one identified human reads the assembled final candidate sequentially.
This whole-publication reader may rely on specialist findings but cannot be
replaced by packet-status aggregation.

The campaign also performs an adversarial central-claims review that attempts
to falsify the manuscript's principal conclusions and detect overstatement.

## Closure gate

A campaign may enter `CLOSED` only when:

- the final candidate has an exact immutable binding;
- every substantive page has primary-reader coverage;
- every packet has a recorded technical outcome;
- no `MUST_FIX` finding remains open;
- unresolved evidence produces an explicit `REVIEW_INCONCLUSIVE` outcome rather
  than an implicit pass;
- every `HUMAN_DECISION_REQUIRED` finding has a recorded human selection;
  deferral is permitted only when current evidence supports reclassification as
  `SAFE_TO_DEFER` with a revisit condition or a recorded scope decision removes
  it from the campaign;
- required redlines have human outcome confirmation;
- cross-packet and adversarial reviews are recorded;
- the whole-publication reader has completed the final sequential read;
- declared deterministic checks pass or their failures are retained as open
  findings; and
- the closure record states residual limitations and nonclaims.

Closure requires a human lead editor's confirmation of the observable assembled
candidate. It does not authorize commit, push, external computation,
submission, publication, release, or a scientific-status change.

Use the versioned [`closure template`](templates/closure.md).

## Retention and supersession

Campaign records are retained with the publication. A closed campaign is not
rewritten to describe a later manuscript. Corrections to the historical record
are additive, identify the original error, and do not change the candidate that
was reviewed.

A later campaign names the prior campaign it supersedes and explains why a new
review was required; the earlier closure record need not be edited to point
forward.

Review conversations in external systems may support collaboration, but the
repository campaign retains the decisions, evidence references, and closure
needed to understand the outcome without depending on an external discussion
service.

## Authority boundary

Campaign closure does not by itself establish:

- correctness beyond the reviewed scope;
- scientific validation or uncertainty quantification;
- independent reproduction not explicitly recorded;
- acceptance of a calculation, scientific setting, or software capability;
- submission, acceptance, publication, or release; or
- authorization for computation, external transmission, or another protected
  action.
