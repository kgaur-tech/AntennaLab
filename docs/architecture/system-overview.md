# System Architecture

## Purpose

AntennaLab is a deterministic RF-design platform. A request flows from a browser
through a versioned HTTP API to internal engineering models; it never delegates
antenna calculations to an external calculation service.

## Runtime Boundaries

```text
React client
  -> FastAPI transport layer
    -> application services and model registry
      -> engineering domain models
        -> canonical design, geometry, and analysis results
```

The frontend owns interaction state and presentation. The backend owns HTTP
contracts, orchestration, and future persistence. The engineering package owns
units, validation, equations, geometry, assumptions, and validity limits.

## Repository Map

| Directory | Responsibility | Must not contain |
| --- | --- | --- |
| `frontend/src/app` | Application composition and global styles | RF calculations |
| `frontend/src/features/engineering` | Engineering-workflow views | API transport details |
| `frontend/src/services` | Typed HTTP clients | UI state |
| `backend/app/api` | Versioned HTTP routes and schemas | Antenna equations |
| `backend/app/services` | Use-case orchestration | UI concerns |
| `backend/app/models` | Application records | Transport validation |
| `engineering` | Deterministic RF domain library | FastAPI or React imports |
| `docs/decisions` | Immutable architecture decisions | Implementation code |

## Contract Rules

- The API uses `{ "success": true, "data": ... }` for every successful
  versioned endpoint and `{ "success": false, "error": ... }` for failures.
- Inputs normalize to SI units inside `engineering`; frequency is Hz and length
  is meters.
- A model registration is the sole supported way to expose a new antenna family.
- Canonical designs are immutable outputs identified by a deterministic hash.
- Every analysis result records result class, assumptions, warnings, and validity.

## Extension Paths

Add an antenna family by implementing the `AntennaModel` contract, registering
its factory and capability metadata in `model_registry.py`, then adding focused
engineering and API tests. Add a persistence implementation behind
`DesignRepository`; services and routes should not acquire database details.

Workers and database packages are reserved integration boundaries. They remain
out of the synchronous request path until a queued, persistent implementation is
introduced.
