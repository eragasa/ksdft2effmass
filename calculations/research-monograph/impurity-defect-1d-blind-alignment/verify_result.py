#!/usr/bin/env python3
"""Independently verify the retained blind-alignment result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]


class BlindAlignmentResultVerifier:
    """Rebuild the hidden-map benchmark without importing its runner."""

    __slots__ = ()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        result = self._load(result_path)
        if self._integer(result["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported result schema")
        if result["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        provenance = self._mapping(result["provenance"], "provenance")
        input_path = repository_root / self._string(
            provenance["input_path"], "input path"
        )
        script_path = repository_root / self._string(
            provenance["script_path"], "script path"
        )
        self._assert_text(
            self._sha256(input_path), provenance["input_sha256"], "input sha256"
        )
        self._assert_text(
            self._sha256(script_path), provenance["script_sha256"], "script sha256"
        )
        source = self._load(input_path)
        baseline_source, baseline_result, parent = self._load_sources(
            source, result, repository_root
        )
        size, momentum, host, transforms, defects, shift = self._baseline(
            baseline_source, baseline_result, parent
        )
        policy = self._mapping(source["inference_policy"], "policy")
        rank_tolerance = self._real(policy["anchor_rank_tolerance"], "rank tolerance")
        condition_limit = self._real(
            policy["maximum_anchor_condition_number"], "condition limit"
        )
        angle_limit = self._real(
            policy["maximum_principal_angle_radians"], "angle limit"
        )
        minimum_energy_rank = self._integer(
            policy["minimum_energy_anchor_rank"], "minimum energy rank"
        )
        core_radius = self._integer(policy["core_radius_cells"], "core radius")
        exact_source = self._records(source["exact_cases"], "exact cases")
        exact_result = self._records(result["exact_full_rank_cases"], "exact results")
        if len(exact_source) != len(exact_result):
            raise ValueError("exact case count mismatch")
        for request, retained in zip(exact_source, exact_result, strict=True):
            identifier = self._string(request["id"], "exact id")
            defect_id = self._string(request["defect_id"], "defect id")
            spin_count = self._integer(request["spin_count"], "spin count")
            minimum = self._real(
                request["minimum_anchor_singular_value"], "minimum singular"
            )
            recalculated = self._calculate_case(
                identifier,
                host,
                transforms[spin_count],
                defects[defect_id],
                shift,
                size,
                spin_count,
                minimum,
                0.0,
                0,
                core_radius,
                rank_tolerance,
                condition_limit,
                angle_limit,
                minimum_energy_rank,
            )
            self._assert_record(retained, recalculated)
        noise_source = self._mapping(source["noise_sweep"], "noise sweep")
        noise_result = self._records(result["noise_sweep"], "noise results")
        radians = self._reals(noise_source["unitary_noise_radians"], "noise radians")
        if len(noise_result) != len(radians):
            raise ValueError("noise case count mismatch")
        noise_id = self._string(noise_source["id"], "noise id")
        noise_defect = self._string(noise_source["defect_id"], "noise defect")
        noise_spin = self._integer(noise_source["spin_count"], "noise spin")
        noise_minimum = self._real(
            noise_source["minimum_anchor_singular_value"], "noise minimum"
        )
        noise_seed = self._integer(noise_source["generator_seed"], "noise seed")
        for value, retained in zip(radians, noise_result, strict=True):
            identifier = f"{noise_id}-{value:.1e}"
            recalculated = self._calculate_case(
                identifier,
                host,
                transforms[noise_spin],
                defects[noise_defect],
                shift,
                size,
                noise_spin,
                noise_minimum,
                value,
                noise_seed,
                core_radius,
                rank_tolerance,
                condition_limit,
                angle_limit,
                minimum_energy_rank,
            )
            recalculated["unitary_noise_radians"] = value
            self._assert_record(retained, recalculated)
        self._verify_gauge(
            source,
            result,
            host,
            transforms,
            defects,
            shift,
            size,
            core_radius,
            rank_tolerance,
            condition_limit,
            angle_limit,
            minimum_energy_rank,
        )
        self._verify_stops(source, result, condition_limit, angle_limit)
        self._verify_diagnostics(
            source,
            result,
            host,
            transforms,
            defects,
            shift,
            size,
            core_radius,
            rank_tolerance,
            condition_limit,
            angle_limit,
            minimum_energy_rank,
        )
        information = self._mapping(
            result["information_boundary"], "information boundary"
        )
        declared = self._mapping(
            information["declared_observation_contract"],
            "declared observation contract",
        )
        source_declared = self._mapping(
            source["observation_information_contract"],
            "source observation contract",
        )
        if declared != source_declared or set(declared) != {
            "anchor_cross_covariance",
            "site_anchor_labels",
            "orbital_labels",
            "spin_frame",
            "energy_reference",
        }:
            raise ValueError("observation information contract mismatch")
        withheld = information["withheld_from_inference"]
        if not isinstance(withheld, list) or len(withheld) != 4:
            raise ValueError("withheld inference information is incomplete")
        limitations = result["limitations"]
        if not isinstance(limitations, list) or len(limitations) != 4:
            raise ValueError("four limitations are required")

    def _load_sources(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        root: Path,
    ) -> tuple[dict[str, JsonValue], dict[str, JsonValue], dict[str, JsonValue]]:
        sources = self._mapping(source["baseline_sources"], "baseline sources")
        input_path = root / self._string(sources["input_path"], "baseline input")
        result_path = root / self._string(sources["result_path"], "baseline result")
        input_sha = self._string(sources["input_sha256"], "baseline input sha")
        result_sha = self._string(sources["result_sha256"], "baseline result sha")
        self._assert_text(self._sha256(input_path), input_sha, "baseline input")
        self._assert_text(self._sha256(result_path), result_sha, "baseline result")
        baseline_source = self._load(input_path)
        baseline_result = self._load(result_path)
        parent_source = self._mapping(
            baseline_source["parent_sources"], "parent sources"
        )
        parent_path = root / self._string(
            parent_source["composite_result_path"], "parent path"
        )
        parent_sha = self._string(
            parent_source["composite_result_sha256"], "parent sha"
        )
        self._assert_text(self._sha256(parent_path), parent_sha, "parent")
        retained_identities = self._records(
            result["source_identities"], "source identities"
        )
        retained = {
            self._string(item["path"], "identity path"): self._string(
                item["sha256"], "identity sha"
            )
            for item in retained_identities
        }
        expected = {
            input_path.relative_to(root).as_posix(): input_sha,
            result_path.relative_to(root).as_posix(): result_sha,
            parent_path.relative_to(root).as_posix(): parent_sha,
        }
        if retained != expected:
            raise ValueError("source identity set mismatch")
        return baseline_source, baseline_result, self._load(parent_path)

    def _baseline(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        parent: dict[str, JsonValue],
    ) -> tuple[
        int,
        float,
        ComplexMatrix,
        dict[int, ComplexMatrix],
        dict[str, ComplexMatrix],
        float,
    ]:
        extraction = self._mapping(source["extraction_control"], "extraction")
        alignment = self._mapping(source["alignment_control"], "alignment")
        parent_source = self._mapping(source["parent_sources"], "parent source")
        size = self._integer(extraction["supercell_size"], "size")
        momentum = (
            self._real(extraction["reduced_momentum_times_supercell"], "momentum")
            / size
        )
        group_id = self._string(parent_source["composite_group_id"], "group id")
        hopping_range = self._integer(
            parent_source["parent_hopping_range_cells"], "hopping range"
        )
        groups = self._records(parent["groups"], "groups")
        matches = [item for item in groups if item["id"] == group_id]
        if len(matches) != 1:
            raise ValueError("parent group mismatch")
        hoppings: list[tuple[int, ComplexMatrix]] = []
        for record in self._records(matches[0]["smooth_hopping_blocks"], "hoppings"):
            representative = self._integer(
                record["representative_cells"], "representative"
            )
            if abs(representative) <= hopping_range:
                hoppings.append(
                    (
                        representative,
                        self._complex_matrix(record["matrix"], "hopping"),
                    )
                )
        host = self._supercell(tuple(hoppings), size, momentum)
        transforms = {
            1: self._transform(size, momentum, 1, alignment),
            2: self._transform(size, momentum, 2, alignment),
        }
        defects: dict[str, ComplexMatrix] = {}
        for record in self._records(
            result["extraction_controls"], "extraction controls"
        ):
            identifier = self._string(record["id"], "defect id")
            spin_count = self._integer(record["spin_count"], "defect spin")
            defects[identifier] = self._compact(
                record["compact_planted_blocks"], size, 2 * spin_count
            )
        shift = self._real(alignment["energy_reference_shift"], "energy shift")
        return size, momentum, host, transforms, defects, shift

    def _calculate_case(
        self,
        identifier: str,
        spinless_host: ComplexMatrix,
        transform: ComplexMatrix,
        defect: ComplexMatrix,
        shift: float,
        size: int,
        spin_count: int,
        minimum_singular: float,
        noise_radians: float,
        seed: int,
        core_radius: int,
        rank_tolerance: float,
        condition_limit: float,
        angle_limit: float,
        minimum_energy_rank: int,
    ) -> dict[str, JsonValue]:
        host = (
            spinless_host
            if spin_count == 1
            else np.asarray(np.kron(spinless_host, np.eye(2)), dtype=np.complex128)
        )
        dimension = host.shape[0]
        noise = self._unitary_noise(dimension, noise_radians, seed)
        anchors = (
            np.diag(np.linspace(1.0, minimum_singular, dimension)) @ noise @ transform
        )
        candidate = transform.conj().T @ (host + defect) @ transform + shift * np.eye(
            dimension
        )
        exterior = self._exterior(size, 2 * spin_count, core_radius)
        calculated = self._infer(
            host,
            candidate,
            anchors,
            np.eye(dimension, dtype=np.complex128),
            exterior,
            rank_tolerance,
            condition_limit,
            angle_limit,
            minimum_energy_rank,
            False,
        )
        return self._evaluate(identifier, calculated, transform, defect, shift, size)

    def _verify_gauge(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        spinless_host: ComplexMatrix,
        transforms: dict[int, ComplexMatrix],
        defects: dict[str, ComplexMatrix],
        shift: float,
        size: int,
        core_radius: int,
        rank_tolerance: float,
        condition_limit: float,
        angle_limit: float,
        minimum_energy_rank: int,
    ) -> None:
        request = self._mapping(source["gauge_equivalent_case"], "gauge request")
        identifier = self._string(request["id"], "gauge id")
        defect_id = self._string(request["defect_id"], "gauge defect")
        spin_count = self._integer(request["spin_count"], "gauge spin")
        identified_sites = self._integer(
            request["identified_site_count"], "identified sites"
        )
        minimum = self._real(
            request["minimum_nonzero_anchor_singular_value"], "gauge minimum"
        )
        rotation = self._real(
            request["complement_rotation_radians"], "complement rotation"
        )
        seed = self._integer(request["generator_seed"], "gauge seed")
        host = (
            spinless_host
            if spin_count == 1
            else np.asarray(np.kron(spinless_host, np.eye(2)), dtype=np.complex128)
        )
        transform = transforms[spin_count]
        defect = defects[defect_id]
        dimension = host.shape[0]
        active_dimension = identified_sites * 2 * spin_count
        singular = np.zeros(dimension)
        singular[:active_dimension] = np.linspace(1.0, minimum, active_dimension)
        anchors = np.diag(singular) @ transform
        candidate = transform.conj().T @ (host + defect) @ transform + shift * np.eye(
            dimension
        )
        calculated = self._infer(
            host,
            candidate,
            anchors,
            np.eye(dimension, dtype=np.complex128),
            self._exterior(size, 2 * spin_count, core_radius),
            rank_tolerance,
            condition_limit,
            angle_limit,
            minimum_energy_rank,
            True,
        )
        record = self._evaluate(identifier, calculated, transform, defect, shift, size)
        alignment = calculated["alignment"]
        projector = calculated["projector"]
        if not isinstance(alignment, np.ndarray) or not isinstance(
            projector, np.ndarray
        ):
            raise TypeError("gauge case must return matrices")
        complement = np.eye(dimension) - projector
        values, vectors = np.linalg.eigh(complement)
        basis = vectors[:, values > 0.5]
        noise = self._unitary_noise(basis.shape[1], rotation, seed)
        rotated = projector + basis @ noise @ basis.conj().T
        first = transform
        second = rotated @ transform
        first_extraction = (
            first @ (candidate - shift * np.eye(dimension)) @ first.conj().T - host
        )
        second_extraction = (
            second @ (candidate - shift * np.eye(dimension)) @ second.conj().T - host
        )
        record["identified_dimension"] = active_dimension
        record["unidentified_complement_dimension"] = dimension - active_dimension
        record["full_completion_extraction_disagreement"] = self._norm(
            first_extraction - second_extraction
        )
        record["compressed_completion_extraction_disagreement"] = self._norm(
            projector @ (first_extraction - second_extraction) @ projector
        )
        record["partial_map_agreement_between_completions"] = self._norm(
            projector @ first - projector @ second
        )
        retained = self._mapping(result["gauge_equivalent_case"], "gauge result")
        self._assert_record(retained, record)

    def _verify_stops(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        condition_limit: float,
        angle_limit: float,
    ) -> None:
        requests = self._records(source["stopping_cases"], "stopping requests")
        retained = self._records(result["stopping_cases"], "stopping results")
        if len(requests) != len(retained):
            raise ValueError("stopping case count mismatch")
        expected = {
            "anchor-condition": "BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED",
            "principal-angle": "BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED",
            "rank-mismatch": "BLIND_ALIGNMENT.RANK_MISMATCH",
            "spin-mismatch": "BLIND_ALIGNMENT.SPIN_MISMATCH",
            "energy-anchor": "BLIND_ALIGNMENT.ENERGY_ANCHOR_INSUFFICIENT",
        }
        for request, record in zip(requests, retained, strict=True):
            kind = self._string(request["kind"], "stopping kind")
            self._assert_text(
                self._string(request["id"], "stopping id"),
                record["id"],
                "stopping id",
            )
            if record["status"] != "stopped":
                raise ValueError("stopping case returned a nominal alignment")
            issues = record["issue_codes"]
            if not isinstance(issues, list) or issues != [expected[kind]]:
                raise ValueError("stopping issue mismatch")
            if (
                record["alignment_map"] is not None
                or record["extracted_operator"] is not None
                or record["inferred_energy_shift"] is not None
            ):
                raise ValueError("stopping case retained nominal outputs")
            if kind == "anchor-condition":
                condition = self._real(record["anchor_condition_number"], "condition")
                if condition <= condition_limit:
                    raise ValueError("ill-conditioned case did not exceed limit")
            if kind == "principal-angle":
                angle = self._real(record["maximum_principal_angle_radians"], "angle")
                if angle <= angle_limit:
                    raise ValueError("principal-angle case did not exceed limit")

    def _verify_diagnostics(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        spinless_host: ComplexMatrix,
        transforms: dict[int, ComplexMatrix],
        defects: dict[str, ComplexMatrix],
        shift: float,
        size: int,
        core_radius: int,
        rank_tolerance: float,
        condition_limit: float,
        angle_limit: float,
        minimum_energy_rank: int,
    ) -> None:
        request = self._mapping(source["debugging_diagnostics"], "diagnostic request")
        retained = self._mapping(result["debugging_diagnostics"], "diagnostic result")
        host = spinless_host
        transform = transforms[1]
        defect = defects["orbital-onsite"]
        dimension = host.shape[0]
        candidate = transform.conj().T @ (host + defect) @ transform + shift * np.eye(
            dimension
        )
        exterior = self._exterior(size, 2, core_radius)

        minima = self._reals(
            request["conditioning_minimum_singular_values"],
            "conditioning minima",
        )
        noise_amplitude = self._real(
            request["conditioning_additive_anchor_noise"],
            "conditioning noise",
        )
        noise_seed = self._integer(
            request["conditioning_noise_seed"], "conditioning seed"
        )
        additive = self._normalized_complex_noise(dimension, dimension, noise_seed)
        expected_conditions: list[dict[str, JsonValue]] = []
        for minimum in minima:
            identifier = f"conditioning-{minimum:.1e}"
            anchors = (
                np.diag(np.linspace(1.0, minimum, dimension)) @ transform
                + noise_amplitude * additive
            )
            singular = np.linalg.svd(anchors, compute_uv=False)
            rank = int(np.sum(singular > rank_tolerance))
            active = singular[singular > rank_tolerance]
            actual_minimum = float(np.min(active))
            condition = float(np.max(active) / actual_minimum)
            if condition > condition_limit:
                record = self._stop_record(
                    identifier,
                    "BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED",
                    rank=rank,
                    condition=condition,
                    minimum=actual_minimum,
                    angle=0.0,
                )
            else:
                calculated = self._infer(
                    host,
                    candidate,
                    anchors,
                    np.eye(dimension, dtype=np.complex128),
                    exterior,
                    rank_tolerance,
                    condition_limit,
                    angle_limit,
                    minimum_energy_rank,
                    False,
                )
                record = self._evaluate(
                    identifier,
                    calculated,
                    transform,
                    defect,
                    shift,
                    size,
                )
            record["requested_minimum_anchor_singular_value"] = minimum
            record["additive_anchor_noise_spectral_norm"] = noise_amplitude
            expected_conditions.append(record)
        self._assert_records(
            self._records(retained["conditioning_boundary"], "conditioning result"),
            tuple(expected_conditions),
        )

        angles = self._reals(request["principal_angle_radians"], "principal angles")
        expected_angles: list[dict[str, JsonValue]] = []
        anchors = np.diag(np.linspace(1.0, 0.75, dimension)) @ transform
        for angle in angles:
            identifier = f"principal-angle-{angle:.2f}"
            overlap_singular = np.ones(dimension)
            overlap_singular[-1] = np.cos(angle)
            overlap = np.diag(overlap_singular).astype(np.complex128)
            if angle > angle_limit:
                record = self._stop_record(
                    identifier,
                    "BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED",
                    angle=angle,
                )
            else:
                calculated = self._infer(
                    host,
                    candidate,
                    anchors,
                    overlap,
                    exterior,
                    rank_tolerance,
                    condition_limit,
                    angle_limit,
                    minimum_energy_rank,
                    False,
                )
                record = self._evaluate(
                    identifier,
                    calculated,
                    transform,
                    defect,
                    shift,
                    size,
                )
            record["requested_principal_angle_radians"] = angle
            record["minimum_subspace_overlap_singular_value"] = float(np.cos(angle))
            record["diagnostic_reference_basis_indices"] = [dimension - 1]
            expected_angles.append(record)
        self._assert_records(
            self._records(retained["principal_angle_boundary"], "angle result"),
            tuple(expected_angles),
        )

        rank_drop = self._integer(request["rank_drop"], "rank drop")
        candidate_dimension = dimension - rank_drop
        isometry = transform[:, :candidate_dimension]
        projector = isometry @ isometry.conj().T
        rank_candidate = isometry.conj().T @ host @ isometry + shift * np.eye(
            candidate_dimension
        )
        rank_anchors = isometry @ np.diag(np.linspace(1.0, 0.75, candidate_dimension))
        rank_calculated = self._infer(
            host,
            rank_candidate,
            rank_anchors,
            isometry,
            projector,
            rank_tolerance,
            condition_limit,
            angle_limit,
            minimum_energy_rank,
            True,
        )
        rank_expected = self._evaluate(
            "rank-reconciled-partial-isometry",
            rank_calculated,
            isometry,
            np.zeros_like(host, dtype=np.complex128),
            shift,
            size,
        )
        rank_expected["direct_comparison_issue_code"] = "BLIND_ALIGNMENT.RANK_MISMATCH"
        rank_expected["reference_dimension"] = dimension
        rank_expected["candidate_dimension"] = candidate_dimension
        rank_expected["dropped_dimension"] = rank_drop
        rank_expected["resolution"] = "explicit_rectangular_partial_isometry"
        self._assert_record(
            self._mapping(retained["rank_reconciliation"], "rank result"),
            rank_expected,
        )

        spin_calculated = self._calculate_case(
            "spin-lifted-reconciliation",
            spinless_host,
            transforms[2],
            defects["spin-mixing"],
            shift,
            size,
            2,
            0.65,
            0.0,
            0,
            core_radius,
            rank_tolerance,
            condition_limit,
            angle_limit,
            minimum_energy_rank,
        )
        spin_defect = defects["spin-mixing"]
        spatial_dimension = spin_defect.shape[0] // 2
        tensor = spin_defect.reshape(spatial_dimension, 2, spatial_dimension, 2)
        spin_independent = 0.5 * np.einsum("asbs->ab", tensor)
        lifted = np.kron(spin_independent, np.eye(2))
        spin_retained = self._mapping(retained["spin_reconciliation"], "spin result")
        if (
            spin_retained["direct_comparison_status"] != "stopped"
            or spin_retained["direct_comparison_issue_code"]
            != "BLIND_ALIGNMENT.SPIN_MISMATCH"
            or spin_retained["resolution"]
            != "explicit_spin_lift_to_common_spinor_space"
            or spin_retained["lossless_spin_restriction_available"] is not False
        ):
            raise ValueError("spin reconciliation metadata mismatch")
        np.testing.assert_allclose(
            self._real(
                spin_retained["spin_independent_restriction_residual"],
                "spin residual",
            ),
            self._norm(spin_defect - lifted),
            rtol=5.0e-12,
            atol=5.0e-14,
        )
        self._assert_record(
            self._mapping(spin_retained["lifted_alignment"], "lifted alignment"),
            spin_calculated,
        )

        energy_ranks = self._integers(request["energy_anchor_ranks"], "energy ranks")
        exterior_indices = np.flatnonzero(np.diag(exterior).real > 0.5)
        expected_energy: list[dict[str, JsonValue]] = []
        for requested_rank in energy_ranks:
            identifier = f"energy-anchor-rank-{requested_rank}"
            energy_anchor = np.zeros_like(exterior)
            selected = exterior_indices[:requested_rank]
            energy_anchor[selected, selected] = 1.0
            if requested_rank < minimum_energy_rank:
                record = self._stop_record(
                    identifier,
                    "BLIND_ALIGNMENT.ENERGY_ANCHOR_INSUFFICIENT",
                    rank=dimension,
                    condition=4.0 / 3.0,
                    minimum=0.75,
                    angle=0.0,
                    energy_rank=float(requested_rank),
                )
            else:
                calculated = self._infer(
                    host,
                    candidate,
                    anchors,
                    np.eye(dimension, dtype=np.complex128),
                    energy_anchor,
                    rank_tolerance,
                    condition_limit,
                    angle_limit,
                    minimum_energy_rank,
                    False,
                )
                record = self._evaluate(
                    identifier,
                    calculated,
                    transform,
                    defect,
                    shift,
                    size,
                )
            record["requested_energy_anchor_rank"] = requested_rank
            expected_energy.append(record)
        self._assert_records(
            self._records(retained["energy_anchor_boundary"], "energy result"),
            tuple(expected_energy),
        )
        if retained["interpretation"] != (
            "Neighboring admissible probes diagnose the stopping boundaries; "
            "they do not weaken or replace the original negative controls."
        ):
            raise ValueError("diagnostic interpretation mismatch")

    def _infer(
        self,
        host: ComplexMatrix,
        candidate: ComplexMatrix,
        anchors: ComplexMatrix,
        subspace_overlap: ComplexMatrix,
        exterior: ComplexMatrix,
        rank_tolerance: float,
        condition_limit: float,
        angle_limit: float,
        minimum_energy_rank: int,
        allow_partial: bool,
    ) -> dict[str, ComplexMatrix | float | int | str]:
        dimension = host.shape[0]
        subspace_singular = np.linalg.svd(subspace_overlap, compute_uv=False)
        maximum_angle = float(np.arccos(np.min(np.clip(subspace_singular, 0.0, 1.0))))
        if maximum_angle > angle_limit:
            raise ValueError("unexpected incompatible subspace in successful case")
        left, singular, right_adjoint = np.linalg.svd(anchors, full_matrices=False)
        active = singular > rank_tolerance
        rank = int(np.sum(active))
        minimum = float(np.min(singular[active]))
        condition = float(np.max(singular[active]) / minimum)
        if condition > condition_limit:
            raise ValueError("unexpected ill-conditioning in successful case")
        if rank < dimension and not allow_partial:
            raise ValueError("unexpected rank deficiency in successful case")
        alignment = left[:, active] @ right_adjoint[active, :]
        projector = alignment @ alignment.conj().T
        energy_anchor = projector @ exterior @ projector
        energy_rank = float(
            np.sum(np.linalg.svd(energy_anchor, compute_uv=False) > rank_tolerance)
        )
        energy_weight = float(np.trace(energy_anchor).real)
        if energy_rank < minimum_energy_rank:
            raise ValueError("unexpected missing energy anchor")
        aligned = alignment @ candidate @ alignment.conj().T
        compressed_host = projector @ host @ projector
        inferred_shift = float(
            np.trace(energy_anchor @ (aligned - compressed_host) @ energy_anchor).real
            / energy_weight
        )
        extracted = aligned - inferred_shift * projector - compressed_host
        return {
            "status": "aligned_full" if rank == dimension else "aligned_partial",
            "alignment": alignment,
            "projector": projector,
            "extracted": extracted,
            "rank": rank,
            "condition": condition,
            "minimum": minimum,
            "maximum_angle": maximum_angle,
            "energy_rank": energy_rank,
            "shift": inferred_shift,
        }

    def _evaluate(
        self,
        identifier: str,
        calculated: dict[str, ComplexMatrix | float | int | str],
        transform: ComplexMatrix,
        defect: ComplexMatrix,
        shift: float,
        cell_count: int,
    ) -> dict[str, JsonValue]:
        alignment = calculated["alignment"]
        projector = calculated["projector"]
        extracted = calculated["extracted"]
        if not all(
            isinstance(value, np.ndarray) for value in (alignment, projector, extracted)
        ):
            raise TypeError("calculated matrices are missing")
        alignment_matrix = cast(ComplexMatrix, alignment)
        projector_matrix = cast(ComplexMatrix, projector)
        extracted_matrix = cast(ComplexMatrix, extracted)
        expected_map = projector_matrix @ transform
        phase = np.angle(np.trace(expected_map.conj().T @ alignment_matrix))
        map_defect = self._norm(alignment_matrix - np.exp(1j * phase) * expected_map)
        target = projector_matrix @ defect @ projector_matrix
        extraction_defect = self._norm(extracted_matrix - target)
        if target.shape[0] % cell_count != 0:
            raise ValueError("operator dimension must be divisible by cell count")
        block_size = target.shape[0] // cell_count
        extracted_model = np.zeros_like(extracted_matrix)
        extracted_model[:block_size, :block_size] = extracted_matrix[
            :block_size, :block_size
        ]
        planted_model = np.zeros_like(target)
        planted_model[:block_size, :block_size] = target[:block_size, :block_size]
        values, vectors = np.linalg.eigh(projector_matrix)
        active_basis = vectors[:, values > 0.5]
        extracted_active = active_basis.conj().T @ extracted_matrix @ active_basis
        target_active = active_basis.conj().T @ target @ active_basis
        extracted_values, extracted_vectors = np.linalg.eigh(extracted_active)
        target_values, target_vectors = np.linalg.eigh(target_active)
        lowest_mask = np.abs(target_values - target_values[0]) <= 1.0e-11
        lowest_dimension = int(np.sum(lowest_mask))
        target_lowest_projector = (
            target_vectors[:, :lowest_dimension]
            @ target_vectors[:, :lowest_dimension].conj().T
        )
        extracted_lowest_projector = (
            extracted_vectors[:, :lowest_dimension]
            @ extracted_vectors[:, :lowest_dimension].conj().T
        )
        lowest_fidelity: float | None = None
        if lowest_dimension == 1:
            lowest_fidelity = float(
                np.clip(
                    abs(np.vdot(extracted_vectors[:, 0], target_vectors[:, 0])) ** 2,
                    0.0,
                    1.0,
                )
            )
        inferred_shift = float(calculated["shift"])
        return {
            "id": identifier,
            "status": str(calculated["status"]),
            "issue_codes": [],
            "dimension": defect.shape[0],
            "anchor_rank": int(calculated["rank"]),
            "anchor_condition_number": float(calculated["condition"]),
            "minimum_anchor_singular_value": float(calculated["minimum"]),
            "maximum_principal_angle_radians": float(calculated["maximum_angle"]),
            "energy_anchor_rank": float(calculated["energy_rank"]),
            "inferred_energy_shift": inferred_shift,
            "energy_shift_error": inferred_shift - shift,
            "phase_quotiented_alignment_frobenius_defect": map_defect,
            "extraction_frobenius_defect": extraction_defect,
            "extraction_relative_frobenius_defect": (
                extraction_defect / self._norm(target)
                if self._norm(target) > 0.0
                else 0.0
            ),
            "planted_onsite_model_class_residual": self._norm(target - planted_model),
            "extracted_onsite_model_class_residual": self._norm(
                extracted_matrix - extracted_model
            ),
            "active_spectral_maximum_absolute_defect": float(
                np.max(np.abs(extracted_values - target_values))
            ),
            "active_lowest_state_fidelity": lowest_fidelity,
            "active_lowest_eigenspace_dimension": lowest_dimension,
            "active_lowest_eigenspace_projector_defect": self._norm(
                extracted_lowest_projector - target_lowest_projector
            ),
            "alignment_map_sha256": self._matrix_sha256(alignment_matrix),
            "extracted_operator_sha256": self._matrix_sha256(extracted_matrix),
        }

    @staticmethod
    def _stop_record(
        identifier: str,
        issue: str,
        *,
        rank: int = 0,
        condition: float | None = None,
        minimum: float | None = None,
        angle: float | None = None,
        energy_rank: float | None = None,
    ) -> dict[str, JsonValue]:
        return {
            "id": identifier,
            "status": "stopped",
            "issue_codes": [issue],
            "anchor_rank": rank,
            "anchor_condition_number": condition,
            "minimum_anchor_singular_value": minimum,
            "maximum_principal_angle_radians": angle,
            "energy_anchor_rank": energy_rank,
            "alignment_map": None,
            "inferred_energy_shift": None,
            "extracted_operator": None,
        }

    def _assert_records(
        self,
        retained: tuple[dict[str, JsonValue], ...],
        expected: tuple[dict[str, JsonValue], ...],
    ) -> None:
        if len(retained) != len(expected):
            raise ValueError("diagnostic record count mismatch")
        for actual, reconstructed in zip(retained, expected, strict=True):
            self._assert_record(actual, reconstructed)

    def _assert_record(
        self, retained: dict[str, JsonValue], expected: dict[str, JsonValue]
    ) -> None:
        if set(retained) != set(expected):
            raise ValueError("retained and reconstructed fields differ")
        for key, expected_value in expected.items():
            actual = retained[key]
            if isinstance(expected_value, float):
                np.testing.assert_allclose(
                    self._real(actual, key), expected_value, rtol=5.0e-12, atol=5.0e-14
                )
            elif actual != expected_value:
                raise ValueError(f"retained field mismatch: {key}")

    def _transform(
        self,
        size: int,
        momentum: float,
        spin_count: int,
        control: dict[str, JsonValue],
    ) -> ComplexMatrix:
        cells = self._integer(control["translation_cells"], "translation")
        translation = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            raw = source + cells
            target = raw % size
            crossings = (raw - target) // size
            translation[target, source] = np.exp(
                2j * np.pi * momentum * size * crossings
            )
        angle = self._real(control["orbital_rotation_angle_radians"], "orbital angle")
        rotation = np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=np.complex128,
        )
        permutation_values = self._integers(
            control["orbital_permutation"], "permutation"
        )
        permutation = np.eye(2)[np.asarray(permutation_values, dtype=np.int64)]
        phase_values = self._reals(control["orbital_phases_radians"], "orbital phases")
        orbital_phases = np.diag(np.exp(1j * np.asarray(phase_values)))
        reference_to_candidate = np.asarray(
            np.kron(
                translation,
                orbital_phases @ permutation @ rotation,
            ),
            dtype=np.complex128,
        )
        step = self._real(control["site_phase_step_radians"], "site phase")
        diagonal = np.asarray(
            [
                np.exp(1j * step * (site + 0.5 * orbital))
                for site in range(size)
                for orbital in range(2)
            ]
        )
        reference_to_candidate = np.diag(diagonal) @ reference_to_candidate
        if spin_count == 2:
            axis = np.asarray(self._reals(control["spin_rotation_axis"], "spin axis"))
            axis /= np.linalg.norm(axis)
            spin_angle = self._real(
                control["spin_rotation_angle_radians"], "spin angle"
            )
            pauli_x = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
            pauli_y = np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128)
            pauli_z = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
            generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
            spin_rotation = (
                np.cos(spin_angle / 2.0) * np.eye(2)
                - 1j * np.sin(spin_angle / 2.0) * generator
            )
            reference_to_candidate = np.asarray(
                np.kron(reference_to_candidate, spin_rotation),
                dtype=np.complex128,
            )
        return reference_to_candidate.conj().T

    @staticmethod
    def _supercell(
        hoppings: tuple[tuple[int, ComplexMatrix], ...], size: int, momentum: float
    ) -> ComplexMatrix:
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for source in range(size):
            for representative, block in hoppings:
                raw = source + representative
                target = raw % size
                crossings = (raw - target) // size
                result[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += np.exp(2j * np.pi * momentum * size * crossings) * block
        return result

    def _compact(self, value: JsonValue, size: int, block_size: int) -> ComplexMatrix:
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for record in self._records(value, "compact blocks"):
            row = self._integer(record["row_site"], "row site")
            column = self._integer(record["column_site"], "column site")
            result[
                block_size * row : block_size * (row + 1),
                block_size * column : block_size * (column + 1),
            ] = self._complex_matrix(record["matrix"], "compact matrix")
        return result

    @staticmethod
    def _normalized_complex_noise(rows: int, columns: int, seed: int) -> ComplexMatrix:
        rng = np.random.default_rng(seed)
        values = rng.normal(size=(rows, columns)) + 1j * rng.normal(
            size=(rows, columns)
        )
        norm = float(np.linalg.norm(values, 2))
        if norm == 0.0:
            raise ValueError("additive anchor noise must be nonzero")
        return np.asarray(values / norm, dtype=np.complex128)

    @staticmethod
    def _unitary_noise(dimension: int, radians: float, seed: int) -> ComplexMatrix:
        if radians == 0.0:
            return np.eye(dimension, dtype=np.complex128)
        generator = np.zeros((dimension, dimension), dtype=np.complex128)
        rng = np.random.default_rng(seed)
        for index in range(dimension - 1):
            value = rng.normal() + 1j * rng.normal()
            generator[index, index + 1] = value
            generator[index + 1, index] = value.conjugate()
        generator /= np.linalg.norm(generator, 2)
        values, vectors = np.linalg.eigh(generator)
        return np.asarray(
            vectors @ np.diag(np.exp(1j * radians * values)) @ vectors.conj().T,
            dtype=np.complex128,
        )

    @staticmethod
    def _exterior(size: int, block_size: int, radius: int) -> ComplexMatrix:
        coordinates = np.arange(size, dtype=np.int64)
        coordinates = np.where(
            coordinates <= size // 2, coordinates, coordinates - size
        )
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for site, coordinate in enumerate(coordinates):
            if abs(coordinate) > radius:
                begin = block_size * site
                result[begin : begin + block_size, begin : begin + block_size] = np.eye(
                    block_size
                )
        return result

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _norm(matrix: ComplexMatrix) -> float:
        return float(np.linalg.norm(matrix))

    @staticmethod
    def _load(path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError("JSON root must be an object")
        return value

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._integer(item, name) for item in value)

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._real(item, name) for item in value)

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be arrays")
            parsed: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} values must be complex pairs")
                parsed.append(
                    complex(self._real(pair[0], name), self._real(pair[1], name))
                )
            rows.append(parsed)
        return np.asarray(rows, dtype=np.complex128)

    def _assert_text(self, expected: str, actual: JsonValue, name: str) -> None:
        if self._string(actual, name) != expected:
            raise ValueError(f"{name} mismatch")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt one result path into the independent verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[3]
    BlindAlignmentResultVerifier().execute(arguments.result.resolve(), repository_root)
    print("independent verification: PASS")


if __name__ == "__main__":
    main()
