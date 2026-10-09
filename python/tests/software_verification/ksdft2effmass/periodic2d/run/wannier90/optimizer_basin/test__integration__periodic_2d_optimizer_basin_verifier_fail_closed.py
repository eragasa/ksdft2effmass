r"""Artifact-owned fail-closed evidence for the row-052 portable verifier.

Evidence profile: claim_bearing

These tests mutate copies of authenticated compact wires to demonstrate that endpoint
multiplicity and repository-source confinement cannot be bypassed. They do not alter
retained artifacts, access native execution data, validate optimizer convergence,
quantify uncertainty, or record scientific acceptance.
"""

import copy
import hashlib
import json
from collections.abc import Callable
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    Periodic2DOptimizerBasinEncodedDocuments,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.verify import (
    Periodic2DOptimizerBasinCampaignVerificationRequest,
    Periodic2DOptimizerBasinCampaignVerifier,
)
from ksdft2effmass.serialization.json import JsonValue

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DOptimizerBasinCampaignVerifier


def repository_root() -> Path:
    """Return the repository root containing the compact retained evidence."""
    return Path(__file__).resolve().parents[8]


def retained_documents() -> tuple[bytes, bytes]:
    """Read exact retained study and result wires without modifying either artifact."""
    retained = (
        repository_root()
        / "calculations/research-monograph/periodic-2d-optimizer-basin"
    )
    return (
        retained.joinpath("study-input.json").read_bytes(),
        retained.joinpath("result.json").read_bytes(),
    )


def decoded_object(payload: bytes, label: str) -> dict[str, JsonValue]:
    """Decode one retained test fixture as an exact object for mutation only."""
    decoded = json.loads(payload)
    if type(decoded) is not dict:
        raise TypeError(f"retained {label} must be an object")
    return decoded


def encoded_object(value: dict[str, JsonValue]) -> bytes:
    """Encode one test-only alternate wire without claiming canonical identity."""
    return json.dumps(value, allow_nan=False, separators=(",", ":")).encode("utf-8")


def mutated_result(mutation: Callable[[dict[str, JsonValue]], None]) -> bytes:
    """Return a deterministic result wire after applying one test-only mutation."""
    _, result_payload = retained_documents()
    decoded = decoded_object(result_payload, "result")
    mutation(decoded)
    return encoded_object(decoded)


def request(
    result_payload: bytes,
    *,
    root: Path | None = None,
) -> Periodic2DOptimizerBasinCampaignVerificationRequest:
    """Return one verification request using exact retained input bytes."""
    input_payload, _ = retained_documents()
    return Periodic2DOptimizerBasinCampaignVerificationRequest(
        Periodic2DOptimizerBasinEncodedDocuments(input_payload, result_payload),
        repository_root() if root is None else root,
    )


class TestPeriodic2DOptimizerBasinCampaignVerifierFailClosed:
    """Own adversarial structural and repository-boundary evidence for row 052."""

    def test_execute__rejects_duplicate_endpoint_gauge_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRUCTURE-001.

        Requirement: Every configuration contains exactly one endpoint for each of the
        eight declared deterministic initial gauges.

        Acceptance: Duplicating a nonconverged endpoint and adjusting aggregate counts
        cannot pass through set-based identity comparisons.
        """

        def duplicate_endpoint(result: dict[str, JsonValue]) -> None:
            """Duplicate a nonconverged start and reconcile aggregate counts."""
            configurations = result["configurations"]
            summary = result["execution_summary"]
            assert type(configurations) is list
            assert type(summary) is dict
            configuration = configurations[0]
            assert type(configuration) is dict
            starts = configuration["starts"]
            nonconverged_ids = configuration["nonconverged_gauge_ids"]
            assert type(starts) is list
            assert type(nonconverged_ids) is list
            nonconverged_id = nonconverged_ids[0]
            endpoint = next(
                item
                for item in starts
                if type(item) is dict and item["gauge_id"] == nonconverged_id
            )
            starts.append(copy.deepcopy(endpoint))
            assert type(summary["localization_count"]) is int
            assert type(summary["nonconverged_localization_count"]) is int
            summary["localization_count"] += 1
            summary["nonconverged_localization_count"] += 1

        with pytest.raises(AssertionError, match="expected exactly eight starts"):
            SUT().execute(request(mutated_result(duplicate_endpoint)))

    def test_execute__rejects_duplicate_nonconverged_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRUCTURE-002.

        Requirement: The retained nonconverged identity list is a duplicate-free
        representation of the nonconverged endpoint partition.

        Acceptance: Repeating a listed identity cannot disappear through set equality.
        """

        def duplicate_identity(result: dict[str, JsonValue]) -> None:
            """Repeat one nonconverged identifier without changing endpoints."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configuration = configurations[0]
            assert type(configuration) is dict
            nonconverged_ids = configuration["nonconverged_gauge_ids"]
            assert type(nonconverged_ids) is list
            nonconverged_ids.append(nonconverged_ids[0])

        with pytest.raises(
            AssertionError, match="duplicate nonconverged gauge identity"
        ):
            SUT().execute(request(mutated_result(duplicate_identity)))

    @pytest.mark.parametrize(
        "declared_path",
        ["/tmp/outside-row-052-source.py", "../outside-row-052-source.py"],
    )
    def test_execute__rejects_repository_source_escape(
        self, declared_path: str
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-CONFINEMENT-001.

        Requirement: Directly declared compact sources resolve within the explicit
        repository root before any source bytes are read.

        Acceptance: Absolute and parent-traversal paths escaping the repository fail
        with the documented confinement error.
        """

        def escape_source(result: dict[str, JsonValue]) -> None:
            """Replace one compact-source declaration with an escaping path."""
            provenance = result["provenance"]
            assert type(provenance) is dict
            provenance["extractor_path"] = declared_path

        with pytest.raises(ValueError, match="must resolve within repository_root"):
            SUT().execute(request(mutated_result(escape_source)))

    def test_execute__rejects_duplicate_configuration_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRUCTURE-003.

        Requirement: Both study declarations and result configurations contain exactly
        nine unique identities before dictionary correlation can collapse duplicates.

        Acceptance: Replacing the final declaration and result with copies of their
        predecessors fails at the declaration-uniqueness boundary.
        """
        input_payload, result_payload = retained_documents()
        study = decoded_object(input_payload, "study")
        result = decoded_object(result_payload, "result")
        declarations = study["configurations"]
        configurations = result["configurations"]
        assert type(declarations) is list
        assert type(configurations) is list
        declarations[-1] = copy.deepcopy(declarations[-2])
        configurations[-1] = copy.deepcopy(configurations[-2])
        changed_input = encoded_object(study)
        provenance = result["provenance"]
        assert type(provenance) is dict
        provenance["study_input_sha256"] = hashlib.sha256(changed_input).hexdigest()
        documents = Periodic2DOptimizerBasinEncodedDocuments(
            changed_input, encoded_object(result)
        )
        duplicate_request = Periodic2DOptimizerBasinCampaignVerificationRequest(
            documents, repository_root()
        )

        with pytest.raises(
            AssertionError, match="expected nine unique declared configurations"
        ):
            SUT().execute(duplicate_request)

    def test_execute__rejects_incomplete_best_endpoint_copy(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRUCTURE-004.

        Requirement: ``best_observed_converged`` is the complete retained copy of the
        minimum-spread converged endpoint, not merely a matching gauge label.

        Acceptance: Changing one copied spread while preserving its gauge identity
        fails full endpoint correlation.
        """

        def change_best_spread(result: dict[str, JsonValue]) -> None:
            """Change copied best-endpoint data without changing its gauge identity."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configuration = configurations[0]
            assert type(configuration) is dict
            best = configuration["best_observed_converged"]
            assert type(best) is dict
            spread = best["native_total_spread_cell_squared"]
            assert type(spread) is float
            best["native_total_spread_cell_squared"] = spread + 1.0

        with pytest.raises(AssertionError, match="best observed endpoint disagrees"):
            SUT().execute(request(mutated_result(change_best_spread)))

        def substitute_boolean_with_integer(result: dict[str, JsonValue]) -> None:
            """Exploit Python's ordinary equality between ``True`` and integer one."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configuration = configurations[0]
            assert type(configuration) is dict
            best = configuration["best_observed_converged"]
            assert type(best) is dict
            best["completed"] = 1

        with pytest.raises(AssertionError, match="best observed endpoint disagrees"):
            SUT().execute(request(mutated_result(substitute_boolean_with_integer)))

    def test_execute__preserves_campaign_metadata_and_claim_boundary(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-BOUNDARY-001.

        Requirement: Result identity, authority, and claim boundary match the study,
        while input and result retain their distinct exact evidence-status roles.

        Acceptance: Promotional claim text or an input-status substitution fails before
        retained observations can produce a passing verification result.
        """

        def promote_claim(result: dict[str, JsonValue]) -> None:
            """Replace the bounded result claim with an unsupported promotion."""
            result["claim_boundary"] = "This result proves global convergence."

        with pytest.raises(AssertionError, match="campaign claim_boundary disagrees"):
            SUT().execute(request(mutated_result(promote_claim)))

        def substitute_input_status(result: dict[str, JsonValue]) -> None:
            """Erase the distinction between authorized input and calculated result."""
            result["evidence_status"] = "authorized synthetic non-DFT study input"

        with pytest.raises(AssertionError, match="campaign evidence statuses disagree"):
            SUT().execute(request(mutated_result(substitute_input_status)))

    def test_execute__preserves_non_global_dispositions(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-BOUNDARY-002.

        Requirement: Per-configuration and aggregate declarations retain their explicit
        observed-only and non-global/non-general scientific boundaries.

        Acceptance: Clearing either retained boundary flag fails verification.
        """

        def promote_best(result: dict[str, JsonValue]) -> None:
            """Clear one configuration's observed-only best-endpoint boundary."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configuration = configurations[0]
            assert type(configuration) is dict
            configuration["best_is_observed_not_proven_global"] = False

        with pytest.raises(
            AssertionError, match="global-optimum claim boundary changed"
        ):
            SUT().execute(request(mutated_result(promote_best)))

        def promote_assessment(result: dict[str, JsonValue]) -> None:
            """Clear the aggregate non-global/non-general boundary."""
            assessment = result["convergence_assessment"]
            assert type(assessment) is dict
            assessment["not_a_global_or_general_claim"] = False

        with pytest.raises(
            AssertionError, match="global/general claim boundary changed"
        ):
            SUT().execute(request(mutated_result(promote_assessment)))

    def test_execute__correlates_aggregate_process_completion(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRUCTURE-005.

        Requirement: The aggregate completion disposition agrees with the individually
        checked completed endpoints.

        Acceptance: Clearing the aggregate completion flag fails verification even when
        every retained endpoint remains complete.
        """

        def clear_completion(result: dict[str, JsonValue]) -> None:
            """Contradict endpoint completion at the aggregate summary boundary."""
            summary = result["execution_summary"]
            assert type(summary) is dict
            summary["all_localization_processes_completed"] = False

        with pytest.raises(
            AssertionError, match="aggregate process-completion disposition disagrees"
        ):
            SUT().execute(request(mutated_result(clear_completion)))

    def test_execute__rejects_malformed_provenance_digest(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-PROVENANCE-001.

        Requirement: Provenance digests use the shared exact lowercase SHA-256 contract,
        rather than degrading malformed values into generic content mismatches.

        Acceptance: An uppercase declared extractor digest raises ``ValueError`` at the
        digest-representation boundary.
        """

        def uppercase_digest(result: dict[str, JsonValue]) -> None:
            """Replace one valid provenance digest with uppercase hexadecimal."""
            provenance = result["provenance"]
            assert type(provenance) is dict
            digest = provenance["extractor_sha256"]
            assert type(digest) is str
            provenance["extractor_sha256"] = digest.upper()

        with pytest.raises(ValueError, match="lowercase SHA-256 digest"):
            SUT().execute(request(mutated_result(uppercase_digest)))

    def test_execute__correlates_configuration_study_axes(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRUCTURE-006.

        Requirement: Result configurations retain their explicitly declared study axes;
        axes are not inferred from identifiers or numerical controls.

        Acceptance: Replacing a mesh-axis declaration with a cutoff-axis declaration
        fails exact configuration correlation.
        """

        def change_axis(result: dict[str, JsonValue]) -> None:
            """Replace one retained result axis without changing its identifier."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configuration = configurations[0]
            assert type(configuration) is dict
            configuration["study_axes"] = ["cutoff"]

        with pytest.raises(AssertionError, match="study axes disagree"):
            SUT().execute(request(mutated_result(change_axis)))

    def test_execute__correlates_declared_finest_pair_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-BOUNDARY-003.

        Requirement: Mesh and cutoff assessment endpoints are selected from explicit
        study axes and ordered finest-pair controls, never inferred from names.

        Acceptance: Substituting another valid configuration identity fails before its
        occupancy can influence the negative disposition.
        """

        def change_pair_identity(result: dict[str, JsonValue]) -> None:
            """Substitute a valid but undeclared lower mesh endpoint."""
            assessment = result["convergence_assessment"]
            assert type(assessment) is dict
            pair = assessment["mesh_finest_pair"]
            assert type(pair) is dict
            pair["lower_configuration_id"] = "mesh_n11_p4_c11"

        with pytest.raises(
            AssertionError,
            match="mesh_finest_pair: configuration identities disagree",
        ):
            SUT().execute(request(mutated_result(change_pair_identity)))

    def test_execute__preserves_frozen_negative_method_and_text(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-BOUNDARY-004.

        Requirement: The frozen method requires both best and median stability, and the
        result retains its exact negative disposition text.

        Acceptance: Promotional disposition text or removal of the joint-stability
        requirement fails verification.
        """

        def promote_disposition(result: dict[str, JsonValue]) -> None:
            """Replace the retained negative text with an unsupported positive claim."""
            assessment = result["convergence_assessment"]
            assert type(assessment) is dict
            assessment["disposition"] = "supports convergence"

        with pytest.raises(
            AssertionError, match="retained negative disposition text changed"
        ):
            SUT().execute(request(mutated_result(promote_disposition)))

        input_payload, result_payload = retained_documents()
        study = decoded_object(input_payload, "study")
        result = decoded_object(result_payload, "result")
        method = study["convergence_method"]
        assert type(method) is dict
        method["require_both_best_and_median_stability"] = False
        changed_input = encoded_object(study)
        provenance = result["provenance"]
        assert type(provenance) is dict
        provenance["study_input_sha256"] = hashlib.sha256(changed_input).hexdigest()
        documents = Periodic2DOptimizerBasinEncodedDocuments(
            changed_input, encoded_object(result)
        )
        changed_method_request = Periodic2DOptimizerBasinCampaignVerificationRequest(
            documents, repository_root()
        )

        with pytest.raises(
            AssertionError, match="best-and-median stability requirement changed"
        ):
            SUT().execute(changed_method_request)

    def test_execute__correlates_embedding_sensitivity_summaries(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRUCTURE-007.

        Requirement: Each embedding-sensitivity summary is an exact bounded projection
        of its identified full configuration record.

        Acceptance: Changing a copied basin count fails summary correlation.
        """

        def change_embedding_summary(result: dict[str, JsonValue]) -> None:
            """Change one copied embedding basin count only."""
            assessment = result["convergence_assessment"]
            assert type(assessment) is dict
            summaries = assessment["embedding_sensitivity"]
            assert type(summaries) is list
            summary = summaries[0]
            assert type(summary) is dict
            count = summary["observed_converged_basin_count"]
            assert type(count) is int
            summary["observed_converged_basin_count"] = count + 1

        with pytest.raises(
            AssertionError,
            match="embedding sensitivity observed_converged_basin_count disagrees",
        ):
            SUT().execute(request(mutated_result(change_embedding_summary)))

    def test_execute__rejects_in_root_symlink_resolving_outside(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-CONFINEMENT-002.

        Requirement: Source confinement applies to resolved targets rather than lexical
        path prefixes, so an in-root symlink cannot grant access outside the root.

        Acceptance: A relative in-root declaration whose symlink target is outside the
        repository root fails before target bytes are read.
        """
        isolated_root = tmp_path / "repository"
        isolated_root.mkdir()
        outside_source = tmp_path / "outside-source.py"
        outside_source.write_bytes(b"outside")
        isolated_root.joinpath("linked-source.py").symlink_to(outside_source)

        def symlink_source(result: dict[str, JsonValue]) -> None:
            """Declare the in-root symlink as one compact repository source."""
            provenance = result["provenance"]
            assert type(provenance) is dict
            provenance["extractor_path"] = "linked-source.py"

        with pytest.raises(ValueError, match="must resolve within repository_root"):
            SUT().execute(
                request(mutated_result(symlink_source), root=isolated_root.resolve())
            )

    def test_execute__documents_missing_required_schema_field(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-SCHEMA-001.

        Requirement: The public verifier contract declares failure for absent required
        retained-schema fields.

        Acceptance: Removing ``schema_version`` produces the documented ``KeyError``.
        """

        def remove_required_field(result: dict[str, JsonValue]) -> None:
            """Remove one required result field from a test-only wire."""
            del result["schema_version"]

        with pytest.raises(KeyError, match="schema_version"):
            SUT().execute(request(mutated_result(remove_required_field)))
