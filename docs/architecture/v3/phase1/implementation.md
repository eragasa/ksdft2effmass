# Phase 1 implementation boundary

## Source files

```text
python/src/ksdft2effmass/operators/
├── representations/
│   ├── __init__.py
│   ├── domains.py
│   ├── spaces.py
│   ├── identities.py
│   └── fields.py
└── transformations/
    ├── __init__.py
    ├── identities.py
    └── base.py
```

The initializers define no flattened public inventory. There is no compatibility facade
or operators-root re-export.

## Dependency rule

`operators.transformations` may consume `operators.representations`.
`operators.representations` must not consume transformations. Neither package imports
analysis, campaigns, Workflow, serializers, schemas, retained data, publications, or
formal runtime code.

## Verification boundary

Focused tests cover exact types, immutable storage, domain and role agreement, identity
construction, edge transitions, nominal transformation abstractness, enum agreement, and
import direction over an explicit authorized Phase 1 module inventory. Every future actual concrete transformation triple requires
its own direct strict-mypy and runtime test module; synthetic ABC tests cannot substitute
for that verification. Passing tests establishes those software contracts only.

Detailed implementation pages:

- [representation implementation](../src/ksdft2effmass/operators/representations/implementation.md);
- [transformation implementation](../src/ksdft2effmass/operators/transformations/implementation.md).
