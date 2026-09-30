# `authoring` schematic

```mermaid
flowchart TD
    Target["ManuscriptTargetContext<br/>full section + exact span"]
    Owners["References + Ingestion + Search results"]
    Adapters["exact owner adapters"]
    Retrieval["EvidenceRetrievalProjection"]
    Request["ManuscriptAuthoringRequest"]
    Author["EvidenceGroundedManuscriptAuthor.execute"]
    Prompt["ManuscriptInferenceRequest<br/>separate target/evidence JSON"]
    Port["LocalManuscriptInferencePort"]
    Response["ManuscriptInferenceResponse"]
    Checks["correlation, bounds,<br/>evidence and citation checks"]
    Proposal["ManuscriptProposal<br/>NOT_EVALUATED"]
    Failure["ManuscriptAuthoringResult<br/>failed closed"]

    Target --> Request
    Owners --> Adapters
    Adapters --> Retrieval
    Retrieval --> Request
    Request --> Author
    Author -->|admissible| Prompt
    Author -->|stale / insufficient / inspection| Failure
    Prompt --> Port
    Port --> Response
    Response --> Checks
    Checks -->|admitted| Proposal
    Checks -->|mismatch / warning / overflow| Failure
    Proposal --> Result["ManuscriptAuthoringResult<br/>PROPOSAL_READY"]
```

No arrow writes the target or bibliography. Retrieval is already complete before this
flow begins.
