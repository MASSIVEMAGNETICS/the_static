import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css';
import { AIFactoryProvider } from './hooks/useAIFactory';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AIFactoryProvider>
      <App />
    </AIFactoryProvider>
  </React.StrictMode>,
);
