# Candidate and change control

## Candidate freeze gate

A campaign cannot enter `CANDIDATE_FROZEN` until its candidate record contains:

- campaign identifier and protocol version;
- exact protocol and candidate Git revisions;
- clean-worktree confirmation for the candidate revision;
- ordered composition root and all consumed source paths;
- SHA-256 manifest for consumed source and bibliography bytes;
- rendered artifact SHA-256 and page count;
- build commands, relevant tool versions, and build result;
- calculation or evidence indexes used during review;
- included and explicitly excluded appendices or supplements;
- intended audience and publication purpose;
- current evidence boundary and known unavailable evidence;
- assigned lead editor and initial reviewer roles; and
- human confirmation that this is the intended initial candidate.

A dirty worktree, branch name without commit identity, unretained source bytes,
or missing composition scope cannot satisfy the gate.

The candidate source revision and the later campaign-record revision need not be
the same commit. The campaign record binds the reviewed source bytes; updating
review records without changing those source bytes does not create a new
publication candidate.

## Required packet brief

Before human reading begins, the review orchestrator prepares a brief containing:

- exact candidate version, source files, and PDF page range;
- purpose and expected prerequisite knowledge;
- upstream and downstream packet dependencies;
- substantive claim inventory;
- definitions, conventions, units, state spaces, bases, gauges, energy
  references, and geometry assumptions used by the packet;
- numerical values and their evidence owners;
- citations and unresolved citation notes;
- known limitations, proposed work, and open decisions;
- mechanical-check evidence; and
- no more than five immediate questions for human attention.

The brief is a navigation aid. It does not permit the human primary reader to
skip the complete packet.

## Candidate revisions

Review never floats across changed bytes. Every revision candidate receives a
new candidate-version identifier and exact commit or retained-byte manifest.
The campaign records the diff from its predecessor and never overwrites the
predecessor's binding.

At minimum:

- a changed source reopens its packet until a human inspects the redline;
- a changed definition, convention, notation rule, bibliography entry, or
  shared equation reopens every dependent packet identified by the packet map;
- a changed numerical result reopens its evidence review and every prose claim
  that consumes it;
- a changed evidence-status statement reopens the evidence-boundary and
  conclusion reviews;
- a changed abstract, introduction, or conclusion triggers central-claim
  reconciliation; and
- a formatting-only change may be recorded as `NO_ACTION_REQUIRED` only after
  the diff and rendered effect are checked.

Automated impact analysis may recommend affected packets. A human lead editor
confirms the impact set. Uncertain impact reopens the potentially affected
packet.

## Source and artifact retention

A rendered PDF need not become a normal publication artifact in version
control, but the campaign must retain an accessible review artifact or approved
review attachment and record its SHA-256. Generated build directories do not
substitute for a source manifest or build record.

Historical candidate records remain immutable descriptions of the bytes they
bound. If a manifest or identity was wrong, add a correction record and do not
silently replace the original value.
