# ksdft2effmass project profile

## Composition

`harness/local/profiles/ksdft2effmass-v2.json` is the maintained project-local profile instance with identity `ksdft2effmass.profile.v2`. It binds public contract version `1` to generic manifest `pih.generic.resources` version `2` and local extension manifest `ksdft2effmass.local.resources` version `2`. Under the H1 version-boundary rules, the skill-name correction changes the profile instance and both manifest contents without changing the profile schema, Python public contract, serialized-record schemas, or the skill behavior version.

The caller supplies the generic root, generic manifest and manifest byte identity, and the local root, local manifest and manifest byte identity explicitly. The profile names expected identities and versions; it contains no absolute root. Loading or resolution must not discover a profile or root from the current directory, Git, `.pi`, environment variables, parent directories, or installed-package fallback.

The local manifest has layer `local`, declares `extends_manifest_id = pih.generic.resources`, and uses `extend_only` composition. It introduces only:

- `ksdft2effmass.extension.evidence-documentation.v1`;
- `ksdft2effmass.extension.ownership-compatibility.v1`;
- `ksdft2effmass.profile.v2`;
- `ksdft2effmass.validation.current-local-replay.v1`; and
- `ksdft2effmass.profile.validation-route.v1`.

The maintained route selects `local` and retains `legacy` as rollback. The
current local replay runs the current H3 manifest/resource validator, the
current eight-skill capability validator, and the controlled architecture-
decision cases; it does not consume immutable H4 checksum inventories. The route wrapper validates a closed structured result
and fails closed on a missing script, malformed output, missing/duplicate check,
nonzero exit, or non-PASS check. Historical H4 replay and catalogs remain
unchanged and are used only by the retained historical/rollback mechanism.

The H4 identity mapping is `document-research-python` to `document-python-research-software`, `pih.skill.document-research-python.v1` to `pih.skill.document-python-research-software.v1`, `pih.manifest.skill-descriptor.document-research-python.v1` to `pih.manifest.skill-descriptor.document-python-research-software.v1`, and `ksdft2effmass.profile.v1` to `ksdft2effmass.profile.v2`. The renamed skill retains behavior version `1`; no compatibility alias is maintained.

Local resources may depend on generic resources. They may not replace or reuse a generic resource ID or path. Generic resources never depend on these local identities. The only accepted direction is:

```text
project-local -> generic
never generic -> project-local
```

Matching content hashes do not permit replacement. The profile, manifests, format/behavior versions, and exact SHA-256 byte identities are checked independently and fail closed on mismatch.

## Markers, namespaces, and scopes

The local marker vocabulary is `software_verification`, `numerical_verification`, `scientific_validation`, and `uncertainty_quantification`. The profile assigns audited evidence namespaces only to the software-verification and numerical-verification directory-tree scopes:

- `python/tests/software_verification` uses marker `software_verification` and the listed `SV-*` prefix/range/width rules;
- `python/tests/numerical_verification` uses marker `numerical_verification` and the listed `NV-*` prefix/range/width rules.

Namespace stems, inclusive numeric bounds, decimal widths, scope paths, and allowed markers are profile data, not generic literals. A marker must agree with its explicit scope and namespace. `scientific_validation` and `uncertainty_quantification` are vocabulary only in this profile: they have no assigned evidence-ID family and do not assert that corresponding evidence exists.

Filename policy identity `ksdft2effmass.filename-policy.test-evidence.v1` selects the accepted local convention. Class-owned modules normally use `test__<ClassName>.py` unless an accepted facet layout applies; artifact-owned modules use a descriptive artifact or boundary name. The generic evidence auditor does not interpret this local filename policy.

## Protected debt and legacy compatibility

`protected_unowned_functions` records 22 exact `(module_path, test_function)` pairs as protected migration debt. A match produces the declared protected-gap warning. The profile does not assign an evidence identifier, waive the gap, repair the function, or authorize editing it. Assertions, fixtures, parameterization, represented meaning, and historical paths remain unchanged unless a later task separately authorizes migration.

Compatibility-adapter version `1` preserves accepted P1 version-1 inputs. In particular, historical `boundary_owned` remains unchanged at its source. For generic comparison only, the local adapter may expose the accepted Python/JSON agreement as one `artifact_owned` relation with:

```text
relation_kind = agreement
left_side_id = workflow-cpn-v1-python-runtime
right_side_id = workflow-cpn-v1-json-schema-wire-contract
direction = none
```

This is preservation plus relation metadata, not a rename and not a third primary kind. Other P1 inventory fields, exceptions, exact filenames, identifiers, node mappings, manifests, schemas, fixtures, and completion commands remain local compatibility inputs. A later adapter behavior change requires a new local adapter version with retained source and target identities.

## Paths and local policy

Profile ownership scopes use `OwnershipScopePath` with explicit file or directory-tree semantics. Resource entries use `ResourcePath` and identify regular files below the separately supplied generic or local root. Findings use neutral `DiagnosticPath | null`, which may spell a file, directory, or ownership-scope prefix but makes no existence, file-kind, or containment claim. These meanings are not interchangeable even when their lexical spelling is the same.

Local fixtures exercise explicit-profile requirements, extension-only overlay and project-leakage behavior, scope/marker/namespace classification, and protected-gap reporting. They are structural software-verification fixtures. A numerical-verification label is classification input only; the fixtures contain no new numerical result.

## Claim and handoff boundary

Profile or H3 completion validation may check schema conformance, supported versions, manifest closure, exact content identities, explicit-root use, dependency direction, overlay rejection, local leakage controls, namespace classification, protected-gap handling, and fixture consistency. A pass does not establish skill authorization, human acceptance, physical correctness, scientific validation, uncertainty quantification, package readiness, or publication readiness.

After H3 is separately human-accepted, H2 may consume this profile, both manifests, their resource closures, schemas, fixtures, and canonical vectors as immutable contract inputs. H2 may use the project data to test generic profile loading, resource validation/resolution, evidence auditing, and compatibility boundaries; it must not embed this project's literals in the generic layer.

This description does not activate H2. H2 still requires accepted H3, separate explicit human authorization, and its own validated ownership manifest. No H4 cutover, skill retirement, P2 work, external execution, scientific execution, release, or publication is authorized by the profile or this handoff.
