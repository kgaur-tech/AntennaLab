interface WarningsPanelProps {
  warnings: string[];
}

export default function WarningsPanel({ warnings }: WarningsPanelProps) {
  return (
    <section className="panel warning-panel">
      <p className="eyebrow">Warnings</p>
      <h2>Model Limitations</h2>
      {warnings.length ? (
        <ul className="dense-list">
          {warnings.map((warning) => (
            <li key={warning}>{warning}</li>
          ))}
        </ul>
      ) : (
        <p className="muted">No warnings returned by the current model.</p>
      )}
    </section>
  );
}
