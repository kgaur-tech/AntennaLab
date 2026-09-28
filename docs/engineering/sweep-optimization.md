# Parameter Sweep and Optimization Baseline

## Scope

`SweepService` evaluates bounded, reproducible candidate designs through the
registered AntennaLab models. It does not calculate antenna physics itself.
Each point is an isolated copy of a canonical base design and is validated and
analyzed by the appropriate internal model.

## APIs

- `POST /api/v1/designs/{design_id}/sweeps`
- `POST /api/v1/designs/{design_id}/optimizations`

Both accept an editable parameter path, start/stop/step, and a metric that is
actually emitted by the selected model analysis. Sweeps are bounded to 101
candidates; invalid points are recorded without aborting the rest of the sweep.

## Optimization

The initial optimizer is `deterministic-grid-search v1`: it evaluates the same
finite range as a sweep, filters invalid candidates, and sorts feasible points
by one declared metric and direction. A reported candidate is the highest
objective score among evaluated feasible candidates—not a universal or global
optimum. No AI or external optimization service is involved.

## Reproducibility and Limits

Sweep identity hashes the canonical base design and complete sweep definition.
Identical runs safely reuse a cached process-local result. Available metrics are
model-specific; unsupported metrics return invalid points rather than invented
curves. Results and cache are not durable until database-backed persistence is
introduced.
