import React from 'react';
import { Card, CardContent, Box, Typography, Chip, useTheme } from '@mui/material';
import DescriptionIcon from '@mui/icons-material/Description';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';

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
  const theme = useTheme();
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'primary';
      case 'passed': return 'success';
      case 'failed': return 'error';
      case 'executed': return 'secondary';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <AccessTimeIcon color="primary" fontSize="small" />;
      case 'passed': return <CheckCircleIcon color="success" fontSize="small" />;
      case 'failed': return <CancelIcon color="error" fontSize="small" />;
      case 'executed': return <CheckCircleIcon color="secondary" fontSize="small" />;
      default: return <DescriptionIcon color="action" fontSize="small" />;
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'default';
    }
  };

  const getPredictionColor = (prediction: number) => {
    if (prediction >= 0.7) return 'success';
    if (prediction >= 0.5) return 'warning';
    return 'error';
  };

  return (
    <Card
      variant="outlined"
      className={`proposalcard-root${onClick ? ' proposalcard-clickable' : ''}`}
      onClick={onClick}
    >
      <CardContent>
        <Box display="flex" alignItems="flex-start" justifyContent="space-between" mb={2}>
          <Box display="flex" alignItems="center">
            <DescriptionIcon color="primary" sx={{ mr: 1 }} />
            <Box>
              <Typography variant="subtitle1" fontWeight={700}>{proposal.title}</Typography>
              <Typography variant="caption" color="text.secondary">
                Proposed by {proposal.proposer.slice(0, 8)}...{proposal.proposer.slice(-6)}
              </Typography>
            </Box>
          </Box>
          <Chip
            icon={getStatusIcon(proposal.status)}
            label={proposal.status}
            color={getStatusColor(proposal.status) as any}
            size="small"
            className="proposalcard-status"
          />
        </Box>

        <Typography variant="body2" color="text.secondary" mb={2} className="proposalcard-desc">
          {proposal.description}
        </Typography>

        <Box display="flex" alignItems="center" justifyContent="space-between" mt={2}>
          <Box display="flex" alignItems="center" gap={2}>
            {proposal.prediction !== undefined && (
              <Chip
                label={`Prediction: ${(proposal.prediction * 100).toFixed(0)}%`}
                color={getPredictionColor(proposal.prediction) as any}
                size="small"
              />
            )}
            {proposal.risk_level && (
              <Chip
                label={`Risk: ${proposal.risk_level.toUpperCase()}`}
                color={getRiskColor(proposal.risk_level) as any}
                size="small"
              />
            )}
          </Box>
          {proposal.voting_end && (
            <Typography variant="caption" color="text.secondary">
              Ends: {new Date(proposal.voting_end).toLocaleDateString()}
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ProposalCard;