# `proposal` implementation

```mermaid
flowchart LR
    Contracts["contracts.py"] --> Proposal["proposal.py"]
    Statuses["statuses.py"] --> Proposal
    Proposal --> Inference["inference.py<br/>citation + marker IDs"]
    Proposal --> Author["author.py"]
```

Each record is frozen, slotted, and content-identified. Fully keyed and
citation-gap-ready results contain a proposal and inference-response identity. A gap
result contains exact `ProposedEvidenceMarker` records plus the canonical
`CITATION_GAPS_REQUIRE_INSPECTION` issue; failed results contain no proposal. Every
path remains explicitly `HumanAcceptanceStatus.NOT_EVALUATED`.
