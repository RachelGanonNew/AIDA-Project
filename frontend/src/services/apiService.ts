import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use(
  (config) => {
    console.log(` API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => {
    console.log(` API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error(' API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const health = async () => (await apiClient.get('/health')).data;
export const getDAOHealth = async (daoAddress: string) => (await apiClient.get(`/api/dao/${daoAddress}/health`)).data;
export const analyzeProposal = async (data: any) => (await apiClient.post('/api/proposals/analyze', data)).data;
export const getProposalSummary = async (proposalId: string) => (await apiClient.get(`/api/proposals/${proposalId}/summary`)).data;
export const executeAction = async (data: any) => (await apiClient.post('/api/actions/execute', data)).data;
export const getTreasuryAnalysis = async (daoAddress: string) => (await apiClient.get(`/api/treasury/${daoAddress}/analysis`)).data;
export const getGovernanceMetrics = async (daoAddress: string) => (await apiClient.get(`/api/governance/${daoAddress}/metrics`)).data;
export const getProposalPredictions = async (daoAddress: string, limit: number = 10) => (await apiClient.get(`/api/predictions/${daoAddress}/proposals?limit=${limit}`)).data;
export const getCrossChainAssets = async (daoAddress: string) => (await apiClient.get(`/api/cross-chain/${daoAddress}/assets`)).data;
export const getHathorContractStatus = async (contractAddress: string) => (await apiClient.get(`/api/hathor/contracts/${contractAddress}/status`)).data;
export const estimateHathorGas = async (data: any) => (await apiClient.post('/api/hathor/gas/estimate', data)).data;

const apiService = {
  health,
  getDAOHealth,
  analyzeProposal,
  getProposalSummary,
  executeAction,
  getTreasuryAnalysis,
  getGovernanceMetrics,
  getProposalPredictions,
  getCrossChainAssets,
  getHathorContractStatus,
  estimateHathorGas,
};

export { apiService };
export default apiService;
