# ksdft2effmass ownership-compatibility extension

Extension ID: `ksdft2effmass.extension.ownership-compatibility.v1`

This extension records project-local compatibility-adapter version `1` for
accepted legacy ownership inputs. It depends on the generic normalized
ownership view `pih.schema.record-ownership-manifest-view.v1`; it does not
replace that schema or add a generic ownership kind.

## P1 version-1 boundary compatibility

The accepted P1 manifest value `boundary_owned` remains unchanged in its
historical and local input. For comparison with the generic evidence grammar,
the local adapter may expose that one value as:

```text
ownership_kind = artifact_owned
relation_kind = agreement
left_side_id = workflow-cpn-v1-python-runtime
right_side_id = workflow-cpn-v1-json-schema-wire-contract
direction = none
```

This representation applies to the accepted P1 Python/JSON contract boundary
whose current module is
`python/tests/software_verification/ksdft2effmass/integration/test__workflow_cpn_v1_python_json_contract.py`.
It preserves the original `boundary_owned` string and the named two-sided
boundary as relation metadata. It is not a rename, a third primary kind, or
authority to modify P1 filenames, tests, evidence identifiers, manifests,
schemas, fixtures, inventory exceptions, completion commands, or retained
records.

All other P1 version-1 inventory fields, object kinds, marker exceptions,
package/schema gates, exact artifact filenames, and completion-validator
identity remain local adapter inputs. Generic resources never import or depend
on this extension. Any later adapter behavior change requires a new local
compatibility-adapter version and retained source/target identities.
