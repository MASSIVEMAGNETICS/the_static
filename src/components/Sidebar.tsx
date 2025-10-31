import React from 'react';
import { PREDEFINED_NODES } from '../constants';
import { useAIFactory } from '../hooks/useAIFactory';

const Sidebar: React.FC = () => {
  const { addNode } = useAIFactory();

  return (
    <div className="w-64 bg-gray-100 p-4">
      <h2 className="text-lg font-bold mb-4">Nodes</h2>
      {PREDEFINED_NODES.map((node, i) => (
        <div
          key={i}
          className="p-2 mb-2 bg-white rounded shadow cursor-pointer"
          onClick={() => addNode(node)}
        >
          {node.label}
        </div>
      ))}
    </div>
  );
};

export default Sidebar;
