# `ksdft2effmass.serialization.json`

This package owns reusable strict JSON wire mechanics. It is infrastructure rather than
a scientific-model, representation, campaign, provenance, or evidence-acceptance owner.

- `StrictJsonDecoder` owns strict UTF-8 object parsing, duplicate-key rejection,
  nonfinite-extension rejection, closed built-in JSON values, primitive type checks,
  SHA-256 syntax checks, and explicit binary64 conversion.
- [`immutable`](immutable/index.md) owns recursively immutable JSON containers and
  deterministic canonical byte conversion.

Schema versions, scientific fields, units, bases, gauges, state spaces, operator
meaning, artifact authentication, provenance, and acceptance remain with domain owners.
