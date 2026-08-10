# H5 — Standalone extraction readiness

Status: optional; blocked by accepted H4 and separate explicit H5 activation; inactive

## Objective

Mechanically demonstrate that the accepted generic extraction unit can become a standalone package without publishing it, while the project-local overlay continues to work against the package candidate.

## Prerequisite

`H4:human_accepted` plus separate explicit human activation of H5. Accepted H4
does not activate H5.

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

H5 concludes at human acceptance of standalone extraction readiness. It remains
optional work after H4, does not publish a package, is not a P2 prerequisite,
and activates neither P2 nor any other task. P2 has its own separate gate after
accepted H4.
