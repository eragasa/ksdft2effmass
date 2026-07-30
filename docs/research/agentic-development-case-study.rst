Agentic development case study
==============================

The repository contains a prospective longitudinal embedded case study of
human-governed, specification-first agentic development in scientific software.
The study records how control-plane decisions, public validation surfaces,
role-separated agents, and human checkpoints affect development of
``ksdft2effmass``.

Objective
---------

The objective is to study a development process, not to validate a physical
model. Evidence is collected from repository records, public specifications,
fixtures, source, tests, documentation, integration reviews, and human decisions.

Research questions
------------------

The study asks:

1. How does the control plane convert scientific and numerical assumptions into
   public validation surfaces?
2. Which defects are found by object tests, integration review, specification
   fixtures, documentation builds, and human checkpoints?
3. Which uncertainties require human intervention?
4. Can a fresh session reconstruct accepted project state from repository
   evidence?
5. Can language-neutral specifications support independent Python and Rust
   implementations?

The propositions under examination are recorded in
``docs/research/agentic-development-case-study/research-questions.md``. They are
not conclusions already established.

Embedded episodes
-----------------

``E00`` records the completed operator-record refactor retrospectively as a
pilot. Its purpose is to document failures and corrections that motivated the
prospective protocol. Unknown prompts, model versions, token counts, runtimes,
and exact commits are recorded as unknown when repository evidence does not
establish them.

``E01`` records Graphify integration prospectively, including the correction
from assumed separate skill surfaces to the observed shared project-skill model:
``.agents/skills/graphify/`` is discovered by both Codex and pi in the validated
environment and intentionally shadows the same-named global pi fallback. It is
an infrastructure episode and is not evidence of scientific validity.

Evidence model
--------------

Machine-readable episode records use JSON so syntax can be checked with standard
Python tooling. The case-study records live under:

``docs/research/agentic-development-case-study/``

The episode schema is:

``docs/research/agentic-development-case-study/instruments/episode-record.schema.json``

The case register is:

``docs/research/agentic-development-case-study/case-register.json``

Scientific-validation boundary
------------------------------

The study distinguishes software verification, numerical verification, and
scientific validation. A successful test suite, type checker, connected graph,
serializer round trip, documentation build, or agreement between implementations
without an independent reference does not establish scientific validation.

Methodology and publication target
----------------------------------

The protocol follows the case-study reporting guidance of Per Runeson and Martin
Höst, "Guidelines for conducting and reporting case study research in software
engineering," *Empirical Software Engineering* 14, 131-164 (2009),
https://doi.org/10.1007/s10664-008-9102-8.

The intended initial publication target is the fully peer-reviewed Software
Engineering track of *Computing in Science & Engineering*. This is a target, not
a claim of submission, acceptance, or publication.

Current status
--------------

The case-study protocol and records are active. ``E00`` is retrospectively
recorded. ``E01`` implementation and verification are complete. Human final acceptance
was recorded on 2026-07-30, and ``E01`` is closed as accepted.
