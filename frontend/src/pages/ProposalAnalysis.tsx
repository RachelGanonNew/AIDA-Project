import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  DocumentTextIcon, 
  CheckCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { apiService } from '../services/apiService';

const ProposalAnalysis: React.FC = () => {
  const [proposalData, setProposalData] = useState({
    dao_address: '0x1234567890123456789012345678901234567890',
    proposal_id: '',
    title: '',
    description: '',
    proposer: '',
    voting_start: '',
    voting_end: ''
  });
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setProposalData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAnalyze = async () => {
    if (!proposalData.title || !proposalData.description) {
      toast.error('Please fill in the proposal title and description');
      return;
    }

    try {
      setLoading(true);
      const result = await apiService.analyzeProposal(proposalData);
      setAnalysis(result);
      toast.success('Proposal analysis completed!');
    } catch (error) {
      console.error('Error analyzing proposal:', error);
      toast.error('Failed to analyze proposal');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'low': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'high': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getPredictionColor = (prediction: number) => {
    if (prediction >= 0.7) return 'text-green-400';
    if (prediction >= 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Proposal Analysis</h1>
        <p className="mt-2 text-sm text-gray-400">
          AI-powered analysis of governance proposals with predictions and recommendations
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-slate-800 rounded-lg p-6 border border-slate-700"
        >
          <h2 className="text-lg font-semibold text-white mb-4">Analyze New Proposal</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Proposal Title
              </label>
              <input
                type="text"
                name="title"
                value={proposalData.title}
                onChange={handleInputChange}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter proposal title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Proposal Description
              </label>
              <textarea
                name="description"
                value={proposalData.description}
                onChange={handleInputChange}
                rows={6}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter detailed proposal description..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Proposer Address
              </label>
              <input
                type="text"
                name="proposer"
                value={proposalData.proposer}
                onChange={handleInputChange}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0x..."
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Analyzing...
                </>
              ) : (
                <>
                  <DocumentTextIcon className="h-4 w-4 mr-2" />
                  Analyze Proposal
                </>
              )}
            </button>
          </div>
        </motion.div>

        {/* Analysis Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          {analysis ? (
            <>
              {/* Prediction */}
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">AI Prediction</h3>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${getPredictionColor(analysis.prediction)} bg-opacity-20`}>
                    {(analysis.prediction * 100).toFixed(0)}% Success
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Confidence</span>
                    <span className="text-white">{(analysis.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Risk Level</span>
                    <span className={`${getRiskColor(analysis.risk_assessment)}`}>
                      {analysis.risk_assessment}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Sentiment</span>
                    <span className={`${analysis.sentiment_score > 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {analysis.sentiment_score > 0 ? 'Positive' : 'Negative'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Summary */}
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-4">AI Summary</h3>
                <p className="text-gray-300 text-sm leading-relaxed">
                  {analysis.summary}
                </p>
              </div>

              {/* Key Points */}
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-4">Key Points</h3>
                <div className="space-y-2">
                  {analysis.key_points?.map((point: string, index: number) => (
                    <div key={index} className="flex items-start">
                      <div className="flex-shrink-0 w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3"></div>
                      <p className="text-sm text-gray-300">{point}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-4">AI Recommendations</h3>
                <div className="space-y-2">
                  {analysis.recommendations?.map((rec: string, index: number) => (
                    <div key={index} className="flex items-start">
                      <CheckCircleIcon className="h-4 w-4 text-green-400 mt-0.5 mr-3 flex-shrink-0" />
                      <p className="text-sm text-gray-300">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="text-center">
                <DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-white mb-2">No Analysis Yet</h3>
                <p className="text-gray-400 text-sm">
                  Fill out the form and click "Analyze Proposal" to get AI-powered insights
                </p>
              </div>
            </div>
          )}
        </motion.div>
      </div>

      {/* Sample Proposals */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-slate-800 rounded-lg p-6 border border-slate-700"
      >
        <h2 className="text-lg font-semibold text-white mb-4">Sample Proposals</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-slate-700 rounded-lg">
            <h4 className="font-medium text-white mb-2">Treasury Diversification</h4>
            <p className="text-sm text-gray-400 mb-3">
              Propose to diversify treasury holdings by allocating 20% to DeFi protocols...
            </p>
            <div className="flex items-center text-xs text-gray-500">
              <ClockIcon className="h-4 w-4 mr-1" />
              Estimated: 75% success
            </div>
          </div>
          
          <div className="p-4 bg-slate-700 rounded-lg">
            <h4 className="font-medium text-white mb-2">Governance Token Distribution</h4>
            <p className="text-sm text-gray-400 mb-3">
              Update token distribution model to incentivize long-term participation...
            </p>
            <div className="flex items-center text-xs text-gray-500">
              <ClockIcon className="h-4 w-4 mr-1" />
              Estimated: 60% success
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ProposalAnalysis; 