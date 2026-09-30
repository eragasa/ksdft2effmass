# `EvidenceRetrievalProjection`

`EvidenceRetrievalProjection` is the minimal complete-result view consumed by
authoring. It binds the external retrieval-result identity, the exact Project Koios
References source `citation_identity_projection_id`, exact ingestion selection
references, projected retrieval outcome, ranked excerpt order, and result-level
warnings. Available retrieval requires available ingestion selections, and every
excerpt correlates to a retained selection result. It neither selects transcript
blocks, retrieves, reranks, nor resolves citation identity. A future adapter must
preserve these fields exactly.
