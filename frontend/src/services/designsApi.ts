import type {
  ApiResponse,
  ApiFailure,
  DesignCreateInput,
  DesignGenerationResult,
  ModelListResult,
  ValidationResult,
} from '../types';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') ?? '';

function apiUrl(path: string): string {
  return `${apiBaseUrl}${path}`;
}

export class EngineeringApiError extends Error {
  code: string;
  field?: string | null;
  details: Record<string, unknown>;

  constructor(message: string, code = 'UNKNOWN_ERROR', field?: string | null, details: Record<string, unknown> = {}) {
    super(message);
    this.name = 'EngineeringApiError';
    this.code = code;
    this.field = field;
    this.details = details;
  }
}

function isApiFailure(value: unknown): value is ApiFailure {
  return (
    typeof value === 'object' &&
    value !== null &&
    'success' in value &&
    (value as { success: unknown }).success === false &&
    'error' in value
  );
}

async function parseApiResponse<T>(response: Response, fallbackMessage: string): Promise<T> {
  let json: ApiResponse<T>;

  try {
    json = (await response.json()) as ApiResponse<T>;
  } catch (error) {
    throw new EngineeringApiError(
      response.ok ? 'Malformed API response.' : fallbackMessage,
      response.ok ? 'MALFORMED_RESPONSE' : 'HTTP_ERROR',
      null,
      { status: response.status, cause: error instanceof Error ? error.message : String(error) },
    );
  }

  if (!response.ok || !json.success) {
    if (isApiFailure(json)) {
      throw new EngineeringApiError(json.error.message, json.error.code, json.error.field, json.error.details);
    }
    throw new EngineeringApiError(fallbackMessage, 'HTTP_ERROR', null, { status: response.status });
  }

  return json.data;
}

async function requestJson<T>(path: string, init?: RequestInit, fallbackMessage = 'Request failed.'): Promise<T> {
  try {
    const response = await fetch(path, init);
    return parseApiResponse<T>(response, fallbackMessage);
  } catch (error) {
    if (error instanceof EngineeringApiError) {
      throw error;
    }
    throw new EngineeringApiError(
      'Backend cannot be reached. Check that the API server is running.',
      'NETWORK_ERROR',
      null,
      { cause: error instanceof Error ? error.message : String(error) },
    );
  }
}

export async function generateDesign(payload: DesignCreateInput): Promise<DesignGenerationResult> {
  return requestJson<DesignGenerationResult>(apiUrl('/api/v1/designs'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  }, 'Design generation failed.');
}

export async function validateRequirements(payload: DesignCreateInput): Promise<ValidationResult> {
  return requestJson<ValidationResult>(apiUrl('/api/v1/requirements/validate'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  }, 'Requirement validation failed.');
}

export async function getModels(): Promise<ModelListResult> {
  return requestJson<ModelListResult>(apiUrl('/api/v1/models'), undefined, 'Model listing failed.');
}

export async function runDesignAnalysis(designId: string): Promise<DesignGenerationResult['analysis'] & { analysis_id: string; input_hash: string; duration_ms: number; cache_hit: boolean; analysis_type: string; status: string }> {
  return requestJson(`/api/v1/designs/${designId}/analysis`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ settings: {} }) }, 'Analysis failed.');
}

export const listModels = getModels;
export const validateDesignRequirement = validateRequirements;
