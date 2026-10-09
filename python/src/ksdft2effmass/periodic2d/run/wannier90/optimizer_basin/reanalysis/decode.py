"""Schema-specific decoding for optimizer-basin reanalysis documents."""

from __future__ import annotations

from ksdft2effmass.serialization.json import (
    ImmutableJsonCodec,
    JsonValue,
    StrictJsonDecoder,
)

from .encoded_documents import Periodic2DOptimizerReanalysisEncodedDocuments
from .records import (
    OptimizerBasinSourceConfiguration,
    OptimizerBasinSourceEndpoint,
    OptimizerBasinSourceResult,
    OptimizerReanalysisBasin,
    OptimizerReanalysisConfiguration,
    OptimizerReanalysisDecodedDocuments,
    OptimizerReanalysisEndpoint,
    OptimizerReanalysisMethod,
    OptimizerReanalysisProvenance,
    OptimizerReanalysisRefinement,
    OptimizerReanalysisRefinementSize,
    OptimizerReanalysisResult,
    OptimizerReanalysisSpreadComponents,
    PeriodicCenterSet2D,
)

_SCHEMA_VERSION = 1


class Periodic2DOptimizerReanalysisDocumentDecoder:
    """Decode strict row-053 wires into closed immutable verification records.

    This Action owns schema adaptation only. It assigns no scientific validity,
    provenance truth, convergence, optimizer completeness, uncertainty, or acceptance.
    """

    __slots__ = ("decoder", "immutable_json")

    def __init__(self) -> None:
        """Create one decoder with shared strict and immutable JSON collaborators."""
        self.decoder = StrictJsonDecoder()
        self.immutable_json = ImmutableJsonCodec()

    def execute(
        self, documents: Periodic2DOptimizerReanalysisEncodedDocuments
    ) -> OptimizerReanalysisDecodedDocuments:
        """Decode exact source and result wires into immutable records.

        Parameters
        ----------
        documents
            Exact encoded source-result and reanalysis-result wires.

        Returns
        -------
        OptimizerReanalysisDecodedDocuments
            Closed immutable records containing verifier-owned fields.

        Raises
        ------
        TypeError
            If a wire or represented field has an incompatible exact representation.
        ValueError
            If strict JSON, finite-real, or digest syntax is invalid.
        OverflowError
            If integer-to-binary64 conversion is not finite.
        KeyError
            If a required verifier-owned field is absent.
        MemoryError
            If decoding or immutable adaptation cannot allocate required state.
        RecursionError
            If a document exceeds parser or adapter recursion depth.
        """
        if type(documents) is not Periodic2DOptimizerReanalysisEncodedDocuments:
            raise TypeError(
                "documents must be Periodic2DOptimizerReanalysisEncodedDocuments"
            )
        source_root = self.decoder.document(documents.source_result_payload)
        result_root = self.decoder.document(documents.result_payload)
        return OptimizerReanalysisDecodedDocuments(
            source_result=self.source_result(source_root),
            reanalysis_result=self.reanalysis_result(result_root),
        )

    def source_result(self, root: dict[str, JsonValue]) -> OptimizerBasinSourceResult:
        """Adapt verifier-owned fields from the source optimizer-basin result.

        Parameters
        ----------
        root
            Strict-decoded source-result JSON object.

        Returns
        -------
        OptimizerBasinSourceResult
            Closed frozen source-result record.

        Raises
        ------
        AssertionError
            If the schema version is unsupported.
        KeyError
            If a required field is absent.
        TypeError
            If a required field has an incompatible exact representation.
        ValueError
            If a represented primitive is invalid.
        OverflowError
            If a nested integer-to-binary64 conversion is not finite.
        """
        schema_version = self.decoder.integer(
            root["schema_version"], "source.schema_version"
        )
        if schema_version != _SCHEMA_VERSION:
            raise AssertionError("source schema changed")
        configurations_value = root["configurations"]
        if type(configurations_value) is not list:
            raise TypeError("source configurations must be a JSON array")
        return OptimizerBasinSourceResult(
            schema_version=schema_version,
            configurations=tuple(
                self.source_configuration(value, index)
                for index, value in enumerate(configurations_value)
            ),
        )

    def source_configuration(
        self, value: JsonValue, index: int
    ) -> OptimizerBasinSourceConfiguration:
        """Adapt one source configuration used by reanalysis correlation.

        Parameters
        ----------
        value
            Strict-decoded candidate configuration value.
        index
            Zero-based position used only in diagnostics.

        Returns
        -------
        OptimizerBasinSourceConfiguration
            Closed frozen source-configuration record.

        Raises
        ------
        KeyError
            If a required field is absent.
        TypeError
            If a required field has an incompatible exact representation.
        ValueError
            If a represented primitive is invalid.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError(f"source.configurations[{index}] must be a JSON object")
        label = f"source.configurations[{index}]"
        starts_value = value["starts"]
        if type(starts_value) is not list:
            raise TypeError(f"{label}.starts must be a JSON array")
        return OptimizerBasinSourceConfiguration(
            configuration_id=self.decoder.string(
                value["configuration_id"], f"{label}.configuration_id"
            ),
            plane_wave_cutoff=self.decoder.integer(
                value["plane_wave_cutoff"], f"{label}.plane_wave_cutoff"
            ),
            reciprocal_mesh_size=self.decoder.integer(
                value["reciprocal_mesh_size"], f"{label}.reciprocal_mesh_size"
            ),
            transverse_lattice_length=self.decoder.real(
                value["transverse_lattice_length"],
                f"{label}.transverse_lattice_length",
            ),
            starts=tuple(
                self.source_endpoint(start, label, start_index)
                for start_index, start in enumerate(starts_value)
            ),
        )

    def source_endpoint(
        self, value: JsonValue, configuration_label: str, index: int
    ) -> OptimizerBasinSourceEndpoint:
        """Adapt one source endpoint used by reanalysis correlation.

        Parameters
        ----------
        value
            Strict-decoded candidate endpoint value.
        configuration_label
            Validated enclosing label used only in diagnostics.
        index
            Zero-based endpoint position used only in diagnostics.

        Returns
        -------
        OptimizerBasinSourceEndpoint
            Closed frozen source-endpoint record.

        Raises
        ------
        KeyError
            If a required field is absent.
        TypeError
            If a required field has an incompatible exact representation.
        ValueError
            If a represented primitive is invalid.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError(
                f"{configuration_label}.starts[{index}] must be a JSON object"
            )
        label = f"{configuration_label}.starts[{index}]"
        return OptimizerBasinSourceEndpoint(
            gauge_id=self.decoder.string(value["gauge_id"], f"{label}.gauge_id"),
            convergence_criterion_satisfied=self.decoder.boolean(
                value["convergence_criterion_satisfied"],
                f"{label}.convergence_criterion_satisfied",
            ),
            native_total_spread_cell_squared=self.decoder.real(
                value["native_total_spread_cell_squared"],
                f"{label}.native_total_spread_cell_squared",
            ),
        )

    def reanalysis_result(
        self, root: dict[str, JsonValue]
    ) -> OptimizerReanalysisResult:
        """Adapt verifier-owned fields from the offline reanalysis result.

        Parameters
        ----------
        root
            Strict-decoded reanalysis-result JSON object.

        Returns
        -------
        OptimizerReanalysisResult
            Closed frozen reanalysis-result record.

        Raises
        ------
        AssertionError
            If the schema version is unsupported.
        KeyError
            If a required field is absent.
        TypeError
            If a required field has an incompatible exact representation.
        ValueError
            If a represented primitive is invalid.
        OverflowError
            If a nested integer-to-binary64 conversion is not finite.
        """
        schema_version = self.decoder.integer(
            root["schema_version"], "result.schema_version"
        )
        if schema_version != _SCHEMA_VERSION:
            raise AssertionError("result schema changed")
        configurations_value = root["configurations"]
        if type(configurations_value) is not list:
            raise TypeError("result.configurations must be a JSON array")
        refinements_value = root["common_estimator_refinement"]
        if type(refinements_value) is not list:
            raise TypeError("result.common_estimator_refinement must be a JSON array")
        counts_value = root["diagnostic_classification_counts"]
        if type(counts_value) is not dict:
            raise TypeError(
                "result.diagnostic_classification_counts must be a JSON object"
            )
        return OptimizerReanalysisResult(
            schema_version=schema_version,
            provenance=self.provenance(root["provenance"]),
            method=self.method(root["method"]),
            configurations=tuple(
                self.configuration(value, index)
                for index, value in enumerate(configurations_value)
            ),
            diagnostic_classification_counts=tuple(
                (
                    key,
                    self.decoder.integer(
                        count, f"result.diagnostic_classification_counts.{key}"
                    ),
                )
                for key, count in counts_value.items()
            ),
            common_estimator_refinement=tuple(
                self.refinement(value, index)
                for index, value in enumerate(refinements_value)
            ),
        )

    def provenance(self, value: JsonValue) -> OptimizerReanalysisProvenance:
        """Adapt directly authenticated compact-source declarations.

        Parameters
        ----------
        value
            Strict-decoded provenance value.

        Returns
        -------
        OptimizerReanalysisProvenance
            Closed frozen direct-source declaration record.

        Raises
        ------
        KeyError
            If a required declaration is absent.
        TypeError
            If a declaration has an incompatible exact representation.
        ValueError
            If a path string is empty or a digest is malformed.
        """
        if type(value) is not dict:
            raise TypeError("result.provenance must be a JSON object")
        return OptimizerReanalysisProvenance(
            source_result_sha256=self.decoder.sha256(
                value["source_result_sha256"],
                "result.provenance.source_result_sha256",
            ),
            reanalyzer_path=self.decoder.string(
                value["reanalyzer_path"], "result.provenance.reanalyzer_path"
            ),
            reanalyzer_sha256=self.decoder.sha256(
                value["reanalyzer_sha256"], "result.provenance.reanalyzer_sha256"
            ),
            base_extractor_path=self.decoder.string(
                value["base_extractor_path"],
                "result.provenance.base_extractor_path",
            ),
            base_extractor_sha256=self.decoder.sha256(
                value["base_extractor_sha256"],
                "result.provenance.base_extractor_sha256",
            ),
        )

    def method(self, value: JsonValue) -> OptimizerReanalysisMethod:
        """Adapt method values used by bounded numerical reconstruction.

        Parameters
        ----------
        value
            Strict-decoded method value.

        Returns
        -------
        OptimizerReanalysisMethod
            Closed frozen numerical-method record.

        Raises
        ------
        KeyError
            If a required method field is absent.
        TypeError
            If a method field has an incompatible exact representation.
        ValueError
            If a represented primitive is invalid or nonfinite.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError("result.method must be a JSON object")
        return OptimizerReanalysisMethod(
            common_estimator_fft_sizes=self.decoder.integers(
                value["common_estimator_fft_sizes"],
                "result.method.common_estimator_fft_sizes",
            ),
            basin_spread_absolute_tolerance=self.decoder.real(
                value["basin_spread_absolute_tolerance"],
                "result.method.basin_spread_absolute_tolerance",
            ),
            basin_center_set_periodic_tolerance=self.decoder.real(
                value["basin_center_set_periodic_tolerance"],
                "result.method.basin_center_set_periodic_tolerance",
            ),
        )

    def configuration(
        self, value: JsonValue, index: int
    ) -> OptimizerReanalysisConfiguration:
        """Adapt one reanalysis configuration and its endpoint observations.

        Parameters
        ----------
        value
            Strict-decoded candidate configuration value.
        index
            Zero-based position used only in diagnostics.

        Returns
        -------
        OptimizerReanalysisConfiguration
            Closed frozen reanalysis-configuration record.

        Raises
        ------
        KeyError
            If a required field is absent.
        TypeError
            If a required field has an incompatible exact representation.
        ValueError
            If a represented primitive is invalid.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError(f"result.configurations[{index}] must be a JSON object")
        label = f"result.configurations[{index}]"
        starts_value = value["starts"]
        if type(starts_value) is not list:
            raise TypeError(f"{label}.starts must be a JSON array")
        basins_value = value["symmetry_aware_observed_basins"]
        if type(basins_value) is not list:
            raise TypeError(
                f"{label}.symmetry_aware_observed_basins must be a JSON array"
            )
        return OptimizerReanalysisConfiguration(
            configuration_id=self.decoder.string(
                value["configuration_id"], f"{label}.configuration_id"
            ),
            plane_wave_cutoff=self.decoder.integer(
                value["plane_wave_cutoff"], f"{label}.plane_wave_cutoff"
            ),
            reciprocal_mesh_size=self.decoder.integer(
                value["reciprocal_mesh_size"], f"{label}.reciprocal_mesh_size"
            ),
            transverse_lattice_length=self.decoder.real(
                value["transverse_lattice_length"],
                f"{label}.transverse_lattice_length",
            ),
            starts=tuple(
                self.endpoint(start, f"{label}.starts[{start_index}]")
                for start_index, start in enumerate(starts_value)
            ),
            symmetry_aware_observed_basins=tuple(
                self.basin(
                    basin,
                    f"{label}.symmetry_aware_observed_basins[{basin_index}]",
                )
                for basin_index, basin in enumerate(basins_value)
            ),
            symmetry_aware_observed_basin_count=self.decoder.integer(
                value["symmetry_aware_observed_basin_count"],
                f"{label}.symmetry_aware_observed_basin_count",
            ),
            best_observed_converged_by_omega_tilde=self.endpoint(
                value["best_observed_converged_by_omega_tilde"],
                f"{label}.best_observed_converged_by_omega_tilde",
            ),
        )

    def endpoint(self, value: JsonValue, label: str) -> OptimizerReanalysisEndpoint:
        """Adapt one complete endpoint and verifier-owned numerical fields.

        Parameters
        ----------
        value
            Strict-decoded candidate endpoint value.
        label
            Validated location label used only in diagnostics.

        Returns
        -------
        OptimizerReanalysisEndpoint
            Closed frozen endpoint record retaining a complete immutable JSON copy.

        Raises
        ------
        KeyError
            If a required endpoint field is absent.
        TypeError
            If a field has an incompatible exact representation.
        ValueError
            If a represented primitive or center set is invalid.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError(f"{label} must be a JSON object")
        return OptimizerReanalysisEndpoint(
            configuration_id=self.decoder.string(
                value["configuration_id"], f"{label}.configuration_id"
            ),
            gauge_id=self.decoder.string(value["gauge_id"], f"{label}.gauge_id"),
            convergence_criterion_satisfied=self.decoder.boolean(
                value["convergence_criterion_satisfied"],
                f"{label}.convergence_criterion_satisfied",
            ),
            native_centers_modulo_cell=self.center_set(
                value["native_centers_modulo_cell"],
                f"{label}.native_centers_modulo_cell",
            ),
            spread_components=self.spread_components(
                value["spread_components"], f"{label}.spread_components"
            ),
            complete_document=self.immutable_json.immutable_object(value),
        )

    def spread_components(
        self, value: JsonValue, label: str
    ) -> OptimizerReanalysisSpreadComponents:
        """Adapt spread decomposition and terminal-trace summary fields.

        Parameters
        ----------
        value
            Strict-decoded spread-components value.
        label
            Validated location label used only in diagnostics.

        Returns
        -------
        OptimizerReanalysisSpreadComponents
            Closed frozen spread and trace-diagnostic record.

        Raises
        ------
        KeyError
            If a required component is absent.
        TypeError
            If a component has an incompatible exact representation.
        ValueError
            If a represented real is nonfinite.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError(f"{label} must be a JSON object")
        return OptimizerReanalysisSpreadComponents(
            omega_i_cell_squared=self.decoder.real(
                value["omega_i_cell_squared"], f"{label}.omega_i_cell_squared"
            ),
            omega_d_cell_squared=self.decoder.real(
                value["omega_d_cell_squared"], f"{label}.omega_d_cell_squared"
            ),
            omega_od_cell_squared=self.decoder.real(
                value["omega_od_cell_squared"], f"{label}.omega_od_cell_squared"
            ),
            omega_tilde_cell_squared=self.decoder.real(
                value["omega_tilde_cell_squared"],
                f"{label}.omega_tilde_cell_squared",
            ),
            omega_total_cell_squared=self.decoder.real(
                value["omega_total_cell_squared"],
                f"{label}.omega_total_cell_squared",
            ),
            terminal_spread_slope_per_iteration=self.decoder.real(
                value["terminal_spread_slope_per_iteration"],
                f"{label}.terminal_spread_slope_per_iteration",
            ),
            terminal_detrended_spread_rms=self.decoder.real(
                value["terminal_detrended_spread_rms"],
                f"{label}.terminal_detrended_spread_rms",
            ),
            terminal_median_absolute_delta_spread=self.decoder.real(
                value["terminal_median_absolute_delta_spread"],
                f"{label}.terminal_median_absolute_delta_spread",
            ),
            terminal_median_rms_gradient=self.decoder.real(
                value["terminal_median_rms_gradient"],
                f"{label}.terminal_median_rms_gradient",
            ),
            diagnostic_classification=self.decoder.string(
                value["diagnostic_classification"],
                f"{label}.diagnostic_classification",
            ),
        )

    def basin(self, value: JsonValue, label: str) -> OptimizerReanalysisBasin:
        """Adapt one retained symmetry-aware basin membership list.

        Parameters
        ----------
        value
            Strict-decoded basin value.
        label
            Validated location label used only in diagnostics.

        Returns
        -------
        OptimizerReanalysisBasin
            Closed frozen gauge-membership record.

        Raises
        ------
        KeyError
            If the membership field is absent.
        TypeError
            If the object, array, or gauge identity has an incompatible representation.
        ValueError
            If a gauge identity is empty.
        """
        if type(value) is not dict:
            raise TypeError(f"{label} must be a JSON object")
        gauge_values = value["gauge_ids"]
        if type(gauge_values) is not list:
            raise TypeError(f"{label}.gauge_ids must be a JSON array")
        return OptimizerReanalysisBasin(
            gauge_ids=tuple(
                self.decoder.string(gauge, f"{label}.gauge_ids[{index}]")
                for index, gauge in enumerate(gauge_values)
            )
        )

    def refinement(self, value: JsonValue, index: int) -> OptimizerReanalysisRefinement:
        """Adapt one common-estimator refinement case.

        Parameters
        ----------
        value
            Strict-decoded candidate refinement value.
        index
            Zero-based case position used only in diagnostics.

        Returns
        -------
        OptimizerReanalysisRefinement
            Closed frozen refinement-case record.

        Raises
        ------
        KeyError
            If a required case field is absent.
        TypeError
            If a required field has an incompatible exact representation.
        ValueError
            If a represented primitive is invalid.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError(
                f"result.common_estimator_refinement[{index}] must be a JSON object"
            )
        label = f"result.common_estimator_refinement[{index}]"
        sizes_value = value["sizes"]
        if type(sizes_value) is not list:
            raise TypeError(f"{label}.sizes must be a JSON array")
        comparison = value["refinement_512_to_1024"]
        if type(comparison) is not dict:
            raise TypeError(f"{label}.refinement_512_to_1024 must be a JSON object")
        return OptimizerReanalysisRefinement(
            case_id=self.decoder.string(value["case_id"], f"{label}.case_id"),
            configuration_id=self.decoder.string(
                value["configuration_id"], f"{label}.configuration_id"
            ),
            gauge_id=self.decoder.string(value["gauge_id"], f"{label}.gauge_id"),
            convergence_criterion_satisfied=self.decoder.boolean(
                value["convergence_criterion_satisfied"],
                f"{label}.convergence_criterion_satisfied",
            ),
            sizes=tuple(
                self.refinement_size(size, f"{label}.sizes[{size_index}]")
                for size_index, size in enumerate(sizes_value)
            ),
            relative_total_spread_difference=self.decoder.real(
                comparison["relative_total_spread_difference"],
                f"{label}.refinement_512_to_1024.relative_total_spread_difference",
            ),
            center_set_periodic_distance=self.decoder.real(
                comparison["center_set_periodic_distance"],
                f"{label}.refinement_512_to_1024.center_set_periodic_distance",
            ),
        )

    def refinement_size(
        self, value: JsonValue, label: str
    ) -> OptimizerReanalysisRefinementSize:
        """Adapt one common-estimator FFT-size observation.

        Parameters
        ----------
        value
            Strict-decoded candidate FFT-size observation.
        label
            Validated location label used only in diagnostics.

        Returns
        -------
        OptimizerReanalysisRefinementSize
            Closed frozen estimator-observation record.

        Raises
        ------
        KeyError
            If a required observation field is absent.
        TypeError
            If a required field has an incompatible exact representation.
        ValueError
            If a primitive, digest, or center set is invalid.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        """
        if type(value) is not dict:
            raise TypeError(f"{label} must be a JSON object")
        return OptimizerReanalysisRefinementSize(
            fft_size=self.decoder.integer(value["fft_size"], f"{label}.fft_size"),
            input_path=self.decoder.string(value["input_path"], f"{label}.input_path"),
            input_sha256=self.decoder.sha256(
                value["input_sha256"], f"{label}.input_sha256"
            ),
            common_total_spread_cell_squared=self.decoder.real(
                value["common_total_spread_cell_squared"],
                f"{label}.common_total_spread_cell_squared",
            ),
            common_centers_modulo_cell=self.center_set(
                value["common_centers_modulo_cell"],
                f"{label}.common_centers_modulo_cell",
            ),
        )

    def center_set(self, value: JsonValue, label: str) -> PeriodicCenterSet2D:
        """Adapt one nonempty set of finite two-coordinate periodic centers.

        Parameters
        ----------
        value
            Strict-decoded candidate center-set value.
        label
            Validated location label used only in diagnostics.

        Returns
        -------
        PeriodicCenterSet2D
            Nonempty immutable center set with exact finite binary64 coordinates.

        Raises
        ------
        TypeError
            If the set, a center, or a coordinate has an incompatible representation.
        ValueError
            If the set is empty, a center is not two-dimensional, or a coordinate is
            nonfinite.
        OverflowError
            If an integer coordinate cannot convert to finite binary64.
        """
        if type(value) is not list:
            raise TypeError(f"{label} must be a JSON array")
        if not value:
            raise ValueError(f"{label} must be nonempty")
        centers: list[tuple[float, float]] = []
        for index, center in enumerate(value):
            if type(center) is not list:
                raise TypeError(f"{label}[{index}] must be a JSON array")
            coordinates = tuple(
                self.decoder.real(item, f"{label}[{index}]") for item in center
            )
            if len(coordinates) != 2:
                raise ValueError(f"{label}[{index}] must contain two coordinates")
            centers.append((coordinates[0], coordinates[1]))
        return tuple(centers)
