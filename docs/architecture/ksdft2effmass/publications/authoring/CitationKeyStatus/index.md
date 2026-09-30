# `CitationKeyStatus`

`CitationKeyStatus` is the closed local projection of Project Koios References
citation-identity status: `ACCEPTED_ACTIVE_CANONICAL`,
`ACCEPTED_WITHOUT_ACTIVE_CITEKEY`, `CANDIDATE_PROPOSED_NONCANONICAL`,
`INACTIVE_SUPERSEDED`, and `UNRESOLVED`. Only the active accepted status may carry a
`canonical_citekey`; every other status stops proposal composition for inspection.
No proposed candidate key is copied into the canonical field.
