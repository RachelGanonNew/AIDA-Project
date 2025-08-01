import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Dashboard from './pages/Dashboard';
import ProposalAnalysis from './pages/ProposalAnalysis';
import TreasuryAnalysis from './pages/TreasuryAnalysis';
import GovernanceMetrics from './pages/GovernanceMetrics';
import Layout from './components/Layout';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/proposals" element={<ProposalAnalysis />} />
            <Route path="/treasury" element={<TreasuryAnalysis />} />
            <Route path="/governance" element={<GovernanceMetrics />} />
          </Routes>
        </Layout>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App; 