export interface FunctionalRequirement {
  id: string;
  description: string;
}

export interface NonFunctionalRequirement {
  category: string;
  description: string;
}

export interface RequirementAnalysis {
  functional_requirements: FunctionalRequirement[];
  non_functional_requirements: NonFunctionalRequirement[];
  ambiguities: string[];
  assumptions: string[];
}

export interface EngineeringTask {
  id: string;
  title: string;
  description: string;
  depends_on: string[];
  ai_assistance: string;
}

export interface ArtifactFile {
  path: string;
  description: string;
}

export interface EngineeringArtifacts {
  folder_structure: string[];
  database_schema: string;
  api_contracts: string[];
  key_files: ArtifactFile[];
}

export interface ValidationFinding {
  area: string;
  finding: string;
  severity: string;
}

export interface ValidationReport {
  code_review: ValidationFinding[];
  security_review: ValidationFinding[];
  performance_review: ValidationFinding[];
  missing_edge_cases: string[];
  test_coverage_summary: string;
}

export interface Risk {
  category: string;
  risk: string;
  mitigation: string;
}

export interface RiskAnalysis {
  risks: Risk[];
}

export interface FinalSummary {
  implementation_approach: string;
  generated_artifacts: string[];
  risks_and_validation: string;
  assumptions_and_limitations: string;
}

export interface CopilotResponse {
  requirement_analysis: RequirementAnalysis;
  task_decomposition: EngineeringTask[];
  engineering_artifacts: EngineeringArtifacts;
  validation: ValidationReport;
  risk_analysis: RiskAnalysis;
  final_summary: FinalSummary;
}

export interface ShortenResponse {
  id: number;
  original_url: string;
  short_code: string;
  short_url: string;
  created_at: string;
}

export interface AnalyticsResponse {
  short_code: string;
  original_url: string;
  click_count: number;
  created_at: string;
  last_clicked_at: string | null;
}

export interface ApiError {
  detail: string;
}
