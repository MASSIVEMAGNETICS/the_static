import React from 'react';
import { useAIFactory } from './hooks/useAIFactory';
import Sidebar from './components/Sidebar';
import ControlPanel from './components/ControlPanel';
import IOPanel from './components/IOPanel';
import NodeComponent from './components/Node';
import './App.css';

const App: React.FC = () => {
  const {
    nodes,
    isModalOpen,
    modalType,
    modalData,
    closeModals,
    saveModal,
  } = useAIFactory();

  const [promptInput, setPromptInput] = React.useState('');

  React.useEffect(() => {
    if (modalData && modalType === 'edit') {
      setPromptInput(modalData.prompt || '');
    } else {
      setPromptInput('');
    }
  }, [modalData, modalType]);

  const handleSave = () => {
    if (modalType === 'edit' && modalData) {
      saveModal({ prompt: promptInput });
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AI Flow Studio</h1>
      </header>
      <main className="main">
        <Sidebar />
        <div className="canvas">
          {nodes.map(node => (
            <NodeComponent
              key={node.id}
              id={node.id}
              data={node}
              isSelected={false}
            />
          ))}
        </div>
        <div className="right-sidebar">
          <ControlPanel />
          <IOPanel />
        </div>
      </main>
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>{modalType === 'create' ? 'Create New AI Node' : 'Edit Custom Node Prompt'}</h2>
            <textarea
              className="w-full p-2 border rounded"
              value={promptInput}
              onChange={(e) => setPromptInput(e.target.value)}
              rows={10}
            />
            <div className="mt-4">
              <button
                className="px-4 py-2 bg-blue-500 text-white rounded"
                onClick={handleSave}
              >
                Save
              </button>
              <button
                className="ml-2 px-4 py-2 bg-gray-300 rounded"
                onClick={closeModals}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
