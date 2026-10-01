# Research-monograph citation snapshot

## Ownership

`python/src/ksdft2effmass/campaigns/research_monograph/citation_snapshot/`
owns the canonical, deterministic, unversioned structural citation snapshot for
`docs/publications/research-monograph/manuscript.tex` and its sibling
`references.bib`. The paths are part of the contract and are not caller-selected.

The package contains three ownership layers:

- `records.py` owns immutable source, include, bibliography-entry, call,
  occurrence, group, editorial-todo, source-gap, request, result, locator, and
  content-identity records;
- `parsing.py` owns the closed TeX/BibLaTeX grammar and fails on citation-capable
  syntax outside that grammar; and
- `compilation.py` owns exact Git-HEAD observation, include traversal,
  bibliography reconciliation, deterministic opaque identity generation, and
  complete result assembly.

`ResearchMonographCitationSnapshotCompiler` is the semantic performer. It emits
no partial snapshot. A successful result therefore means that the declared
parser covered the complete resolved graph, not that bibliography metadata or
claim support is scientifically accepted.

## Identity and ordering

The snapshot records the exact repository HEAD, contract and parser/generator
identities, root-relative POSIX paths, source SHA-256 and byte counts, UTF-8 byte
spans, and one-based display locations. Opaque IDs use unversioned semantic
prefixes and length-framed SHA-256 inputs. Clients must not parse IDs.

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

## Boundary

The snapshot contains no manuscript excerpts, absolute source paths, runtime
state, rights or use decisions, ingestion state, Search links, human status, or
scientific acceptance. Placeholder source gaps are separate records and never
invent citation keys. `source_bibliography_observation_id` is nullable and is
always `None` when emitted here; an independent References owner may bind the
exact target bibliography entry and lineage without mutating this snapshot.
