import React from 'react';
import { AppProvider, useAppContext } from './context/AppContext';
import { ErrorBoundary } from './components/ErrorBoundary';
import { QueryInput } from './components/QueryInput';
import { Map } from './components/Map';
import { SQLDisplay } from './components/SQLDisplay';
import { LoadingSpinner } from './components/LoadingSpinner';
import { useQuery } from './hooks';

const AppContent: React.FC = () => {
  const { state } = useAppContext();
  const { executeQuery, isLoading, error } = useQuery();

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-purple-500 via-purple-600 to-indigo-700">
      {/* Header */}
      <header className="bg-white shadow-md px-6 py-4 flex items-center space-x-3">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-full flex items-center justify-center text-white text-xl">
          🌍
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Geo-SQL Agent</h1>
          <p className="text-xs text-gray-600">
            Ask questions in natural language, get spatial SQL queries in real-time
          </p>
        </div>
      </header>

      {/* Main Content - Split View */}
      <main className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <div className="w-2/5 p-4 overflow-y-auto space-y-4">
          {/* Query Input */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
              <span>🔍</span>
              <span>Ask Your Question</span>
            </h2>
            <QueryInput onSubmit={executeQuery} isLoading={isLoading} />
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {/* Loading Spinner */}
          {isLoading && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <LoadingSpinner message="Processing query..." />
            </div>
          )}

          {/* SQL Display - Show generated SQL query */}
          {state.currentQuery && !isLoading && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
                <span>⚙️</span>
                <span>Generated SQL</span>
              </h2>
              <SQLDisplay
                sql={state.currentQuery.sql}
                executionTime={state.currentQuery.execution_time}
              />
            </div>
          )}

          {/* Example Queries */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
              <span>💡</span>
              <span>Example Queries</span>
            </h2>
            <div className="space-y-3 text-sm text-gray-700">
              <p className="hover:text-purple-600 cursor-pointer" onClick={() => executeQuery('Find all cafes within 200 meters of the largest park')}>
                Find all cafes within 200 meters of the largest park
              </p>
              <p className="hover:text-purple-600 cursor-pointer" onClick={() => executeQuery('Show all parks larger than 5000 square meters')}>
                Show all parks larger than 5000 square meters
              </p>
              <p className="hover:text-purple-600 cursor-pointer" onClick={() => executeQuery('Find cafes near main roads')}>
                Find cafes near main roads
              </p>
              <p className="hover:text-purple-600 cursor-pointer" onClick={() => executeQuery('What is the closest cafe to the smallest park?')}>
                What is the closest cafe to the smallest park?
              </p>
              <p className="hover:text-purple-600 cursor-pointer" onClick={() => executeQuery('Show all roads that intersect with parks')}>
                Show all roads that intersect with parks
              </p>
            </div>
          </div>
        </div>

        {/* Right Map */}
        <div className="flex-1 relative">
          <Map
            results={state.currentQuery?.results || []}
            resultCount={state.currentQuery?.result_count || 0}
            executionTime={state.currentQuery?.execution_time || 0}
          />
        </div>
      </main>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </ErrorBoundary>
  );
};
