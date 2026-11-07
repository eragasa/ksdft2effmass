# PIAB1D campaign attempt `20260922T213932Z`

## Status

**Failed attempt; no calculation result or evidence package was produced.**

The locally preserved `run.attempt-1.log` records failure during result serialization.
The serializer attempted to express a KSD source path relative to
`calculations/` rather than the repository root and raised `ValueError`. The local
`run.log` is empty. Both log files are excluded by the repository-wide `*.log` ignore
rule and are not made into scientific evidence by this index record.

Observed local log digests are:

| Local file | SHA-256 |
|---|---|
| `run.attempt-1.log` | `9e77a988f3f452cfaf9d81ca485ae4edb73d1d127712658502994f5b95b722b7` |
| `run.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

No input, producer, result, verification, manifest, or checksum package is retained in
this directory. This attempt must not be described as a completed calculation or as
support for the research-monograph conclusions.

The successful historical PIAB1D calculation package is separately retained at
`calculations/research-monograph/particle-in-box/`.
