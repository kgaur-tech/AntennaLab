# Design Lifecycle and Geometry Contract

Canonical designs are generated only by the registered AntennaLab engineering
models. A design contains its stable ID, family, model version, normalized
frequency, machine-readable parameters, materials, feed, geometry, assumptions,
warnings, and deterministic design hash.

## Lifecycle API

- `POST /api/v1/designs` generates and stores a canonical design.
- `GET /api/v1/designs/{design_id}` retrieves it.
- `PATCH /api/v1/designs/{design_id}` accepts supported parameter changes and
  regenerates through the owning engineering model.
- `POST /api/v1/designs/{design_id}/validate` runs model validation.
- `POST /api/v1/designs/{design_id}/regenerate-geometry` regenerates the
  canonical geometry from the stored parameters.
- `POST /api/v1/designs/{design_id}/revisions` creates an explicit immutable
  revision snapshot.

The current repository implementation is an in-memory persistence adapter. It
preserves the lifecycle during one backend process but does not claim durable
database storage.

## Geometry

Geometry is serialized in meters as named wire elements with length, radius,
position, orientation, and metadata. The frontend 3D viewer receives this
payload; it does not calculate element lengths or positions. The Yagi model
preserves individual director lengths and spacings, so changing `director_3`
does not alter its siblings.
