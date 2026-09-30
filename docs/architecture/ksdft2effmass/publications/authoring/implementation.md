# `authoring` implementation

## One action path

`EvidenceGroundedManuscriptAuthor.execute(request, current_revision_id, inference)` is
the only proposal-composition path. `prompt_for(request)` exposes the deterministic
prompt contract but performs no inference and admits no proposal.

```mermaid
sequenceDiagram
    participant Caller
    participant Author as EvidenceGroundedManuscriptAuthor
    participant Port as LocalManuscriptInferencePort

    Caller->>Author: execute(request, current_revision_id, port)
    Author->>Author: stale/evidence/key/warning checks
    alt preflight rejected
        Author-->>Caller: failed-closed ManuscriptAuthoringResult
    else preflight admitted
        Author->>Author: deterministic prompt_for(request)
        Author->>Port: infer(ManuscriptInferenceRequest)
        Port-->>Author: ManuscriptInferenceResponse
        Author->>Author: correlation/bounds/evidence/citation checks
        Author-->>Caller: proposal-ready or failed-closed result
    end
```

## Package decomposition

The public import `ksdft2effmass.publications.authoring` is an intentional facade over
seven defining modules—`statuses`, `target`, `evidence`, `contracts`, `inference`,
`proposal`, and `author`—plus the owner-specific `adapters` package. The root
`ksdft2effmass.publications` facade reexports the
same objects. Neither facade defines a compatibility class or implementation path.

## Deterministic identities

Canonical identity payloads use UTF-8 JSON with sorted keys and compact separators,
then lowercase SHA-256. Prefixes distinguish represented identity classes. Target
revision identity binds root-relative path, external Git blob SHA-1, and complete-file
SHA-256. Target identity adds section heading, label, revision, and exact section-text
digest. Span identity adds exact selected text and its digest. No identity depends on a
line number.

Request, inference request/response, proposal, result, retrieval projection, excerpt,
and citation identities bind their complete represented inputs. These in-memory
identities define no serialized interchange schema.

## Prompt boundary

The prompt contains two separately labeled canonical JSON sections:

1. `TARGET_CONTEXT_JSON` contains the complete section and exact selected span; and
2. `UNTRUSTED_QUOTED_EVIDENCE_JSON` contains only projected source-linked excerpts.

The fixed instructions state that evidence is quoted data and must not be interpreted
as instructions. The port returns typed bounded text and `ProposedCitation` records;
it receives no callable tool, path resolver, database, browser, network, publication,
or bibliography capability.

## Failed-closed policy

Inference is not called when the target revision is stale, retrieval is insufficient,
a required bibliographic work is missing, a citation key is only candidate, or any
retrieval/excerpt warning needs inspection. After inference, request-correlation,
inference warnings, output bounds, the complete evidence-ID set, citation coverage,
and citation-key/evidence agreement are checked before a proposal is created.
Unexpected inference exceptions propagate rather than being mislabeled as
insufficient evidence.

Every result and proposal has `HumanAcceptanceStatus.NOT_EVALUATED`. Software
admission is not historical verification, citation validation, scientific validation,
publication approval, or human/PI acceptance.

## Project Koios adapters and deferred runtime integration

The [`adapters`](adapters/index.md) package consumes the canonical owner boundaries
`projectkoios.ingestion.transcript.evidence.selection`,
`projectkoios.search.evidence_retrieval`, and
`projectkoios.references.citation_identity`. Exact Git source revisions are declared
in `python/pyproject.toml` and resolved in `python/uv.lock`.

The adapters preserve Search result, evidence-item, ranked-item, and rank identities;
References result, source projection, item, status, and active canonical-key state;
and Ingestion selection, transcript, selected-page, selected-block, page, block, and
block-record identities. Indexed clean and retained raw text must match the exact
`CLEAN_TRANSCRIPT_BLOCK_EXACT_PAIR` and both digests. Search results are iterated in
owner rank order without sorting. Candidate proposed citekeys are never copied into
the canonical field, and non-block-resolved warning selections expose no evidence.
The package duplicates none of the owner selection, retrieval, ranking, or
citation-identity algorithms.

A concrete local model adapter, process isolation, runtime/model identity, timeout and
resource policy, cancellation, and structured-output parsing also remain deferred.
No filesystem or bibliography writer, patch applier, review recorder, acceptance
transition, or publication operation is implemented.
