/**
 * Global Application Context for state management
 */

import React, { createContext, useContext, useReducer, ReactNode, Dispatch } from 'react';
import {
  AppState,
  QueryResponse,
  QueryResult,
  SchemaResponse,
  QueryHistoryItem,
} from '../types';

// ==============================================================================
// Initial State
// ==============================================================================

const initialState: AppState = {
  currentQuestion: '',
  isLoading: false,
  error: null,
  currentQuery: null,
  queryHistory: [],
  mapCenter: [32.0853, 34.7818],  // Tel Aviv coordinates
  mapZoom: 12,
  selectedFeature: null,
  schema: null,
};

// ==============================================================================
// Action Types
// ==============================================================================

type AppAction =
  | { type: 'SET_QUESTION'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_QUERY_RESULT'; payload: QueryResponse }
  | { type: 'ADD_TO_HISTORY'; payload: QueryHistoryItem }
  | { type: 'CLEAR_HISTORY' }
  | { type: 'SET_MAP_CENTER'; payload: [number, number] }
  | { type: 'SET_MAP_ZOOM'; payload: number }
  | { type: 'SET_SELECTED_FEATURE'; payload: QueryResult | null }
  | { type: 'SET_SCHEMA'; payload: SchemaResponse }
  | { type: 'RESET_STATE' };

// ==============================================================================
// Reducer
// ==============================================================================

const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'SET_QUESTION':
      return { ...state, currentQuestion: action.payload };

    case 'SET_LOADING':
      return { ...state, isLoading: action.payload, error: action.payload ? null : state.error };

    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false };

    case 'SET_QUERY_RESULT':
      return {
        ...state,
        currentQuery: action.payload,
        isLoading: false,
        error: null,
      };

    case 'ADD_TO_HISTORY':
      return {
        ...state,
        queryHistory: [action.payload, ...state.queryHistory].slice(0, 10),  // Keep last 10
      };

    case 'CLEAR_HISTORY':
      return { ...state, queryHistory: [] };

    case 'SET_MAP_CENTER':
      return { ...state, mapCenter: action.payload };

    case 'SET_MAP_ZOOM':
      return { ...state, mapZoom: action.payload };

    case 'SET_SELECTED_FEATURE':
      return { ...state, selectedFeature: action.payload };

    case 'SET_SCHEMA':
      return { ...state, schema: action.payload };

    case 'RESET_STATE':
      return initialState;

    default:
      return state;
  }
};

// ==============================================================================
// Context
// ==============================================================================

interface AppContextType {
  state: AppState;
  dispatch: Dispatch<AppAction>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// ==============================================================================
// Provider
// ==============================================================================

interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

// ==============================================================================
// Custom Hook
// ==============================================================================

export const useAppContext = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

// ==============================================================================
// Action Creators (Helper Functions)
// ==============================================================================

export const appActions = {
  setQuestion: (question: string): AppAction => ({
    type: 'SET_QUESTION',
    payload: question,
  }),

  setLoading: (isLoading: boolean): AppAction => ({
    type: 'SET_LOADING',
    payload: isLoading,
  }),

  setError: (error: string | null): AppAction => ({
    type: 'SET_ERROR',
    payload: error,
  }),

  setQueryResult: (result: QueryResponse): AppAction => ({
    type: 'SET_QUERY_RESULT',
    payload: result,
  }),

  addToHistory: (item: QueryHistoryItem): AppAction => ({
    type: 'ADD_TO_HISTORY',
    payload: item,
  }),

  clearHistory: (): AppAction => ({
    type: 'CLEAR_HISTORY',
  }),

  setMapCenter: (center: [number, number]): AppAction => ({
    type: 'SET_MAP_CENTER',
    payload: center,
  }),

  setMapZoom: (zoom: number): AppAction => ({
    type: 'SET_MAP_ZOOM',
    payload: zoom,
  }),

  setSelectedFeature: (feature: QueryResult | null): AppAction => ({
    type: 'SET_SELECTED_FEATURE',
    payload: feature,
  }),

  setSchema: (schema: SchemaResponse): AppAction => ({
    type: 'SET_SCHEMA',
    payload: schema,
  }),

  resetState: (): AppAction => ({
    type: 'RESET_STATE',
  }),
};
