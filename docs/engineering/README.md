# Engineering Layer

## Scope

This layer contains the internal engineering models for AntennaLab. It includes:

- unit conversion helpers
- RF constants
- requirement validation rules
- geometry generation primitives
- analytical antenna family models
- optimization-ready interfaces
- future numerical simulation adapters

## Principles

- No external antenna-calculation API
- All formulas and assumptions belong to AntennaLab
- Results must be reproducible and explainable
- Every model must track assumptions, validity, and warning states

## Phase 1 Core Contracts

### Internal Units

All engineering models normalize inputs to SI units before calculation:

- frequency: Hz
- length: meters
- angle: radians for math functions, degrees for serialized geometry orientation

Supported conversion helpers live under `engineering/core/units/` and reject unsupported units or non-physical positive-only values.

### Constants and Wavelength

Physical constants are centralized in `engineering/core/constants/physics.py`. Wavelength is calculated once through `engineering/core/math/wave.py`:

```text
lambda = c / f
```

where `c` is the vacuum speed of light and `f` is normalized frequency in Hz.

### Antenna Model Interface

Each model exposes:

- `validate(parameters)`
- `calculate(parameters)`
- `generate_design(requirements)`
- `generate_geometry(design)`
- `analyze(design, settings)`
- `evaluate(design)` as a compatibility alias for `analyze`
- `get_assumptions()`
- `get_validity_range()`
- `get_model_version()`

Engineering equations stay inside `engineering/`. API and frontend layers consume serialized designs and results.

### Canonical Design

`AntennaDesign` contains design id, antenna family/type, model version, normalized frequency, dimensions in meters, canonical parameters, materials, feed assumptions, machine-readable geometry, assumptions, warnings, and a deterministic design hash.

The design hash is based on family, model version, canonical parameters, normalized frequency, and optional analysis settings. It excludes timestamps so it can support future caching, sweeps, and revision history.

### Result Object

`AnalysisResult` contains model type/version, result class, inputs, metrics, geometry reference, plot data, assumptions, warnings, validity, and computation metadata.

Phase 1 analytical models use `CALCULATED`. Nothing in this phase is labeled measured or high-fidelity simulated.

## Implemented Models

### Dipole: `dipole-v1`

Purpose: center-fed thin half-wave dipole starting point.

Equations:

- wavelength: `lambda = c / f`
- total length: `lambda / 2`
- each arm: `lambda / 4`

Outputs include canonical dimensions, two wire geometry elements, ideal normalized E-plane half-wave dipole pattern, theoretical reference directivity of 2.15 dBi, and reference input impedance of 73 ohms.

Known limitations: ideal thin conductor, free-space environment, no connector/platform/material-loss/tolerance effects.

### Monopole: `monopole-v1`

Purpose: quarter-wave vertical monopole over an ideal electrically significant ground plane.

Equations:

- wavelength: `lambda = c / f`
- element length: `lambda / 4`

Outputs include canonical dimensions, one vertical wire geometry element, ideal upper-hemisphere normalized pattern, theoretical directivity of 5.15 dBi over ideal ground, and reference input impedance of 36.5 ohms.

Known limitations: finite ground plane, mounting, cable effects, and platform coupling are not modeled.

### Yagi-Uda: `yagi-uda-v1`

Purpose: canonical parameterized Yagi-Uda geometry seed for future interactive editing and optimization.

Supported parameters include frequency, director count, reflector length, driven-element length, individual director lengths, element spacings, boom length, and element radius.

Outputs include reflector, driven element, individually parameterized director geometry, boom length, and element count metrics.

Known limitations: Phase 1 does not calculate Yagi gain, impedance, VSWR, bandwidth, radiation pattern, or front-to-back ratio.

## Reference Tests

Current tests verify unit conversion, invalid units, non-physical values, 915 MHz wavelength, dipole half-wave geometry, monopole quarter-wave geometry, Yagi element/director propagation, deterministic design serialization, and the Phase 1 frequency-to-analysis pipeline.

## Engineering-To-API Flow

Phase 2 exposes the engineering core through thin backend routes and service-layer orchestration:

```text
API request
-> Pydantic request schema
-> DesignService / RecommendationService
-> AntennaModelRegistry
-> engineering antenna model
-> canonical AntennaDesign
-> AnalysisResult
-> structured API success or error response
```

The backend does not duplicate antenna equations. It validates transport-level request shape, normalizes user-facing requirement fields into engineering inputs, selects a registered model, and serializes the canonical engineering output.

Current API-facing model capabilities:

- `dipole`: canonical design, geometry, analytical pattern
- `monopole`: canonical design, geometry, analytical pattern
- `yagi_uda`: canonical design, geometry, dimensional analysis

Structured API errors distinguish validation failures, unsupported antenna types, engineering parameter failures, unsupported analysis, invalid geometry, and unexpected internal errors. Unexpected errors return a safe `INTERNAL_SERVER_ERROR` response rather than stack traces.

Persistence-ready API payloads now include a design record and first revision snapshot, but no database write is performed yet.

## Frontend Engineering Workspace Flow

Phase 3 exposes the engineering pipeline in the React frontend without duplicating engineering calculations:

```text
Frontend requirement form
-> frontend API client
-> backend API
-> engineering core
-> canonical design + analysis
-> frontend result renderer
```

The frontend renders only values returned by the backend:

- supported model metadata and capabilities
- validation and normalized requirement data
- canonical design identifiers, dimensions, parameters, materials, feed, assumptions, warnings, and design hash
- analysis result class, validity, metrics, geometry reference, and raw engineering JSON
- geometry-ready element data for future visualization

Unsupported metrics such as VSWR, S11, measured gain, and efficiency are shown as unavailable in the current engineering model. The UI must not fabricate those values or imply full-wave simulation exists.

The current workspace presentation uses Times New Roman and a dark engineering-console visual style. This is only presentation; the frontend remains a renderer of backend canonical engineering data.

Current frontend tests cover:

- API client success handling
- structured backend error handling
- malformed response handling
- requirement form/model rendering
- validation success state
- design generation success rendering
- generation failure while preserving the previous result
- raw engineering data rendering
