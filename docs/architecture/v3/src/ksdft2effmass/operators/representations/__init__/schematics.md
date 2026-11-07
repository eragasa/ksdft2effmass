# Schematic

```mermaid
flowchart LR
    consumer["consumer"] --> defining["representations.<defining_module>"]
    initializer["representations.__init__"] -. "no re-export" .-> defining
```
