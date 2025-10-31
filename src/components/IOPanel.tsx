import React from 'react';

const IOPanel: React.FC = () => {
  return (
    <div className="p-4 bg-gray-100">
      <h2 className="text-lg font-bold mb-4">Input/Output</h2>
      <textarea className="w-full p-2 border rounded" placeholder="Input..." />
      <button className="mt-2 px-4 py-2 bg-green-500 text-white rounded">
        Run
      </button>
      <div className="mt-4 p-2 bg-white border rounded">
        <p className="text-gray-500">Output will appear here...</p>
      </div>
    </div>
  );
};

export default IOPanel;
