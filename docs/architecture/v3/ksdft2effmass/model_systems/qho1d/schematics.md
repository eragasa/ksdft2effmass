# Schematics

## Calculation and verification

```text
Python-authored Qho1dConfiguration
                │
                ▼
        Qho1dAnalyzer
                │
                ├── analytical number states
                ├── finite Dirichlet Hamiltonian
                ├── retained ladder Hamiltonian
                └── common-coordinate comparison
                │
                ▼
       Qho1dCalculationResult ───────┐
                │                    │
                │ typed JSON         │ independent formulas
                ▼                    ▼
          result.json       Qho1dIndependentReferenceAnalyzer
                                     │
                                     ▼
                              Qho1dVerifier
                                     │
                    ┌────────────────┴───────────────┐
                    ▼                                ▼
           Qho1dVerification              Qho1dVisualizationData
                    └────────────────┬───────────────┘
                                     ▼
                             Qho1dVisualizer
                                     │
                                     ▼
                         three validated PNG values
```

## State spaces

```text
retained number-state coordinates --J--> finite interior-grid coordinates
               D_K                 JᵀH_hJ
                 └──── common retained coordinates ────┘
```

The injection is rectangular. The compared Hamiltonians are square only after both are
represented in the same retained coordinates.
