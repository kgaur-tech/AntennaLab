import type { ModelMetadata } from '../../types';
import { labelize } from './formatters';

interface ModelInfoCardProps {
  model: ModelMetadata | null;
}

export default function ModelInfoCard({ model }: ModelInfoCardProps) {
  return (
    <section className="panel">
      <p className="eyebrow">Model</p>
      <h2>{model ? labelize(model.model) : 'No model selected'}</h2>
      {model ? (
        <>
          <div className="kv-row">
            <span>Version</span>
            <strong>{model.model_version}</strong>
          </div>
          <div className="kv-row">
            <span>Capability Count</span>
            <strong>{model.capabilities.length}</strong>
          </div>
          <div className="tag-row" aria-label="Model capabilities">
            {model.capabilities.map((capability) => (
              <span className="tag" key={capability}>{labelize(capability)}</span>
            ))}
          </div>
        </>
      ) : (
        <p className="muted">Generate a design to see backend model metadata.</p>
      )}
    </section>
  );
}
