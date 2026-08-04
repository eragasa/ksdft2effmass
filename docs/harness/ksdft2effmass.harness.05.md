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

The accepted generic model has exactly two primary evidence ownership kinds:
`class_owned` and `artifact_owned`. Successor task records and manifests must
use this vocabulary before implementation.

### `class_owned`

The module primarily owns evidence for one public class. A project profile may
supply its exact filename rule; the current P1-compatible local form is:

```text
test__<ExactPublicClassName>.py
```

### `artifact_owned`

The module primarily owns evidence for a named schema, fixture family, package
surface, metadata contract, cross-surface agreement, directional mapping, or
approved composed workflow/subnet. Agreement and direction are artifact
relation metadata, not separate primary ownership kinds.

A project profile may supply exact artifact filename rules. Descriptive forms
may include:

```text
test__<artifact_scope>_<contract>.py
test__<left_scope>_<right_scope>_<agreement>.py
test__<producer>_to_<consumer>_<mapping>.py
test__<workflow_or_subnet>_workflow.py
```

Legacy `boundary_owned`, `boundary`, or `workflow` labels are project-local
compatibility inputs only where an accepted historical contract requires them.
They must not become competing generic primary kinds. “Integration” alone is
not sufficient artifact identity because it does not name the agreement or
workflow being tested.

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

Project profiles may approve function-level surface facets including:

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

Function-level `boundary` and `workflow` facets describe what an
`artifact_owned` test exercises; they do not change its primary ownership kind.
Evidence IDs belong in docstrings and manifests rather than serving as the
function's only name.

## Parameterized evidence

One parameterized test may retain one evidence ID when every case exercises the same requirement. Parameter IDs identify cases; they do not automatically create new evidence claims.

Distinct requirements require distinct evidence IDs.

## Structural and semantic review

A deterministic validator may check headings, field presence, naming shape,
markers, evidence prefixes, and ownership manifests. Clean-revision
reproducible validation uses declared versioned inputs. Optional project-local
pre-commit checks may separately inspect an explicitly supplied worktree, but
personal or concurrent working notes are never required resources or reusable
validator inputs.

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
