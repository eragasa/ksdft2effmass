# Case-study protocol

## Design

This study is a prospective longitudinal embedded case study of
human-governed, specification-first agentic development in scientific software.
The unit of analysis is a repository milestone or control-plane intervention.
Embedded units are episodes such as operator-record refactoring, developer-tool
integration, validation-surface creation, and future cross-language conformance
work.

The protocol follows case-study reporting guidance from:

Per Runeson and Martin Höst, "Guidelines for conducting and reporting case study
research in software engineering," *Empirical Software Engineering* 14, 131-164
(2009). https://doi.org/10.1007/s10664-008-9102-8

The intended initial publication target is the fully peer-reviewed Software
Engineering track of *Computing in Science & Engineering*. This is an intended
target, not a claim of acceptance or publication.

## Evidence hierarchy

Repository evidence is interpreted under the project authority hierarchy:

1. explicit human decisions;
2. `AGENTS.md`;
3. accepted task and decision records;
4. public scientific specifications and schemas;
5. production source;
6. tests and validation fixtures;
7. human-reviewed documentation;
8. derived repository-intelligence artifacts such as Graphify graphs.

Derived artifacts may guide navigation and candidate discovery but must be
verified against authoritative files.

## Retrospective and prospective evidence

Episode `E00` is retrospective. It documents failures and corrections that
motivated this protocol using only repository evidence available after the fact.
Unknown dates, prompts, runtimes, token counts, model versions, commit IDs, or
validation results must be recorded as `unknown`, `null`, or `not recorded`.

Episode `E01` and later episodes are prospective. They should record checkpoints,
options, human resolutions, findings, corrective cycles, validation results, and
unresolved decisions as the work proceeds.

## Episode boundaries

An episode begins when a human-approved task or checkpoint identifies an
objective. An episode ends when its implementation status, verification status,
scientific-validation status, and human disposition are recorded. Human final
acceptance is distinct from software verification.

## Verification and validation boundary

The records distinguish:

- software verification: tests, static checks, schema checks, documentation
  builds, import smoke tests, and integration reviews;
- numerical verification: checks against numerical identities, tolerances,
  reference values, or convergence behavior;
- scientific validation: comparison with appropriate physical or computational
  references for a scientific claim.

A successful test suite, connected dependency graph, type checker, serializer
round trip, complete documentation page, or agreement between implementations
without an independent reference never automatically establishes scientific
validation.

## Graphify use

Graphify is optional and read-only with respect to production and scientific
artifacts. It may assist topology, dependency, impact, navigation, and task
selection analysis. Graphify output is derived, may be stale, and cannot approve
architecture, establish scientific validity, or launch implementation work.
Remote semantic processing and hooks require separate explicit human approval.
