import axios from 'axios';
import type {
  DesignRequest,
  DesignResponse,
  StatusResponse,
  ProgressResponse,
  ResultResponse,
  CodeGenerationRequest,
  CodeGenerationResponse,
  ProjectFilesResponse,
  SaveFilesRequest,
  SaveFilesResponse,
} from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Design API
export const designAPI = {
  startDesign: (data: DesignRequest) =>
    api.post<DesignResponse>('/api/design', data),

  startDemoDesign: (domain: string) =>
    api.post<DesignResponse>(`/api/demo/design?domain=${domain}`),

  getDemoScenarios: () =>
    api.get<{ scenarios: Array<{ domain: string; title: string; description: string; features: string[] }> }>('/api/demo/scenarios'),

  getStatus: (runId: string) =>
    api.get<StatusResponse>(`/api/design/${runId}/status`),

  getProgress: (runId: string) =>
    api.get<ProgressResponse>(`/api/design/${runId}/progress`),

  getResult: (runId: string) =>
    api.get<ResultResponse>(`/api/design/${runId}/result`),

  generateCode: (runId: string, data: CodeGenerationRequest) =>
    api.post<CodeGenerationResponse>(`/api/design/${runId}/generate-code`, data),

  downloadProject: (runId: string, projectId: string) =>
    api.get(`/api/design/${runId}/download/${projectId}`, {
      responseType: 'blob',
    }),
};

// Code Editor API
export const codeEditorAPI = {
  getProjectFiles: (projectId: string) =>
    api.get<ProjectFilesResponse>(`/api/code-editor/${projectId}/files`),

  getFileContent: (projectId: string, filePath: string) =>
    api.get<{ content: string }>(`/api/code-editor/${projectId}/file`, {
      params: { file_path: filePath },
    }),

  saveFiles: (projectId: string, data: SaveFilesRequest) =>
    api.post<SaveFilesResponse>(`/api/code-editor/${projectId}/save`, data),

  deleteFile: (projectId: string, filePath: string) =>
    api.delete(`/api/code-editor/${projectId}/file`, {
      params: { file_path: filePath },
    }),

  createFile: (projectId: string, filePath: string, content: string) =>
    api.post(`/api/code-editor/${projectId}/file`, {
      file_path: filePath,
      content,
    }),
};

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Made with Bob
