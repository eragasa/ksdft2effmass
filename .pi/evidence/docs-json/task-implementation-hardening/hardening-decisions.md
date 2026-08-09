# HarnessTask Stage-2A hardening decisions

Status: Implemented software contract pending independent review and explicit human implementation acceptance.

Claim boundary: These decisions define software-verification behavior only. They do not establish semantic migration correctness, scientific validity, authority, or human acceptance.

## Graph diagnostics and precedence

`HarnessTaskGraphValidator` returns the existing project-local `LocalValidationResult`. Findings are unique and ordered lexically by `(code, path or "", detail)`:

1. `PIHL.TASK.DOCUMENTATION_PATH_DUPLICATE`
2. `PIHL.TASK.DUPLICATE_ID`
3. `PIHL.TASK.INTAKE_PATH_DUPLICATE`
4. `PIHL.TASK.PARENT_CYCLE`
5. `PIHL.TASK.PARENT_MISSING`
6. `PIHL.TASK.PREREQUISITE_CYCLE`
7. `PIHL.TASK.PREREQUISITE_MISSING`

The numbered display is lexical for this fixed code set, not a separate priority override. `HarnessTask` rejects intrinsic self-parent, self-prerequisite, and Task/external prerequisite overlap before graph construction; the graph action therefore does not duplicate constructor diagnostics for states that cannot be represented by a valid `HarnessTask`.

Parent and prerequisite cycles are rendered by the lexically least rotation of the cycle's Task identifiers. The validator uses iterative traversal, applies no lifecycle policy, and performs no discovery or I/O.

## Identifier and ResourcePath behavior

Project-local `Identifier` values use exactly:

```text
^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$
```

The runtime reuses the accepted generic `ResourcePath` constructor contract. The v2 schema represents relative-path, traversal, empty-segment, backslash, drive-prefix, Windows-device, C0, DEL/C1, U+2028, and U+2029 rejection. Unicode NFC normalization and escaped unpaired-surrogate rejection remain runtime-owned because JSON Schema pattern matching cannot establish Unicode normalization and JSON text can encode escaped surrogate values.

The indexed invalid fixture family partitions schema-owned and runtime-owned cases explicitly.

## Template parsing

`HarnessTaskProjectionProfile.template_bytes` is the sole authoritative runtime template representation. The maintained JSON profile carries one base64 encoding plus the SHA-256 identity of those bytes; it contains no editable text copy.

The renderer parses only explicit UTF-8 template bytes. Supported tokens are:

```text
{{task.FIELD}}
{{content.MAPPING_ID}}
```

Names use the accepted project-local identifier grammar. Every supplied documentation content mapping must occur exactly once. Unknown fields, unknown content identifiers, unsupported or unclosed token forms, missing content tokens, duplicate content tokens, and final-LF mismatches fail closed.

Task tuples render as Markdown bullets, Booleans as lowercase JSON text, `None` as the exact text `None`, and other values through exact string conversion. Documentation-owned blocks remain opaque built-in bytes: they are never decoded, scanned, normalized, or reparsed after insertion. The renderer does not add or remove line endings; the explicit profile policy requires either exactly one final LF or no final LF.

## Byte comparison

`HarnessTaskDocumentationComparator` applies Python `difflib.SequenceMatcher` to exact byte sequences with `autojunk=False`. It reports non-equal opcodes in source order as:

```text
<tag>:source[<start>:<end>]->rendered[<start>:<end>]
```

Mappings must be ordered, nonoverlapping, in range, source-identity compatible, and exact-span-identity compatible. Coverage gaps are nonempty half-open source ranges. Documentation-owned source blocks must occur unchanged in mapping order in rendered bytes.

Statuses are:

- `EXACT`: source and rendered bytes are identical;
- `MAPPED_DIFFERENCES`: bytes differ, source coverage is complete, and every documentation block is preserved in order; and
- `UNMAPPED_DIFFERENCES`: coverage has a gap or a documentation block is absent, changed, or out of order.

With complete source mapping, zero-width rendered insertions are mechanically mapped. This is a byte-structural attribution only. It does not establish that inserted Task text is semantically correct or accepted by a human.

## Packet and disposition checks

Packet preparation recomputes and requires agreement for:

- globally unique mapping identifiers;
- complete ordered source coverage and exact span identities;
- canonical Task JSON;
- source/documentation identities;
- documentation mapping identifiers, exact blocks, and documentation target path;
- explicit rendering;
- explicit comparison;
- canonical generic human-review packet;
- source revision; and
- source and rendered target paths.

The disposition recorder retains the exact generic review packet and uses only this closed table:

| Generic disposition | Migration disposition |
|---|---|
| `accepted` | `ACCEPT_FILE_MIGRATION` |
| `bounded_correction` | `REVISE_CONTRACT_OR_MAPPING` |
| `rejected` | `RETAIN_DOCUMENTATION_OWNERSHIP` |
| `deferred` | `DEFER_FILE` |

Neither operation persists data, modifies files, interprets natural language, authenticates authority, activates Stage 2B, or selects a successor.
