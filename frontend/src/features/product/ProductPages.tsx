import { useState, type ReactNode } from 'react';

import { EngineeringApiError } from '../../services/designsApi';
import { getExplainableRecommendations } from '../../services/requirementsApi';
import type { ExplainableRecommendationResponse, RequirementInput } from '../../types';

export type PageName =
  | 'home' | 'explore' | 'detail' | 'design' | 'recommendations' | 'workspace'
  | 'simulation' | 'sweep' | 'optimization' | 'designs' | 'datasheets' | 'learn'
  | 'fabrication' | 'manufacturing' | 'projects' | 'docs' | 'about';

export interface AppRoute { page: PageName; slug?: string }

const nav = [
  ['Home', '/'], ['Explore', '/explore'], ['Design', '/design'], ['Recommendations', '/recommendations'],
  ['Workspace', '/workspace'], ['Simulation', '/simulation'], ['Optimization', '/optimization'],
  ['Design History', '/designs'], ['Learn', '/learn'], ['Datasheets', '/datasheets'], ['Manufacturing', '/manufacturing'],
] as const;

const families = {
  dipole: {
    title: 'Dipole', directionality: 'Omnidirectional broadside pattern', polarization: 'Linear',
    applications: 'Telemetry, general RF links, reference antennas', status: 'Canonical design, geometry, and analytical pattern available.',
    method: 'Half-wave thin-dipole approximation using normalized frequency and free-space wavelength.',
    assumptions: 'Thin conductor and free-space conditions. Feed, installation, and material effects are not included.',
    parameters: ['Frequency', 'Element radius'],
  },
  monopole: {
    title: 'Monopole', directionality: 'Upper-hemisphere pattern', polarization: 'Vertical',
    applications: 'Embedded devices, IoT nodes, vehicle and ground-plane installations', status: 'Canonical design, geometry, and analytical pattern available.',
    method: 'Quarter-wave monopole image-theory approximation over an ideal ground plane.',
    assumptions: 'An electrically significant ideal ground plane is assumed. Platform and cable coupling are not included.',
    parameters: ['Frequency', 'Element radius'],
  },
  'yagi-uda': {
    title: 'Yagi-Uda', directionality: 'Directional', polarization: 'Linear',
    applications: 'Point-to-point links, directional telemetry, ground stations', status: 'Canonical parameterized geometry available; analysis is dimensional and heuristic.',
    method: 'Canonical proportional dimensions for reflector, driven element, directors, spacing, and boom.',
    assumptions: 'This is a geometry seed. Gain, impedance, VSWR, bandwidth, and radiation pattern are not calculated.',
    parameters: ['Frequency', 'Director count', 'Reflector length', 'Driven element length', 'Director lengths', 'Element spacings', 'Element radius'],
  },
} as const;

export function resolveRoute(hash: string): AppRoute {
  const path = (hash.replace(/^#/, '') || '/').split('?')[0];
  if (path === '/') return { page: 'home' };
  if (path.startsWith('/explore/')) return { page: 'detail', slug: path.split('/')[2] };
  if (path.startsWith('/design/')) return { page: 'workspace' };
  if (path.startsWith('/learn/')) return { page: 'learn', slug: path.split('/')[2] };
  const mapping: Record<string, PageName> = {
    '/explore': 'explore', '/design': 'design', '/recommendations': 'recommendations', '/workspace': 'workspace',
    '/simulation': 'simulation', '/sweep': 'sweep', '/optimization': 'optimization', '/designs': 'designs',
    '/datasheets': 'datasheets', '/history': 'designs', '/learn': 'learn', '/fabrication': 'fabrication', '/manufacturing': 'manufacturing',
    '/projects': 'projects', '/docs': 'docs', '/about': 'about',
  };
  return { page: mapping[path] ?? 'home' };
}

const Link = ({ to, children, className = '' }: { to: string; children: ReactNode; className?: string }) => (
  <a className={className} href={`#${to}`}>{children}</a>
);

export function ProductShell({ route, children }: { route: AppRoute; children: ReactNode }) {
  return <div className="product-shell">
    <a className="skip-link" href="#main-content">Skip to main content</a>
    <header className="product-header">
      <Link to="/" className="brand"><span className="brand-mark">A</span><span>AntennaLab</span></Link>
      <nav aria-label="Primary navigation" className="primary-nav">
        {nav.map(([label, href]) => <Link key={href} to={href} className={route.page === (href === '/' ? 'home' : href.slice(1).replace('designs', 'designs')) ? 'active' : ''}>{label}</Link>)}
      </nav>
      <Link to="/design" className="button primary-button header-cta">Start designing</Link>
    </header>
    <main id="main-content" className={route.page === 'workspace' ? 'workspace-page' : 'product-main'}>{children}</main>
    <footer className="product-footer"><span>© 2026 AntennaLab</span><span>Internal engineering models · Traceable results · No external antenna APIs</span><Link to="/docs">Documentation</Link></footer>
  </div>;
}

function PageHeader({ eyebrow, title, description, actions }: { eyebrow: string; title: string; description: string; actions?: ReactNode }) {
  return <section className="page-header"><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{description}</p>{actions && <div className="header-actions">{actions}</div>}</section>;
}

function StatusBadge({ children, kind = 'available' }: { children: ReactNode; kind?: 'available' | 'limited' | 'planned' | 'example' }) {
  return <span className={`status-badge ${kind}`}>{children}</span>;
}

function EmptyState({ title, children, action }: { title: string; children: ReactNode; action?: ReactNode }) {
  return <section className="empty-state"><p className="eyebrow">Current availability</p><h2>{title}</h2><p>{children}</p>{action}</section>;
}

function Home() {
  return <>
    <section className="home-hero">
      <div><p className="eyebrow">Engineering software for antenna work</p><h1>From requirements to antenna design.</h1><p>Design, analyze, and understand antennas without manually managing every engineering workflow. Every result is generated by AntennaLab’s internal models and carries its assumptions.</p><div className="header-actions"><Link to="/design" className="button primary-button">Start designing</Link><Link to="/explore" className="button secondary-button">Explore antennas</Link></div></div>
      <aside className="hero-card"><StatusBadge>Engineering-first workflow</StatusBadge><ol><li>Capture requirements</li><li>Recommend a family</li><li>Generate canonical geometry</li><li>Inspect calculated results</li><li>Prepare to build and measure</li></ol></aside>
    </section>
    <section><div className="section-heading"><p className="eyebrow">Workflow</p><h2>One connected engineering path</h2></div><div className="workflow"><span>Requirements</span><i>→</i><span>Recommendation</span><i>→</i><span>Design</span><i>→</i><span>Analyze</span><i>→</i><span>Optimize</span><i>→</i><span>Build</span></div></section>
    <section><div className="section-heading"><p className="eyebrow">Platform</p><h2>Designed to grow with the work</h2></div><div className="feature-grid">{[
      ['Requirement-driven design', 'Translate practical goals into structured engineering input.', 'available'], ['Canonical calculations', 'Generate reproducible dimensions with explicit model versions.', 'available'], ['3D geometry', 'Inspect the returned engineering geometry in the design workspace.', 'available'], ['Analysis', 'Review only metrics supported by the selected internal model.', 'available'], ['Parameter sweeps', 'Compare a model parameter against calculated metrics.', 'planned'], ['Optimization', 'Define objectives and constraints for future solver workflows.', 'planned'], ['Datasheets', 'Prepare traceable design summaries from canonical outputs.', 'planned'], ['Learning', 'Connect engineering decisions to responsible RF fundamentals.', 'available'],
    ].map(([title, text, state]) => <article className="feature-card" key={title}><StatusBadge kind={state as 'available' | 'planned'}>{state === 'available' ? 'Available' : 'Planned'}</StatusBadge><h3>{title}</h3><p>{text}</p></article>)}</div></section>
    <section><div className="section-heading"><p className="eyebrow">Supported families</p><h2>Start with a defensible model</h2></div><div className="family-grid">{Object.entries(families).map(([slug, family]) => <article className="family-card" key={slug}><StatusBadge kind={slug === 'yagi-uda' ? 'limited' : 'available'}>{slug === 'yagi-uda' ? 'Geometry model' : 'Analytical model'}</StatusBadge><h3>{family.title}</h3><p>{family.applications}</p><Link to={`/explore/${slug}`} className="text-link">View model details →</Link></article>)}</div></section>
  </>;
}

function Explore() { return <><PageHeader eyebrow="Model library" title="Explore antennas" description="Understand the capabilities, assumptions, and applicability of the engineering models currently available in AntennaLab." /> <div className="family-grid">{Object.entries(families).map(([slug, family]) => <article className="family-card detailed" key={slug}><StatusBadge kind={slug === 'yagi-uda' ? 'limited' : 'available'}>{slug === 'yagi-uda' ? 'Limited analysis' : 'Calculated pattern'}</StatusBadge><h2>{family.title}</h2><dl><dt>Applications</dt><dd>{family.applications}</dd><dt>Directionality</dt><dd>{family.directionality}</dd><dt>Polarization</dt><dd>{family.polarization}</dd><dt>Model status</dt><dd>{family.status}</dd></dl><Link to={`/explore/${slug}`} className="button secondary-button">Explore {family.title}</Link></article>)}</div></>; }

function Detail({ slug }: { slug?: string }) {
  const family = families[slug as keyof typeof families] ?? families.dipole;
  const stableSlug = slug && slug in families ? slug : 'dipole';
  return <><PageHeader eyebrow="Antenna model" title={family.title} description={family.status} actions={<Link to={`/design?family=${stableSlug}`} className="button primary-button">Design this antenna</Link>} /> <div className="detail-grid"><section className="panel light-panel"><h2>Overview</h2><p>{family.title} is represented by an internal, versioned AntennaLab model. The model turns normalized requirements into a canonical design and geometry payload.</p><h2>Typical applications</h2><p>{family.applications}</p><h2>Design method</h2><p>{family.method}</p></section><section className="panel light-panel"><h2>Engineering parameters</h2><ul className="dense-list">{family.parameters.map((item) => <li key={item}>{item}</li>)}</ul><h2>Assumptions and validity</h2><p>{family.assumptions}</p><StatusBadge kind="limited">Review before fabrication</StatusBadge></section></div><section className="panel light-panel"><p className="eyebrow">Analysis availability</p><h2>What this model can report</h2><p>{stableSlug === 'yagi-uda' ? 'Canonical dimensions, element count, and boom length. No gain, impedance, VSWR, or radiation-pattern values are generated.' : 'Canonical dimensions, idealized reference impedance/directivity, and a normalized analytical pattern. These are calculated results, not full-wave simulation.'}</p></section></>;
}

const startingRequirement: RequirementInput = { application: 'Custom application', frequency_hz: 915_000_000, polarization: 'linear', is_directional: false, directionality: 'no_preference', target_impedance_ohms: 50, environment: 'general', priority_weights: { gain: 1, size: 1, bandwidth: 1, simplicity: 1 } };

function DesignWizard() {
  const [step, setStep] = useState(1); const [form, setForm] = useState(startingRequirement);
  const update = (patch: Partial<RequirementInput>) => setForm((current) => ({ ...current, ...patch }));
  const fields: Record<number, ReactNode> = {
    1: <label>What are you trying to build?<input value={form.application} onChange={(e) => update({ application: e.target.value })} placeholder="Rocket telemetry, Wi-Fi link, custom application" /></label>,
    2: <label>Operating frequency (Hz)<input type="number" min="1" value={form.frequency_hz} onChange={(e) => update({ frequency_hz: Number(e.target.value) })} /></label>,
    3: <div className="form-grid"><label>Target gain (dBi)<input type="number" value={form.gain_db ?? ''} onChange={(e) => update({ gain_db: Number(e.target.value) })} /></label><label>Polarization<select value={form.polarization} onChange={(e) => update({ polarization: e.target.value })}><option value="no_preference">No preference</option><option value="linear">Linear</option><option value="vertical">Vertical</option><option value="horizontal">Horizontal</option><option value="circular">Circular</option></select></label><label>Directionality<select value={form.directionality ?? 'no_preference'} onChange={(e) => update({ directionality: e.target.value as RequirementInput['directionality'], is_directional: e.target.value === 'directional' || e.target.value === 'highly_directional' })}><option value="no_preference">No preference</option><option value="omnidirectional">Omnidirectional</option><option value="directional">Directional</option><option value="highly_directional">Highly directional</option></select></label></div>,
    4: <label>Maximum dimension (m)<input type="number" min="0" step="any" value={form.max_dimension_m ?? ''} onChange={(e) => update({ max_dimension_m: Number(e.target.value) })} /></label>,
    5: <label>Environment<select value={form.environment} onChange={(e) => update({ environment: e.target.value })}><option value="general">General</option><option value="free_space">Free space</option><option value="ground_mounted">Ground mounted</option><option value="vehicle_mounted">Vehicle mounted</option><option value="rocket_uav_mounted">Rocket / UAV mounted</option></select></label>,
    6: <div><p>Priorities are used by the current internal recommendation engine where supported.</p><div className="form-grid">{['gain', 'size', 'bandwidth'].map((key) => <label key={key}>{key}<input type="number" min="0" max="3" step="0.5" value={form.priority_weights?.[key] ?? 1} onChange={(e) => update({ priority_weights: { ...form.priority_weights, [key]: Number(e.target.value) } })} /></label>)}</div></div>,
  };
  return <><PageHeader eyebrow="New design" title="What are you trying to build?" description="Capture the operating context first. AntennaLab will use these structured requirements to request an internal recommendation." /><section className="wizard panel light-panel"><div className="stepper">{['Application', 'Frequency', 'Performance', 'Constraints', 'Environment', 'Priorities'].map((label, index) => <span className={index + 1 === step ? 'current' : index + 1 < step ? 'done' : ''} key={label}>{index + 1}. {label}</span>)}</div><h2>Step {step}: {['Application', 'Frequency', 'Performance requirements', 'Physical constraints', 'Environment', 'Priorities'][step - 1]}</h2>{fields[step]}<div className="header-actions"><button className="secondary-button" type="button" disabled={step === 1} onClick={() => setStep(step - 1)}>Back</button>{step < 6 ? <button className="primary-button" type="button" onClick={() => setStep(step + 1)}>Continue</button> : <a href="#/recommendations" className="button primary-button" onClick={() => sessionStorage.setItem('antennaLab.requirement', JSON.stringify(form))}>Review recommendations</a>}</div></section><p className="helper-note">This representative wizard holds the requirement locally until recommendation. It does not claim to save a project.</p></>;
}

function Recommendations() {
  const [result, setResult] = useState<ExplainableRecommendationResponse | null>(null); const [error, setError] = useState<string | null>(null); const [loading, setLoading] = useState(false);
  const saved = sessionStorage.getItem('antennaLab.requirement');
  const requirement = saved ? JSON.parse(saved) as RequirementInput : startingRequirement;
  const run = async () => { setLoading(true); setError(null); try { setResult(await getExplainableRecommendations(requirement)); } catch (reason) { setError(reason instanceof EngineeringApiError ? reason.message : 'Recommendations are unavailable while the backend cannot be reached.'); } finally { setLoading(false); } };
  const renderCandidate = (item: NonNullable<ExplainableRecommendationResponse['recommended']>[number], primary = false) => <article className="recommendation-card" key={item.family}><StatusBadge kind={primary ? 'available' : 'example'}>{primary ? 'Highest-scoring eligible candidate' : 'Alternative'}</StatusBadge><h2>{families[item.family === 'yagi_uda' ? 'yagi-uda' : item.family]?.title ?? item.family}</h2><p className="score">Compatibility score <strong>{item.score?.toFixed(2) ?? 'Not evaluated'}</strong></p><h3>Why considered</h3><ul className="dense-list">{item.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul>{item.tradeoffs.length > 0 && <><h3>Tradeoffs</h3><ul className="dense-list">{item.tradeoffs.map((tradeoff) => <li key={tradeoff}>{tradeoff}</li>)}</ul></>}<p className="muted">{item.score_components.filter((component) => component.status !== 'EVALUATED').map((component) => component.message).join(' ')}</p><Link to="/workspace" className="text-link">Design this antenna →</Link></article>;
  return <><PageHeader eyebrow="Internal recommendation engine" title="Recommended antenna types" description="Candidates are filtered by hard constraints, then ranked with deterministic, versioned scoring. Scores and reasons come from AntennaLab—not an external antenna service." actions={<button className="primary-button" onClick={() => void run()} disabled={loading}>{loading ? 'Evaluating antenna models…' : 'Find suitable antennas'}</button>} />{error && <section className="status status-error" role="alert"><strong>Recommendation unavailable</strong><span>{error}</span></section>}{result ? <><section className="panel light-panel"><p className="eyebrow">Requirement summary · {result.engine_version}</p><h2>{String(result.requirement.application)} at {String(result.requirement.frequency_hz)} Hz</h2>{result.warnings.map((warning) => <p className="muted" key={warning}>{warning}</p>)}</section>{result.recommended.length ? <section className="recommendation-grid">{renderCandidate(result.recommended[0], true)}{result.alternatives.map((item) => renderCandidate(item))}</section> : <EmptyState title="No eligible antenna model found">No currently supported model satisfies every hard constraint. Review excluded options below to understand why.</EmptyState>}<section className="panel light-panel"><p className="eyebrow">Excluded options</p><h2>Hard-constraint decisions</h2>{result.excluded_candidates.length ? <ul className="dense-list">{result.excluded_candidates.map((item) => <li key={item.family}><strong>{item.family}</strong>: {item.reasons.join(' ')}</li>)}</ul> : <p className="muted">No candidates were excluded by hard constraints.</p>}</section></> : <EmptyState title="No recommendation run yet">Start with the internal recommendation engine. It reports unsupported criteria rather than inventing engineering results.</EmptyState>}</>;
}

const pageContent: Partial<Record<PageName, { eyebrow: string; title: string; description: string; state: string; action?: [string, string] }>> = {
  simulation: { eyebrow: 'Analysis', title: 'Simulation and analysis', description: 'Inspect available analysis results from a generated design. AntennaLab distinguishes calculated, predicted, simulated, and measured results.', state: 'No simulation is available yet. Generate a design in the workspace to inspect its available calculated analysis.' , action: ['Open workspace', '/workspace'] },
  sweep: { eyebrow: 'Analysis', title: 'Parameter sweep', description: 'Compare a model-supported parameter against an internal engineering metric.', state: 'Parameter sweeps are not implemented. No example curve is shown because that could be mistaken for a calculated result.', action: ['Explore models', '/explore'] },
  optimization: { eyebrow: 'Optimization', title: 'Optimization workspace', description: 'Future objectives, constraints, variables, search strategy, and candidate designs will remain traceable to the internal engineering engine.', state: 'Limited preview. An optimization engine is not implemented, so no candidates or optimized values are shown.' },
  designs: { eyebrow: 'Library', title: 'Design history', description: 'Designs will group revisions by model version, requirements, canonical parameters, and result summaries.', state: 'Temporary empty state: persistence is not implemented, so AntennaLab cannot claim these designs are saved permanently.', action: ['Create a design', '/design'] },
  datasheets: { eyebrow: 'Documentation output', title: 'Datasheets', description: 'A future datasheet will assemble a canonical design, geometry, calculated metrics, assumptions, warnings, model version, and revision.', state: 'Datasheet export is planned. Generate a canonical design first; no fabricated preview values are displayed.', action: ['Open workspace', '/workspace'] },
  fabrication: { eyebrow: 'Build workflow', title: 'Fabrication guidance', description: 'Move responsibly from calculated design to physical implementation.', state: 'Use a canonical design as the starting point, then account for materials, dimensional tolerances, connectors, mounting, measurement, and comparison against calculated behavior.' },
  manufacturing: { eyebrow: 'Future workflow', title: 'Manufacturing', description: 'A future request flow will select a design, material, quantity, and notes before submission.', state: 'Manufacturing workflow coming soon. No quote or manufacturer request is submitted from this representative interface.' },
  projects: { eyebrow: 'Workspace', title: 'Projects', description: 'Future projects will organize recent designs, saved antennas, analysis, and revisions.', state: 'Projects require authentication and persistence. Neither is implemented, so no example project is presented as saved data.', action: ['Start a design', '/design'] },
  docs: { eyebrow: 'Documentation', title: 'How AntennaLab works', description: 'AntennaLab routes structured requirements through internal versioned models to return canonical designs with assumptions and validity.', state: 'Result classifications: CALCULATED uses a deterministic formula; PREDICTED uses a model estimate; SIMULATED requires a numerical solver; MEASURED requires recorded physical data. Current results are labeled accurately.' },
  about: { eyebrow: 'About AntennaLab', title: 'Engineering, software, education, and fabrication', description: 'AntennaLab is built to make RF design workflows more understandable and reproducible without hiding model limitations.', state: 'The platform combines requirement intake, internal engineering, visual geometry, analysis, learning, and future manufacturing workflows. It does not use external antenna-calculation APIs.' },
};

function InformationalPage({ page }: { page: PageName }) { const content = pageContent[page] ?? pageContent.docs!; return <><PageHeader eyebrow={content.eyebrow} title={content.title} description={content.description} />{page === 'fabrication' && <div className="workflow fabrication-flow"><span>Design</span><i>→</i><span>Dimensions</span><i>→</i><span>Materials</span><i>→</i><span>Build</span><i>→</i><span>Measure</span><i>→</i><span>Compare</span></div>}<EmptyState title={page === 'optimization' ? 'Optimization: limited preview' : 'Current implementation state'}>{content.state}</EmptyState>{content.action && <div className="center-action"><Link to={content.action[1]} className="button primary-button">{content.action[0]}</Link></div>}</>; }

function Learn() { const topics = ['Fundamentals', 'Design guides', 'Fabrication', 'Measurement']; return <><PageHeader eyebrow="Learning center" title="Learn antenna engineering responsibly" description="Practical explanations supporting the same concepts used by the product—without presenting idealized models as fabricated measurements." /><div className="feature-grid">{topics.map((topic) => <article className="feature-card" key={topic}><StatusBadge kind="example">Reference topic</StatusBadge><h2>{topic}</h2><p>{topic === 'Fundamentals' ? 'Wavelength, frequency, polarization, gain, directivity, impedance, VSWR, bandwidth, and radiation patterns.' : topic === 'Measurement' ? 'VNA basics, measurement setup, and comparison of measured versus calculated behavior.' : 'Guidance is being expanded with clear scope, assumptions, and source-aware educational material.'}</p><Link to={`/learn/${topic.toLowerCase().replace(' ', '-')}`} className="text-link">Read topic →</Link></article>)}</div></>; }

export function ProductPage({ route }: { route: AppRoute }) {
  if (route.page === 'home') return <Home />;
  if (route.page === 'explore') return <Explore />;
  if (route.page === 'detail') return <Detail slug={route.slug} />;
  if (route.page === 'design') return <DesignWizard />;
  if (route.page === 'recommendations') return <Recommendations />;
  if (route.page === 'learn') return <Learn />;
  return <InformationalPage page={route.page} />;
}
