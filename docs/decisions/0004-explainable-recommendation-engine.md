# ADR 0004: Explainable Deterministic Recommendation Engine

## Status

Accepted.

## Decision

Recommendation logic uses a backend capability registry and versioned
deterministic evaluator. Hard constraints exclude candidates before soft scoring.
Every decision is returned as a reason code and user-readable message. Unsupported
criteria are explicitly marked rather than estimated.

## Consequences

The frontend renders backend recommendation data and does not reproduce scoring.
Adding a future antenna model requires capability registration and evaluation
tests. A scoring-method change requires an engine version change.
