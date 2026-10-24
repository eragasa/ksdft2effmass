r"""Software verification of PIAB1D version-two result serialization."""

import json
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.model_systems.piab1d import (
    JsonValue,
    Piab1dResidualStudyEvaluator,
    Piab1dStudyInputDeserializer,
    Piab1dStudyResultSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Piab1dStudyResultSerializer


class TestPiab1dStudyResultSerializer:
    """Own software evidence for the particle-in-box result serializer."""

    @staticmethod
    def repository_root() -> Path:
        return Path(__file__).resolve().parents[6]

    def test_method__execute__retains_distinct_normalizations_and_sources(self) -> None:
        root = self.repository_root()
        calculation = root / "calculations" / "piab1d"
        input_path = calculation / "input.json"
        definition = Piab1dStudyInputDeserializer().execute(input_path.read_bytes())
        result = Piab1dResidualStudyEvaluator().execute(definition)
        authored = cast(
            dict[str, JsonValue],
            json.loads(
                Piab1dStudyResultSerializer()
                .execute(result, input_path, calculation / "run_experiment.py", root)
                .decode("utf-8")
            ),
        )

        assert authored["schema_version"] == 2
        quadrature = cast(dict[str, JsonValue], authored["quadrature"])
        assert quadrature["enabled"] is True
        assert quadrature["rule_version"] == 1
        matrices = cast(dict[str, JsonValue], authored["matrices"])
        assert "retained_eigenvectors_euclidean" in matrices
        assert "retained_nodal_amplitudes_quadrature_normalized" in matrices
        provenance = cast(dict[str, JsonValue], authored["provenance"])
        assert provenance["eigensolver"] == "scipy.linalg.eigh_tridiagonal"
        identities = provenance["implementation_identities"]
        assert isinstance(identities, list)
        paths = {
            cast(dict[str, JsonValue], identity)["path"] for identity in identities
        }
        assert paths == {
            "python/src/ksdft2effmass/model_systems/study/base.py",
            "python/src/ksdft2effmass/analysis/operators/compression_residuals.py",
            "python/src/ksdft2effmass/operators/hamiltonians.py",
            "python/src/ksdft2effmass/operators/subspaces.py",
            "python/src/ksdft2effmass/linalg/quantities.py",
            "python/src/ksdft2effmass/model_systems/piab1d/study/records.py",
            "python/src/ksdft2effmass/model_systems/piab1d/study/input.py",
            "python/src/ksdft2effmass/model_systems/piab1d/study/evaluation.py",
            "python/src/ksdft2effmass/model_systems/piab1d/study/serialization.py",
        }
        dependencies = provenance["dependency_identities"]
        assert isinstance(dependencies, list)
        physkit = cast(dict[str, JsonValue], dependencies[1])
        assert physkit["revision"] == "ccdcfcda4a2c7cef29be01b3c09831fda022c55a"
