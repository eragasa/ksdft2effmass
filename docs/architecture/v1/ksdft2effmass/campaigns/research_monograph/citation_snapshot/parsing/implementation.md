# Parsing implementation

The TeX parser supports balanced multiline and multikey `cite`, the exact `eqincite`
and `citationtodo` definitions, contextual `texttt` expansion inside markers,
`include`/`input`, comments, escaped percent signs, and harmless definitions. Unknown
citation-capable commands, changed known-macro semantics, malformed groups, and unsafe
definitions fail closed.

The BibLaTeX parser recognizes balanced entries, skips structural comment/string/
preamble entries, preserves literal case-sensitive keys and file order, and rejects
malformed or duplicate keys. Citation and bibliography keys must match ASCII
`[A-Za-z0-9._-]{1,200}` for exact downstream compatibility. Both parsers require
UTF-8 and expose deterministic
character-to-byte and line/column conversion owned by their parsed source records.
