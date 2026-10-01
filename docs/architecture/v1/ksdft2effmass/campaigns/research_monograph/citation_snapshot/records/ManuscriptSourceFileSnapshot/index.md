# `ManuscriptSourceFileSnapshot`

Immutable descriptor for one unique TeX source: deterministic file ID, root-relative
path, exact byte size/SHA-256, and first-seen graph order. Multiple include instances
may reference one descriptor. Every descriptor must be represented by at least one
include instance and must match its exact HEAD blob during compilation.
