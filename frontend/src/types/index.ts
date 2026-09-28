export type AntennaFamily = 'dipole' | 'monopole' | 'yagi_uda';

export interface RequirementInput {
  application: string;
  frequency_hz: number;
  bandwidth_hz?: number;
  gain_db?: number;
  polarization: string;
  is_directional: boolean;
  directionality?: 'no_preference' | 'omnidirectional' | 'directional' | 'highly_directional';
  max_dimension_m?: number;
  max_width_m?: number;
  max_height_m?: number;
  max_volume_m3?: number;
  target_impedance_ohms: number;
  environment: string;
  feed_type?: string;
  connector?: string;
  notes?: string;
  priority_weights?: Record<string, number>;
  antenna_family_preferences?: AntennaFamily[];
}

export interface RecommendationCandidate {
  family: AntennaFamily;
  score: number;
  reasons: string[];
  alternatives: string[];
}

export interface RecommendationComponent {
  criterion: string;
  status: 'EVALUATED' | 'NOT_EVALUATED' | 'UNSUPPORTED';
  score: number | null;
  reason_code: string;
  message: string;
}

export interface ExplainableRecommendationCandidate {
  family: AntennaFamily;
  model_version: string;
  status: 'eligible' | 'excluded';
  score: number | null;
  hard_constraints: RecommendationComponent[];
  score_components: RecommendationComponent[];
  reasons: string[];
  tradeoffs: string[];
  warnings: string[];
}

export interface ExplainableRecommendationResponse {
  engine_version: string;
  requirement: Record<string, unknown>;
  recommended: ExplainableRecommendationCandidate[];
  alternatives: ExplainableRecommendationCandidate[];
  excluded_candidates: ExplainableRecommendationCandidate[];
  warnings: string[];
}

export interface ApiErrorPayload {
  code: string;
  message: string;
  field?: string | null;
  details: Record<string, unknown>;
}

export interface ApiSuccess<T> {
  success: true;
  data: T;
}

export interface ApiFailure {
  success: false;
  error: ApiErrorPayload;
}

export type ApiResponse<T> = ApiSuccess<T> | ApiFailure;

export interface ModelMetadata {
  model: AntennaFamily;
  model_version: string;
  capabilities: string[];
}

export interface GeometryElement {
  name: string;
  kind: string;
  length_m?: number | null;
  radius_m?: number | null;
  position_m: [number, number, number];
  orientation_deg: number;
  metadata: Record<string, unknown>;
}

export interface GeometryModel {
  family: AntennaFamily;
  elements: GeometryElement[];
  metadata: Record<string, unknown>;
}

export interface CanonicalDesign {
  design_id: string;
  antenna_type: AntennaFamily;
  family: AntennaFamily;
  model_version: string;
  frequency_hz: number;
  dimensions_m: Record<string, unknown>;
  parameters: Record<string, unknown>;
  materials: Record<string, unknown>;
  feed: Record<string, unknown>;
  geometry: GeometryModel | null;
  assumptions: string[];
  warnings: string[];
  design_hash: string;
}

export interface AnalysisResult {
  model_type: AntennaFamily;
  model_version: string;
  result_class: 'CALCULATED' | 'PREDICTED' | 'SIMULATED' | 'MEASURED';
  inputs: Record<string, unknown>;
  metrics: Record<string, unknown>;
  geometry_reference?: Record<string, unknown> | null;
  plots: Array<Record<string, unknown>>;
  assumptions: string[];
  warnings: string[];
  validity: string;
  computation_metadata: Record<string, unknown>;
}

export interface DesignCreateInput {
  antenna_type: AntennaFamily | string;
  frequency?: number;
  frequency_unit?: 'Hz' | 'kHz' | 'MHz' | 'GHz' | 'hz' | 'khz' | 'mhz' | 'ghz';
  frequency_hz?: number;
  application?: string;
  polarization?: string;
  max_dimension_m?: number;
  target_impedance_ohms?: number;
  mounting?: string;
  platform?: string;
  gain_db?: number;
  bandwidth_hz?: number;
  director_count?: number;
  director_lengths_m?: number[];
  element_spacings_m?: number[];
  reflector_length_m?: number;
  driven_element_length_m?: number;
  element_radius_m?: number;
}

export interface DesignGenerationResult {
  design: CanonicalDesign;
  analysis: AnalysisResult;
  model: ModelMetadata;
  design_hash: string;
  record: Record<string, unknown>;
  revision: Record<string, unknown>;
}

export interface ModelListResult {
  models: ModelMetadata[];
}

export type WorkspaceState =
  | 'idle'
  | 'loading_models'
  | 'validating'
  | 'validation_success'
  | 'validation_error'
  | 'generating'
  | 'success'
  | 'generation_error';

export interface ValidationResult {
  is_valid: boolean;
  antenna_type: string;
  normalized: Record<string, unknown>;
  model: ModelMetadata;
  warnings: string[];
}

export type EngineeringMessageLevel = 'ERROR' | 'WARNING' | 'INFO' | 'VALID';

export interface EngineeringMessage {
  level: EngineeringMessageLevel;
  title: string;
  message: string;
  field?: string | null;
}
