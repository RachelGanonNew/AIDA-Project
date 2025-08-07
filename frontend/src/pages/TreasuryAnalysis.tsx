import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BanknotesIcon, 
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ArrowTrendingUpIcon
} from '@heroicons/react/24/outline';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import toast from 'react-hot-toast';
import { apiService } from '../services/apiService';

const TreasuryAnalysis: React.FC = () => {
  const [treasuryData, setTreasuryData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTreasuryData();
  }, []);

  const loadTreasuryData = async () => {
    try {
      setLoading(true);
      const daoAddress = '0x1234567890123456789012345678901234567890';
      const data = await apiService.getTreasuryAnalysis(daoAddress);
      setTreasuryData(data);
    } catch (error) {
      console.error('Error loading treasury data:', error);
      toast.error('Failed to load treasury data');
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

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
        <h1 className="heading-responsive font-bold text-white">Treasury Analysis</h1>
        <p className="mt-2 text-responsive text-gray-400">
          AI-powered treasury health analysis and optimization recommendations
        </p>
      </div>

      {treasuryData && (
        <>
          {/* Overview Cards */}
          <div className="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 gap-2 xs:gap-3 sm:gap-4 md:gap-5 lg:gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex items-center">
                <BanknotesIcon className="h-5 w-5 text-blue-400" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Total Value</p>
                  <p className="text-2xl font-semibold text-white">
                    ${treasuryData.total_value_usd?.toLocaleString()}
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
                <ChartBarIcon className="h-5 w-5 text-green-400" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Diversification</p>
                  <p className="text-2xl font-semibold text-white">
                    {(treasuryData.asset_diversification_score * 100).toFixed(0)}%
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
                <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Risk Score</p>
                  <p className="text-2xl font-semibold text-white">
                    {(treasuryData.risk_score * 100).toFixed(0)}%
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
                <ArrowTrendingUpIcon className="h-5 w-5 text-purple-400" />

                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-400">Liquidity</p>
                  <p className="text-2xl font-semibold text-white">
                    {(treasuryData.liquidity_score * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Asset Allocation Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <h2 className="text-lg font-semibold text-white mb-4">Asset Allocation</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={treasuryData.top_holdings}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value_usd"
                  >
                    {treasuryData.top_holdings?.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Risk Factors & Recommendations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex items-center mb-4">
                <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400 mr-2" />
                <h3 className="text-lg font-semibold text-white">Risk Factors</h3>
              </div>
              <div className="space-y-2">
                {treasuryData.risk_factors?.map((risk: string, index: number) => (
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
              transition={{ delay: 0.7 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex items-center mb-4">
                <CheckCircleIcon className="h-5 w-5 text-green-400 mr-2" />
                <h3 className="text-lg font-semibold text-white">AI Recommendations</h3>
              </div>
              <div className="space-y-2">
                {treasuryData.recommendations?.map((rec: string, index: number) => (
                  <div key={index} className="flex items-start">
                    <CheckCircleIcon className="h-4 w-4 text-green-400 mt-0.5 mr-3 flex-shrink-0" />
                    <p className="text-sm text-gray-300">{rec}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Rebalancing Suggestions */}
          {treasuryData.rebalancing_suggestions && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <h3 className="text-lg font-semibold text-white mb-4">Rebalancing Suggestions</h3>
              <div className="space-y-4">
                {treasuryData.rebalancing_suggestions.map((suggestion: any, index: number) => (
                  <div key={index} className="p-4 bg-slate-700 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-white">{suggestion.action}</h4>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        suggestion.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                        suggestion.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {suggestion.priority}
                      </span>
                    </div>
                    <p className="text-sm text-gray-300 mb-2">{suggestion.description}</p>
                    <p className="text-xs text-gray-400">Impact: {suggestion.estimated_impact}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </>
      )}
    </div>
  );
};

export default TreasuryAnalysis; 