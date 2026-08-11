# ksdft2effmass evidence-documentation extension

Extension ID: `ksdft2effmass.extension.evidence-documentation.v1`

This project-local extension applies the generic
`pih.reference.test-evidence-conventions.v1` grammar without copying or
replacing it. The generic primary ownership kinds remain exactly
`class_owned` and `artifact_owned`; this extension adds project configuration,
not a third ownership kind.

## Local evidence policy

The project declares the pytest markers `software_verification`,
`numerical_verification`, `scientific_validation`, and
`uncertainty_quantification`. Only the first two currently own audited evidence
identifier namespaces. Software-verification modules use the `SV-*` namespaces
and marker; numerical-verification modules use the `NV-*` namespaces and
marker. Namespace stems, inclusive ranges, decimal widths, module scopes, and
the exact protected unowned functions are data in
`ksdft2effmass.profile.v2`.

`scientific_validation` and `uncertainty_quantification` are declared marker
vocabulary only. Their presence does not create an evidence-ID family or imply
that such evidence exists. Passing software or numerical verification does not
establish scientific validation or uncertainty quantification.

## Filename policy

Filename policy identity
`ksdft2effmass.filename-policy.test-evidence.v1` denotes the accepted local
policy derived from the maintained evidence convention. Class-owned modules use
`test__<ClassName>.py` unless an explicitly accepted facet layout applies;
artifact-owned modules use an accepted descriptive artifact or boundary name.
P1 exact artifact filenames, inventories, exceptions, and node-ID mappings
remain compatibility input and are not generalized by this identity.

The generic evidence auditor does not interpret this filename policy. A local
adapter or validator must apply it explicitly and must preserve historical
paths, evidence identifiers, assertions, fixtures, parameterization, and
represented meaning during any separately authorized migration.

The 22 profile-listed unowned functions are exact protected migration debt for
their historical contract only. Under the separately activated repository-wide
conformance task they remain explicit migration inputs, not waivers.

## Repository-wide completion policy

Configured Python test sources and embedded declarations, the generic profile matrix,
and the explicit predecessor map are authoritative. The maintained inventory at
`.pi/evidence/python-conformance/module-inventory.json` is a synchronized comparison
projection that retains baseline and current source-derived node counts and content
identities. The local completion command is
`python/.venv/bin/python python/src/cli/validate_evidence_repository_conformance.py --repository-root <absolute-repository-root>`.
It invokes maintained Python conformance directly without pytest, nested CLI execution,
or generated-input authority. Its PASS establishes only structural source and
projection agreement; independent review still owns semantic cohesion, oracle
independence, completeness, scientific meaning, and human acceptance.
