import React from 'react';
import { motion } from 'framer-motion';
import { DocumentTextIcon, ClockIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

interface ProposalCardProps {
  proposal: {
    id: string;
    title: string;
    description: string;
    status: 'active' | 'passed' | 'failed' | 'executed';
    prediction?: number;
    risk_level?: 'low' | 'medium' | 'high';
    proposer: string;
    voting_start?: string;
    voting_end?: string;
  };
  onClick?: () => void;
}

const ProposalCard: React.FC<ProposalCardProps> = ({ proposal, onClick }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-blue-400';
      case 'passed': return 'text-green-400';
      case 'failed': return 'text-red-400';
      case 'executed': return 'text-purple-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <ClockIcon className="h-5 w-5" />;
      case 'passed': return <CheckCircleIcon className="h-5 w-5" />;
      case 'failed': return <XCircleIcon className="h-5 w-5" />;
      case 'executed': return <CheckCircleIcon className="h-5 w-5" />;
      default: return <DocumentTextIcon className="h-5 w-5" />;
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
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
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-slate-800 rounded-lg p-6 border border-slate-700 ${onClick ? 'cursor-pointer hover:bg-slate-750 transition-colors' : ''}`}
      onClick={onClick}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <DocumentTextIcon className="h-6 w-6 text-blue-400 mr-3" />
          <div>
            <h3 className="text-lg font-semibold text-white">{proposal.title}</h3>
            <p className="text-sm text-gray-400">Proposed by {proposal.proposer.slice(0, 8)}...{proposal.proposer.slice(-6)}</p>
          </div>
        </div>
        <div className={`flex items-center ${getStatusColor(proposal.status)}`}>
          {getStatusIcon(proposal.status)}
          <span className="ml-2 text-sm font-medium capitalize">{proposal.status}</span>
        </div>
      </div>

      <p className="text-gray-300 text-sm mb-4 line-clamp-3">
        {proposal.description}
      </p>

      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {proposal.prediction !== undefined && (
            <div className="flex items-center">
              <span className="text-sm text-gray-400 mr-2">Prediction:</span>
              <span className={`text-sm font-medium ${getPredictionColor(proposal.prediction)}`}>
                {(proposal.prediction * 100).toFixed(0)}%
              </span>
            </div>
          )}
          {proposal.risk_level && (
            <div className="flex items-center">
              <span className="text-sm text-gray-400 mr-2">Risk:</span>
              <span className={`text-sm font-medium ${getRiskColor(proposal.risk_level)}`}>
                {proposal.risk_level.toUpperCase()}
              </span>
            </div>
          )}
        </div>

        {proposal.voting_end && (
          <div className="text-sm text-gray-400">
            Ends: {new Date(proposal.voting_end).toLocaleDateString()}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ProposalCard; 