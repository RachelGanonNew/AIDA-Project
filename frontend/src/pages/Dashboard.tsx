import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  DocumentTextIcon, 
  BanknotesIcon, 
  UsersIcon,
  TrendingUpIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { apiService } from '../services/apiService';

interface DashboardData {
  daoHealth: any;
  recentProposals: any[];
  treasuryOverview: any;
  governanceMetrics: any;
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      // Mock DAO address for demo
      const daoAddress = '0x1234567890123456789012345678901234567890';
      
      const [daoHealth, treasuryOverview, governanceMetrics] = await Promise.all([
        apiService.getDAOHealth(daoAddress),
        apiService.getTreasuryAnalysis(daoAddress),
        apiService.getGovernanceMetrics(daoAddress)
      ]);

      setData({
        daoHealth,
        recentProposals: [], // Would be populated from API
        treasuryOverview,
        governanceMetrics
      });
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 0.7) return 'text-green-400';
    if (score >= 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getHealthStatus = (score: number) => {
    if (score >= 0.7) return 'Excellent';
    if (score >= 0.5) return 'Good';
    return 'Needs Attention';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="mt-2 text-sm text-gray-400">
            AI-powered insights for DAO governance and treasury management
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={loadDashboardData}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Refresh Data
          </button>
        </div>
      </div>

      {/* Health Overview */}
      {data?.daoHealth && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-slate-800 rounded-lg p-6 border border-slate-700"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">DAO Health Overview</h2>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getHealthColor(data.daoHealth.overall_health_score)} bg-opacity-20`}>
              {getHealthStatus(data.daoHealth.overall_health_score)}
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className={`text-2xl font-bold ${getHealthColor(data.daoHealth.overall_health_score)}`}>
                {(data.daoHealth.overall_health_score * 100).toFixed(0)}%
              </div>
              <div className="text-sm text-gray-400">Overall Health</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getHealthColor(data.daoHealth.governance_score)}`}>
                {(data.daoHealth.governance_score * 100).toFixed(0)}%
              </div>
              <div className="text-sm text-gray-400">Governance</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getHealthColor(data.daoHealth.financial_score)}`}>
                {(data.daoHealth.financial_score * 100).toFixed(0)}%
              </div>
              <div className="text-sm text-gray-400">Financial</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getHealthColor(data.daoHealth.community_score)}`}>
                {(data.daoHealth.community_score * 100).toFixed(0)}%
              </div>
              <div className="text-sm text-gray-400">Community</div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-slate-800 rounded-lg p-6 border border-slate-700 card-hover"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <BanknotesIcon className="h-8 w-8 text-blue-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-400">Treasury Value</p>
              <p className="text-2xl font-semibold text-white">
                ${data?.treasuryOverview?.total_value_usd?.toLocaleString() || '0'}
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-slate-800 rounded-lg p-6 border border-slate-700 card-hover"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <DocumentTextIcon className="h-8 w-8 text-green-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-400">Active Proposals</p>
              <p className="text-2xl font-semibold text-white">
                {data?.governanceMetrics?.active_proposals || 0}
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-slate-800 rounded-lg p-6 border border-slate-700 card-hover"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <UsersIcon className="h-8 w-8 text-purple-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-400">Voter Participation</p>
              <p className="text-2xl font-semibold text-white">
                {((data?.governanceMetrics?.average_voter_participation || 0) * 100).toFixed(0)}%
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-slate-800 rounded-lg p-6 border border-slate-700 card-hover"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUpIcon className="h-8 w-8 text-yellow-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-400">Success Rate</p>
              <p className="text-2xl font-semibold text-white">
                {((data?.governanceMetrics?.proposal_success_rate || 0) * 100).toFixed(0)}%
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Risk Factors & Recommendations */}
      {data?.daoHealth && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <div className="flex items-center mb-4">
              <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400 mr-2" />
              <h3 className="text-lg font-semibold text-white">Risk Factors</h3>
            </div>
            <div className="space-y-2">
              {data.daoHealth.risk_factors?.slice(0, 3).map((risk: string, index: number) => (
                <div key={index} className="flex items-start">
                  <div className="flex-shrink-0 w-2 h-2 bg-yellow-400 rounded-full mt-2 mr-3"></div>
                  <p className="text-sm text-gray-300">{risk}</p>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <div className="flex items-center mb-4">
              <CheckCircleIcon className="h-5 w-5 text-green-400 mr-2" />
              <h3 className="text-lg font-semibold text-white">AI Recommendations</h3>
            </div>
            <div className="space-y-2">
              {data.daoHealth.recommendations?.slice(0, 3).map((rec: string, index: number) => (
                <div key={index} className="flex items-start">
                  <div className="flex-shrink-0 w-2 h-2 bg-green-400 rounded-full mt-2 mr-3"></div>
                  <p className="text-sm text-gray-300">{rec}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="bg-slate-800 rounded-lg p-6 border border-slate-700"
      >
        <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="flex items-center justify-center px-4 py-3 border border-slate-600 rounded-lg text-sm font-medium text-gray-300 hover:bg-slate-700 hover:text-white transition-colors">
            <DocumentTextIcon className="h-5 w-5 mr-2" />
            Analyze New Proposal
          </button>
          <button className="flex items-center justify-center px-4 py-3 border border-slate-600 rounded-lg text-sm font-medium text-gray-300 hover:bg-slate-700 hover:text-white transition-colors">
            <BanknotesIcon className="h-5 w-5 mr-2" />
            Rebalance Treasury
          </button>
          <button className="flex items-center justify-center px-4 py-3 border border-slate-600 rounded-lg text-sm font-medium text-gray-300 hover:bg-slate-700 hover:text-white transition-colors">
            <ChartBarIcon className="h-5 w-5 mr-2" />
            View Analytics
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard; 