import { lazy, Suspense, useEffect, useMemo, useState } from 'react';

import { EngineeringApiError, generateDesign, getModels, validateRequirements } from '../../services/designsApi';
import type {
  DesignCreateInput,
  DesignGenerationResult,
  EngineeringMessage,
  ModelMetadata,
  ValidationResult,
  WorkspaceState,
} from '../../types';
import AnalysisMetrics from './AnalysisMetrics';
import AssumptionsPanel from './AssumptionsPanel';
import DesignSummary from './DesignSummary';
import GeometrySummary from './GeometrySummary';
import ModelInfoCard from './ModelInfoCard';
import RawEngineeringData from './RawEngineeringData';
import RequirementForm from './RequirementForm';
import ValidationStatus from './ValidationStatus';
import WarningsPanel from './WarningsPanel';
import WorkspaceOverview from './WorkspaceOverview';

const GeometryViewer = lazy(() => import('./GeometryViewer'));

const defaultRequirement: DesignCreateInput = {
  antenna_type: 'dipole',
  frequency: 915,
  frequency_unit: 'MHz',
  application: 'rocket telemetry',
  polarization: 'linear',
  max_dimension_m: 0.35,
  target_impedance_ohms: 50,
};

function toMessage(error: unknown, title: string): EngineeringMessage {
  if (error instanceof EngineeringApiError) {
    return {
      level: 'ERROR',
      title,
      message: error.message,
      field: error.field,
    };
  }
  return {
    level: 'ERROR',
    title,
    message: error instanceof Error ? error.message : 'Unexpected frontend error.',
  };
}

export default function EngineeringWorkspace() {
  const [models, setModels] = useState<ModelMetadata[]>([]);
  const [requirement, setRequirement] = useState<DesignCreateInput>(defaultRequirement);
  const [state, setState] = useState<WorkspaceState>('loading_models');
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [result, setResult] = useState<DesignGenerationResult | null>(null);
  const [message, setMessage] = useState<EngineeringMessage | null>(null);
  const [copiedHash, setCopiedHash] = useState(false);

  useEffect(() => {
    let active = true;
    getModels()
      .then((response) => {
        if (!active) {
          return;
        }
        setModels(response.models);
        if (response.models.length && !response.models.some((model) => model.model === requirement.antenna_type)) {
          setRequirement((current) => ({ ...current, antenna_type: response.models[0].model }));
        }
        setState('idle');
      })
      .catch((error: unknown) => {
        if (!active) {
          return;
        }
        setState('validation_error');
        setMessage(toMessage(error, 'Model catalog unavailable'));
      });
    return () => {
      active = false;
    };
  }, []);

  const isBusy = state === 'loading_models' || state === 'validating' || state === 'generating';
  const activeModel = useMemo(
    () => result?.model ?? models.find((model) => model.model === requirement.antenna_type) ?? null,
    [models, requirement.antenna_type, result],
  );

  const handleValidate = async () => {
    setState('validating');
    setMessage(null);
    try {
      const nextValidation = await validateRequirements(requirement);
      setValidation(nextValidation);
      setState('validation_success');
      setMessage({
        level: 'VALID',
        title: 'Requirements valid',
        message: 'Backend validation and normalization completed.',
      });
    } catch (error) {
      setValidation(null);
      setState('validation_error');
      setMessage(toMessage(error, 'Requirement validation failed'));
    }
  };

  const handleGenerate = async () => {
    setState('generating');
    setMessage(null);
    setCopiedHash(false);
    try {
      const nextResult = await generateDesign(requirement);
      setResult(nextResult);
      setValidation(null);
      setState('success');
      setMessage({
        level: 'VALID',
        title: 'Design generated',
        message: 'Canonical backend design and analysis result received.',
      });
    } catch (error) {
      setState('generation_error');
      setMessage(toMessage(error, 'Design generation failed'));
    }
  };

  const handleCopyHash = async () => {
    if (!result?.design.design_hash) {
      return;
    }
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(result.design.design_hash);
    }
    setCopiedHash(true);
  };

  const warnings = result?.analysis.warnings ?? result?.design.warnings ?? [];
  const assumptions = result?.analysis.assumptions ?? result?.design.assumptions ?? [];

  return (
    <main className="workspace-shell">
      <section className="workspace-hero">
        <div>
          <p className="eyebrow">AntennaLab</p>
          <h1>Antenna Engineering Workspace</h1>
          <p className="hero-copy">
            Validate requirements, generate canonical antenna designs, and inspect calculated engineering results from the local backend.
          </p>
        </div>
        <div className="hero-status" aria-live="polite">
          {state === 'generating' ? 'Generating canonical antenna design...' : `State: ${state.replace(/_/g, ' ')}`}
        </div>
      </section>

      <WorkspaceOverview state={state} models={models} validation={validation} result={result} />

      <div className="workspace-grid">
        <div className="workspace-column">
          <RequirementForm
            value={requirement}
            models={models}
            isLoadingModels={state === 'loading_models'}
            isBusy={isBusy}
            onChange={setRequirement}
            onValidate={handleValidate}
            onGenerate={handleGenerate}
          />
          <ValidationStatus state={state} validation={validation} message={message} />
        </div>

        <div className="workspace-column wide-column">
          <DesignSummary design={result?.design ?? null} onCopyHash={handleCopyHash} copied={copiedHash} />
          <section className="panel">
            <p className="eyebrow">Engineering Geometry</p>
            <h2>3D Viewer</h2>
            <Suspense fallback={<div className="viewer-empty">Loading geometry viewer…</div>}>
              <GeometryViewer geometry={result?.design.geometry ?? null} />
            </Suspense>
          </section>
          <GeometrySummary geometry={result?.design.geometry ?? null} />
          <RawEngineeringData data={result} />
        </div>

        <div className="workspace-column">
          <ModelInfoCard model={activeModel} />
          <AnalysisMetrics analysis={result?.analysis ?? null} />
          <AssumptionsPanel assumptions={assumptions} />
          <WarningsPanel warnings={warnings} />
        </div>
      </div>
    </main>
  );
}
