interface AssumptionsPanelProps {
  assumptions: string[];
}

export default function AssumptionsPanel({ assumptions }: AssumptionsPanelProps) {
  return (
    <section className="panel">
      <p className="eyebrow">Assumed</p>
      <h2>Engineering Assumptions</h2>
      {assumptions.length ? (
        <ul className="dense-list">
          {assumptions.map((assumption) => (
            <li key={assumption}>{assumption}</li>
          ))}
        </ul>
      ) : (
        <p className="muted">No assumptions returned yet.</p>
      )}
    </section>
  );
}
