# AntennaLab Development Log

## 2026-09-29

### Phase
Phase 3 — Design Workspace and Interactive Geometry Foundation.

### Implementation
- Replaced the repository placeholder with an in-memory canonical design and revision adapter.
- Added design retrieval, parameter update, server-side validation, geometry regeneration, and explicit revision APIs.
- Kept all generation and validation inside the existing engineering models.
- Added lifecycle coverage demonstrating that a Yagi director change preserves the other individual director dimensions.
- Documented the lifecycle and geometry contract.

### Verification
- `python -m pytest`: 36 passed.
- `npm --prefix frontend run lint`: passed.
- `npm --prefix frontend run test`: 11 passed.
- `npm --prefix frontend run build`: passed.

### Known Limitations
- Design/revision persistence is process-local until a database adapter is introduced.
- The 3D viewer has orbit, pan, and zoom. Camera reset, explicit element highlighting, and dimension overlays remain future workspace refinements.
- No full-wave simulation, calculated Yagi gain, impedance, VSWR, or bandwidth was added.

### Next Step
Phase 4: add only genuine analysis/plot workflows supported by internal models.

## 2026-09-29

### Phase
Phase 2 — Requirement Engine and Explainable Antenna Recommendation.

### Implementation
- Added structured capability metadata and a versioned deterministic recommendation engine.
- Added hard frequency, directionality, polarization, and size constraints before soft scoring.
- Added score components, stable reason codes, alternatives, excluded candidates, warnings, and unsupported-criterion states.
- Added requirement normalization and explainable recommendation API endpoints.
- Connected the product wizard and recommendation page to the new backend contract.

### Engineering Decisions
- Capability descriptions are not engineering performance results.
- Gain and bandwidth are marked unsupported for recommendation scoring until the internal models can evaluate them.
- A high soft score never overrides a hard-constraint failure.

### Verification
- `python -m pytest`: 35 passed.
- `npm --prefix frontend run lint`: passed.
- `npm --prefix frontend run test`: 11 passed.
- `npm --prefix frontend run build`: passed.

### Next Step
Phase 3: persist canonical revisions and add safe parameter editing before implementing genuine sweeps or optimization.

## 2026-09-29

### Phase
Representative product UI expansion.

### Implementation
- Added a hash-routed, responsive AntennaLab product shell and connected navigation.
- Added Home, Explore, antenna detail, multi-step requirements, recommendations, workspace, simulation, sweep, optimization, history, datasheets, Learn, fabrication, manufacturing, projects, documentation, and About pages.
- Connected the recommendations experience to the internal API and passed wizard requirements through browser session state.
- Added a lazy-loaded 3D geometry viewer using React Three Fiber; it renders only canonical geometry returned by the engineering engine.
- Added public-facing metadata, accessible skip navigation, focus styles, labels, empty states, status badges, and explicit implementation-state messaging.
- Added route and engineering-honesty frontend coverage.

### Real vs Representative Functionality
- Real: model catalog, requirement validation, design generation, canonical geometry, analytical results where implemented, and internal recommendations.
- Representative only: saved projects/history, sweeps, optimization, numerical simulation, datasheet export, manufacturing requests, and authentication. These pages state their unavailable status and do not show fabricated engineering results.

### Verification
- `python -m pytest`: 30 passed.
- `npm --prefix frontend run lint`: passed.
- `npm --prefix frontend run test`: 11 passed.
- `npm --prefix frontend run build`: passed. The 3D renderer is emitted as a lazy-loaded chunk.

### Known Limitations
- The 3D viewer provides rotate, pan, and zoom; reset, visibility controls, and dimension annotations are future workspace enhancements.
- The browser verification connector could not initialize in this environment due to missing sandbox metadata; automated tests and production build completed successfully.

### Next Step
Build persistence-backed revisions and editable canonical parameters before adding actual sweeps or optimization.

## 2026-09-29

### Phase
Architecture hardening.

### Implementation
- Added root workspace commands and Python test configuration.
- Added FastAPI application-factory composition and settings-driven API prefix.
- Unified recommendation success responses with the established versioned API envelope.
- Added deployment-safe Vite API-base configuration support.
- Added architecture reference documentation and ADR 0003.

### Files Changed
- `pyproject.toml`, `package.json`, and `.env.example`
- `backend/app/main.py`, `backend/app/core/config.py`, and `backend/app/api/router.py`
- `backend/app/api/routes/requirements.py` and `backend/tests/test_phase2_api_contracts.py`
- `frontend/src/services/designsApi.ts`, `frontend/src/services/requirementsApi.ts`, and `frontend/src/vite-env.d.ts`
- `docs/architecture/system-overview.md` and `docs/decisions/0003-layer-boundaries-and-api-envelopes.md`
- `README.md`, `PROJECT_STATUS.md`, and `DEVELOPMENT_LOG.md`

### Decisions
- Backend route modules remain prefix-agnostic; the application factory owns the configured API prefix.
- All versioned API endpoints return the shared success/error envelope.
- The Vite API base is optional so development retains the local proxy while deployments can target a configured backend URL.

### Verification
- `python -m pytest`: 30 passed.
- `npm --prefix frontend run lint`: passed.
- `npm --prefix frontend run test`: 8 passed.
- `npm --prefix frontend run build`: passed.

### Known Limitations
- Architecture hardening does not add persistence, 3D rendering, full-wave simulation, authentication, or observability.
- The current model catalog and engineering-validity limitations remain unchanged.

### Next Step
Start Phase 4 visualization only with the existing canonical geometry contract as its input boundary.


## 2026-09-17

### Phase
Phase 1 Engineering Core completion.

### Implementation
- Added structured engineering exceptions for invalid parameters, unsupported ranges, invalid geometry, outside-validity cases, and unsupported analysis.
- Added angle conversion helpers and strengthened frequency/length normalization.
- Centralized RF constant exports through the physics constants module.
- Added structured validation statuses for missing, invalid, out-of-range, unsupported, and valid inputs.
- Made geometry elements and geometry models serializable.
- Added result classes and geometry references to analysis results.
- Added canonical design serialization and deterministic design hashes.
- Updated the antenna model contract with `calculate`, `analyze`, and `get_model_version`.
- Updated dipole, monopole, and Yagi-Uda models to use shared wavelength/unit helpers.
- Removed unsupported Yagi gain/front-to-back claims from Phase 1 analysis output.
- Added defensible analytical normalized radiation samples for the ideal dipole and ideal-ground monopole cases.
- Connected the backend design service to canonical engineering design and analysis payloads.
- Switched requirement API validation to the Pydantic requirement schema before constructing the service dataclass.

### Files Changed
- `engineering/core/exceptions.py`
- `engineering/core/units/angle.py`
- `engineering/core/units/frequency.py`
- `engineering/core/units/length.py`
- `engineering/core/units/converter.py`
- `engineering/core/constants/rf.py`
- `engineering/core/validation/schema.py`
- `engineering/core/math/wave.py`
- `engineering/core/geometry/model.py`
- `engineering/analysis/result.py`
- `engineering/analysis/radiation.py`
- `engineering/antennas/base.py`
- `engineering/antennas/dipole/dipole.py`
- `engineering/antennas/monopole/monopole.py`
- `engineering/antennas/yagi_uda/yagi_uda.py`
- `backend/app/services/design_service.py`
- `backend/app/api/routes/requirements.py`
- `frontend/package-lock.json`
- `engineering/tests/test_unit_system.py`
- `engineering/tests/test_models.py`
- `engineering/tests/test_design_integration.py`
- `docs/engineering/README.md`
- `docs/development/ROADMAP.md`
- `docs/decisions/0001-engineering-core-contracts.md`
- `PROJECT_STATUS.md`
- `DEVELOPMENT_LOG.md`

### Engineering Decisions
- Phase 1 Yagi-Uda output is limited to canonical geometry and dimensional metadata until a validated analysis model is implemented.
- Dipole and monopole directivity values are exposed only as ideal theoretical reference quantities with assumptions and metadata.
- Design hashes exclude timestamps so they can support deterministic caching, revisions, sweeps, and optimization.

### Tests
- `PYTHONPATH='backend;.' python -m pytest`
- Result: 18 passed in 1.03s
- `npm run build`
- Result: passed; TypeScript and Vite production build completed
- `npm run lint`
- Result: failed because no ESLint 9 `eslint.config.*` file exists in the scaffold
- `npm run test`
- Result: failed because no frontend test files exist yet

### Problems
- Running `python -m pytest` without `PYTHONPATH='backend;.'` fails because `backend/tests/test_health.py` imports `app.main`.
- `npm install` reports 5 frontend dependency vulnerabilities: 3 moderate, 1 high, 1 critical.
- ESLint is declared but not configured for ESLint 9.
- Vitest is declared but no frontend tests exist yet.

### Resolutions
- Verified the complete suite with the repository import path set explicitly.
- Verified frontend TypeScript/build output after installing declared dependencies.
- Recorded backend import normalization as a Phase 2 task instead of hiding the issue.

### Known Limitations
- No numerical/full-wave solver.
- No VSWR/S11 or matching network model.
- No finite ground-plane or installed-environment model.
- No persistence-backed revisions yet.
- Frontend does not yet render geometry or analysis plots.

### Next Step
Begin Phase 2 by normalizing backend package imports, hardening API validation/error mapping, and preparing persistence-ready design/revision contracts.

## 2026-09-17

### Phase
Phase 2 Backend Requirement/API Foundation.

### Objective
Create a stable backend API contract around the completed engineering core without moving engineering formulas out of `engineering/`.

### Implementation
- Standardized backend imports on `backend.app.*` from the repository root.
- Added centralized API error and exception mapping in `backend/app/core/errors.py`.
- Added safe JSON error responses for request validation, engineering errors, unsupported models, and unexpected internal failures.
- Disabled FastAPI debug traceback responses for API runtime safety.
- Added `AntennaModelRegistry` with deterministic model metadata and capabilities.
- Added typed design/request schema contracts.
- Added `DesignRecord` and `DesignRevisionRecord` persistence-ready dataclasses.
- Reworked `DesignService` into the Phase 2 requirement-to-design pipeline.
- Added `POST /api/v1/designs`.
- Added `POST /api/v1/requirements/validate`.
- Added `GET /api/v1/models`.
- Preserved existing recommendation and compatibility design routes.
- Added frontend TypeScript contract types and `frontend/src/services/designsApi.ts`.
- Added backend API tests for model listing, design generation, validation, structured errors, unsupported models, deterministic hashing, equivalent units, and unexpected exception handling.

### Files Changed
- `backend/app/main.py`
- `backend/app/api/router.py`
- `backend/app/api/routes/designs.py`
- `backend/app/api/routes/requirements.py`
- `backend/app/api/routes/models.py`
- `backend/app/core/errors.py`
- `backend/app/models/design.py`
- `backend/app/schemas/common.py`
- `backend/app/schemas/design_schema.py`
- `backend/app/schemas/requirement_schema.py`
- `backend/app/services/design_service.py`
- `backend/app/services/model_registry.py`
- `backend/tests/test_design_service.py`
- `backend/tests/test_health.py`
- `backend/tests/test_phase2_api_contracts.py`
- `frontend/src/types/index.ts`
- `frontend/src/services/designsApi.ts`
- `docs/engineering/README.md`
- `docs/development/ROADMAP.md`
- `docs/decisions/0002-backend-package-and-api-foundation.md`
- `PROJECT_STATUS.md`
- `DEVELOPMENT_LOG.md`

### Engineering Decisions
- Backend routes remain transport adapters; they do not contain antenna equations.
- API schemas remain separate from engineering-core dataclasses.
- Model extensibility is handled through a registry/factory rather than route conditionals.
- Persistence-ready records are emitted but not stored until a database phase.
- Equivalent normalized requirements must preserve deterministic design hashes.

### Tests
- `PYTHONPATH='.' python -m pytest`
- Result: 29 passed in 1.20s
- `PYTHONPATH='backend;.' python -m pytest`
- Result: 29 passed in 1.17s
- `npm run build`
- Result: passed
- `npm run lint`
- Result: failed because no ESLint 9 `eslint.config.*` file exists
- `npm run test`
- Result: failed because no frontend test files exist yet

### Problems
- FastAPI debug mode originally returned plaintext traceback responses for unexpected errors in tests.
- Frontend lint/test commands remain scaffold-incomplete.
- Frontend dependency tree still reports 5 npm audit vulnerabilities from the installed packages.

### Resolutions
- Turned FastAPI debug response mode off so unexpected errors use the safe JSON API handler.
- Verified both the new project-root Python import path and the previous test command.
- Documented frontend lint/test/audit issues as remaining scaffold work rather than forcing unrelated dependency changes.

### Known Limitations
- No database writes yet.
- No auth/rate limiting/quotas/observability yet.
- API validation covers currently supported model parameters only.
- Frontend has typed API clients but does not yet render canonical design or analysis output.

### Next Step
Begin Phase 3 by connecting the React workspace to `POST /api/v1/designs` and displaying canonical model metadata, assumptions, warnings, metrics, and geometry-ready data.

## 2026-09-20

### Phase
Phase 3 Frontend Engineering Workspace Foundation.

### Objective
Make the current UI presentable, connect it to the completed backend contracts, verify the project twice, update project tracking files, and leave the app running live.

### Implementation
- Replaced the scaffold app shell with the engineering workspace as the primary UI.
- Added reusable frontend components for requirements, validation status, workspace overview, model metadata, design summary, analysis metrics, assumptions, warnings, geometry-ready data, and raw engineering JSON.
- Hardened the frontend API client with structured error handling for backend errors, malformed responses, HTTP failures, and network failures.
- Added explicit frontend types for canonical design, analysis result, model metadata, geometry, validation result, API envelopes, and workspace state.
- Added ESLint 9 flat config and Vitest/jsdom setup.
- Added frontend tests for API client behavior and workspace rendering/state behavior.
- Polished the workspace styling for a quieter engineering UI with clearer hierarchy, status strip, responsive panels, accessible labels, visible loading/error states, and no fabricated engineering values.
- Fixed CSS typography constraints by removing viewport-scaled hero type and nonzero letter spacing.

### Files Changed
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/eslint.config.js`
- `frontend/vite.config.ts`
- `frontend/src/app/App.tsx`
- `frontend/src/app/styles.css`
- `frontend/src/test/setup.ts`
- `frontend/src/types/index.ts`
- `frontend/src/services/designsApi.ts`
- `frontend/src/services/designsApi.test.ts`
- `frontend/src/features/engineering/EngineeringWorkspace.tsx`
- `frontend/src/features/engineering/EngineeringWorkspace.test.tsx`
- `frontend/src/features/engineering/RequirementForm.tsx`
- `frontend/src/features/engineering/ValidationStatus.tsx`
- `frontend/src/features/engineering/StatusMessage.tsx`
- `frontend/src/features/engineering/WorkspaceOverview.tsx`
- `frontend/src/features/engineering/ModelInfoCard.tsx`
- `frontend/src/features/engineering/DesignSummary.tsx`
- `frontend/src/features/engineering/AnalysisMetrics.tsx`
- `frontend/src/features/engineering/AssumptionsPanel.tsx`
- `frontend/src/features/engineering/WarningsPanel.tsx`
- `frontend/src/features/engineering/GeometrySummary.tsx`
- `frontend/src/features/engineering/RawEngineeringData.tsx`
- `frontend/src/features/engineering/formatters.ts`
- `PROJECT_STATUS.md`
- `DEVELOPMENT_LOG.md`
- `docs/development/ROADMAP.md`
- `docs/engineering/README.md`

### Engineering Decisions
- The frontend remains a renderer and workflow controller only; it does not calculate antenna dimensions or analysis metrics.
- Unsupported metrics are explicitly marked unavailable.
- The most recent successful design remains visible after a later failed generation.
- Geometry is displayed as structured, geometry-ready data only; 2D/3D rendering is deferred to Phase 4.

### Tests
- First pass:
  - `PYTHONPATH='.' python -m pytest`: 29 passed in 1.76s
  - `npm run test`: 8 passed in 23.77s
  - `npm run lint`: passed
  - `npm run build`: passed
- Second pass:
  - `PYTHONPATH='.' python -m pytest`: 29 passed in 1.30s
  - `npm run test`: 8 passed in 22.22s
  - `npm run lint`: passed
  - `npm run build`: passed
- Live API checks:
  - Dipole 915 MHz design generation succeeded
  - 915 MHz and 0.915 GHz returned the same design hash
  - Invalid negative frequency returned a structured `VALIDATION_ERROR`
  - Fresh backend and frontend dev servers were started and verified on ports 8000 and 5173

### Problems
- Browser automation through the in-app browser skill could not run because the Node browser-control tool returned a sandbox metadata error.
- Frontend dependencies still report 5 npm audit vulnerabilities from the installed dependency tree.

### Resolutions
- Used API, build, lint, and test verification instead of relying on the unavailable browser-control path.
- Kept dependency-audit remediation out of this UI task because `npm audit fix --force` would permit breaking dependency changes.

### Known Limitations
- No 2D/3D antenna geometry renderer yet.
- No radiation plot rendering yet.
- No frontend saved-design history yet.
- No database persistence, auth, quotas, rate limits, or observability yet.

### Next Step
When requested, begin Phase 4 by rendering canonical geometry payloads in a dedicated visualization layer without moving engineering calculations into the frontend.

## 2026-09-20

### Phase
Phase 3 UI presentation refinement.

### Objective
Make the current workspace look more professional and futuristic while using Times New Roman and preserving engineering honesty.

### Implementation
- Converted the workspace visual system to Times New Roman across the app.
- Restyled the app as a dark engineering console with technical grid background, high-contrast panels, emerald/amber instrumentation accents, stronger hierarchy, and polished status cards.
- Added a clearer hero description and expanded current-status strip.
- Added extra model/design/geometry context fields without introducing new calculations.
- Preserved backend-only engineering calculations and unsupported-metric disclaimers.

### Files Changed
- `frontend/src/app/styles.css`
- `frontend/src/features/engineering/EngineeringWorkspace.tsx`
- `frontend/src/features/engineering/WorkspaceOverview.tsx`
- `frontend/src/features/engineering/RequirementForm.tsx`
- `frontend/src/features/engineering/DesignSummary.tsx`
- `frontend/src/features/engineering/GeometrySummary.tsx`
- `frontend/src/features/engineering/ModelInfoCard.tsx`
- `PROJECT_STATUS.md`
- `DEVELOPMENT_LOG.md`
- `docs/development/ROADMAP.md`
- `docs/engineering/README.md`

### Tests
- First pass:
  - `PYTHONPATH='.' python -m pytest`: 29 passed in 1.36s
  - `npm run test`: 8 passed in 24.22s
  - `npm run lint`: passed
  - `npm run build`: passed
- Second pass:
  - `PYTHONPATH='.' python -m pytest`: 29 passed in 1.52s
  - `npm run test`: 8 passed in 18.39s
  - `npm run lint`: passed
  - `npm run build`: passed

### Known Limitations
- Styling is polished, but still no 2D/3D geometry renderer or plot renderer.
- Browser automation remains unavailable through the in-app browser tool in this environment.

### Next Step
Keep the app live and proceed to Phase 4 visualization only when requested.
