/**
 * TypeScript type definitions for Geo-SQL Agent
 */

// ==============================================================================
// API Types
// ==============================================================================

export interface QueryRequest {
  question: string;
}

export interface QueryResponse {
  sql: string;
  results: QueryResult[];
  execution_time: number;
  result_count: number;
  timestamp: string;
}

export interface QueryResult {
  id: number;
  name?: string;
  pl_name?: string;
  geojson: GeoJSON;
  [key: string]: any;  // Allow additional dynamic properties
}

export interface GeoJSON {
  type: 'Point' | 'LineString' | 'Polygon' | 'MultiPoint' | 'MultiLineString' | 'MultiPolygon';
  coordinates: number[] | number[][] | number[][][];
}

export interface HealthResponse {
  status: string;
  database: string;
  version: string;
  environment: string;
  timestamp: string;
}

export interface TableInfo {
  count: number;
  columns: string[];
  geometry_type: string;
  description?: string;
}

export interface SchemaResponse {
  tables: Record<string, TableInfo>;
  total_records: number;
  timestamp: string;
}

export interface ErrorResponse {
  error: string;
  message: string;
  detail?: string;
  timestamp: string;
}

// ==============================================================================
// Application State Types
// ==============================================================================

export interface AppState {
  // Query State
  currentQuestion: string;
  isLoading: boolean;
  error: string | null;

  // Results State
  currentQuery: QueryResponse | null;
  queryHistory: QueryHistoryItem[];

  // Map State
  mapCenter: [number, number];
  mapZoom: number;
  selectedFeature: QueryResult | null;

  // Schema State
  schema: SchemaResponse | null;
}

export interface QueryHistoryItem {
  id: string;
  question: string;
  sql: string;
  result_count: number;
  execution_time: number;
  timestamp: string;
}

// ==============================================================================
// Component Props Types
// ==============================================================================

export interface MapProps {
  results: QueryResult[];
  center?: [number, number];
  zoom?: number;
  onFeatureClick?: (feature: QueryResult) => void;
}

export interface QueryInputProps {
  onSubmit: (question: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
}

export interface ResultsPanelProps {
  query: QueryResponse | null;
  isLoading?: boolean;
  error?: string | null;
}

export interface SQLDisplayProps {
  sql: string;
  executionTime: number;
}

export interface StatsDisplayProps {
  resultCount: number;
  executionTime: number;
}

export interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

// ==============================================================================
// Utility Types
// ==============================================================================

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface ApiError extends Error {
  status?: number;
  response?: ErrorResponse;
}
