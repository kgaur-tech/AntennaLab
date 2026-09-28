import type { EngineeringMessage, ValidationResult, WorkspaceState } from '../../types';
import { formatValue, labelize } from './formatters';
import StatusMessage from './StatusMessage';

interface ValidationStatusProps {
  state: WorkspaceState;
  validation: ValidationResult | null;
  message: EngineeringMessage | null;
}

export default function ValidationStatus({ state, validation, message }: ValidationStatusProps) {
  return (
    <section className="panel">
      <p className="eyebrow">Validation Status</p>
      <h2>Requirement Check</h2>
      {state === 'idle' && <p className="muted">Enter antenna requirements to begin.</p>}
      {state === 'validating' && <p className="muted" aria-live="polite">Validating engineering requirements...</p>}
      {message && <StatusMessage message={message} />}
      {validation && (
        <div className="normalized-grid">
          <h3>Normalized Inputs</h3>
          {Object.entries(validation.normalized).map(([key, value]) => (
            <div className="kv-row" key={key}>
              <span>{labelize(key)}</span>
              <strong>{formatValue(value)}</strong>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
