import React from 'react';
import { NodeType } from '../types';

export const NodeIcon: React.FC<{ type: NodeType }> = ({ type }) => {
  const icons = {
    custom: '🤖',
    'text-generation': '📝',
    'image-analysis': '🖼️',
    'data-extraction': '📊',
  };

  return <span style={{ fontSize: '1.5rem' }}>{icons[type] || '❓'}</span>;
};
