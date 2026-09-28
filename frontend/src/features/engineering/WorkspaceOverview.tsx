import type { DesignGenerationResult, ModelMetadata, ValidationResult, WorkspaceState } from '../../types';
import { formatValue, labelize } from './formatters';

interface WorkspaceOverviewProps {
  state: WorkspaceState;
  models: ModelMetadata[];
  validation: ValidationResult | null;
  result: DesignGenerationResult | null;
}

export default function WorkspaceOverview({ state, models, validation, result }: WorkspaceOverviewProps) {
  const selectedModel = result?.model.model ?? validation?.model.model ?? 'None';
  const resultClass = result?.analysis.result_class ?? 'Not generated';
  const frequency = result?.design.frequency_hz ?? validation?.normalized.frequency_hz ?? null;

  return (
    <section className="overview-strip" aria-label="Current project status">
      <div className="overview-item">
        <span>Workspace State</span>
        <strong>{labelize(state)}</strong>
      </div>
      <div className="overview-item">
        <span>Models Loaded</span>
        <strong>{models.length}</strong>
      </div>
      <div className="overview-item">
        <span>Active Model</span>
        <strong>{labelize(String(selectedModel))}</strong>
      </div>
      <div className="overview-item">
        <span>Normalized Frequency</span>
        <strong>{frequency ? `${formatValue(frequency)} Hz` : 'Pending'}</strong>
      </div>
      <div className="overview-item">
        <span>Result Class</span>
        <strong>{resultClass}</strong>
      </div>
    </section>
  );
}
