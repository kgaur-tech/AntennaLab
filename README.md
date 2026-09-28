# AntennaLab

AntennaLab is a deterministic RF engineering workspace that turns requirements
into traceable canonical antenna designs. The current product supports dipole,
monopole, and Yagi-Uda workflows through a React client, FastAPI API, and an
internal Python engineering library.

## Architecture at a Glance

`frontend/` owns presentation and interaction. `backend/` owns versioned HTTP
contracts and use-case orchestration. `engineering/` owns units, validation,
equations, geometry, and analysis. Antenna equations never live in the UI or
routes. Read the [system architecture](docs/architecture/system-overview.md)
before adding a new capability.

## Local Commands

```powershell
python -m pytest
npm --prefix frontend run test
npm --prefix frontend run lint
npm --prefix frontend run build
npm run dev
```

The root development command starts the API on port 8000 and the Vite client on
port 5173. Install Python dependencies from `backend/requirements.txt` and UI
dependencies with `npm --prefix frontend install` first.

## Product Vision

AntennaLab is built around the closed design loop:

Requirement → Recommendation → Design → Simulation → Modification → Re-simulation → Optimization → Datasheet → Manufacturing / Learn

The system is designed for students, engineers, and teams who need a practical workflow from requirements to a manufacturable antenna design while understanding assumptions and limitations.

## Core Principles

- Deterministic engineering logic lives in the AntennaLab engineering layer.
- AI assists with requirement interpretation and documentation, not with fabricated engineering values.
- Core antenna calculations and geometry generation are implemented internally.
- The first release focuses on a small set of well-understood antenna families and validated workflows.
- Simulation and optimization are asynchronous, debounced, and cache-aware.

## Repository Structure

- frontend/: user interface, data layer, visualization, dashboard, and RF workflow screens
- backend/: API server, domain models, schemas, business logic, orchestration, and persistence
- engineering/: internal RF mathematical model library, geometry, validation, and antenna families
- workers/: async simulation, optimization, and export workers
- database/: schemas and migrations for persistent application state
- docs/: architecture, engineering methods, API references, and decision records
- tests/: cross-cutting validation and integration tests

## Implementation Phases

1. Phase 0 — Scope freeze and system contracts
2. Phase 1 — Engineering core and first validated antenna models
3. Phase 2 — FastAPI backend and persistence layer
4. Phase 3 — Requirement wizard and recommendation UI
5. Phase 4 — 3D parameterized designer
6. Phase 5 — Fast simulation and plotting
7. Phase 6 — Sweeps and design revisions
8. Phase 7 — Optimization engine
9. Phase 8 — High-accuracy worker pipeline
10. Phase 9 — Datasheets and learning flows
11. Phase 10 — Manufacturing workflow
12. Phase 11 — Production hardening and monitoring

## Engineering Constraint

No external antenna-calculation API is used. All relevant calculations are implemented in the internal engineering modules under the repository's engineering namespace.

## Getting Started

This repository is scaffolded for a monorepo architecture. The repository is intentionally designed to evolve phase-by-phase rather than fake a full product in a single pass.

- Backend: Python with FastAPI
- Frontend: React + TypeScript (or compatible modern UI stack)
- Engineering: Python numerical and analytical models
- Data: PostgreSQL and Redis patterns, with simple interfaces for future implementation

## Status

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for the current milestone and progress summary.
