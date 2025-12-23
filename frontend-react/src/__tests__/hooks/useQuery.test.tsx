/**
 * useQuery hook tests
 */

import { renderHook, act, waitFor } from '@testing-library/react';
import { AppProvider } from '../../context/AppContext';
import { useQuery } from '../../hooks/useQuery';
import * as api from '../../services/api';

jest.mock('../../services/api');

describe('useQuery Hook', () => {
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <AppProvider>{children}</AppProvider>
  );

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('executes query successfully', async () => {
    const mockResponse = {
      sql: 'SELECT * FROM cafes',
      results: [{ id: 1, name: 'Test Cafe' }],
      execution_time: 1.5,
      result_count: 1,
      timestamp: '2024-01-01T00:00:00',
    };

    (api.api.query as jest.Mock).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useQuery(), { wrapper });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();

    await act(async () => {
      await result.current.executeQuery('Show all cafes');
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.currentQuery).toEqual(mockResponse);
    expect(result.current.error).toBeNull();
  });

  test('handles query errors', async () => {
    const mockError = new Error('API Error');
    (api.api.query as jest.Mock).mockRejectedValue(mockError);

    const { result } = renderHook(() => useQuery(), { wrapper });

    await act(async () => {
      try {
        await result.current.executeQuery('Invalid query');
      } catch (e) {
        // Expected to throw
      }
    });

    await waitFor(() => {
      expect(result.current.error).toBe('API Error');
    });

    expect(result.current.isLoading).toBe(false);
  });

  test('adds query to history', async () => {
    const mockResponse = {
      sql: 'SELECT * FROM cafes',
      results: [],
      execution_time: 1.0,
      result_count: 0,
      timestamp: '2024-01-01T00:00:00',
    };

    (api.api.query as jest.Mock).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useQuery(), { wrapper });

    await act(async () => {
      await result.current.executeQuery('Test question');
    });

    await waitFor(() => {
      expect(result.current.queryHistory).toHaveLength(1);
    });

    expect(result.current.queryHistory[0].question).toBe('Test question');
  });
});
