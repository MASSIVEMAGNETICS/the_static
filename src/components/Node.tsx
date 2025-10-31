import React from 'react';
import { Node as NodeType } from '../types';
import { useAIFactory } from '../hooks/useAIFactory';
import { NodeIcon } from './icons';

interface NodeProps {
  id: string;
  data: Omit<NodeType, 'id'>;
  isSelected: boolean;
}

const NodeComponent: React.FC<NodeProps> = ({ id, data, isSelected }) => {
  const { openEditModal } = useAIFactory();

  const handleDoubleClick = () => {
    if (data.type === 'custom') {
      openEditModal({ id, ...data });
    }
  };

  return (
    <div
      className={`relative p-3 rounded-lg shadow-md cursor-pointer transition-all ${
        isSelected ? 'ring-2 ring-blue-500 shadow-lg scale-105' : 'hover:shadow-lg'
      }`}
      onDoubleClick={handleDoubleClick}
      style={{
        backgroundColor: data.type === 'custom' ? '#f0f7ff' : '#f9f9f9',
        border: data.type === 'custom' ? '1px dashed #3b82f6' : '1px solid #e5e7eb',
      }}
    >
      <div className="flex items-center space-x-2">
        <NodeIcon type={data.type} />
        <h3 className="font-bold">{data.label}</h3>
      </div>
      <div className="text-xs text-gray-500 mt-1">
        {data.type === 'custom' && (
          <p className="italic">✏️ Double-click to edit prompt</p>
        )}
        {data.type !== 'custom' && <p>{data.type}</p>}
      </div>
      {/* Input Ports */}
      {data.inputs?.map((input, i) => (
        <div key={i} className="absolute -left-2 top-1/2 w-4 h-4 bg-gray-400 rounded-full" />
      ))}
      {/* Output Ports */}
      {data.outputs?.map((output, i) => (
        <div key={i} className="absolute -right-2 top-1/2 w-4 h-4 bg-gray-400 rounded-full" />
      ))}
      {data.type === 'custom' && (
        <div className="mt-2 p-2 bg-gray-100 rounded text-xs text-gray-600">
          {data.prompt?.substring(0, 80)}{data.prompt?.length > 80 ? '...' : ''}
        </div>
      )}
    </div>
  );
};

export default NodeComponent;
