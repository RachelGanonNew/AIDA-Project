import axios from 'axios';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const apiEndpoints = {
  health: () => apiClient.get('/health'),
  daoHealth: (daoAddress: string) => apiClient.get(`/api/dao/${daoAddress}/health`),
  analyzeProposal: (data: any) => apiClient.post('/api/proposals/analyze', data),
  proposalSummary: (proposalId: string) => apiClient.get(`/api/proposals/${proposalId}/summary`),
  executeAction: (data: any) => apiClient.post('/api/actions/execute', data),
  treasuryAnalysis: (daoAddress: string) => apiClient.get(`/api/treasury/${daoAddress}/analysis`),
  governanceMetrics: (daoAddress: string) => apiClient.get(`/api/governance/${daoAddress}/metrics`),
  proposalPredictions: (daoAddress: string, limit: number = 10) => 
    apiClient.get(`/api/predictions/${daoAddress}/proposals?limit=${limit}`),
  crossChainAssets: (daoAddress: string) => apiClient.get(`/api/cross-chain/${daoAddress}/assets`),
};

// React Query hooks
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: apiEndpoints.health,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useDAOHealth = (daoAddress: string) => {
  return useQuery({
    queryKey: ['daoHealth', daoAddress],
    queryFn: () => apiEndpoints.daoHealth(daoAddress),
    enabled: !!daoAddress,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

export const useProposalAnalysis = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: apiEndpoints.analyzeProposal,
    onSuccess: (data, variables) => {
      // Invalidate and refetch related queries
      queryClient.invalidateQueries({ queryKey: ['proposals'] });
      queryClient.invalidateQueries({ queryKey: ['daoHealth', variables.dao_address] });
    },
  });
};

export const useProposalSummary = (proposalId: string) => {
  return useQuery({
    queryKey: ['proposalSummary', proposalId],
    queryFn: () => apiEndpoints.proposalSummary(proposalId),
    enabled: !!proposalId,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useActionExecution = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: apiEndpoints.executeAction,
    onSuccess: () => {
      // Invalidate related queries after action execution
      queryClient.invalidateQueries({ queryKey: ['treasury'] });
      queryClient.invalidateQueries({ queryKey: ['governance'] });
    },
  });
};

export const useTreasuryAnalysis = (daoAddress: string) => {
  return useQuery({
    queryKey: ['treasuryAnalysis', daoAddress],
    queryFn: () => apiEndpoints.treasuryAnalysis(daoAddress),
    enabled: !!daoAddress,
    staleTime: 3 * 60 * 1000, // 3 minutes
  });
};

export const useGovernanceMetrics = (daoAddress: string) => {
  return useQuery({
    queryKey: ['governanceMetrics', daoAddress],
    queryFn: () => apiEndpoints.governanceMetrics(daoAddress),
    enabled: !!daoAddress,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

export const useProposalPredictions = (daoAddress: string, limit: number = 10) => {
  return useQuery({
    queryKey: ['proposalPredictions', daoAddress, limit],
    queryFn: () => apiEndpoints.proposalPredictions(daoAddress, limit),
    enabled: !!daoAddress,
    staleTime: 1 * 60 * 1000, // 1 minute
  });
};

export const useCrossChainAssets = (daoAddress: string) => {
  return useQuery({
    queryKey: ['crossChainAssets', daoAddress],
    queryFn: () => apiEndpoints.crossChainAssets(daoAddress),
    enabled: !!daoAddress,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Legacy functions for backward compatibility
export const getDAOHealth = async (daoAddress: string) => {
  const response = await apiEndpoints.daoHealth(daoAddress);
  return response.data;
};

export const analyzeProposal = async (data: any) => {
  const response = await apiEndpoints.analyzeProposal(data);
  return response.data;
};

export const getTreasuryAnalysis = async (daoAddress: string) => {
  const response = await apiEndpoints.treasuryAnalysis(daoAddress);
  return response.data;
};

export const getGovernanceMetrics = async (daoAddress: string) => {
  const response = await apiEndpoints.governanceMetrics(daoAddress);
  return response.data;
};

export const getProposalPredictions = async (daoAddress: string, limit: number = 10) => {
  const response = await apiEndpoints.proposalPredictions(daoAddress, limit);
  return response.data;
};

export const getCrossChainAssets = async (daoAddress: string) => {
  const response = await apiEndpoints.crossChainAssets(daoAddress);
  return response.data;
};

// Default export for backward compatibility
const apiService = {
  apiEndpoints,
  getDAOHealth,
  analyzeProposal,
  getTreasuryAnalysis,
  getGovernanceMetrics,
  getProposalPredictions,
  getCrossChainAssets,
};

export { apiService };
export default apiService; 