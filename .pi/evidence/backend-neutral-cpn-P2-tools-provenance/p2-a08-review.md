# P2-A08 targeted semantic review

Status: **one bounded finding corrected**

Reviewer run: `351add6c-8635-4576-a934-859e71869491`

The assigned read-only integration reviewer inspected only
`python/tests/software_verification/ksdft2effmass/integration/provenance/test__package_wheel.py`
and the read-only packaging/source context needed to verify its fixed oracles. No other
provenance integration test was inspected.

The reviewer confirmed exact provenance-module equality, exact path-component test
exclusion, truthful offline/no-isolation build policy, isolated `python -I -S` import,
exact wheel origin and sentinel, build-once separation, evidence ownership and
migration, complete documentation, and bounded claims.

One bounded finding identified that setup counted only project-pattern wheel names, so a
second differently named wheel could escape the exactly-one-output check. The single
allowed correction pass now inventories all `*.whl` outputs, requires exactly one, and
then requires that artifact's filename to identify `ksdft2effmass`. Focused and family
regressions, structural validation, Ruff, and mypy passed after correction. The reviewer
made no mutations, and no second review was launched.
