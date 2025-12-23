import React from 'react';

interface SQLDisplayProps {
  sql: string;
  executionTime: number;
}

export const SQLDisplay: React.FC<SQLDisplayProps> = ({ sql, executionTime }) => {
  const [copied, setCopied] = React.useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-gray-900 rounded-lg p-4 relative">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-gray-400">Generated SQL</span>
        <div className="flex items-center space-x-2">
          <span className="text-xs text-gray-400">⏱️ {executionTime.toFixed(3)}s</span>
          <button
            onClick={copyToClipboard}
            className="px-2 py-1 text-xs bg-gray-800 hover:bg-gray-700 text-white rounded"
          >
            {copied ? '✓ Copied!' : '📋 Copy'}
          </button>
        </div>
      </div>
      <pre className="text-green-400 text-sm overflow-x-auto">{sql}</pre>
    </div>
  );
};
