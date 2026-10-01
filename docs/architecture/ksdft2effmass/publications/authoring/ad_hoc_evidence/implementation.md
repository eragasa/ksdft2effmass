# `ad_hoc_evidence` implementation

```mermaid
flowchart TD
    Bytes["exact fetched abstract-page bytes"] --> Digest["source_document_sha256"]
    Metadata["title + authors + date + DOI"] --> Identity["evidence identity"]
    Abstract["publisher abstract text"] --> Identity
    Digest --> Identity
    Owner["ProjectedCitationIdentity"] --> Identity
    Local["local noncanonical candidate label"] --> Identity
    Identity --> Projection["canonical ad-hoc projection identity"]
```

`AuthorSuppliedPublisherAbstractEvidence` accepts only the three authorized
`journals.aps.org/.../abstract/...` URLs. Every record fixes
`EvidenceProvenanceStatus.AUTHOR_SUPPLIED_AD_HOC` and
`EvidenceSourceScope.PUBLISHER_ABSTRACT`, binds the exact fetched-page SHA-256,
metadata, abstract, exact References projection identity, local candidate label, and
warnings, and rejects a full-text URL. Citation status and canonical key are derived
from that exact projection. Projection evidence is canonically ordered by work and
evidence identity; direct noncanonical projection construction is rejected.

Warnings are retained rather than normalized away. The authoring Action fails closed
before inference when either a record or projection carries a warning. An absence of
warnings establishes only that this bounded extraction reported none; it does not
establish full-paper review, rights clearance, or scientific correctness.
