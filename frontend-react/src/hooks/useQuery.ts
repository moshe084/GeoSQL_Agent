/**
 * Custom hook for executing natural language queries
 */

import { useCallback } from 'react';
import { useAppContext, appActions } from '../context/AppContext';
import { api, getErrorMessage } from '../services/api';
import { QueryHistoryItem } from '../types';

export const useQuery = () => {
  const { state, dispatch } = useAppContext();

  const executeQuery = useCallback(
    async (question: string) => {
      try {
        // Set loading state
        dispatch(appActions.setLoading(true));
        dispatch(appActions.setQuestion(question));

        // Execute query
        const result = await api.query({ question });

        // Update state with results
        dispatch(appActions.setQueryResult(result));

        // Add to history
        const historyItem: QueryHistoryItem = {
          id: Date.now().toString(),
          question,
          sql: result.sql,
          result_count: result.result_count,
          execution_time: result.execution_time,
          timestamp: result.timestamp,
        };
        dispatch(appActions.addToHistory(historyItem));

        return result;
      } catch (error) {
        const errorMessage = getErrorMessage(error);
        dispatch(appActions.setError(errorMessage));
        throw error;
      }
    },
    [dispatch]
  );

  return {
    executeQuery,
    isLoading: state.isLoading,
    error: state.error,
    currentQuery: state.currentQuery,
    queryHistory: state.queryHistory,
  };
};
