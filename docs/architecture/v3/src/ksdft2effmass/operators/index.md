# `ksdft2effmass.operators`

## Source boundary

The existing operator package owns finite represented-operator metadata and numerical
operations. The documented Phase 1 additions are two direct-import sibling packages:

- [`representations`](representations/index.md), which owns intrinsic finite carriers,
  represented-space identity, representation identity, and immutable matrix fields;
- [`transformations`](transformations/index.md), which owns directed edge identity and
  nominal request/result/Action contracts.

The required generic dependency direction is

```text
operators.records -> operators.representations -> operators.transformations
```

`operators.representations` must not import `operators.transformations`. Neither generic
package owns campaign policy, serializers, schemas, retained data, or formal runtime
classes. Their package initializers remain documentation-only and do not flatten exports.

Concrete mathematical operator-family packages are outside the implemented Phase 1
surface.
