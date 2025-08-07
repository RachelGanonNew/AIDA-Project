import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  UsersIcon, 
  ArrowTrendingUpIcon,
  ClockIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import toast from 'react-hot-toast';
import { apiService } from '../services/apiService';

const GovernanceMetrics: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGovernanceMetrics();
  }, []);

  const loadGovernanceMetrics = async () => {
    try {
      setLoading(true);
      const daoAddress = '0x1234567890123456789012345678901234567890';
      const data = await apiService.getGovernanceMetrics(daoAddress);
      setMetrics(data);
    } catch (error) {
      console.error('Error loading governance metrics:', error);
      toast.error('Failed to load governance metrics');
    } finally {
      setLoading(false);
    }
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
      <div>
        <h1 className="text-2xl font-bold text-white">Governance Metrics</h1>
        <p className="mt-2 text-sm text-gray-400">
          Comprehensive governance analytics and AI-powered predictions
        </p>
      </div>

      {metrics && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex items-center">
                <DocumentTextIcon className="h-5 w-5 text-blue-400" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Total Proposals</p>
                  <p className="text-2xl font-semibold text-white">
                    {metrics.total_proposals}
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex items-center">
                <ClockIcon className="h-5 w-5 text-green-400" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Active Proposals</p>
                  <p className="text-2xl font-semibold text-white">
                    {metrics.active_proposals}
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex items-center">
                <UsersIcon className="h-5 w-5 text-purple-400" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Voter Participation</p>
                  <p className="text-2xl font-semibold text-white">
                    {(metrics.average_voter_participation * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex items-center">
                <ArrowTrendingUpIcon className="h-5 w-5 text-yellow-400" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Success Rate</p>
                  <p className="text-2xl font-semibold text-white">
                    {(metrics.proposal_success_rate * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Governance Trends */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <h2 className="text-lg font-semibold text-white mb-4">Governance Trends</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4">
              {Object.entries(metrics.governance_trends).map(([key, value]: [string, any]) => (
                <div key={key} className="p-4 bg-slate-700 rounded-lg">
                  <h4 className="font-medium text-white mb-2 capitalize">
                    {key.replace('_', ' ')}
                  </h4>
                  <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${
                    value === 'increasing' ? 'bg-green-500/20 text-green-400' :
                    value === 'decreasing' ? 'bg-red-500/20 text-red-400' :
                    'bg-blue-500/20 text-blue-400'
                  }`}>
                    {value}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Top Voters */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <h2 className="text-lg font-semibold text-white mb-4">Top Voters</h2>
            <div className="space-y-3">
              {metrics.top_voters?.map((voter: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-700 rounded-lg">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-sm font-medium text-white">
                      {index + 1}
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-white">{voter.address}</p>
                      <p className="text-xs text-gray-400">{voter.votes} votes</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-white">
                      {(voter.percentage * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* AI Predictions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <h2 className="text-lg font-semibold text-white mb-4">AI Predictions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
              <div>
                <h3 className="text-md font-medium text-white mb-3">Next Month Forecast</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Voter Participation</span>
                    <span className="text-white">
                      {(metrics.predictions.next_month_participation * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Success Probability</span>
                    <span className="text-white">
                      {(metrics.predictions.proposal_success_probability * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="text-md font-medium text-white mb-3">Trending Topics</h3>
                <div className="space-y-2">
                  {metrics.predictions.trending_topics?.map((topic: string, index: number) => (
                    <div key={index} className="flex items-center">
                      <div className="flex-shrink-0 w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                      <span className="text-sm text-gray-300 capitalize">
                        {topic.replace('_', ' ')}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Performance Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <h2 className="text-lg font-semibold text-white mb-4">Voting Performance</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={[
                  { month: 'Jan', participation: 65, success: 70 },
                  { month: 'Feb', participation: 68, success: 75 },
                  { month: 'Mar', participation: 72, success: 68 },
                  { month: 'Apr', participation: 70, success: 72 },
                  { month: 'May', participation: 75, success: 80 },
                  { month: 'Jun', participation: 78, success: 85 }
                ]}>
                  <XAxis dataKey="month" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip />
                  <Bar dataKey="participation" fill="#3B82F6" name="Participation %" />
                  <Bar dataKey="success" fill="#10B981" name="Success %" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        </>
      )}
    </div>
  );
};

export default GovernanceMetrics; 