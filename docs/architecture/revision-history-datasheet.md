# Revision History, Comparison, and Datasheet Contract

Saved revisions are immutable snapshots of a canonical design. The in-memory
repository stores revision number, timestamp, requirement snapshot, canonical
design snapshot, and analysis summary. Subsequent working-design changes do not
rewrite an earlier revision.

## APIs

- `GET /api/v1/designs/{design_id}/revisions`
- `GET /api/v1/designs/{design_id}/compare?left=1&right=2`
- `GET /api/v1/designs/{design_id}/datasheet?revision=1`

Comparison is structured from actual parameter snapshots. Indexed list values,
such as `director_lengths_m[2]`, are reported individually. Metrics are compared
only when they exist in the relevant stored analysis summaries; otherwise their
status is `NOT_AVAILABLE`.

The datasheet endpoint currently returns an engineering-document payload,
including canonical design, revision, analysis summary, assumptions, warnings,
model version, design hash, and reproducibility metadata. A rendered PDF export
is deliberately not claimed until a verified document-rendering pipeline exists.
