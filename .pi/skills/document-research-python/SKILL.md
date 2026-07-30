---
name: document-research-python
description: Documents public research-software Python APIs and Sphinx pages. Use for new public Python APIs, scientific data models, numerical conventions, serialization schemas, and Sphinx conceptual or API documentation.
---

# Document Research Python

Use this skill when public Python APIs or scientific conventions are created or changed.

## Requirements

- Write complete NumPy-style docstrings for public modules, classes, methods, functions, properties, enums, exceptions, parameters, returns, raised exceptions, dataclass fields, public attributes, and examples when practical.
- Define symbols, units, shapes, index ordering, gauge, energy-zero, and tolerance conventions at the point where they enter the public model.
- Distinguish physical model, mathematical operator, numerical representation, and software implementation.
- Document validation rules and exception cases; do not hide scientific assumptions in tests or private methods only.
- Document every private method and private attribute in maintained first-party source. Explain owned responsibility, accepted and rejected types, canonicalization, invariants, error taxonomy, why the method or state is private, and whether the logic is mechanical, numerical, or scientific.
- Add nearby comments for scientifically, numerically, or architecturally meaningful local variables such as canonicalized values, residuals, norms, singular values, compatibility findings, validation state, unit conversions, shapes, and deterministic ordering state.
- Keep Python-version claims consistent with the supported Python 3.14 environment.
- Include runnable examples using the supported public import path.
- Add or update Sphinx conceptual documentation and API reference pages.
- Integrate new pages into a discoverable toctree.
- Build Sphinx with warnings treated as errors, for example by discovering the repository's actual command and using `sphinx-build -W` semantics.
- Do not commit generated `_build` artifacts.

## Review checklist

- Are claims limited to implemented behavior or explicitly marked as planned?
- Are DataObject/ActionObject boundaries visible to users?
- Are serialization schemas versioned with fixed field names?
- Are examples executable without private imports?
- Does the docs build pass with warnings as errors?
- Do source docstrings, tests, public schemas or fixtures, Sphinx API pages, concept pages, and control-plane records describe the same behavior?
- Does read-only documentation review report no unresolved material source-documentation findings?
