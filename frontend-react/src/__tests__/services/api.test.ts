/**
 * API service tests
 */

import axios from 'axios';
import { api, getErrorMessage, isApiError } from '../../services/api';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('health check', () => {
    test('calls health endpoint', async () => {
      const mockResponse = {
        status: 'healthy',
        database: 'connected',
        version: '1.0.0',
        environment: 'test',
        timestamp: '2024-01-01T00:00:00',
      };

      mockedAxios.create = jest.fn().mockReturnValue({
        get: jest.fn().mockResolvedValue({ data: mockResponse }),
        post: jest.fn(),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() },
        },
      } as any);

      // Re-import to get mocked axios
      const { api: freshApi } = await import('../../services/api');
      const result = await freshApi.health();

      expect(result).toEqual(mockResponse);
    });
  });

  describe('error handling', () => {
    test('isApiError identifies API errors correctly', () => {
      const apiError = new Error('Test') as any;
      apiError.status = 400;
      apiError.response = { message: 'Test error' };

      expect(isApiError(apiError)).toBe(true);
      expect(isApiError(new Error('Regular error'))).toBe(false);
      expect(isApiError('not an error')).toBe(false);
    });

    test('getErrorMessage extracts message from API errors', () => {
      const apiError = new Error('API Error') as any;
      apiError.status = 400;
      apiError.response = { message: 'Validation failed' };

      expect(getErrorMessage(apiError)).toBe('Validation failed');
    });

    test('getErrorMessage handles regular errors', () => {
      const error = new Error('Regular error');
      expect(getErrorMessage(error)).toBe('Regular error');
    });

    test('getErrorMessage handles unknown errors', () => {
      expect(getErrorMessage('string error')).toBe('An unknown error occurred');
      expect(getErrorMessage(null)).toBe('An unknown error occurred');
      expect(getErrorMessage(undefined)).toBe('An unknown error occurred');
    });
  });
});
