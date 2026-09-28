# AntennaLab Project Status

## Last Updated
2026-09-29

## Current Phase
Phase 6: revision-history, comparison, and datasheet backend foundation complete; frontend delivery remains partial.

Phase 1 Engineering Core and Phase 2 Backend/API Foundation are complete for the current MVP foundation. Phase 3 is now implemented as a presentable, tested engineering workspace UI.

## Current Milestone
Complete the Phase 6 frontend timeline/comparison/datasheet presentation before
beginning Phase 7 learning, fabrication, and measurement workflows.

## Architecture Hardening Completed
- Added a root `pyproject.toml` for reliable Python test discovery and lint configuration.
- Added root workspace commands for development, test, lint, and frontend build workflows.
- Converted the backend startup composition to a `create_app()` factory with configurable API prefix and environment-aware settings.
- Standardized recommendation responses on the same versioned API envelope as all other API endpoints.
- Added typed frontend support for an optional `VITE_API_BASE_URL` deployment configuration.
- Documented repository boundaries and extension rules in `docs/architecture/system-overview.md`.
- Recorded the boundary/envelope decision in ADR 0003 and added an API contract test for recommendation responses.

## Overall Progress
85%

## Phase 6 Backend Foundation Completed
- Added immutable revision retrieval, parameter-snapshot comparison, and engineering datasheet payload APIs.
- Parameter diffs include indexed Yagi values; unavailable historical metrics remain explicitly unavailable.
- Datasheet payload includes canonical design, revision, analysis summary, warnings, assumptions, and reproducibility metadata.
- PDF rendering, frontend timeline/comparison screens, and a broader visual-professionalization pass remain pending.

## Phase 5 Sweep and Optimization Baseline Completed
- Added bounded parameter-sweep APIs over isolated canonical design candidates.
- Each point uses existing internal model validation and analysis; invalid points are retained as structured partial results.
- Added deterministic sweep identity/cache and a single-objective grid-search baseline.
- Supports only metrics genuinely returned by each selected analysis model.
- Candidate visualization, inspection, and promotion UI remain the next focused increment.

## Phase 4 Analysis Completed
- Added a versioned Tier 1 fast analytical analysis service with deterministic SHA-256 input identity and safe in-memory caching.
- Added analysis run/latest/result APIs for canonical design IDs.
- Added a workspace “Run analysis” action with explicit calculated—not simulated—status labeling.
- Added dipole reference tests for normalized angular pattern data, deterministic hashes, cache reuse, and unavailable metrics.
- No full-wave solver, artificial gain/VSWR, or external engineering service was added.

## Phase 3 Design Lifecycle Completed
- Added in-memory canonical design storage and revision snapshots behind a future database adapter boundary.
- Added get, patch, validate, regenerate-geometry, and revision endpoints for existing designs.
- Preserved deterministic model geometry; Yagi individual director updates are tested.
- The workspace continues to render backend-generated geometry in its lazy-loaded 3D viewer.

## Requirement and Recommendation Engine Completed
- Added canonical requirement validation and normalization at `POST /api/v1/requirements`.
- Added a capability registry for dipole, monopole, and Yagi-Uda model support metadata.
- Added `POST /api/v1/recommendations` with hard-constraint filtering, weighted soft scoring, reason codes, alternatives, excluded candidates, warnings, and `recommendation-engine-v1` versioning.
- Added a seven-step requirement wizard with directionality and supported polarization options.
- Connected the recommendations screen to the explainable internal endpoint and design handoff.
- Marks gain/bandwidth compatibility as unsupported instead of inventing values.

## Product UI Expansion Completed
- Added a cohesive hash-routed product shell with accessible global navigation, footer, responsive layout, and public page metadata.
- Added Home, Explore, antenna detail, requirements wizard, recommendations, workspace, simulation, parameter sweep, optimization, design history, datasheets, Learn, fabrication, manufacturing, projects, documentation, and About experiences.
- Connected recommendations to the internal backend recommendation service; the wizard transfers its structured requirement locally to that flow.
- Added model-specific details that distinguish the calculated dipole/monopole models from the Yagi-Uda geometry-only model.
- Added a lazy-loaded React Three Fiber geometry viewer that consumes canonical backend geometry rather than recalculating dimensions in the frontend.
- Marked unimplemented persistence, sweeps, optimization, simulation, manufacturing, and export workflows as unavailable or planned—no demo engineering values are presented as real results.

## Completed Engineering Core
- Centralized physical constants in `engineering/core/constants/physics.py`
- Unit normalization for Hz/kHz/MHz/GHz, m/cm/mm, and degrees/radians
- Reusable wavelength and electrical-length calculations
- Structured engineering exceptions and validation status concepts
- Versioned antenna model contract with `calculate`, `generate_design`, `generate_geometry`, and `analyze`
- Serializable canonical `AntennaDesign` with deterministic design hash
- Serializable geometry model and elements
- Structured `AnalysisResult` with result classification and geometry references
- Deterministic analytical radiation foundation for supported dipole/monopole preview data

## Completed Backend/API Foundation
- Standardized backend imports on `backend.app.*`
- Added centralized API error mapping and safe JSON error responses
- Added typed request/response schema modules
- Added deterministic antenna model registry with model capabilities
- Added `POST /api/v1/designs` for canonical design generation
- Added `POST /api/v1/requirements/validate` for validation/normalization without design generation
- Added `GET /api/v1/models` for supported model metadata
- Preserved compatibility endpoints for families, legacy design generation, and recommendations
- Added persistence-ready `DesignRecord` and `DesignRevisionRecord` contracts
- Verified equivalent normalized unit inputs produce the same design hash

## Completed Frontend Workspace Foundation
- Added a presentable engineering workspace as the primary app screen
- Restyled the workspace into a professional futuristic engineering console using Times New Roman throughout
- Loads model catalog from `GET /api/v1/models`
- Validates requirements through `POST /api/v1/requirements/validate`
- Generates canonical designs through `POST /api/v1/designs`
- Displays validation status, normalized values, loading states, and structured errors
- Displays model metadata, capabilities, assumptions, warnings, analysis metrics, canonical design, design hash, geometry-ready data, and raw engineering JSON
- Shows unsupported metrics explicitly as unavailable instead of fabricating values
- Preserves the last successful design if a later generation fails
- Added frontend API client tests and workspace rendering/state tests
- Added ESLint 9 flat config and jsdom/Vitest setup

## Implemented Models
- Dipole `dipole-v1`: half-wave dimensions, two-arm geometry, ideal normalized E-plane pattern, documented free-space assumptions
- Monopole `monopole-v1`: quarter-wave element, ground-plane assumptions, ideal upper-hemisphere normalized pattern
- Yagi-Uda `yagi-uda-v1`: parameterized reflector, driven element, individual directors, spacing list, boom length, mutable geometry parameters

## Verified Test Status
- `python -m pytest`: 42 passed
- `npm --prefix frontend run test`: 11 passed
- `npm --prefix frontend run lint`: passed
- `npm --prefix frontend run build`: passed
- Live API checks: dipole 915 MHz generation succeeds, 915 MHz and 0.915 GHz produce the same design hash, invalid frequency returns a structured validation error
- Live dev servers confirmed on `http://127.0.0.1:8000` and `http://127.0.0.1:5173/`

## Known Limitations
- Yagi-Uda Phase 1 model does not calculate gain, impedance, VSWR, bandwidth, radiation pattern, or front-to-back ratio
- Dipole and monopole analytical outputs assume idealized free-space or ideal ground conditions
- No finite-material, feed, connector, mounting, tolerance, or platform-coupling effects are modeled
- No numerical/full-wave simulation worker exists yet
- Database schemas, migrations, and worker queues remain placeholders
- Persistence-ready records are returned but not stored in a database
- Frontend displays geometry-ready data but does not yet render 2D/3D geometry
- `npm install` reports 5 dependency vulnerabilities in the frontend tree

## Current Issues
- Browser automation through the in-app browser plugin could not be used in this environment because the browser-control Node tool returned a sandbox metadata error
- No application-level auth, rate limiting, quotas, or observability yet

## Next Task
Proceed to Phase 4 only when requested: build the first geometry visualization layer using the existing canonical geometry payload, while keeping all engineering calculations in the backend/engineering core.
