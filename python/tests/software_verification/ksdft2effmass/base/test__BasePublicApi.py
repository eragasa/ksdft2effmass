"""Public API verification for package-wide data-object bases."""

from __future__ import annotations

import ksdft2effmass.base as api


class TestBasePublicApi:
    """Require one explicit thin base hierarchy at the package root."""

    def test__public_api__exports_exact_thin_hierarchy(self) -> None:
        assert api.__all__ == (
            "DataObject",
            "DataObjectActionRequest",
            "DataObjectActionResult",
            "DataObjectActionizer",
            "DataObjectModel",
        )
