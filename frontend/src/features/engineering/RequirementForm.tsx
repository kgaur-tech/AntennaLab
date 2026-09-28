import type { DesignCreateInput, ModelMetadata } from '../../types';

interface RequirementFormProps {
  value: DesignCreateInput;
  models: ModelMetadata[];
  isLoadingModels: boolean;
  isBusy: boolean;
  onChange: (value: DesignCreateInput) => void;
  onValidate: () => void;
  onGenerate: () => void;
}

const frequencyUnits = ['Hz', 'kHz', 'MHz', 'GHz'] as const;

function setOptionalNumber(value: string): number | undefined {
  return value === '' ? undefined : Number(value);
}

export default function RequirementForm({
  value,
  models,
  isLoadingModels,
  isBusy,
  onChange,
  onValidate,
  onGenerate,
}: RequirementFormProps) {
  const update = (patch: Partial<DesignCreateInput>) => onChange({ ...value, ...patch });

  return (
    <form className="panel requirement-panel" onSubmit={(event) => event.preventDefault()}>
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Requirement Input</p>
          <h2>Requirement Builder</h2>
        </div>
        <span className="phase-pill">Phase 3</span>
      </div>

      {isLoadingModels ? (
        <p className="muted" aria-live="polite">Loading supported antenna models...</p>
      ) : null}

      <label>
        Antenna Type
        <select
          value={value.antenna_type}
          onChange={(event) => update({ antenna_type: event.target.value })}
          disabled={isBusy || isLoadingModels}
        >
          {models.map((model) => (
            <option key={model.model} value={model.model}>
              {model.model} ({model.model_version})
            </option>
          ))}
        </select>
      </label>

      <div className="field-row">
        <label>
          Operating Frequency
          <input
            type="number"
            min="0"
            step="any"
            value={value.frequency ?? ''}
            onChange={(event) => update({ frequency: setOptionalNumber(event.target.value), frequency_hz: undefined })}
            disabled={isBusy}
          />
        </label>
        <label>
          Unit
          <select
            value={value.frequency_unit ?? 'MHz'}
            onChange={(event) => update({ frequency_unit: event.target.value as DesignCreateInput['frequency_unit'] })}
            disabled={isBusy}
          >
            {frequencyUnits.map((unit) => (
              <option key={unit} value={unit}>{unit}</option>
            ))}
          </select>
        </label>
      </div>

      <label>
        Use Case
        <input
          value={value.application ?? ''}
          onChange={(event) => update({ application: event.target.value })}
          placeholder="rocket telemetry, IoT sensor, ground link"
          disabled={isBusy}
        />
      </label>

      <div className="field-row">
        <label>
          Polarization
          <select
            value={value.polarization ?? 'linear'}
            onChange={(event) => update({ polarization: event.target.value })}
            disabled={isBusy}
          >
            <option value="linear">Linear</option>
            <option value="vertical">Vertical</option>
            <option value="horizontal">Horizontal</option>
          </select>
        </label>
        <label>
          Max Dimension (m)
          <input
            type="number"
            min="0"
            step="any"
            value={value.max_dimension_m ?? ''}
            onChange={(event) => update({ max_dimension_m: setOptionalNumber(event.target.value) })}
            disabled={isBusy}
          />
        </label>
      </div>

      <div className="field-row">
        <label>
          Target Impedance (ohms)
          <input
            type="number"
            min="0"
            step="any"
            value={value.target_impedance_ohms ?? ''}
            onChange={(event) => update({ target_impedance_ohms: setOptionalNumber(event.target.value) })}
            disabled={isBusy}
          />
        </label>
        <label>
          Director Count
          <input
            type="number"
            min="1"
            max="20"
            step="1"
            value={value.director_count ?? ''}
            onChange={(event) => update({ director_count: setOptionalNumber(event.target.value) })}
            disabled={isBusy || value.antenna_type !== 'yagi_uda'}
          />
        </label>
      </div>

      <div className="button-row">
        <button type="button" className="secondary-button" onClick={onValidate} disabled={isBusy || isLoadingModels}>
          Validate Requirements
        </button>
        <button type="button" className="primary-button" onClick={onGenerate} disabled={isBusy || isLoadingModels}>
          Generate Design
        </button>
      </div>
    </form>
  );
}
