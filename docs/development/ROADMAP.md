# AntennaLab Roadmap

## Phase 0: Scope and Contracts

Status: complete.

- Product vision established
- No external antenna-calculation API rule established
- Layered architecture documented
- Initial monorepo layout created

## Phase 1: Engineering Core

Status: complete for the current MVP foundation.

- Central physical constants
- Unit normalization for frequency, length, and angle
- Wavelength and electrical-length helpers
- Structured engineering validation and exceptions
- Versioned antenna model contract
- Canonical design object with deterministic hash
- Machine-readable geometry objects
- Structured result object with result classification
- Dipole, monopole, and Yagi-Uda initial models
- Analytical radiation foundation where defensible
- Reference, determinism, model, and integration tests

Known limits:

- Yagi-Uda Phase 1 model is dimensional only
- No impedance matching network model
- No VSWR/S11 model
- No numerical/full-wave solver
- No persistence-backed revisions yet

## Phase 2: Backend and Requirement Foundation

Status: complete for the current API foundation.

- Normalize backend import/package setup: complete
- Harden requirement schema: complete for supported Phase 2 inputs
- Map engineering exceptions to user-correctable API responses: complete
- Return canonical design and analysis payloads consistently: complete
- Add model registry and model capability listing: complete
- Add persistence contracts for saved designs and revisions: complete
- Add frontend API contract types/client for design generation: complete

Known limits:

- No actual database persistence yet
- No authentication, rate limiting, quotas, or production observability
- API validation covers current supported model parameters only
- Frontend does not yet render returned designs or analysis

## Phase 3: Frontend Foundation

Status: complete for the current engineering workspace foundation.

- Load available models from the backend: complete
- Validate requirements against backend API: complete
- Generate canonical backend designs: complete
- Display validation status and normalized inputs: complete
- Display model metadata, assumptions, warnings, result class, metrics, design hash, and geometry-ready data: complete
- Display unsupported metrics as unavailable rather than fabricated: complete
- Add raw engineering data view: complete
- Add frontend tests for API client and workspace rendering/state: complete
- Add ESLint 9 flat config: complete
- Professional futuristic Times New Roman UI presentation: complete

Known limits:

- No 2D or 3D geometry rendering yet
- No interactive parameter editing yet
- No plots for returned radiation pattern samples yet
- No saved frontend design history yet

## Phase 4: 3D Designer

Status: next when requested.

- Render geometry with Three.js / React Three Fiber
- Add parameter controls and validation feedback
- Regenerate geometry from canonical state

## Later Phases

- Fast analysis and plots
- Sweeps and revisions
- Optimization
- Worker-based high-accuracy analysis
- Datasheets and learning material
- Manufacturing request workflow
- Production hardening
