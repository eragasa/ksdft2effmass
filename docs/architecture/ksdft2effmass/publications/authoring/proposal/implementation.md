# `proposal` implementation

```mermaid
flowchart LR
    Contracts["contracts.py"] --> Proposal["proposal.py"]
    Statuses["statuses.py"] --> Proposal
    Proposal --> Inference["inference.py<br/>ProposedCitation only"]
    Proposal --> Author["author.py"]
```

Each record is frozen, slotted, and content-identified. A proposal-ready result alone
contains a proposal and inference-response identity; every failed result contains a
canonical nonempty issue tuple and no proposal. Both result paths remain explicitly
`HumanAcceptanceStatus.NOT_EVALUATED`.
