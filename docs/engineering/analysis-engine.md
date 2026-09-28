# Fast Analytical Analysis Engine

## Scope

Phase 4 exposes internal Tier 1 analysis through `AnalysisService`. It runs
registered engineering models synchronously and returns a versioned, structured
result for the exact canonical design input.

## Supported Analysis

The dipole model is the first complete reference pipeline. It uses the existing
thin, center-fed half-wave dipole analytical E-plane power expression:

```text
[cos((π / 2) cos θ) / sin θ]²
```

The axis null is defined by its limiting value of zero. Samples span 0°–180°;
θ is the polar angle from the element axis. Responses are normalized power, not
absolute gain. The model also returns wavelength, electrical length, theoretical
reference directivity, and reference input impedance as explicitly idealized
calculated quantities.

Monopole analytical outputs and Yagi-Uda dimensional outputs remain available
through their existing models, with their stated assumptions and limitations.
Yagi-Uda does not report gain, impedance, VSWR, bandwidth, or radiation pattern.

## Result Classification and Cache

Results are `CALCULATED`, `fast_analytical`, and `COMPLETED`. They are not
full-wave simulations or measurements. The cache key is a SHA-256 hash of model
family/version, normalized frequency, canonical parameters, and settings.
Identical input returns the cached result; relevant parameter changes produce a
new hash.

## API

- `POST /api/v1/designs/{design_id}/analysis`
- `GET /api/v1/designs/{design_id}/analysis`
- `GET /api/v1/analysis/{analysis_id}`

Each result reports design/analysis IDs, input hash, computation time, timestamp,
model version, assumptions, validity, warnings, metrics, and plotting samples.
