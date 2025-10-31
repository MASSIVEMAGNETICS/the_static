import React, { useState, useCallback, createContext, useContext, ReactNode } from 'react';
import { Node, Edge } from '../types';
import { generateCustomNode } from '../services/geminiService';

export interface AIFactoryState {
  nodes: Node[];
  edges: Edge[];
  selectedNode: string | null;
  isModalOpen: boolean;
  modalType: 'create' | 'edit';
  modalData: Partial<Node> | null;
}

export interface AIFactoryContextProps extends AIFactoryState {
  addNode: (node: Omit<Node, 'id'>) => void;
  deleteNode: (nodeId: string) => void;
  createCustomNodeFromText: (description: string) => Promise<void>;
  openEditModal: (node: Node) => void;
  openCreateModal: () => void;
  closeModals: () => void;
  saveModal: (data: Partial<Node>) => void;
  updateNodePrompt: (nodeId: string, newPrompt: string) => void;
}

const AIFactoryContext = createContext<AIFactoryContextProps | undefined>(undefined);

export const AIFactoryProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AIFactoryState>({
    nodes: [],
    edges: [],
    selectedNode: null,
    isModalOpen: false,
    modalType: 'create',
    modalData: null,
  });

  const addNode = useCallback((node: Omit<Node, 'id'>) => {
    const newNode: Node = {
      id: `node-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      ...node,
    };
    setState(prev => ({ ...prev, nodes: [...prev.nodes, newNode] }));
  }, []);

  const updateNodePrompt = useCallback((nodeId: string, newPrompt: string) => {
    setState(prev => ({
      ...prev,
      nodes: prev.nodes.map(node =>
        node.id === nodeId && node.type === 'custom'
          ? { ...node, prompt: newPrompt }
          : node
      ),
    }));
  }, []);

  const deleteNode = useCallback((nodeId: string) => {
    setState(prev => ({
      ...prev,
      nodes: prev.nodes.filter(n => n.id !== nodeId),
      edges: prev.edges.filter(e => e.source !== nodeId && e.target !== nodeId),
    }));
  }, []);

  const createCustomNodeFromText = useCallback(async (description: string) => {
    const nodeData = await generateCustomNode(description);
    addNode(nodeData);
  }, [addNode]);

  const openEditModal = useCallback((node: Node) => {
    if (node.type !== 'custom') return;
    setState(prev => ({
      ...prev,
      isModalOpen: true,
      modalType: 'edit',
      modalData: node,
    }));
  }, []);

  const openCreateModal = useCallback(() => {
    setState(prev => ({
      ...prev,
      isModalOpen: true,
      modalType: 'create',
      modalData: null,
    }));
  }, []);

  const closeModals = useCallback(() => {
    setState(prev => ({ ...prev, isModalOpen: false, modalData: null }));
  }, []);

  const saveModal = useCallback((data: Partial<Node>) => {
    if (state.modalType === 'create') {
      addNode(data as Omit<Node, 'id'>);
    } else if (state.modalType === 'edit' && state.modalData?.id) {
      updateNodePrompt(state.modalData.id, data.prompt || '');
    }
    closeModals();
  }, [state.modalType, state.modalData, addNode, updateNodePrompt, closeModals]);

  const value = {
    ...state,
    addNode,
    deleteNode,
    createCustomNodeFromText,
    openEditModal,
    openCreateModal,
    closeModals,
    saveModal,
    updateNodePrompt,
  };

  return (
    <AIFactoryContext.Provider value={value}>
      {children}
    </AIFactoryContext.Provider>
  );
};

export const useAIFactory = () => {
  const context = useContext(AIFactoryContext);
  if (context === undefined) {
    throw new Error('useAIFactory must be used within an AIFactoryProvider');
  }
  return context;
};
