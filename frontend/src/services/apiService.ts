import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  // DAO Health
  async getDAOHealth(daoAddress: string) {
    const response = await api.get(`/api/dao/${daoAddress}/health`);
    return response.data;
  },

  // Proposal Analysis
  async analyzeProposal(proposalData: any) {
    const response = await api.post('/api/proposals/analyze', proposalData);
    return response.data;
  },

  async getProposalSummary(proposalId: string) {
    const response = await api.get(`/api/proposals/${proposalId}/summary`);
    return response.data;
  },

  async getProposalPredictions(daoAddress: string, limit: number = 10) {
    const response = await api.get(`/api/predictions/${daoAddress}/proposals?limit=${limit}`);
    return response.data;
  },

  // Treasury Analysis
  async getTreasuryAnalysis(daoAddress: string) {
    const response = await api.get(`/api/treasury/${daoAddress}/analysis`);
    return response.data;
  },

  // Governance Metrics
  async getGovernanceMetrics(daoAddress: string) {
    const response = await api.get(`/api/governance/${daoAddress}/metrics`);
    return response.data;
  },

  // Cross-chain Assets
  async getCrossChainAssets(daoAddress: string) {
    const response = await api.get(`/api/cross-chain/${daoAddress}/assets`);
    return response.data;
  },

  // Action Execution
  async executeAction(actionData: any) {
    const response = await api.post('/api/actions/execute', actionData);
    return response.data;
  },

  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService; 