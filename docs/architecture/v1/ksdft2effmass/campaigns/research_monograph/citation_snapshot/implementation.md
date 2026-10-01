# Citation snapshot implementation

## Source mapping

| Source | Responsibility |
|---|---|
| `citation_snapshot/records.py` | Immutable public DataObjects, Request, Result, enums, and structured failures |
| `citation_snapshot/parsing.py` | Closed, non-executing TeX and BibLaTeX structural parser |
| `citation_snapshot/integrity.py` | Canonical identities, complete relationship replay, output bounds, and result projection |
| `citation_snapshot/compilation.py` | Git revision/source admission, include traversal, semantic assembly, and public performer |
| `citation_snapshot/__init__.py` | Deliberate supported package route |

## Execution sequence

1. Validate the absolute repository root and derive a machine-independent request
   identity from the fixed operation and relative paths.
2. Read the exact 40-character HEAD and resolve the monograph include graph without
   leaving the monograph directory.
3. Parse the closed citation grammar and sibling bibliography.
4. Compare every consumed byte sequence with `git cat-file blob <HEAD>:<path>`;
   reject dirty, untracked, absent, or unreadable relevant sources.
5. Assemble immutable indexed records and source-lineage snapshot identity.
6. Replay all IDs, indexes, parent/child links, locators, citation bindings, closure
   sets, marker links, and output limits.
7. Encode every Result field in a fixed length-framed projection, check the
   20,000,000-byte limit, and derive `citation-result:<sha256>`.
8. Construct a Result that independently repeats the same replay.

## Failure and evidence boundary

Structural failures return no partial snapshot. Limits reject oversized output before
hashing. Successful software verification establishes only agreement with these
software contracts; it does not establish source truth, claim support, rights,
scientific validation, uncertainty quantification, or human acceptance.
