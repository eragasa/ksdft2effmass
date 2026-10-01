# Research-monograph citation snapshot

## Ownership

`python/src/ksdft2effmass/campaigns/research_monograph/citation_snapshot/`
owns the canonical, deterministic, unversioned structural citation snapshot for
`docs/publications/research-monograph/manuscript.tex` and its sibling
`references.bib`. The paths are part of the contract and are not caller-selected.

The package contains four ownership layers:

- [`records.py`](records/index.md) owns immutable source, include,
  bibliography-entry, call, occurrence, group, editorial-marker, source-gap,
  request, result, locator, and content-identity records;
- [`parsing.py`](parsing/index.md) owns the closed TeX/BibLaTeX grammar and fails
  on citation-capable syntax outside that grammar;
- [`integrity.py`](integrity/index.md) owns the single complete identity,
  relationship, locator, output-bound, and canonical-result replay path; and
- [`compilation.py`](compilation/index.md) owns exact Git-HEAD source admission,
  include traversal, bibliography reconciliation, and complete result assembly.

`ResearchMonographCitationSnapshotCompiler` is the semantic performer. It emits
no partial snapshot. Every consumed TeX and bibliography byte sequence must equal
its blob at the recorded HEAD; unrelated worktree changes do not matter. The
compiler and `ResearchMonographCitationSnapshotResult` both use
`ResearchMonographCitationSnapshotIntegrityValidator`, so downstream receives a
replay-valid owner Result rather than an unchecked snapshot. A successful result
means that the declared parser covered the complete resolved graph, not that
bibliography metadata or claim support is scientifically accepted.

## Identity and ordering

The snapshot records the exact repository HEAD, contract and parser/generator
identities, root-relative POSIX paths, source SHA-256 and byte counts, UTF-8 byte
spans, and one-based display locations. Opaque snapshot-record IDs use unversioned semantic prefixes and length-framed
SHA-256 inputs. The durable request identity excludes the machine-local absolute
repository root. The result identity hashes a canonical projection containing the
request identity and every snapshot field after complete replay. Clients must not
parse IDs.

Sources and include instances follow depth-first manuscript order. Calls,
occurrences, todos, and source gaps follow include order and source byte offset.
Keys within a call retain source order. Bibliography entries retain file order;
citation groups use literal case-sensitive key order.

## Supported grammar

The closed grammar supports:

- balanced multiline and multikey `\cite` calls;
- the project-owned `\eqincite` expansion;
- contextual `\citationtodo` expansion in which each nested `\texttt` token
  becomes one rendered citation call;
- TeX comments and escaped percent signs;
- `\include` and `\input` graph traversal relative to each including file and
  confined to the monograph directory;
- exact known citation macro definitions and harmless noncitation `\def`,
  `\newcommand`, `\renewcommand`, and `\newenvironment` definitions; and
- BibLaTeX entry types and exact case-sensitive keys.

Unknown citation-capable macros, unsafe definitions, missing sources, include
cycles, path escapes, malformed groups, and duplicate bibliography keys fail
closed.

## Output limits

Identifiers are limited to 512 UTF-8 bytes. Literal citation keys must match
ASCII ``[A-Za-z0-9._-]{1,200}``. Paths and descriptive text are limited to 4096
UTF-8 bytes. A source and all consumed source bytes together are limited
to 100,000,000 bytes. Per-record reference tuples are limited to 256; source
files, global record families, and their aggregate are limited to 10,000. The
complete canonical projection must be no larger than 20,000,000 bytes before its
result identity is hashed. Locators are correlated to exact file identities,
include instances, source spans, and record indexes.

## Boundary

The snapshot contains no manuscript excerpts, absolute source paths, runtime
state, rights or use decisions, ingestion state, Search links, human status, or
scientific acceptance. Placeholder source gaps are separate records and never
invent citation keys. `source_bibliography_observation_id` is nullable and is
always `None` when emitted here; an independent References owner may bind the
exact target bibliography entry and lineage without mutating this snapshot.

```{toctree}
:maxdepth: 3
:hidden:

schematic
implementation
records/index
parsing/index
integrity/index
compilation/index
```
