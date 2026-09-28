import { useState } from 'react';
import type { RequirementInput } from '../types';

interface RequirementWizardProps {
  initialValue: RequirementInput;
  onSubmit: (value: RequirementInput) => void;
}

export default function RequirementWizard({ initialValue, onSubmit }: RequirementWizardProps) {
  const [form, setForm] = useState<RequirementInput>(initialValue);

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit(form);
      }}
      style={{ display: 'grid', gap: '1rem' }}
    >
      <label>
        Application
        <input
          value={form.application}
          onChange={(event) => setForm({ ...form, application: event.target.value })}
          style={{ display: 'block', width: '100%', marginTop: 4 }}
        />
      </label>

      <label>
        Frequency (Hz)
        <input
          type="number"
          value={form.frequency_hz}
          onChange={(event) => setForm({ ...form, frequency_hz: Number(event.target.value) })}
          style={{ display: 'block', width: '100%', marginTop: 4 }}
        />
      </label>

      <label>
        Gain (dB)
        <input
          type="number"
          value={form.gain_db ?? 0}
          onChange={(event) => setForm({ ...form, gain_db: Number(event.target.value) })}
          style={{ display: 'block', width: '100%', marginTop: 4 }}
        />
      </label>

      <button type="submit" style={{ width: 220, padding: '0.7rem 1rem' }}>
        Evaluate Requirement
      </button>
    </form>
  );
}
