# PI Harness Evidence and Test Conventions

## Evidence classes

The harness distinguishes four activities.

| Evidence class | Question answered |
| --- | --- |
| Software verification | Does the software satisfy its specified public contract? |
| Numerical verification | Does the numerical implementation satisfy an independently defined mathematical contract? |
| Scientific validation | Does the model agree with independent evidence about the physical system? |
| Uncertainty quantification | How do represented input uncertainties affect reported outputs? |

Synthetic software fixtures do not establish scientific validation. Analytical matrix cases generally provide numerical verification rather than physical validation.

## Module ownership

Every evidence module declares one primary ownership type.

### Class-owned

One primary public class:

```text
test__<ExactPublicClassName>.py
```

### Artifact-owned

One named schema, fixture family, package surface, or metadata contract:

```text
test__<artifact_scope>_<contract>.py
```

### Boundary-owned

One explicit agreement between two surfaces:

```text
test__<left_scope>_<right_scope>_<agreement>.py
```

Directional mappings use

```text
test__<producer>_to_<consumer>_<mapping>.py
```

### Workflow-owned

One approved composed workflow or subnet:

```text
test__<workflow_or_subnet>_workflow.py
```

“Integration” is not sufficient ownership because it does not name the boundary being tested.

## Module documentation

Every evidence module uses the same structural grammar:

```text
Evidence class and represented meaning
Owned contract, oracle, and scope
VVUQ and scientific exclusions
```

The first section defines the represented behavior, mathematical rule, or observable and lists the owned evidence IDs. The second identifies intrinsic versus cross-object ownership and defines the independent oracle. The third states exactly what passing does and does not establish.

## Test-function documentation

Every evidence-bearing test documents these fields in order:

```text
Evidence ID
Requirement
Method
Oracle
Acceptance
Interpretation
Limitations
```

An oracle must come from an approved contract, schema, analytical result, manufactured solution, independent reference calculation, or physical reference evidence appropriate to the evidence class. Repeating the implementation is not an independent oracle.

## Function naming

Use

```text
test_<surface_kind>__<member_or_facet>__<expected_behavior>
```

Approved surface kinds include:

- `constructor`;
- `field`;
- `property`;
- `method`;
- `classmethod`;
- `staticmethod`;
- `protocol`;
- `public_api`;
- `artifact`;
- `boundary`;
- `workflow`.

Examples:

```python
def test_field__iteration_index__rejects_boolean() -> None:
    ...


def test_method__execute__returns_overflow_error_at_maximum_revision() -> None:
    ...


def test_boundary__python_json_numeric_contract__preserves_runtime_agreement() -> None:
    ...
```

Evidence IDs belong in docstrings and manifests rather than serving as the function's only name.

## Parameterized evidence

One parameterized test may retain one evidence ID when every case exercises the same requirement. Parameter IDs identify cases; they do not automatically create new evidence claims.

Distinct requirements require distinct evidence IDs.

## Structural and semantic review

A deterministic validator may check headings, field presence, naming shape, markers, evidence prefixes, and ownership manifests.

It cannot prove:

- oracle independence;
- mathematical correctness;
- scientific validity;
- tolerance adequacy;
- UQ adequacy.

Those require substantive review.

## Navigation

- [Previous: Skills and textual resources](./ksdft2effmass.harness.04.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Project-local extension model](./ksdft2effmass.harness.06.md)
