/**
 * Query Input Component
 * Allows users to enter natural language questions
 */

import React, { useState, FormEvent } from 'react';

interface QueryInputProps {
  onSubmit: (question: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
}

export const QueryInput: React.FC<QueryInputProps> = ({
  onSubmit,
  isLoading = false,
  disabled = false,
}) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (question.trim() && !isLoading && !disabled) {
      onSubmit(question.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <textarea
        id="question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="What is the closest cafe to the smallest park?"
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-all"
        rows={4}
        disabled={isLoading || disabled}
      />

      <div className="flex space-x-3">
        <button
          type="submit"
          disabled={!question.trim() || isLoading || disabled}
          className="flex-1 px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-all"
        >
          {isLoading ? 'Processing...' : 'Execute Query'}
        </button>
        <button
          type="button"
          onClick={() => setQuestion('')}
          className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium rounded-lg transition-all"
        >
          Clear
        </button>
      </div>
    </form>
  );
};
