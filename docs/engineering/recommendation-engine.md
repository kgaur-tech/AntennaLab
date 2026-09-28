# Requirement and Recommendation Engine

## Scope

`recommendation-engine-v1` ranks only the registered AntennaLab models: dipole,
monopole, and Yagi-Uda. It is deterministic and runs entirely inside the
backend; it does not call external antenna, simulation, or AI services.

## Requirement Contract

Requirements capture application, frequency and unit, optional bandwidth/gain,
polarization, directionality, maximum dimensions, environment, feed metadata,
and priority weights. Frequency normalization reuses `engineering.core.units`.
Current accepted weights are `gain`, `size`, `bandwidth`, `efficiency`,
`simplicity`, and `cost`, each in the range 0–3.

## Evaluation

Hard constraints are checked before scores are calculated:

- model frequency validity range;
- explicit directionality requirement;
- explicit supported polarization;
- supplied maximum dimension against the model's canonical dimensional envelope.

A failing hard constraint excludes the candidate. It cannot be offset by any
soft score. Eligible candidates receive a 0–100 weighted score from only
evaluated components. The current evaluated components are simplicity and size
when a size constraint is supplied. Gain and bandwidth compatibility are marked
`UNSUPPORTED`, because the registered models do not calculate those requirement
fits. No missing engineering value is inferred.

## Output and Reproducibility

`POST /api/v1/recommendations` returns the normalized requirement, engine
version, highest-scoring eligible candidate, alternatives, excluded candidates,
hard-constraint decisions, score components, reason codes, tradeoffs, and
warnings. The same requirement produces the same ordered response.

`POST /api/v1/requirements` validates and normalizes an independent requirement
payload. The original compatibility route remains available at
`POST /api/v1/requirements/recommend`.

## Limitations

The capability registry describes model support, not measured or simulated
performance. Environment, connector, and feed requirements are captured but are
not presently evaluated as engineering constraints. The recommended candidate
means “highest-scoring eligible registered model,” not “universally best
antenna.”
