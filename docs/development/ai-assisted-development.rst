AI-assisted development
=======================

``ksdft2effmass`` permits AI-assisted development as a provisional aid for
reading files, proposing changes, writing tests, drafting documentation, and
coordinating control-plane work. Human maintainers remain responsible for
scientific meaning, architectural decisions, public API acceptance, validation
claims, releases, and publication statements.

Scope of AI use
---------------

Agents may help with repository navigation, implementation drafts, review,
validation commands, and documentation. Agent output is not automatically
reviewed, validated, or release-ready. The repository distinguishes generated
artifacts, verified software artifacts, and scientifically validated results.

Generated, verified, and scientifically validated artifacts
-----------------------------------------------------------

Generated artifacts are produced by an agent or tool and must be treated as
provisional. Software verification includes tests, type checks, linters, schema
checks, public-import smoke tests, and documentation builds. Scientific
validation requires comparison with appropriate physical or computational
references under explicit acceptance criteria. Passing software checks alone does
not validate a represented Hamiltonian, a reduction model, or a scientific
claim.

Human review and acceptance
---------------------------

Human checkpoints are required for scientific conventions, mathematical meaning,
public APIs, schema semantics, architecture, compatibility, scope, release
status, and unresolved validation failures. A task is not finally accepted until
the human acceptance record says so.

Provenance practices
--------------------

Durable task records should identify the objective, final status, human
acceptance, artifacts produced, public API or scientific result, validation
evidence, known limitations, unresolved decisions, dependencies now satisfied,
and explicitly deferred work. Records should link to evidence instead of
duplicating long implementation reports.

Unpublished research and external services
------------------------------------------

Unpublished research material, private calculations, credentials, and restricted
data must not be transmitted externally without explicit human approval. API keys
must not be configured or stored silently. Remote semantic-processing backends,
including Gemini, OpenAI-compatible services, or other external model services,
require explicit approval before use.

Release and publication disclosure
----------------------------------

Development work must not be described as reviewed, released, or scientifically
validated unless the human PI authorizes that status. Formal releases, DOI
updates, tags, publications, and claims about scientific results follow the
repository release and scientific-integrity policies in ``AGENTS.md``.

Limitations
-----------

AI agents can miss context, hallucinate references, conflate software
verification with scientific validation, or overfit to recent conversation
history. Repository evidence and human decisions remain authoritative.
