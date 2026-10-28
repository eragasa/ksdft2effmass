# `Periodic1DFourierLocalityVerification` numerics

SHA-256 values are lowercase 64-character hexadecimal strings validated structurally.
They identify exact bytes and are not numerical tolerances.

Comparison names form a unique, deterministic ordered inventory. Counts must equal the
number of comparison dispositions. Aggregate `passes` is true only when every required
comparison passes and no comparison is unresolved or absent.

The projection digest is calculated from canonical typed bytes of the verifier-owned
projection constructed from the admitted result. Constructor validation rejects a digest
or component inventory that is structurally inconsistent; byte-owning stored admission
recomputes and exact-compares the aggregate and projection bytes.

The class performs no scientific arithmetic beyond correlation of already calculated
comparison records.
