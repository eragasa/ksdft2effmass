# `AdHocEvidenceRetrievalProjection`

`AdHocEvidenceRetrievalProjection` groups one to thirty-two distinct author-supplied
publisher abstracts with unique bibliographic-work and evidence identities. Evidence
must use canonical `(bibliographic_work_id, evidence_id)` order, so one bounded set has
one content identity and prompt order. The projection remains separate from and does
not imitate a Project Koios result, while every contained record binds an exact
References projection identity.
