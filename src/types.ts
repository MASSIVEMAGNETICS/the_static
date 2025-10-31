export interface Node {
  id: string;
  type: NodeType;
  label: string;
  prompt?: string;
  inputs?: string[];
  outputs?: string[];
}

export type NodeType = 'custom' | 'text-generation' | 'image-analysis' | 'data-extraction';

export interface Edge {
  id: string;
  source: string;
  target: string;
}
