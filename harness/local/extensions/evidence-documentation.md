# ksdft2effmass evidence-documentation extension

Extension ID: `ksdft2effmass.extension.evidence-documentation.v1`

This project-local extension applies the generic
`pih.reference.test-evidence-documentation.v1` grammar without copying or
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

The 22 profile-listed unowned functions are exact protected migration debt.
They remain warnings in the current audit; the profile neither assigns them
identifiers nor waives, repairs, or authorizes edits to them.
