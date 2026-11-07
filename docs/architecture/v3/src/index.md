# Source architecture

## Documentation rule

This tree mirrors maintained code under `python/src/`. Source files and authoritative
specifications determine the documented contract. A page must distinguish:

- implemented public types and imports;
- runtime invariants and failure behavior;
- mathematical interpretation;
- numerical representation and limits;
- dependencies and ownership boundaries; and
- behavior that remains absent or prospective.

Package initializers that intentionally export nothing are documented as such. Python
qualified names are not treated as wire-schema discriminators.

## Source map

```text
python/src/ksdft2effmass/
    docs/architecture/v3/src/ksdft2effmass/
```

- [`ksdft2effmass`](ksdft2effmass/index.md)

## Evidence boundary

Software tests can establish constructor, typing, immutability, dependency, and numerical
software behavior. They do not establish physical correctness, scientific validation,
retained evidence, or theorem applicability unless a separate authoritative contract says
so.
