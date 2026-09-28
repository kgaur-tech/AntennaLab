import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';

import EngineeringWorkspace from './EngineeringWorkspace';

const fetchMock = vi.fn();

globalThis.fetch = fetchMock;

const modelResponse = {
  success: true,
  data: {
    models: [
      { model: 'dipole', model_version: 'dipole-v1', capabilities: ['canonical_design', 'geometry', 'analytical_pattern'] },
      { model: 'yagi_uda', model_version: 'yagi-uda-v1', capabilities: ['canonical_design', 'geometry', 'dimensional_analysis'] },
    ],
  },
};

const validationResponse = {
  success: true,
  data: {
    is_valid: true,
    antenna_type: 'dipole',
    normalized: { frequency_hz: 915000000, wavelength_m: 0.327642 },
    model: { model: 'dipole', model_version: 'dipole-v1', capabilities: ['geometry'] },
    warnings: [],
  },
};

const designResponse = {
  success: true,
  data: {
    design: {
      design_id: 'design-1',
      antenna_type: 'dipole',
      family: 'dipole',
      model_version: 'dipole-v1',
      frequency_hz: 915000000,
      dimensions_m: { total_length: 0.163821, half_length: 0.08191, radius: 0.000819 },
      parameters: { wavelength_m: 0.327642 },
      materials: { conductor: 'wire' },
      feed: { impedance_ohms: 73, type: 'balanced' },
      geometry: {
        family: 'dipole',
        metadata: {},
        elements: [
          {
            name: 'left_arm',
            kind: 'wire',
            length_m: 0.08191,
            radius_m: 0.000819,
            position_m: [-0.04095, 0, 0],
            orientation_deg: 0,
            metadata: { axis: 'x' },
          },
        ],
      },
      assumptions: ['Half-wave dipole approximation.'],
      warnings: [],
      design_hash: 'hash-915',
    },
    analysis: {
      model_type: 'dipole',
      model_version: 'dipole-v1',
      result_class: 'CALCULATED',
      inputs: { frequency_hz: 915000000 },
      metrics: { wavelength_m: 0.327642, electrical_length_wavelengths: 0.5 },
      geometry_reference: { design_id: 'design-1', design_hash: 'hash-915' },
      plots: [],
      assumptions: ['Half-wave dipole approximation.'],
      warnings: [],
      validity: 'valid',
      computation_metadata: { method: 'test' },
    },
    model: { model: 'dipole', model_version: 'dipole-v1', capabilities: ['canonical_design', 'geometry', 'analytical_pattern'] },
    design_hash: 'hash-915',
    record: {},
    revision: {},
  },
};

function jsonResponse(body: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(body), { status }));
}

afterEach(() => {
  fetchMock.mockReset();
});

describe('EngineeringWorkspace', () => {
  it('renders the requirement form and loaded models', async () => {
    fetchMock.mockResolvedValueOnce(await jsonResponse(modelResponse));

    render(<EngineeringWorkspace />);

    expect(screen.getByLabelText(/Operating Frequency/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getAllByText(/dipole-v1/i).length).toBeGreaterThan(0));
  });

  it('shows validation success and normalized values', async () => {
    const user = userEvent.setup();
    fetchMock
      .mockResolvedValueOnce(await jsonResponse(modelResponse))
      .mockResolvedValueOnce(await jsonResponse(validationResponse));

    render(<EngineeringWorkspace />);

    await user.click(await screen.findByRole('button', { name: /Validate Requirements/i }));

    expect(await screen.findByText(/Requirements valid/i)).toBeInTheDocument();
    expect(screen.getByText(/Frequency Hz/i)).toBeInTheDocument();
  });

  it('generates and renders canonical engineering result', async () => {
    const user = userEvent.setup();
    fetchMock
      .mockResolvedValueOnce(await jsonResponse(modelResponse))
      .mockResolvedValueOnce(await jsonResponse(designResponse));

    render(<EngineeringWorkspace />);

    await user.click(await screen.findByRole('button', { name: /Generate Design/i }));

    expect(await screen.findByText(/Design generated/i)).toBeInTheDocument();
    expect(screen.getByText('design-1')).toBeInTheDocument();
    expect(screen.getByText('hash-915')).toBeInTheDocument();
    expect(screen.getAllByText(/Half-wave dipole approximation/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Left Arm/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Not available in current engineering model/i).length).toBeGreaterThan(0);
  });

  it('shows structured generation failures without clearing previous result', async () => {
    const user = userEvent.setup();
    fetchMock
      .mockResolvedValueOnce(await jsonResponse(modelResponse))
      .mockResolvedValueOnce(await jsonResponse(designResponse))
      .mockResolvedValueOnce(
        await jsonResponse(
          {
            success: false,
            error: {
              code: 'VALIDATION_ERROR',
              message: 'Input should be greater than 0',
              field: 'frequency',
              details: {},
            },
          },
          422,
        ),
      );

    render(<EngineeringWorkspace />);

    await user.click(await screen.findByRole('button', { name: /Generate Design/i }));
    expect(await screen.findByText('hash-915')).toBeInTheDocument();

    const frequencyInput = screen.getByLabelText(/Operating Frequency/i);
    await user.clear(frequencyInput);
    await user.type(frequencyInput, '-1');
    await user.click(screen.getByRole('button', { name: /Generate Design/i }));

    expect(await screen.findByText(/Design generation failed/i)).toBeInTheDocument();
    expect(screen.getByText('hash-915')).toBeInTheDocument();
  });

  it('renders raw engineering data after generation', async () => {
    const user = userEvent.setup();
    fetchMock
      .mockResolvedValueOnce(await jsonResponse(modelResponse))
      .mockResolvedValueOnce(await jsonResponse(designResponse));

    render(<EngineeringWorkspace />);

    await user.click(await screen.findByRole('button', { name: /Generate Design/i }));
    const details = await screen.findByText(/Advanced \/ Raw Engineering Data/i);
    await user.click(details);
    const rawPre = screen.getByText((content, element) => {
      return element?.tagName.toLowerCase() === 'pre' && content.includes('"design_hash": "hash-915"');
    });

    expect(within(rawPre).getByText(/"design_hash": "hash-915"/i)).toBeInTheDocument();
  });
});
