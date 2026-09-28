# ADR 0001: Phase 1 Engineering Core Contracts

## Status

Accepted.

## Context

AntennaLab must keep antenna calculations deterministic, internal, reproducible, and separate from API/UI transport. The Phase 1 implementation needed a stable contract for units, model outputs, geometry, result classification, and future caching.

## Decision

- Normalize frequency to Hz and length to meters inside engineering models.
- Centralize constants and wavelength calculations in `engineering/core`.
- Use versioned antenna models with explicit assumptions and validity ranges.
- Serialize designs through `AntennaDesign.to_dict()`.
- Generate deterministic design hashes from model identity, normalized inputs, canonical parameters, and analysis settings.
- Use `AnalysisResult` with explicit result classes.
- Mark Phase 1 Yagi-Uda output as dimensional/heuristic geometry only and avoid unsupported gain, impedance, VSWR, or front-to-back claims.

## Consequences

- Backend and frontend must consume canonical engineering payloads rather than recomputing formulas.
- Future caches, revisions, sweeps, and optimization can use the same deterministic identity.
- Unsupported analysis must be represented by warnings or explicit errors instead of invented metrics.
