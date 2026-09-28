# AntennaLab Architecture

## Current Reference

Read [System Architecture](system-overview.md) for the authoritative repository
map, runtime boundaries, API contract rules, and extension paths. The remaining
content describes the longer-term product direction.

## System Objective

AntennaLab is an RF engineering platform that transforms a user's design requirement into a defensible design recommendation, deterministic calculation pipeline, analysis, optimization, datasheet output, and manufacturing guidance.

## Core Layers

- Frontend: user workflow and interactive visualization
- Backend: API, orchestration, persistence, and business logic
- Engineering: deterministic formulas, geometry rules, and antenna families
- Workers: compute-intensive simulation and export jobs
- Database: persistent project state, designs, revisions, and metadata

## Design Principles

- The engineering layer owns all antenna equations.
- UI is not the source of truth for RF calculations.
- Simulation jobs are debounced and cached.
- Deterministic models are preferred over opaque heuristics.
- Every design output should include assumptions and traceability.

## MVP Scope

- 3 antenna families: dipole, monopole, and Yagi-Uda
- Requirement intake and recommendation workflow
- Deterministic dimension generation
- 3D geometry preview and parameter editing
- Basic optimization and revision support
- Datasheet export and learning content shell
