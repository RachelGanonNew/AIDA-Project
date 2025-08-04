import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from 'react-hot-toast';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import ProposalAnalysis from './pages/ProposalAnalysis';
import TreasuryAnalysis from './pages/TreasuryAnalysis';
import GovernanceMetrics from './pages/GovernanceMetrics';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/proposals" element={<ProposalAnalysis />} />
            <Route path="/treasury" element={<TreasuryAnalysis />} />
            <Route path="/governance" element={<GovernanceMetrics />} />
          </Routes>
        </Layout>
      </Router>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1e293b',
            color: '#fff',
            border: '1px solid rgba(255, 255, 255, 0.1)',
          },
        }}
      />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App; 