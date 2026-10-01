Research-monograph citation snapshot
====================================

The research-monograph citation snapshot is an immutable structural inventory of
one exact manuscript graph and bibliography.  It exists so another system can
reason about citation calls, individual key occurrences, key groups, prospective
citation markers, bibliography entries, and unresolved source placeholders
without receiving manuscript excerpts or inferring scholarly acceptance.

Scope and completeness
----------------------

The entrypoint and bibliography are fixed to
``docs/publications/research-monograph/manuscript/manuscript.tex`` and
``docs/publications/research-monograph/references.bib``.  The compiler follows
``include`` and ``input`` directives in source order while enforcing the monograph
boundary.  The canonical composition root is built from the monograph directory, so
its authored chapter and appendix targets are monograph-root relative; nested source
targets are relative to the including file.  A successful result is complete for the
closed supported grammar.  Unknown
citation-capable macros, unsafe definitions, missing files, cycles, path escapes,
malformed groups, and duplicate bibliography keys raise a structured error; no
partial snapshot is returned.  Every consumed source must equal its exact blob at the
recorded Git HEAD, while unrelated worktree changes are irrelevant.

Rendered calls and occurrences are distinct.  One multikey ``cite`` command is
one call with multiple occurrences.  Each ``texttt`` key token inside a
``citationtodo`` marker expands to a separate rendered call and occurrence.
The marker remains a separate editorial source construct.  An ``eqincite`` call
is represented as its own command kind and expansion origin even though the
current manuscript does not invoke it.

Identity and locators
---------------------

Each source file has exact SHA-256 and byte-count lineage.  Locators contain a
root-relative path, include-instance order, exact source identity, half-open
UTF-8 byte span, and one-based line and column.  They contain no source excerpt.
Opaque call, occurrence, group, todo, entry, gap, include, file, snapshot, request,
and result identities are deterministic and unversioned; clients must treat them as
opaque.  The request identity excludes the absolute repository root.  The result
identity covers the request identity and every field in the complete canonical
snapshot projection after relationship and identity replay.

Bibliography and source gaps
----------------------------

A bibliography entry retains its file lineage, source order, literal
case-sensitive key, entry type, exact byte span, and entry-level content
identity.  The nullable ``source_bibliography_observation_id`` is reserved for
an independent References binding and is always unset by this package.

Literal citation keys use the exact ASCII grammar
``[A-Za-z0-9._-]{1,200}``.  A placeholder source record is not a malformed citation
key.  Such records are
emitted as separate source gaps with exact locators and reason codes.  They do
not enter missing-key or uncited-key closure.

Output bounds
-------------

Identifiers are limited to 512 UTF-8 bytes, paths and descriptive text to 4096 UTF-8
bytes, and source and aggregate source sizes to 100,000,000 bytes.  Per-record
reference tuples are limited to 256; source files and global citation records to
10,000.  The
complete canonical projection is checked against a 20,000,000-byte limit before the
result identity is hashed.

Canonical Result wire
---------------------

``ResearchMonographCitationSnapshotResultJsonCodec`` serializes exactly one complete
Result to deterministic newline-terminated UTF-8 JSON.  The unversioned object contains
only ``request_id``, ``result_id``, and every stored snapshot field and family in owner
order.  It has no schema or version tag, timestamp, absolute repository root, excerpt,
runtime state, or downstream-authority field.  The codec returns bytes and accepts
explicit bytes; it has no writer, default path, persistence behavior, CLI, stdout
adapter, or repository discovery.

Decoding is limited to 20,000,000 input bytes, 64 JSON nesting levels, and 20
decimal digits per integer token before stricter record-domain limits apply.  It
rejects non-UTF-8, malformed, duplicated, missing, unknown, wrong-type, trailing, and
noncanonical input.  A decoded
value is accepted only after immutable record construction, snapshot integrity replay,
and exact request, snapshot, and Result identity verification.  A consumer therefore
need not parse TeX or BibLaTeX, but must receive the bytes through its own explicit
configuration boundary.

Optional Project Koios projection
---------------------------------

The optional ``ksdft2effmass.integration.projectkoios`` boundary maps a replay-valid
owner Result one way to ``projectkoios.references.citations.CitationTargetSnapshot``.
It preserves literal keys and neutral target records while deliberately renaming
``bibliography_entry_id`` to ``entry_id`` and ``bibliography_path`` to
``bibliography_source_path``.  Source files, includes, calls, todos, request and Result
identities, parser and generator identities, and the repository revision remain
owner-only.

The adapter leaves every ``source_bibliography_observation_id`` unset.  Project Koios
References independently parses exact bibliography bytes and owns later observation
and binding decisions.  The adapter performs no bibliography intake, TeX or BibTeX
rescan, acquisition, identity resolution, availability assessment, rights decision,
processing authority, or projection-status assignment.

Evidence boundary
-----------------

The snapshot verifies represented repository structure only.  Bibliography
presence does not mean that a source was read, that metadata is correct, that a
source supports a local claim, or that rights and allowed uses have been
admitted.  The snapshot records no ingestion, Search linkage, API URL, runtime
state, scientific validation, uncertainty quantification, or human acceptance.
