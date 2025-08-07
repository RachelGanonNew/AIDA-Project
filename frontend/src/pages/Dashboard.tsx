import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  DocumentTextIcon, 
  BanknotesIcon, 
  UsersIcon,
  ArrowTrendingUpIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import './Dashboard.css';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { apiService } from '../services/apiService';
import HealthCard from '../components/HealthCard';
import LoadingSpinner from '../components/LoadingSpinner';

interface DashboardData {
  daoHealth: any;
  recentProposals: any[];
  treasuryOverview: any;
  governanceMetrics: any;
}

const DEMO_DAO_HEALTH = {
  overall_health_score: 0.82,
  governance_score: 0.88,
  financial_score: 0.76,
  community_score: 0.79,
};

// const DEMO_PROPOSALS = [
//   {
//     id: 'prop-001',
//     title: 'Update Treasury Allocation',
//     description: 'Rebalance the DAO treasury to optimize yield and reduce risk.',
//     status: 'Active',
//     prediction: 'Likely to Pass',
//     risk_level: 'Medium',
//     proposer: '0x123...abcd',
//   },
//   {
//     id: 'prop-002',
//     title: 'Add New Governance Module',
//     description: 'Implement a new voting mechanism to increase participation.',
//     status: 'Pending',
//     prediction: 'Uncertain',
//     risk_level: 'Low',
//     proposer: '0x456...efgh',
//   },
// ];

function Dashboard() {
  const [demoMode, setDemoMode] = useState(true);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    // Show onboarding modal on first load
    if (window.localStorage.getItem('aida_onboarding_shown') !== 'true') {
      setShowOnboarding(true);
      window.localStorage.setItem('aida_onboarding_shown', 'true');
    }
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

  // Use demo data if demoMode is enabled
  const daoHealth = demoMode ? DEMO_DAO_HEALTH : data?.daoHealth;
      // const proposals = demoMode ? [] : data?.recentProposals;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size={48} text="Loading dashboard data..." />
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Page Header */}
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-description">Overview of your DAO's health, governance, and treasury metrics</p>
      </div>

      {/* Onboarding Modal */}
      {showOnboarding && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70">
          <div className="bg-slate-800 rounded-lg shadow-lg p-8 max-w-md w-full text-center border border-slate-700">
            <h2 className="text-2xl font-bold mb-4 text-white">Welcome to AIDA!</h2>
            <p className="mb-4 text-gray-300">
              This is a live demo of the AI-Driven DAO Analyst. Explore the dashboard, analyze proposals, and see AI-powered insights in action.
            </p>
            <button
              className="mt-2 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              onClick={() => setShowOnboarding(false)}
            >
              Get Started
            </button>
          </div>
        </div>
      )}

      {/* Demo Mode Toggle */}
      <div className="flex justify-end">
        <label className="flex items-center space-x-2 cursor-pointer bg-slate-800 px-4 py-2 rounded-lg border border-slate-700">
          <input
            type="checkbox"
            checked={demoMode}
            onChange={() => setDemoMode((v) => !v)}
            className="form-checkbox h-4 w-4 text-blue-600"
          />
          <span className="text-sm text-gray-600 dark:text-gray-300">Demo Mode</span>
        </label>
      </div>

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
      {daoHealth && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">DAO Health Overview</h2>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getHealthColor(daoHealth.overall_health_score)} bg-opacity-20`}>
              {getHealthStatus(daoHealth.overall_health_score)}
            </div>
          </div>
          
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <HealthCard
              title="Overall Health"
              value={`${(daoHealth.overall_health_score * 100).toFixed(0)}%`}
              subtitle={getHealthStatus(daoHealth.overall_health_score)}
              icon={<ChartBarIcon className="h-6 w-6" />}
              color="bg-blue-500/20 text-blue-400"
              trend={{
                direction: daoHealth.overall_health_score > 0.7 ? 'up' : 'stable',
                value: '+5%'
              }}
            />
            <HealthCard
              title="Governance"
              value={`${(daoHealth.governance_score * 100).toFixed(0)}%`}
              icon={<DocumentTextIcon className="h-6 w-6" />}
              color="bg-green-500/20 text-green-400"
            />
            <HealthCard
              title="Financial"
              value={`${(daoHealth.financial_score * 100).toFixed(0)}%`}
              icon={<BanknotesIcon className="h-6 w-6" />}
              color="bg-yellow-500/20 text-yellow-400"
            />
            <HealthCard
              title="Community"
              value={`${(daoHealth.community_score * 100).toFixed(0)}%`}
              icon={<UsersIcon className="h-6 w-6" />}
              color="bg-purple-500/20 text-purple-400"
            />
          </div>
        </motion.div>
      )}

      {/* Key Metrics */}
      <div>
        <h2 className="section-title">Key Metrics</h2>
        <div className="metrics-grid">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="metric-card"
        >
          <div className="metric-content">
            <BanknotesIcon className="metric-icon blue" />
            <div className="metric-info">
              <p className="metric-label">Treasury Value</p>
              <p className="metric-value">
                ${data?.treasuryOverview?.total_value_usd?.toLocaleString() || '0'}
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="metric-card"
        >
          <div className="metric-content">
            <DocumentTextIcon className="metric-icon green" />
            <div className="metric-info">
              <p className="metric-label">Active Proposals</p>
              <p className="metric-value">
                {data?.governanceMetrics?.active_proposals || 0}
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="metric-card"
        >
          <div className="metric-content">
            <UsersIcon className="metric-icon purple" />
            <div className="metric-info">
              <p className="metric-label">Voter Participation</p>
              <p className="metric-value">
                {((data?.governanceMetrics?.average_voter_participation || 0) * 100).toFixed(0)}%
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="metric-card"
        >
          <div className="metric-content">
            <ArrowTrendingUpIcon className="metric-icon yellow" />
            <div className="metric-info">
              <p className="metric-label">Success Rate</p>
              <p className="metric-value">
                {((data?.governanceMetrics?.proposal_success_rate || 0) * 100).toFixed(0)}%
              </p>
            </div>
          </div>
        </motion.div>
        </div>
      </div>

      {/* Risk Factors & Recommendations */}
      {daoHealth && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-white">Risk Assessment & Recommendations</h2>
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
              {daoHealth.risk_factors?.slice(0, 3).map((risk: string, index: number) => (
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
              {daoHealth.recommendations?.slice(0, 3).map((rec: string, index: number) => (
                <div key={index} className="flex items-start">
                  <div className="flex-shrink-0 w-2 h-2 bg-green-400 rounded-full mt-2 mr-3"></div>
                  <p className="text-sm text-gray-300">{rec}</p>
                </div>
              ))}
            </div>
          </motion.div>
          </div>
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
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
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
}

export default Dashboard; 