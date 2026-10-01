# Compilation schematic

```mermaid
flowchart TD
    root[Absolute repository root] --> revision[Read exact HEAD]
    root --> graph[Resolve manuscript include graph]
    graph --> parse[Parse exact source bytes]
    revision --> admit[Compare each source with HEAD blob]
    parse --> admit
    admit --> assemble[Assemble immutable snapshot]
    assemble --> replay[Integrity replay and Result identity]
    replay --> result[Replay-valid Result]
```

Relative includes resolve from each including file and remain confined to the
monograph directory. Traversal is depth-first and records each include instance even
when a source file is reused.
