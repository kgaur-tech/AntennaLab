# ADR 0002: Backend Package And API Foundation

## Status

Accepted.

## Context

Phase 2 needed a stable backend boundary around the completed engineering core. The previous backend mixed `app.*` and `backend.app.*` imports, returned loose dictionaries from routes, and had no centralized mapping from engineering failures to stable API errors.

## Decision

- Standardize backend imports on `backend.app.*` from the repository root.
- Keep existing files in place rather than moving packages.
- Keep routes thin: routes accept Pydantic request schemas and call services.
- Keep engineering formulas and canonical design generation inside `engineering/`.
- Use `DesignService` as the requirement-to-design orchestration layer.
- Use `AntennaModelRegistry` for supported model lookup and capabilities.
- Return API envelopes of the form `{ "success": true, "data": ... }` and `{ "success": false, "error": ... }`.
- Install FastAPI exception handlers for request validation, engineering exceptions, explicit API exceptions, and unexpected internal exceptions.
- Turn FastAPI debug response mode off so unexpected errors return safe JSON instead of stack traces.
- Add persistence-ready `DesignRecord` and `DesignRevisionRecord` contracts without connecting a database.
- Keep API schemas separate from engineering-core objects so transport contracts can evolve without changing scientific model internals.

## Consequences

- Tests now pass from the project root with `PYTHONPATH='.'` and also with the previous `PYTHONPATH='backend;.'` command.
- Future models can be added by registering model metadata and a factory.
- Frontend code can consume typed canonical design and analysis responses.
- Database persistence can be added later around the existing record/revision payloads without redesigning the design-generation endpoint.
