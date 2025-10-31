import { Node } from './types';

export const PREDEFINED_NODES: Omit<Node, 'id'>[] = [
  {
    type: 'text-generation',
    label: 'Text Generation',
    inputs: ['prompt'],
    outputs: ['text'],
  },
  {
    type: 'image-analysis',
    label: 'Image Analysis',
    inputs: ['image'],
    outputs: ['description'],
  },
  {
    type: 'data-extraction',
    label: 'Data Extraction',
    inputs: ['document'],
    outputs: ['data'],
  },
];
