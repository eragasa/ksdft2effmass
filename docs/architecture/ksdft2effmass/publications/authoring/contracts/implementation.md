# `contracts` implementation

```mermaid
flowchart TD
    Target["target.py"] --> Contracts["contracts.py"]
    Evidence["evidence.py"] --> Contracts
    Contracts --> Inference["inference.py"]
    Contracts --> Proposal["proposal.py"]
    Contracts --> Author["author.py"]
```

`ManuscriptAuthoringRequest` validates exact owner types, unique bounded required-work
identities, trimmed instruction text, and caller-selected output limits. Its identity
binds target/span, retrieval projection, required works, instruction, and bounds.
