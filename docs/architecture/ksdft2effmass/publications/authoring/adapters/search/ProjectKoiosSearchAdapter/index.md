# `ProjectKoiosSearchAdapter`

`ProjectKoiosSearchAdapter` is the stateless final owner-composition ActionObject. It
projects one exact Search result in existing rank order, joins every ranked item to
one References item and one available Ingestion block, and returns the local
`EvidenceRetrievalProjection`. It performs no retrieval, ranking, or citation
resolution.
