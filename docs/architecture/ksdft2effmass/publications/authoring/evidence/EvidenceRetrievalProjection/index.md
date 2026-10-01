# `EvidenceRetrievalProjection`

`EvidenceRetrievalProjection` is the minimal complete-result view consumed by
authoring. It binds the external retrieval-result identity, the exact Project Koios
References source projection and projection-result identities, exact Ingestion
selection references, projected Search outcome, ranked excerpt order, and result-level
warnings. Available retrieval requires available ingestion selections, every excerpt
correlates to a retained selection result, and Search ranks remain contiguous in the
owner-supplied order. It neither selects transcript blocks, retrieves, reranks, nor
resolves citation identity; the Project Koios adapters preserve these fields exactly.
