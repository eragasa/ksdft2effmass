# Mathieu1D legacy-contract retirement

## Scope and authorization

After the predecessor runs, calculation-local code, installed `study/` package, and live
publication bindings were removed, four version-one contract files had no consumer. The
operator explicitly authorized their deletion:

- `calculations/mathieu1d/input.json`;
- `calculations/mathieu1d/schemas/input.schema.json`;
- `calculations/mathieu1d/schemas/result.schema.json`;
- `calculations/mathieu1d/schemas/verification.schema.json`.

These files are absent from the live tree. The direct runtime accepts only constructor-
validated typed records owned by `ksdft2effmass.model_systems.mathieu1d`; it does not
accept the deleted schema-v1 wires.

## Git recovery boundary

The deleted bytes remain recoverable only from existing Git history:

- recovery revision: `2ea109d5165366bc507d8900cf85a67de1a2bf73`;
- input blob: `a59b30283dda8c44362889ad8bb6880184413401`;
- schemas tree: `203f631200b8d2b6fbc91f2b1c0e4d1e79f4eba7`;
- file count: 4;
- sorted path inventory SHA-256:
  `589af01d7a80511427bf54c7ffd0209e1e963648b9bbcbba716dd0be18cb1445`;
- sorted path-and-content-digest inventory SHA-256:
  `80d29aeacb0ca2cc186c5481b3d62f15eb65054bd26fc19ab5dc574690988eb6`.

| Removed file | SHA-256 |
|---|---|
| `input.json` | `5dc6c4ab4a70c5dd169f6da3bbc70583a5970906cee78f8cf25fe23ba52e5e2e` |
| `schemas/input.schema.json` | `51f5cc6da6be7249900189b4c8510159f02f3bc0bc7a58c5773d5883c5dca7d6` |
| `schemas/result.schema.json` | `91c08e092a5ff2e876728b00d796019d4f6c1239a7082dd47bbc693f663b419b` |
| `schemas/verification.schema.json` | `9e905816af6caf49dc787a90be172ac5398cc83327094c2d2bad3c6150d4f8db` |

These locators establish recovery only. They are not live schemas, supported data,
publication inputs, or evidence of scientific validity.
