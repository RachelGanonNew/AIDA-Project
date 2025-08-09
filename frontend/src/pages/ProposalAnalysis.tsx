import React, { useState } from 'react';
import Grid from '@mui/material/Grid';
import { Box, Typography, Button, TextField, Paper, CircularProgress, Chip } from '@mui/material';
import DescriptionIcon from '@mui/icons-material/Description';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import toast from 'react-hot-toast';
import { apiService } from '../services/apiService';

// Helper functions for MUI color
const getPredictionColor = (prediction: number) => {
  if (prediction >= 0.7) return 'success';
  if (prediction >= 0.5) return 'warning';
  return 'error';
};

const getRiskColor = (risk: string) => {
  switch (risk.toLowerCase()) {
    case 'low': return 'success';
    case 'medium': return 'warning';
    case 'high': return 'error';
    default: return 'default';
  }
};

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
    // ...existing code...
  };

  return (
    <Box className="propanalysis-root">
      <Box>
        <Typography variant="h4" fontWeight={700}>Proposal Analysis</Typography>
        <Typography color="text.secondary" mt={1}>
          AI-powered analysis of governance proposals with predictions and recommendations
        </Typography>
      </Box>
      <Grid container spacing={4}>
  <Grid item xs={12} lg={6}>
    <Paper elevation={2} className="propanalysis-section" style={{ maxWidth: 520, margin: '0 auto', border: '1px solid #e0e0e0', borderRadius: 2, padding: '2rem', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <Typography variant="h6" fontWeight={600} mb={2} align="center">Analyze New Proposal</Typography>
            <Box component="form" className="propanalysis-form" style={{ width: '100%', maxWidth: 520 }}>
              <Box my={2}>
                <TextField
                  label="Proposal Title"
                  name="title"
                  value={proposalData.title}
                  onChange={handleInputChange}
                  fullWidth
                  required
                />
              </Box>
              <Box my={2}>
                <TextField
                  label="Proposal Description"
                  name="description"
                  value={proposalData.description}
                  onChange={handleInputChange}
                  fullWidth
                  required
                  multiline
                  minRows={4}
                />
              </Box>
              <Box my={2}>
                <TextField
                  label="Proposer Address"
                  name="proposer"
                  value={proposalData.proposer}
                  onChange={handleInputChange}
                  fullWidth
                />
              </Box>
              <Button
                onClick={handleAnalyze}
                disabled={loading}
                variant="contained"
                color="primary"
                fullWidth
                startIcon={loading ? <CircularProgress size={18} /> : <DescriptionIcon />}
              >
                {loading ? 'Analyzing...' : 'Analyze Proposal'}
              </Button>
            </Box>
          </Paper>
        </Grid>
  <Grid item xs={12} lg={6}>
          {analysis ? (
            <Box className="propanalysis-results">
              <Paper elevation={2} className="propanalysis-section" style={{ border: '1px solid #e0e0e0', borderRadius: 2, padding: '2rem' }}>
                <Box className="propanalysis-prediction-header">
                  <Typography variant="h6" fontWeight={600}>AI Prediction</Typography>
                  <Chip label={`${(analysis.prediction * 100).toFixed(0)}% Success`} color={getPredictionColor(analysis.prediction)} />
                </Box>
                <Box className="propanalysis-prediction-list">
                  <Box display="flex" justifyContent="space-between">
                    <Typography color="text.secondary">Confidence</Typography>
                    <Typography>{(analysis.confidence * 100).toFixed(0)}%</Typography>
                  </Box>
                  <Box display="flex" justifyContent="space-between">
                    <Typography color="text.secondary">Risk Level</Typography>
                    <Chip label={analysis.risk_assessment} color={getRiskColor(analysis.risk_assessment)} size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between">
                    <Typography color="text.secondary">Sentiment</Typography>
                    <Chip label={analysis.sentiment_score > 0 ? 'Positive' : 'Negative'} color={analysis.sentiment_score > 0 ? 'success' : 'error'} size="small" />
                  </Box>
                </Box>
              </Paper>
              <Paper elevation={2} className="propanalysis-section" style={{ border: '1px solid #e0e0e0', borderRadius: 2, padding: '2rem' }}>
                <Typography variant="h6" fontWeight={600} mb={2}>AI Summary</Typography>
                <Typography color="text.secondary">{analysis.summary}</Typography>
              </Paper>
              <Paper elevation={2} className="propanalysis-section" style={{ border: '1px solid #e0e0e0', borderRadius: 2, padding: '2rem' }}>
                <Typography variant="h6" fontWeight={600} mb={2}>Key Points</Typography>
                <Box className="propanalysis-keypoints-list">
                  {analysis.key_points?.map((point: string, index: number) => (
                    <Box key={index} display="flex" alignItems="center" gap={1}>
                      <Box className="propanalysis-keypoint-dot" />
                      <Typography variant="body2" color="text.secondary">{point}</Typography>
                    </Box>
                  ))}
                </Box>
              </Paper>
              <Paper elevation={2} className="propanalysis-section" style={{ border: '1px solid #e0e0e0', borderRadius: 2, padding: '2rem' }}>
                <Typography variant="h6" fontWeight={600} mb={2}>AI Recommendations</Typography>
                <Box className="propanalysis-recommend-list">
                  {analysis.recommendations?.map((rec: string, index: number) => (
                    <Box key={index} display="flex" alignItems="center" gap={1}>
                      <CheckCircleIcon color="success" fontSize="small" className="propanalysis-recommend-dot" />
                      <Typography variant="body2" color="text.secondary">{rec}</Typography>
                    </Box>
                  ))}
                </Box>
              </Paper>
            </Box>
          ) : (
            <Paper elevation={2} className="propanalysis-section propanalysis-empty" style={{ border: '1px solid #e0e0e0', borderRadius: 2, padding: '2rem' }}>
              <DescriptionIcon color="disabled" className="propanalysis-empty-icon" />
              <Typography variant="h6" fontWeight={600} mb={1}>No Analysis Yet</Typography>
              <Typography color="text.secondary">Fill out the form and click "Analyze Proposal" to get AI-powered insights</Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
  <Paper elevation={2} className="propanalysis-section propanalysis-samples" style={{ maxWidth: 1170, width: '100%', marginTop: '3rem', border: '1px solid #e0e0e0', borderRadius: 2, padding: '2rem 2rem 1.5rem 2rem', marginLeft: 'auto', marginRight: 'auto' }}>
        <Typography variant="h6" fontWeight={600} mb={2}>Sample Proposals</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Paper elevation={1} style={{ padding: '1.25rem', border: '1px solid #e0e0e0', borderRadius: 2, boxShadow: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <Typography variant="subtitle1" fontWeight={700}>Treasury Diversification</Typography>
              <Typography color="text.secondary">
                Propose to diversify treasury holdings by allocating 20% to DeFi protocols...
              </Typography>
              <Box display="flex" alignItems="center" gap={1}>
                <AccessTimeIcon fontSize="small" />
                <Typography variant="body2">Estimated: 75% success</Typography>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Paper elevation={1} style={{ padding: '1.25rem', border: '1px solid #e0e0e0', borderRadius: 2, boxShadow: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <Typography variant="subtitle1" fontWeight={700}>Governance Token Distribution</Typography>
              <Typography color="text.secondary">
                Update token distribution model to incentivize long-term participation...
              </Typography>
              <Box display="flex" alignItems="center" gap={1}>
                <AccessTimeIcon fontSize="small" />
                <Typography variant="body2">Estimated: 60% success</Typography>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}

export default ProposalAnalysis; 