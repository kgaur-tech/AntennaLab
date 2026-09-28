import type { AnalysisResult } from '../../types';
import { formatValue, labelize } from './formatters';

interface AnalysisMetricsProps {
  analysis: AnalysisResult | null;
}

const unsupportedMetrics = ['VSWR', 'S11', 'Efficiency', 'Measured Gain'];

export default function AnalysisMetrics({ analysis }: AnalysisMetricsProps) {
  return (
    <section className="panel">
      <p className="eyebrow">Calculated</p>
      <h2>Analysis Metrics</h2>
      {analysis ? (
        <>
          <div className="kv-row">
            <span>Result Class</span>
            <strong>{analysis.result_class}</strong>
          </div>
          <div className="kv-row">
            <span>Validity</span>
            <strong>{analysis.validity}</strong>
          </div>
          {Object.entries(analysis.metrics).map(([key, value]) => (
            <div className="kv-row" key={key}>
              <span>{labelize(key)}</span>
              <strong>{formatValue(value)}</strong>
            </div>
          ))}
          <div className="unsupported-list">
            {unsupportedMetrics.map((metric) => (
              <div className="kv-row muted-row" key={metric}>
                <span>{metric}</span>
                <strong>Not available in current engineering model</strong>
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
