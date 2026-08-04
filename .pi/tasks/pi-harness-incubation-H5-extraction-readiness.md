# H5 — Standalone extraction readiness

Status: blocked by accepted H4

## Objective

Mechanically demonstrate that the accepted generic extraction unit can become a standalone package without publishing it, while the project-local overlay continues to work against the package candidate.

## Prerequisite

`H4:human_accepted`.

## Extraction unit

```text
python/src/ksdft2effmass/harness/pi/ excluding local/
harness/pi/
```

The local Python/resources and `.pi` state remain in this repository.

## Planned evidence

Construct a disposable isolated source tree and verify build/install, public imports, any accepted CLI, schemas, skill/resource discovery, manifest/validator execution, generic tests without local state, wheel/sdist contents, dependency metadata, and absence of project-relative paths/domain imports. Then verify the project-local overlay against the extracted candidate.

H5 may propose distribution/import/CLI names, initial version, Python/dependency policy, package data, license/notices, and compatibility policy for human decision. It must not publish a package.

## Exclusions

No PyPI or other publication, release/tag, P2 launch, external/scientific execution, scientific-validation claim, or UQ claim.

## Completion and downstream boundary

H5 concludes at human acceptance of extraction readiness. Accepted H5 only satisfies one P2 prerequisite. P2 still requires accepted P1 and a separate explicit P2 activation; H5 closure must not launch P2.
