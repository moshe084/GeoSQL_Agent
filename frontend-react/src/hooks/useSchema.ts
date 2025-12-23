/**
 * Custom hook for fetching database schema
 */

import { useEffect } from 'react';
import { useAppContext, appActions } from '../context/AppContext';
import { api, getErrorMessage } from '../services/api';

export const useSchema = () => {
  const { state, dispatch } = useAppContext();

  useEffect(() => {
    const fetchSchema = async () => {
      try {
        const schema = await api.schema();
        dispatch(appActions.setSchema(schema));
      } catch (error) {
        console.error('Failed to fetch schema:', getErrorMessage(error));
      }
    };

    if (!state.schema) {
      fetchSchema();
    }
  }, [state.schema, dispatch]);

  return {
    schema: state.schema,
    tables: state.schema?.tables || {},
    totalRecords: state.schema?.total_records || 0,
  };
};
