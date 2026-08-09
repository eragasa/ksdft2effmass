r"""Software verification of import.

Facet and represented meaning

-----------------------------
This artifact-owned module verifies the package-root Python import surface and the
presence of the imported module object.

Intrinsic and cross-object scope

--------------------------------
The ``ksdft2effmass`` root import is the sole artifact. Python import semantics supply
the oracle; subpackage exports and object behavior remain with their dedicated owners.

VVUQ and scientific exclusions

------------------------------
Passing establishes only root-package importability in the configured test environment.
It does not establish export completeness, installation from a wheel, numerical
verification, scientific validation, UQ, physical correctness, portability, release
readiness, or cross-language conformance.
"""

import pytest

pytestmark = pytest.mark.software_verification


def test_public_api__package_import__resolves_module() -> None:
    """Evidence ID: SV-PACKAGE-001

    Requirement: The public root package is importable as ``ksdft2effmass``.

    Method: Import the package through Python's public import statement in the
    configured test
    environment and retain the resulting module binding.

    Oracle: Python import semantics require a successful import to bind a module object;
    the
    accepted public package name is the fixed literal ``ksdft2effmass``.

    Acceptance: Import completes without an exception and the resulting binding is not
    ``None``.

    Interpretation: Failure indicates package discovery, environment configuration, or
    public root-name
    drift; passing establishes only availability in this test environment.

    Limitations: Subpackage exports, installed-wheel behavior, numerical verification,
    scientific
    validation, UQ, portability, release readiness, and cross-language behavior are
    excluded.
    """
    import ksdft2effmass

    assert ksdft2effmass is not None
