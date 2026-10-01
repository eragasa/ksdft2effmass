# Integrity implementation

`CitationIdentityGenerator` uses type-tagged, length-framed semantic parts and SHA-256
with unversioned prefixes. The public validator replays source, include, snapshot,
entry, call, occurrence, group, marker, gap, request, and Result identities. It also
checks unique IDs, contiguous indexes, parent/child include topology, source and
locator identities, span containment, bibliography binding, marker-generated links,
origin counts, and exact missing/duplicate/uncited sets.

The canonical Result projection encodes every stored field in a fixed typed and
length-framed order. Its absolute-root-free request identity is included. The encoder
checks its 20,000,000-byte bound as bytes are appended and again before hashing.
