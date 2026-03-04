// Design Request & Response Types
export interface DesignRequest {
  business_goal: string;
  domain: 'healthcare' | 'finance' | 'ecommerce' | 'education' | 'legal' | 'general';
  modalities: ('text' | 'vision' | 'multimodal' | 'tabular')[];
  constraints: {
    budget: number;
    latency_target_ms: number;
    risk_tolerance: 'low' | 'medium' | 'high';
    compliance_level: 'low' | 'medium' | 'high';
    expected_users: number;
  };
  max_iterations?: number;
}

export interface DesignResponse {
  run_id: string;
  status: string;
  message: string;
}

export interface StatusResponse {
  run_id: string;
  status: 'starting' | 'processing' | 'completed' | 'failed';
  version: number;
  current_iteration: number;
  max_iterations: number;
  errors: string[];
  warnings: string[];
}

export interface ProgressStage {
  stage: string;
  message: string;
  timestamp: string;
}

export interface ProgressResponse {
  run_id: string;
  status: string;
  progress: {
    stages: ProgressStage[];
    current_stage: string;
    current_message: string;
    details: Record<string, any>;
  };
}

// Architecture Types
export interface ArchitectureModule {
  layer: string;
  component: string;
  config: Record<string, any>;
}

export interface Architecture {
  architecture_id: string;
  name: string;
  template: string;
  modules: ArchitectureModule[];
  topology: 'sequential' | 'parallel' | 'hierarchical';
  estimated_metrics?: Record<string, number>;
  final_score?: number;
}

export interface ReflectionFeedback {
  confidence: number;
  strengths: string[];
  weaknesses: string[];
  improvement_suggestions: string[];
  should_iterate: boolean;
}

export interface ResultResponse {
  run_id: string;
  version: number;
  selected_architecture: Architecture;
  metrics: Record<string, number>;
  score: number;
  reflection: ReflectionFeedback;
  executive_report?: string;
  technical_specification?: string;
  deployment_plan?: string;
  monitoring_strategy?: string;
}

// Code Generation Types
export interface CodeGenerationRequest {
  project_name: string;
}

export interface CodeGenerationResponse {
  status: 'success' | 'error';
  project_id: string;
  project_path: string;
  files_generated: string[];
  architecture_type: string;
  message: string;
  download_url: string;
}

export interface FileInfo {
  path: string;
  content: string;
  language: string;
  size: number;
}

export interface ProjectFilesResponse {
  project_id: string;
  files: FileInfo[];
  total_files: number;
}

// Code Editor Types
export interface SaveFilesRequest {
  files: Array<{
    path: string;
    content: string;
  }>;
}

export interface SaveFilesResponse {
  status: 'success' | 'error';
  message: string;
  files_saved: number;
  download_url: string;
}

// Made with Bob
