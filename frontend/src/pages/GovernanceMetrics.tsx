import React, { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid';
import { Box, Typography, Paper, Chip, CircularProgress } from '@mui/material';
import GroupsIcon from '@mui/icons-material/Groups';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import DescriptionIcon from '@mui/icons-material/Description';
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
      <Box display="flex" alignItems="center" justifyContent="center" minHeight={300}>
        <CircularProgress />
      </Box>
    );
  }

  return (
  <div className="layout-main-inner govmetrics-root">

      <Box>
        <Typography variant="h4" fontWeight={700}>Governance Metrics</Typography>
  <Typography color="text.secondary" mt={0}>
          Comprehensive governance analytics and AI-powered predictions
        </Typography>
      </Box>

      {metrics && (
        <>

          <Paper elevation={2} sx={{ px: { xs: 2, sm: 3 }, pt: { xs: 2, sm: 3 }, pb: { xs: 4, sm: 6 }, mb: { xs: 2, sm: 3, md: 4 }, borderRadius: 2, boxShadow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <Grid container spacing={2} alignItems="stretch">
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <DescriptionIcon color="primary" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Total Proposals</Typography>
                  <Typography variant="h6">{metrics.total_proposals}</Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <AccessTimeIcon color="success" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Active Proposals</Typography>
                  <Typography variant="h6">{metrics.active_proposals}</Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <GroupsIcon color="secondary" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Voter Participation</Typography>
                  <Typography variant="h6">{(metrics.average_voter_participation * 100).toFixed(0)}%</Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <TrendingUpIcon color="warning" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Success Rate</Typography>
                  <Typography variant="h6">{(metrics.proposal_success_rate * 100).toFixed(0)}%</Typography>
                </Box>
              </Paper>
            </Grid>
            </Grid>
          </Paper>


          <Paper elevation={2} sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" fontWeight={600} mb={2}>Governance Trends</Typography>
            <Grid container spacing={2}>
              {Object.entries(metrics.governance_trends).map(([key, value]: [string, any]) => (
                <Grid item xs={12} sm={6} md={4} key={key}>
                  <Paper elevation={1} className={`govmetrics-trend-card ${value}`} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2 }}>
                    <Typography variant="subtitle2" fontWeight={600} mb={1} className="govmetrics-trend-title">{key.replace('_', ' ')}</Typography>
                    <Chip label={value} color={value === 'increasing' ? 'success' : value === 'decreasing' ? 'error' : 'primary'} />
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Paper>


          <Paper elevation={2} className="govmetrics-section" sx={{ px: { xs: 2, sm: 3 }, pt: { xs: 2, sm: 3 }, pb: { xs: 7, sm: 9 }, mb: 3, mt: 4, borderRadius: 2 }}>
            <Typography variant="h6" fontWeight={600} mb={2}>Top Voters</Typography>
            <Grid container spacing={2}>
              {metrics.top_voters?.map((voter: any, index: number) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Paper elevation={1} className="govmetrics-voter-card" sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center', border: '1px solid #e0e0e0', borderRadius: 2 }}>
                    <Box display="flex" alignItems="center" width="100%">
                      <Box className="govmetrics-voter-rank" style={{ fontSize: '1.25rem', minWidth: 32, textAlign: 'center', fontWeight: 700 }}>{index + 1}</Box>
                      <Box ml={2} flex={1}>
                        <Typography variant="subtitle1" fontWeight={600}>{voter.address}</Typography>
                        <Typography variant="body2" color="text.secondary">{voter.votes} votes</Typography>
                      </Box>
                      <Typography variant="h6" fontWeight={700} color="primary">{(voter.percentage * 100).toFixed(1)}%</Typography>
                    </Box>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Paper>


          <Paper elevation={2} className="govmetrics-section" sx={{ px: { xs: 2, sm: 4 }, py: { xs: 2, sm: 3 }, mb: 3, borderRadius: 2 }}>
            <Typography variant="h6" fontWeight={600} mb={2}>AI Predictions</Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" fontWeight={600} mb={1}>Next Month Forecast</Typography>
                <Box>
                  <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography color="text.secondary">Voter Participation</Typography>
                    <Typography>{(metrics.predictions.next_month_participation * 100).toFixed(0)}%</Typography>
                  </Box>
                  <Box display="flex" justifyContent="space-between">
                    <Typography color="text.secondary">Success Probability</Typography>
                    <Typography>{(metrics.predictions.proposal_success_probability * 100).toFixed(0)}%</Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" fontWeight={600} mb={1}>Trending Topics</Typography>
                <Box>
                  {metrics.predictions.trending_topics?.map((topic: string, index: number) => (
                    <Box key={index} display="flex" alignItems="center" mb={1}>
                      <Box className="govmetrics-topic-dot" />
                      <Typography variant="body2" color="text.secondary" className="govmetrics-topic-title">{topic.replace('_', ' ')}</Typography>
                    </Box>
                  ))}
                </Box>
              </Grid>
            </Grid>
          </Paper>


          <Paper elevation={2} className="govmetrics-section" sx={{ px: { xs: 2, sm: 4 }, py: { xs: 2, sm: 3 }, mb: 3, borderRadius: 2 }}>
            <Typography variant="h6" fontWeight={600} mb={2}>Voting Performance</Typography>
            <Box height={256}>
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
            </Box>
          </Paper>
        </>
      )}
  </div>
  );
};

export default GovernanceMetrics;