/**
 * API Service for communicating with the Geo-SQL Agent backend
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  QueryRequest,
  QueryResponse,
  HealthResponse,
  SchemaResponse,
  ApiError,
} from '../types';

// ==============================================================================
// API Configuration
// ==============================================================================

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,  // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==============================================================================
// Request Interceptor
// ==============================================================================

apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// ==============================================================================
// Response Interceptor
// ==============================================================================

apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API] Response:`, response.status, response.data);
    return response;
  },
  (error: AxiosError) => {
    const apiError: ApiError = new Error(
      (error.response?.data as any)?.message || error.message || 'An unknown error occurred'
    ) as ApiError;

    apiError.status = error.response?.status;
    apiError.response = error.response?.data as any;

    console.error('[API] Response error:', apiError);
    return Promise.reject(apiError);
  }
);

// ==============================================================================
// API Methods
// ==============================================================================

export const api = {
  /**
   * Health check
   */
  health: async (): Promise<HealthResponse> => {
    const response = await apiClient.get<HealthResponse>('/health');
    return response.data;
  },

  /**
   * Get database schema
   */
  schema: async (): Promise<SchemaResponse> => {
    const response = await apiClient.get<SchemaResponse>('/schema');
    return response.data;
  },

  /**
   * Execute a natural language query
   */
  query: async (request: QueryRequest): Promise<QueryResponse> => {
    const response = await apiClient.post<QueryResponse>('/query', request);
    return response.data;
  },
};

// ==============================================================================
// Error Handling Utilities
// ==============================================================================

export const isApiError = (error: any): error is ApiError => {
  return error instanceof Error && 'status' in error;
};

export const getErrorMessage = (error: unknown): string => {
  if (isApiError(error)) {
    return error.response?.message || error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unknown error occurred';
};

// ==============================================================================
// Export API client for advanced usage
// ==============================================================================

export default apiClient;
