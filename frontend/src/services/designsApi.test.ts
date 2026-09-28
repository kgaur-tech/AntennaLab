import { afterEach, describe, expect, it, vi } from 'vitest';

import { EngineeringApiError, generateDesign, getModels } from './designsApi';

const fetchMock = vi.fn();

globalThis.fetch = fetchMock;

afterEach(() => {
  fetchMock.mockReset();
});

describe('designsApi', () => {
  it('parses successful model listing responses', async () => {
    fetchMock.mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          success: true,
          data: {
            models: [{ model: 'dipole', model_version: 'dipole-v1', capabilities: ['geometry'] }],
          },
        }),
        { status: 200 },
      ),
    );

    const result = await getModels();

    expect(result.models[0].model).toBe('dipole');
  });

  it('throws structured backend errors', async () => {
    fetchMock.mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          success: false,
          error: {
            code: 'UNSUPPORTED_ANTENNA_TYPE',
            message: 'Unsupported antenna type: patch.',
            field: 'antenna_type',
            details: {},
          },
        }),
        { status: 400 },
      ),
    );

    await expect(generateDesign({ antenna_type: 'patch', frequency: 915, frequency_unit: 'MHz' })).rejects.toMatchObject({
      code: 'UNSUPPORTED_ANTENNA_TYPE',
      field: 'antenna_type',
    });
  });

  it('throws malformed response errors', async () => {
    fetchMock.mockResolvedValueOnce(new Response('not json', { status: 200 }));

    await expect(getModels()).rejects.toBeInstanceOf(EngineeringApiError);
  });
});
