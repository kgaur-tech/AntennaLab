import type { AnalysisResult } from '../../types';

interface PatternSample { angle_deg: number; normalized_response: number; }

function samplesFrom(analysis: AnalysisResult | null): PatternSample[] {
  const data = analysis?.plots[0]?.data;
  if (!Array.isArray(data)) return [];
  return data.filter((sample): sample is PatternSample => (
    typeof sample === 'object' && sample !== null
    && typeof sample.angle_deg === 'number'
    && typeof sample.normalized_response === 'number'
  ));
}

export default function RadiationPattern({ analysis }: { analysis: AnalysisResult | null }) {
  const samples = samplesFrom(analysis);
  if (!analysis || !samples.length) return null;

  const width = 720; const height = 330; const padding = 54;
  const path = samples.map((sample, index) => {
    const x = padding + ((width - padding * 2) * sample.angle_deg / 180);
    const y = height - padding - ((height - padding * 2) * sample.normalized_response);
    return `${index ? 'L' : 'M'}${x.toFixed(2)},${y.toFixed(2)}`;
  }).join(' ');
  const cursor = samples[Math.floor(samples.length / 2)];

  return <section className="analysis-plot" aria-labelledby="radiation-pattern-title">
    <div className="plot-toolbar"><div><p className="eyebrow">Scientific plot</p><h2 id="radiation-pattern-title">Normalized radiation response</h2></div><span className="plot-status">{analysis.result_class} · {analysis.model_version}</span></div>
    <div className="plot-viewport"><svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Normalized radiation response from 0 to 180 degrees">
      {[0, .25, .5, .75, 1].map((value) => { const y = height - padding - ((height - padding * 2) * value); return <g key={value}><line x1={padding} y1={y} x2={width - padding} y2={y} className="plot-gridline" /><text x={padding - 12} y={y + 4} className="plot-label" textAnchor="end">{value.toFixed(2)}</text></g>; })}
      {[0, 45, 90, 135, 180].map((value) => { const x = padding + ((width - padding * 2) * value / 180); return <g key={value}><line x1={x} y1={padding} x2={x} y2={height - padding} className="plot-gridline" /><text x={x} y={height - 20} className="plot-label" textAnchor="middle">{value}°</text></g>; })}
      <path d={path} className="plot-line" />
      <circle cx={padding + ((width - padding * 2) * cursor.angle_deg / 180)} cy={height - padding - ((height - padding * 2) * cursor.normalized_response)} r="5" className="plot-point" />
      <text x={width / 2} y={height - 4} className="plot-axis" textAnchor="middle">Polar angle (degrees)</text><text x="15" y={height / 2} className="plot-axis" textAnchor="middle" transform={`rotate(-90 15 ${height / 2})`}>Normalized power</text>
    </svg></div>
    <p className="plot-note">The displayed curve is normalized analytical output returned by the selected engineering model; it is not absolute gain or a full-wave simulation.</p>
  </section>;
}
