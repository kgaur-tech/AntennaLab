# ADR 0003: Layer Boundaries and API Envelopes

## Status

Accepted.

## Context

The project has a working engineering workspace, but its intended ownership
boundaries were not documented in one place. Recommendation responses also used
a legacy response shape while the rest of the versioned API used standard
success/error envelopes.

## Decision

- Treat `frontend`, `backend`, and `engineering` as separate ownership layers.
- Keep the version prefix in application configuration and attach it when the
  FastAPI application is composed.
- Use an application factory so tests and future deployment entry points can
  construct the API consistently.
- Require the standard API success/error envelope for recommendation responses
  as well as design, model, and validation responses.
- Maintain root developer commands and Python test discovery configuration.

## Consequences

- Clients have one predictable failure model for all versioned endpoints.
- A deployment can change the API prefix without editing route modules.
- The current repository remains a modular monorepo without prematurely adding
  microservices or persistence infrastructure.
