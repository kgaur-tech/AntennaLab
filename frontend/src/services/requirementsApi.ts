import { EngineeringApiError } from './designsApi';
import type { ApiResponse, ExplainableRecommendationResponse, RecommendationCandidate, RequirementInput } from '../types';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') ?? '';

export async function recommendAntennas(payload: RequirementInput): Promise<RecommendationCandidate[]> {
  const response = await fetch(`${apiBaseUrl}/api/v1/requirements/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const json = (await response.json()) as ApiResponse<{ recommendations: RecommendationCandidate[] }>;
  if (!response.ok || !json.success) {
    if (!json.success) {
      throw new EngineeringApiError(json.error.message, json.error.code, json.error.field, json.error.details);
    }
    throw new EngineeringApiError('Requirement recommendation failed.', 'HTTP_ERROR', null, { status: response.status });
  }
  return json.data.recommendations;
}

export async function getExplainableRecommendations(payload: RequirementInput): Promise<ExplainableRecommendationResponse> {
  const response = await fetch(`${apiBaseUrl}/api/v1/recommendations`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
  });
  const json = (await response.json()) as ApiResponse<ExplainableRecommendationResponse>;
  if (!response.ok || !json.success) {
    if (!json.success) throw new EngineeringApiError(json.error.message, json.error.code, json.error.field, json.error.details);
    throw new EngineeringApiError('Recommendation generation failed.', 'HTTP_ERROR', null, { status: response.status });
  }
  return json.data;
}
