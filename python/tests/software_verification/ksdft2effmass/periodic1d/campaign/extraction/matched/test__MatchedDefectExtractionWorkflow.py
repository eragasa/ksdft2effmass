r"""Software verification of ``MatchedDefectExtractionWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: matched known-map defect construction from immutable retained
input and accepted periodic-1D parents.

A pass establishes agreement with the retained synthetic capability apart from
implementation-specific provenance identities. It does not validate silicon,
transferability, continuum convergence, or uncertainty quantification.
"""

import json
from pathlib import Path
from typing import cast

import numpy as np
import pytest

from ksdft2effmass.periodic1d.campaign.extraction import matched as matched_extraction
from ksdft2effmass.serialization.json import JsonValue

pytestmark = pytest.mark.software_verification
SUT = matched_extraction.MatchedDefectExtractionWorkflow


class TestMatchedDefectExtractionWorkflow:
    """Own matched known-map extraction workflow evidence."""

    generation_fingerprint_fields = frozenset(
        {
            "alignment_map_sha256",
            "defect_operator_sha256",
            "extracted_operator_sha256",
            "folded_target_sha256",
            "folding_map_sha256",
            "impurity_operator_sha256",
            "lattice_parent_sha256",
            "model_operator_sha256",
            "parabolic_parent_sha256",
            "planted_operator_sha256",
            "raw_operator_sha256",
            "supercell_operator_sha256",
        }
    )

    @staticmethod
    def _repository_root() -> Path:
        return Path(__file__).resolve().parents[8]

    @classmethod
    def _assert_portable_payload_equal(
        cls,
        actual: JsonValue,
        expected: JsonValue,
        *,
        field: str = "root",
    ) -> None:
        """Compare retained semantics without equating floating byte fingerprints."""
        if field in cls.generation_fingerprint_fields:
            for value in (actual, expected):
                assert isinstance(value, str)
                assert len(value) == 64
                assert all(character in "0123456789abcdef" for character in value)
            return
        if expected is None or isinstance(expected, bool | str):
            assert actual == expected
            return
        if isinstance(expected, int):
            assert type(actual) is int
            assert actual == expected
            return
        if isinstance(expected, float):
            assert not isinstance(actual, bool)
            assert isinstance(actual, int | float)
            np.testing.assert_allclose(
                float(actual), expected, rtol=5.0e-13, atol=5.0e-14
            )
            return
        if isinstance(expected, list):
            assert isinstance(actual, list)
            assert len(actual) == len(expected)
            for actual_item, expected_item in zip(actual, expected, strict=True):
                cls._assert_portable_payload_equal(
                    actual_item, expected_item, field=field
                )
            return
        if not isinstance(expected, dict) or not isinstance(actual, dict):
            raise TypeError(f"unsupported JSON values at {field}")
        assert set(actual) == set(expected)
        for key, expected_value in expected.items():
            cls._assert_portable_payload_equal(actual[key], expected_value, field=key)

    def test_method__execute__matches_retained_scientific_payload(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-003.

        Requirement: The maintained workflow reproduces the retained version-one
        synthetic scientific payload while recording its own implementation identity.

        Method: Decode the retained input, authenticate and load its accepted parent
        artifacts, execute the maintained workflow, and compare all fields except the
        provenance block.

        Oracle: Closed decoded JSON documents after removing implementation-specific
        provenance. Discrete fields agree exactly, numerical fields use the verifier's
        reviewed tolerance, and generation-time matrix digests remain content
        identities.

        Acceptance: Every retained scientific, numerical, limitation, and status field
        agrees under its declared comparator; both documents retain valid matrix-digest
        encodings without claiming cross-platform binary64 byte identity.

        Interpretation: A pass establishes behavior preservation for the matched
        known-map capability under the retained input.

        Limitations: Excluding provenance is necessary because the maintained package
        has different source paths and hashes from the historical implementation.
        """
        root = self._repository_root()
        directory = root / "calculations/research-monograph/impurity-defect-1d"
        input_path = directory / "input.json"
        specification = (
            matched_extraction.MatchedDefectExtractionInputDeserializer().execute(
                input_path.read_bytes()
            )
        )
        parent = matched_extraction.MatchedDefectParentDataLoader().execute(
            specification.parent, root
        )

        workflow_result = SUT().execute(
            specification,
            parent,
            root,
            input_path,
            directory / "run_experiment.py",
        )
        generated_path = tmp_path / "result.json"
        generated_path.write_bytes(workflow_result.document)
        matched_extraction.MatchedDefectExtractionResultVerifier().execute(
            generated_path, root
        )
        generated = cast(
            dict[str, JsonValue],
            json.loads(workflow_result.document.decode("utf-8")),
        )
        retained = cast(
            dict[str, JsonValue],
            json.loads((directory / "result.json").read_text(encoding="utf-8")),
        )
        generated.pop("provenance")
        retained.pop("provenance")

        self._assert_portable_payload_equal(generated, retained)
