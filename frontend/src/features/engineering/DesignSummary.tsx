import type { CanonicalDesign } from '../../types';
import { formatValue, labelize } from './formatters';

interface DesignSummaryProps {
  design: CanonicalDesign | null;
  onCopyHash: () => void;
  copied: boolean;
}

export default function DesignSummary({ design, onCopyHash, copied }: DesignSummaryProps) {
  return (
    <section className="panel design-summary">
      <p className="eyebrow">Canonical Design</p>
      <h2>Design Summary</h2>
      {design ? (
        <>
          <div className="kv-row">
            <span>Design ID</span>
            <strong className="mono">{design.design_id}</strong>
          </div>
          <div className="kv-row">
            <span>Frequency</span>
            <strong>{formatValue(design.frequency_hz)} Hz</strong>
          </div>
          <div className="kv-row">
            <span>Antenna Type</span>
            <strong>{labelize(design.family)}</strong>
          </div>
          <div className="kv-row">
            <span>Model Version</span>
            <strong>{design.model_version}</strong>
          </div>
          <div className="hash-row">
            <div>
              <span>Design Hash</span>
              <strong className="mono">{design.design_hash}</strong>
            </div>
            <button type="button" className="icon-button" onClick={onCopyHash} aria-label="Copy design hash">
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>
          <h3>Dimensions</h3>
          <div className="metric-grid">
            {Object.entries(design.dimensions_m).map(([key, value]) => (
              <div className="metric-cell" key={key}>
                <span>{labelize(key)}</span>
                <strong>{formatValue(value)}</strong>
              </div>
            ))}
          </div>
        </>
      ) : (
        <p className="muted">No design generated yet.</p>
      )}
    </section>
  );
}
