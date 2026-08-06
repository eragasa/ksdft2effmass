# P2-HC02 test-evidence migration targeted review

Status: **FAIL_WITH_CONSOLIDATED_CORRECTION_COMPLETED_AND_PARENT_CONFIRMED**

The one authorized independent reviewer used `develop-python-test-evidence` with `REVIEW_ONLY` and returned FAIL with material semantic findings. The source review artifact is `.pi-subagents/artifacts/4419c4f1_ksdft2effmass.ksdft2effmass-integration-reviewer_0_output.md`.

## Findings and disposition

1. **Mixed semantic partitions:** applicable. Type errors, malformed-value errors, lifecycle boundaries, timestamp grammar/order, collection-type errors, direct self-relations, and repeated embedded assertions were separated into cohesive owners. Historical IDs remain on their primary requirements; supplementary owners use stable IDs `SV-PROV-114` through `SV-PROV-142` with rationales in `test-evidence-inventory.json`.
2. **Four ArtifactReference properties:** inapplicable as a required split. The higher-authority human instruction explicitly permits one cohesive four-property delegation-map test when its requirement and oracle define that map. `SV-PROV-107` does so with one construction method, nested-state oracle, exact tuple acceptance rule, and delegation failure interpretation.
3. **Schema/runtime/serialization layering:** applicable. Historical `SV-PROV-067` now owns schema validation; `SV-PROV-135` owns runtime deserialization; `SV-PROV-136` owns canonical serialization/round-trip text. The NFC predicate is the visible, seven-field, ID-free `is_nfc_text` helper.
4. **Stale SV-PROV-097 prose:** applicable. Its seven fields now describe only timestamp semantic-type rejection; equality remains `SV-PROV-112`.

The sole writer performed one consolidated correction pass. Parent inspection confirmed that no test function combines different `pytest.raises` exception classes, no literal hidden test/helper loops remain, the artifact layers are distinct, semantic names and IDs are synchronized, and the explicit delegation-map exception is satisfied. No second general reviewer or repeated correction pass was launched.

## Residual boundary

Structural validation and passing tests do not establish oracle independence beyond the documented public invariants, scientific validation, uncertainty quantification, physical correctness, cross-language conformance, release readiness, or human acceptance. Final acceptance remains pending at `P2-HC03`.
