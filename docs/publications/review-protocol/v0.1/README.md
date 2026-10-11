# Human-in-the-loop publication review protocol, version 0.1

## Status

Version `0.1` is the initial proposed protocol. No campaign has completed it.
A campaign adopts this version only by recording `v0.1` and the exact Git
revision containing the protocol bytes it used.

## Objective

This protocol defines a repeatable, auditable process for reviewing a
repository publication with software-agent assistance and explicit human
control. It is designed for long technical manuscripts whose mathematical,
scientific, computational, evidentiary, pedagogical, and editorial claims
cannot be responsibly collapsed into one undifferentiated approval.

The protocol has two complementary goals:

1. use deterministic tools and software agents to make review tractable; and
2. reserve scientific interpretation, audience outcomes, genuine value choices,
   and publication decisions for identified humans.

No campaign may claim human-in-the-loop review merely because a human was able
to interrupt an automated process. Humans must receive bounded material,
inspect concrete evidence, answer concrete questions, and confirm the resulting
revision.

## Protocol documents

- [`lifecycle-and-roles.md`](lifecycle-and-roles.md) defines campaign and packet
  states, human and agent roles, and the packet cycle.
- [`candidate-control.md`](candidate-control.md) defines exact candidate
  binding, packet briefs, revision candidates, and invalidation.
- [`review-passes.md`](review-passes.md) defines the five required review
  perspectives.
- [`findings-and-decisions.md`](findings-and-decisions.md) defines finding
  dispositions, technical outcomes, and human-decision records.
- [`closure-and-retention.md`](closure-and-retention.md) defines cross-packet
  review, closure, retention, and supersession.
- [`templates/`](templates/) contains the required campaign record shapes.

These files together constitute version `0.1`; the README alone is not the full
protocol.

## Terms

**Protocol**
: This reusable process at a named version and Git revision.

**Campaign**
: One retained application of the protocol to a publication.

**Candidate version**
: An immutable source revision, source manifest, rendered artifact, and build
  record reviewed during a campaign. A campaign may contain an initial
  candidate and one or more revision candidates, but none may be overwritten.

**Packet**
: A bounded, reviewable subset of the candidate with declared dependencies and
  assigned human roles.

**Pass**
: One declared review perspective, such as mathematical correctness or
  undergraduate readability. Passing one perspective does not pass another.

**Finding**
: An evidence-backed problem, decision, deferral, or dismissed concern tied to
  exact candidate content.

**Human decision**
: A choice among materially different defensible options at a human-owned
  boundary.

**Outcome confirmation**
: A human judgment about an inspectable result that cannot be established by a
  mechanical check, such as whether a revised derivation is understandable to
  the intended audience.

**Closure**
: Completion of this protocol's declared gates for the final candidate. Closure
  is not submission, acceptance, scientific validation, release, or publication.

## Non-negotiable invariants

1. **Exact candidate binding.** Review attaches to immutable bytes, not a moving
   branch or dirty worktree.
2. **Complete human coverage.** At least one identified human primary reader
   reads every substantive page in each packet.
3. **Qualified specialist coverage.** Claims requiring specialist mathematical,
   physical, numerical, computational, or literature judgment are assigned to
   a human with the recorded role. If that coverage is unavailable, the result
   is inconclusive rather than silently accepted.
4. **No approval by silence.** Missing human feedback leaves a gate open.
5. **Concrete human questions.** Agents give evidence and a recommendation
   before asking for a decision or outcome confirmation. Humans are not used as
   a generic fallback technical reviewer.
6. **Visible revisions.** A human inspects the relevant redline after changes.
7. **Change invalidation.** Review of earlier bytes does not automatically carry
   over to changed bytes.
8. **Independent dimensions.** Mechanical verification, technical review,
   scientific evidence status, human editorial decisions, and publication
   authorization remain separate.
9. **No authority escalation.** Campaign records do not authorize protected
   calculations, external transmission, submission, release, publication, or
   changes to scientific settings.
10. **Retained disagreement.** Material reviewer disagreement is recorded with
    its evidence and resolution or remains explicitly unresolved.

## Repeatability boundary

The process is repeatable because every campaign binds the same required kinds
of inputs, roles, transitions, passes, decisions, revisions, and outputs. Human
scientific and editorial judgments are not deterministic. Different qualified
reviewers may reach different conclusions; the campaign preserves the
disagreement, evidence, and resolution rather than erasing it.

A campaign may extend the templates for its publication, but it must not remove
required fields, weaken a human gate, or imply that an outcome from one review
dimension establishes another.

## Minimum repeat procedure

To apply version `0.1`:

1. create a publication-owned campaign directory from the versioned templates;
2. assign a unique campaign identifier;
3. bind `v0.1` and its exact Git revision;
4. define purpose, audience, definition of done, packets, dependencies, and
   human roles;
5. freeze the initial candidate under [`candidate-control.md`](candidate-control.md);
6. execute every applicable pass and the human packet cycle;
7. retain each revision candidate and change-impact decision;
8. perform cross-packet, adversarial, and whole-publication review; and
9. close or report the campaign inconclusive without overstating what review
   establishes.

The first planned application is
[`RM-REVIEW-001`](../../research-monograph/reviews/RM-REVIEW-001/README.md).
Planning records do not establish that review has begun.
