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
``docs/publications/research-monograph/manuscript.tex`` and
``docs/publications/research-monograph/references.bib``.  The compiler follows
``include`` and ``input`` directives in source order, resolving each relative path
from the directory of its including file while enforcing the monograph boundary.  A
successful result is complete for the closed supported grammar.  Unknown
citation-capable macros,
unsafe definitions, missing files, cycles, path escapes, malformed groups, and
duplicate bibliography keys raise a structured error; no partial snapshot is
returned.

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
Opaque call, occurrence, group, todo, entry, gap, include, file, and snapshot
identities are deterministic and unversioned; clients must treat them as opaque.

Bibliography and source gaps
----------------------------

A bibliography entry retains its file lineage, source order, literal
case-sensitive key, entry type, exact byte span, and entry-level content
identity.  The nullable ``source_bibliography_observation_id`` is reserved for
an independent References binding and is always unset by this package.

A placeholder source record is not a malformed citation key.  Such records are
emitted as separate source gaps with exact locators and reason codes.  They do
not enter missing-key or uncited-key closure.

Evidence boundary
-----------------

The snapshot verifies represented repository structure only.  Bibliography
presence does not mean that a source was read, that metadata is correct, that a
source supports a local claim, or that rights and allowed uses have been
admitted.  The snapshot records no ingestion, Search linkage, API URL, runtime
state, scientific validation, uncertainty quantification, or human acceptance.
