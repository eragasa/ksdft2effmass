r"""Software verification of the version-two PIAB1D input adapter."""

from pathlib import Path

import pytest

from ksdft2effmass.model_systems.piab1d import Piab1dStudyInputDeserializer

pytestmark = pytest.mark.software_verification
SUT = Piab1dStudyInputDeserializer


class TestPiab1dStudyInputDeserializer:
    """Own software evidence for the closed particle-in-box input adapter."""

    @staticmethod
    def input_path() -> Path:
        return (
            Path(__file__).resolve().parents[6]
            / "calculations"
            / "piab1d"
            / "input.json"
        )

    def test_method__execute__decodes_physkit_model_and_quadrature(self) -> None:
        definition = Piab1dStudyInputDeserializer().execute(
            self.input_path().read_bytes()
        )

        assert definition.model.length == 1.0
        assert definition.model.mass == 1.0
        assert definition.model.hbar_quantity.magnitude == 1.0
        assert definition.Nx_pts_interior == 8
        assert definition.N_retained_eigenpairs == 3
        assert definition.quadrature is True

    def test_method__execute__accepts_explicitly_disabled_quadrature(self) -> None:
        payload = self.input_path().read_bytes().replace(
            b'"quadrature": true',
            b'"quadrature": false',
        )

        definition = Piab1dStudyInputDeserializer().execute(payload)

        assert definition.quadrature is False

    def test_method__execute__rejects_numeric_quadrature_flag(self) -> None:
        payload = self.input_path().read_bytes().replace(
            b'"quadrature": true',
            b'"quadrature": 1',
        )

        with pytest.raises(TypeError, match="quadrature"):
            Piab1dStudyInputDeserializer().execute(payload)
