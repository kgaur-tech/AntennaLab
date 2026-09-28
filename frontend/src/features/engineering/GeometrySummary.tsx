import type { GeometryModel } from '../../types';
import { formatValue, labelize } from './formatters';

interface GeometrySummaryProps {
  geometry: GeometryModel | null;
}

export default function GeometrySummary({ geometry }: GeometrySummaryProps) {
  return (
    <section className="panel geometry-panel">
      <p className="eyebrow">Geometry-Ready Data</p>
      <h2>Geometry Elements</h2>
      {geometry ? (
        <>
          <div className="kv-row">
            <span>Element Count</span>
            <strong>{geometry.elements.length}</strong>
          </div>
          <div className="kv-row">
            <span>Geometry Family</span>
            <strong>{labelize(geometry.family)}</strong>
          </div>
          <div className="geometry-list">
            {geometry.elements.map((element) => (
              <article className="geometry-item" key={element.name}>
                <div>
                  <strong>{labelize(element.name)}</strong>
                  <span>{element.kind}</span>
                </div>
                <dl>
                  <dt>Length</dt>
                  <dd>{formatValue(element.length_m)} m</dd>
                  <dt>Radius</dt>
                  <dd>{formatValue(element.radius_m)} m</dd>
                  <dt>Position</dt>
                  <dd>{formatValue(element.position_m)}</dd>
                  <dt>Orientation</dt>
                  <dd>{formatValue(element.orientation_deg)} deg</dd>
                </dl>
              </article>
            ))}
          </div>
        </>
      ) : (
        <p className="muted">Geometry data will appear after design generation.</p>
      )}
    </section>
  );
}
