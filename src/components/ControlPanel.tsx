import React, { useState } from 'react';
import { useAIFactory } from '../hooks/useAIFactory';

const ControlPanel: React.FC = () => {
  const { createCustomNodeFromText } = useAIFactory();
  const [text, setText] = useState('');

  const handleCreate = () => {
    if (text.trim()) {
      createCustomNodeFromText(text);
      setText('');
    }
  };

  return (
    <div className="p-4 bg-gray-100">
      <h2 className="text-lg font-bold mb-4">Create Custom Node</h2>
      <textarea
        className="w-full p-2 border rounded"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Describe the AI task..."
      />
      <button
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        onClick={handleCreate}
      >
        Create
      </button>
    </div>
  );
};

export default ControlPanel;
