# `Periodic1DAdmissibleSetDisposition`

## Purpose

Closed M3 disposition vocabulary:

- `COMPATIBLE_WITNESS` (`"compatible-witness"`): an explicit retained point and frozen angle
  satisfies both thresholds;
- `CERTIFIED_SEPARATED` (`"certified-separated"`): an independently reconstructable
  lower bound exceeds the declared resolution; and
- `UNRESOLVED` (`"unresolved"`): neither proof obligation is met.

## Interpretation

The enum value alone is not evidence. Its associated `Periodic1DAdmissibleSetCaseResult`
must carry the correlated witness or certificate. Failed finite search maps to
`UNRESOLVED`, not incompatibility.
