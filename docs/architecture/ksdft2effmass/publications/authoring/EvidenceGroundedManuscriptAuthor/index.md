# `EvidenceGroundedManuscriptAuthor`

`EvidenceGroundedManuscriptAuthor` is the stateless semantic ActionObject. Its sole
composition path is `execute`; `prompt_for` exposes deterministic prompt construction
without performing inference. The action checks stale revision, evidence sufficiency,
warnings, accepted keys, response correlation, bounds, evidence identity, citation
coverage, and key agreement before returning a proposal.
