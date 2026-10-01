# `ResearchMonographCitationSnapshotResult`

Immutable successful owner handoff containing durable `request_id`, complete
`result_id`, and one `ManuscriptCitationSnapshot`. Construction repeats full snapshot
integrity replay and canonical projection hashing. The Result identity binds every
stored snapshot field without including the absolute repository root; callers cannot
supply an arbitrary snapshot or identity and obtain an accepted Result.
