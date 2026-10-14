import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import type { AnalysisResult } from '../../types';
import RadiationPattern from './RadiationPattern';

const analysis: AnalysisResult = {
  model_type: 'dipole', model_version: 'dipole-v1', result_class: 'CALCULATED', inputs: {}, metrics: {}, geometry_reference: null,
  plots: [{ name: 'e_plane_normalized_power', data: [{ angle_deg: 0, normalized_response: 0 }, { angle_deg: 90, normalized_response: 1 }, { angle_deg: 180, normalized_response: 0 }] }],
  assumptions: [], warnings: [], validity: 'valid', computation_metadata: {},
};

describe('RadiationPattern', () => {
  it('renders only backend-provided normalized samples', () => {
    render(<RadiationPattern analysis={analysis} />);
    expect(screen.getByRole('img', { name: /normalized radiation response/i })).toBeInTheDocument();
    expect(screen.getByText(/not absolute gain or a full-wave simulation/i)).toBeInTheDocument();
  });

  it('does not create a graph when no plot data exists', () => {
    const { container } = render(<RadiationPattern analysis={{ ...analysis, plots: [] }} />);
    expect(container).toBeEmptyDOMElement();
  });
});
