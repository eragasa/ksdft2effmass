# arXiv readiness assessment

## Decision

The case study can be written and posted as an arXiv preprint. The most natural
primary category is `cs.SE` because the contribution concerns software-process
design, testing, debugging, development environments, agent coordination, and
empirical software-engineering evidence.

arXiv is a dissemination repository, not a peer-reviewed venue. The existing
intended journal target can remain unchanged.

## Current readiness

The repository is ready for manuscript drafting now because it already contains:

- an explicit longitudinal embedded-case-study protocol;
- research questions and propositions;
- one retrospective and two prospective episode records;
- a machine-readable episode schema and defect/severity instruments;
- accepted H0, H1, and H3 harness evidence;
- an active H2 episode with a protected contract conflict, human resolution,
  correction boundary, and independent review artifacts;
- explicit separation of software verification, numerical verification,
  scientific validation, and uncertainty quantification.

The repository is not yet ready for a strong quantitative claim that harness
overhead is offset by avoided rework or context loss. The current records do not
consistently consolidate active time, runtimes, token counts, dispatch counts,
or skill invocations across all episodes.

## Defensible arXiv versions

### Preliminary version

A preliminary manuscript may report:

- the protocol and repository evidence model;
- E00--E05;
- H2 as an explicitly incomplete in-progress episode;
- qualitative evidence that context loss is converted into durable coordination
  artifacts;
- event counts derived reproducibly from repository records;
- limitations caused by unavailable runtimes, prompts, and token counts.

It must not claim that the completed harness has demonstrated lower total cost.

### Stronger version

The preferred first arXiv version should wait until:

1. H2, H4, and H5 have reached recorded dispositions;
2. E03--E08 are schema-valid and evidence-linked;
3. at least one fresh-session reconstruction probe is recorded under a fixed
   protocol;
4. the central cross-episode table can be generated from versioned data;
5. the context-management instrument has been used prospectively;
6. a downstream scientific-software task has used the stabilized harness, if
   the paper claims amortization or reduced total cost.

The sixth condition is not required for a descriptive harness-development case
study. It is required for a stronger claim that harness construction pays for
itself during later domain work.

## Candidate title

> Context Preservation at Coordination Cost: A Longitudinal Case Study of
> Human-Governed Agentic Scientific Software Development

## Candidate central claim

> In long-horizon agentic scientific software development, bounded model
> context creates a tradeoff between local execution efficiency and global
> state preservation. Skills, role-separated subagents, checkpoints, and
> durable repository artifacts make task state inspectable and recoverable, but
> introduce measurable coordination overhead.

## Suggested manuscript structure

1. Introduction
2. Case and scientific-software context
3. Human-governed harness architecture
4. Case-study design and evidence hierarchy
5. Embedded development episodes
6. Context preservation and coordination overhead
7. Defect interception, correction, and recovery
8. Threats to validity
9. Reproducibility, AI disclosure, and research responsibility
10. Conclusions

## Central table

For each episode, report:

- task objective and status;
- agent roles and dispatches;
- handoffs and skills used;
- checkpoints and human decisions;
- corrective cycles;
- defects intercepted;
- context-loss or ambiguity events;
- recovery or fresh-session reconstruction result;
- software-verification status;
- human disposition;
- unavailable fields.

## Submission constraints

- Submit a complete scholarly manuscript, not a project note or repository
  advertisement.
- Use `cs.SE` as the primary category unless the finished paper changes focus.
- Expect possible endorsement requirements for a first submission or new
  category.
- Upload LaTeX source and all included figures; do not upload only a PDF that
  was generated from TeX.
- Choose the arXiv license deliberately and verify compatibility with the
  intended journal before submission.
- Keep all arXiv versions and claims consistent with the immutable repository
  evidence available at their cited revision.

## Official arXiv references

- Submission guidelines: <https://info.arxiv.org/help/submit/index.html>
- Category taxonomy: <https://arxiv.org/category_taxonomy>
- Endorsement: <https://info.arxiv.org/help/endorsement.html>
- License selection: <https://info.arxiv.org/help/license/index.html>
- TeX submission guidance: <https://info.arxiv.org/help/submit_tex.html>
