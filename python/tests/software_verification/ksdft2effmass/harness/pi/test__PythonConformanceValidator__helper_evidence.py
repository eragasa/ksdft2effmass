r"""Software verification of ``PythonConformanceValidator``.

Evidence profile: claim_bearing

Bounded artifact scope: collected-test claims versus non-test helper documentation.

Facet and represented meaning

The validator must require evidence from actual tests, not ID-free support methods.

Intrinsic and cross-object scope

The public validator consumes explicit immutable source and ownership bytes. The
independent oracle is a literal source fixture with one test and one helper.

VVUQ and scientific exclusions

Structural software verification only; no semantic, numerical, scientific, UQ or
human-acceptance conclusion follows from conformance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.conformance.python import (
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)

pytestmark = pytest.mark.software_verification
SUT = PythonConformanceValidator


class TestPythonConformanceValidator:
    """Own the helper-versus-evidence facet without duplicating legacy rules."""

    @staticmethod
    def make_source() -> bytes:
        return (
            Path(__file__).parent / "resources/helper-evidence-source.py.txt"
        ).read_bytes()

    @staticmethod
    def validate_source(source: bytes) -> PythonConformanceResult:
        ownership = b"""{"schema_version":1,"modules":[{
            "path":"test__helper_evidence_fixture.py","mode":"artifact_owned",
            "evidence_class":"software_verification",
            "evidence_profile":"claim_bearing","artifact":"helper evidence fixture"
        }]}"""
        return SUT().execute(
            PythonConformanceRequest(
                (PythonModuleSource("test__helper_evidence_fixture.py", source),),
                "fixture-ownership.json",
                ownership,
            )
        )

    @pytest.mark.parametrize(
        "documentation",
        [
            pytest.param(b"", id="short_undocumented_helper"),
            pytest.param(
                b'        """Return the literal needed by the consuming test."""\n',
                id="ordinary_support_prose",
            ),
            pytest.param(
                b'        """Support SV-HELPER-FIXTURE-001 '
                b'without owning its claim."""\n',
                id="ordinary_reference",
            ),
            pytest.param(
                b'        """Evidence ID: Helper owns no identifier; '
                b'references SV-HELPER-FIXTURE-001."""\n',
                id="legacy_nonownership_reference",
            ),
            pytest.param(
                b'        """Evidence ID: This helper owns no identifier."""\n',
                id="legacy_this_helper_nonownership",
            ),
        ],
    )
    def test_method__execute__accepts_id_free_helpers(
        self, documentation: bytes
    ) -> None:
        """Evidence ID: SV-HELPER-GATE-001

        Requirement: Helpers need no per-test evidence paragraphs or identifier.

        Method: Add no docstring, ordinary prose, or a legitimate reference to a
        hand-authored source fixture and invoke the public validator.

        Oracle: The fixture has exactly one actual test and one support method.

        Acceptance: PASS, no findings, one helper, one test, one evidence owner.

        Interpretation: Failure detects evidence obligations imposed on non-tests.

        Limitations: Structure does not establish the consuming test's semantic quality.
        """
        source = self.make_source().replace(
            b"        return 1", documentation + b"        return 1"
        )
        result = self.validate_source(source)
        assert result.status == "PASS"
        assert result.findings == ()
        assert result.helper_functions == 1
        assert result.test_functions == 1
        assert result.unique_evidence_owners == 1

    @pytest.mark.parametrize(
        "declaration",
        [
            pytest.param(b"Evidence ID: SV-HELPER-CLAIM-001", id="actual_helper_claim"),
            pytest.param(b"Evidence ID: invalid", id="malformed_helper_claim"),
            pytest.param(
                b"Evidence ID: Helper owns no identifier.\n\n        "
                b"Evidence ID: SV-HELPER-CLAIM-001",
                id="second_claim_after_nonownership",
            ),
        ],
    )
    def test_method__execute__rejects_helper_evidence_ownership(
        self, declaration: bytes
    ) -> None:
        """Evidence ID: SV-HELPER-GATE-002

        Requirement: A non-test helper must not acquire evidence ownership.

        Method: Add an explicit identifier declaration to the fixture's helper.

        Oracle: Only the fixture's collected test may own its evidence identifier.

        Acceptance: FAIL with TE.HELPER_ID, while only one actual owner is counted.

        Interpretation: Failure permits false helper evidence or duplicate projection.

        Limitations: Ordinary references remain accepted by separate partitions.
        """
        source = self.make_source().replace(
            b"        return 1", b'        """' + declaration + b'"""\n        return 1'
        )
        result = self.validate_source(source)
        assert result.status == "FAIL"
        assert tuple(item.code for item in result.findings) == ("TE.HELPER_ID",)
        assert result.unique_evidence_owners == 1

    @pytest.mark.parametrize(
        "original,replacement,code",
        [
            pytest.param(
                b"        Requirement: A literal retains its represented value.\n\n",
                b"",
                "TE.FUNCTION_DOC",
                id="missing_collected_test_field",
            ),
            pytest.param(
                b"SV-HELPER-FIXTURE-001",
                b"not-an-identifier",
                "TE.EVIDENCE_ID",
                id="invalid_collected_test_id",
            ),
        ],
    )
    def test_method__execute__still_requires_collected_test_claims(
        self, original: bytes, replacement: bytes, code: str
    ) -> None:
        """Evidence ID: SV-HELPER-GATE-003

        Requirement: Relaxing helper prose must not weaken actual test evidence.

        Method: Remove a required test field or invalidate its identifier.

        Oracle: Claim-bearing profile still requires the actual test's fields and ID.

        Acceptance: FAIL contains the exact corresponding rule code.

        Interpretation: Failure detects a broad documentation or evidence bypass.

        Limitations: Existing regressions cover duplicate actual-test identities.
        """
        result = self.validate_source(self.make_source().replace(original, replacement))
        assert result.status == "FAIL"
        assert code in tuple(item.code for item in result.findings)
