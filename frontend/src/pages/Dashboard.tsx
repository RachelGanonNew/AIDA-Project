

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import { Box, Typography, Button, Paper, Chip, Dialog, DialogTitle, DialogContent, DialogActions, Switch } from '@mui/material';
import BarChartIcon from '@mui/icons-material/BarChart';
import DescriptionIcon from '@mui/icons-material/Description';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import GroupsIcon from '@mui/icons-material/Groups';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import toast from 'react-hot-toast';
import { apiService } from '../services/apiService';
import HealthCard from '../components/HealthCard';
import LoadingSpinner from '../components/LoadingSpinner';

const DEMO_DAO_HEALTH = {
  overall_health_score: 0.82,
  governance_score: 0.78,
  financial_score: 0.85,
  community_score: 0.76,
  risk_factors: [
    'Low voter turnout in last proposal',
    'Treasury allocation imbalance',
    'High proposal rejection rate',
  ],
  recommendations: [
    'Encourage more community participation',
    'Rebalance treasury assets',
    'Simplify proposal process',
  ],
};

const Dashboard = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [demoMode, setDemoMode] = useState(false);

  useEffect(() => {
    loadDashboardData();
    // Show onboarding dialog on first load
    setShowOnboarding(true);
    // eslint-disable-next-line
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // Simulate API call
      const treasuryOverview = { total_value_usd: 1234567 };
      const governanceMetrics = {
        active_proposals: 4,
        average_voter_participation: 0.62,
        proposal_success_rate: 0.81,
      };
      setData({
        daoHealth: DEMO_DAO_HEALTH,
        treasuryOverview,
        governanceMetrics,
      });
    } catch (error) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 0.7) return 'success';
    if (score >= 0.5) return 'warning';
    return 'error';
  };

  const getHealthStatus = (score: number) => {
    if (score >= 0.7) return 'Excellent';
    if (score >= 0.5) return 'Good';
    return 'Needs Attention';
  };

  const daoHealth = demoMode ? DEMO_DAO_HEALTH : data?.daoHealth;

  if (loading) {
    return (
      <Box display="flex" alignItems="center" justifyContent="center" minHeight={300}>
        <LoadingSpinner size={48} text="Loading dashboard data..." />
      </Box>
    );
  }

  return (
    <div className="layout-main-inner dashboard-root">
      <Box className="dashboard-header">
        <Typography variant="h4" fontWeight={700}>Dashboard</Typography>
        <Typography color="text.secondary" mt={1}>Overview of your DAO's health, governance, and treasury metrics</Typography>
      </Box>

      <Dialog open={showOnboarding} onClose={() => setShowOnboarding(false)}>
        <DialogTitle>Welcome to AIDA!</DialogTitle>
        <DialogContent>
          <Typography gutterBottom>
            This is a live demo of the AI-Driven DAO Analyst. Explore the dashboard, analyze proposals, and see AI-powered insights in action.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowOnboarding(false)} variant="contained">Get Started</Button>
        </DialogActions>
      </Dialog>

      <Box display="flex" justifyContent="flex-end">
        <Box display="flex" alignItems="center" bgcolor="background.paper" px={2} py={1} borderRadius={2} border={1} borderColor="divider">
          <Switch checked={demoMode} onChange={() => setDemoMode((v) => !v)} color="primary" />
          <Typography variant="body2" color="text.secondary">Demo Mode</Typography>
        </Box>
      </Box>

      <Box display="flex" alignItems={{ xs: 'flex-start', sm: 'center' }} justifyContent="space-between" flexDirection={{ xs: 'column', sm: 'row' }}>
        <Box>
          <Typography variant="h5" fontWeight={700}>Dashboard</Typography>
          <Typography color="text.secondary" mt={1}>
            AI-powered insights for DAO governance and treasury management
          </Typography>
        </Box>
        <Box mt={{ xs: 2, sm: 0 }}>
          <Button onClick={loadDashboardData} variant="contained" color="primary">Refresh Data</Button>
        </Box>
      </Box>

      {daoHealth && (
        <Paper elevation={2} sx={{ p: 3, border: '1px solid #e0e0e0', borderRadius: 2, mb: 4 }}>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Typography variant="h6" fontWeight={600}>DAO Health Overview</Typography>
            <Chip label={getHealthStatus(daoHealth.overall_health_score)} color={getHealthColor(daoHealth.overall_health_score)} />
          </Box>
          <Grid container spacing={2} justifyContent="center">
            <Grid item xs={12} sm={6} md={3}>
              <HealthCard
                title="Overall Health"
                value={`${(daoHealth.overall_health_score * 100).toFixed(0)}%`}
                subtitle={getHealthStatus(daoHealth.overall_health_score)}
                icon={<BarChartIcon color="primary" />}
                color="primary"
                trend={{
                  direction: daoHealth.overall_health_score > 0.7 ? 'up' : 'stable',
                  value: '+5%'
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <HealthCard
                title="Governance"
                value={`${(daoHealth.governance_score * 100).toFixed(0)}%`}
                icon={<DescriptionIcon color="success" />}
                color="success"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <HealthCard
                title="Financial"
                value={`${(daoHealth.financial_score * 100).toFixed(0)}%`}
                icon={<AccountBalanceIcon color="warning" />}
                color="warning"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <HealthCard
                title="Community"
                value={`${(daoHealth.community_score * 100).toFixed(0)}%`}
                icon={<GroupsIcon color="secondary" />}
                color="secondary"
              />
            </Grid>
          </Grid>
        </Paper>
      )}

      <Paper elevation={2} sx={{ p: 3, border: '1px solid #e0e0e0', borderRadius: 2, mb: 4 }}>
        <Typography variant="h6" fontWeight={600} mb={2} align="center">Key Metrics</Typography>
        <Grid container spacing={2} justifyContent="center">
          <Grid item xs={12} sm={6} md={3}>
            <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', boxShadow: 'none' }}>
              <AccountBalanceIcon color="primary" fontSize="large" />
              <Typography variant="body2" color="text.secondary" mt={1}>Treasury Value</Typography>
              <Typography variant="h6">${data?.treasuryOverview?.total_value_usd?.toLocaleString() || '0'}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', boxShadow: 'none' }}>
              <DescriptionIcon color="success" fontSize="large" />
              <Typography variant="body2" color="text.secondary" mt={1}>Active Proposals</Typography>
              <Typography variant="h6">{data?.governanceMetrics?.active_proposals || 0}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', boxShadow: 'none' }}>
              <GroupsIcon color="secondary" fontSize="large" />
              <Typography variant="body2" color="text.secondary" mt={1}>Voter Participation</Typography>
              <Typography variant="h6">{((data?.governanceMetrics?.average_voter_participation || 0) * 100).toFixed(0)}%</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', boxShadow: 'none' }}>
              <TrendingUpIcon color="warning" fontSize="large" />
              <Typography variant="body2" color="text.secondary" mt={1}>Success Rate</Typography>
              <Typography variant="h6">{((data?.governanceMetrics?.proposal_success_rate || 0) * 100).toFixed(0)}%</Typography>
            </Paper>
          </Grid>
        </Grid>
      </Paper>

      {daoHealth && (
        <Paper elevation={2} sx={{ p: 3, border: '1px solid #e0e0e0', borderRadius: 2, mb: 4 }}>
          <Typography variant="h6" fontWeight={600} mb={2} align="center">Risk Assessment & Recommendations</Typography>
          <Grid container spacing={2} justifyContent="center">
            <Grid item xs={12} md={6}>
              <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', boxShadow: 'none' }}>
                <Box display="flex" alignItems="center" mb={2} justifyContent="center">
                  <WarningAmberIcon color="warning" sx={{ mr: 1 }} />
                  <Typography variant="subtitle1" fontWeight={600}>Risk Factors</Typography>
                </Box>
                <Box>
                  {daoHealth.risk_factors?.slice(0, 3).map((risk: string, index: number) => (
                    <Box key={index} display="flex" alignItems="center" mb={1} justifyContent="center">
                      <Box sx={{ width: 8, height: 8, bgcolor: 'warning.main', borderRadius: '50%', mr: 1 }} />
                      <Typography variant="body2" color="text.secondary">{risk}</Typography>
                    </Box>
                  ))}
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', boxShadow: 'none' }}>
                <Box display="flex" alignItems="center" mb={2} justifyContent="center">
                  <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                  <Typography variant="subtitle1" fontWeight={600}>AI Recommendations</Typography>
                </Box>
                <Box>
                  {daoHealth.recommendations?.slice(0, 3).map((rec: string, index: number) => (
                    <Box key={index} display="flex" alignItems="center" mb={1} justifyContent="center">
                      <CheckCircleIcon color="success" fontSize="small" sx={{ mr: 1 }} />
                      <Typography variant="body2" color="text.secondary">{rec}</Typography>
                    </Box>
                  ))}
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Paper>
      )}

      <Paper elevation={2} sx={{ p: 3, border: '1px solid #e0e0e0', borderRadius: 2, mt: 4 }}>
        <Typography variant="h6" fontWeight={600} mb={2} align="center">Quick Actions</Typography>
        <Grid container spacing={2} justifyContent="center">
          <Grid item xs={12} sm={4}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<DescriptionIcon />}
              onClick={() => navigate('/proposals')}
              sx={{ py: 2, borderRadius: 2, fontWeight: 600 }}
            >
              Analyze New Proposal
            </Button>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<AccountBalanceIcon />}
              onClick={() => navigate('/treasury')}
              sx={{ py: 2, borderRadius: 2, fontWeight: 600 }}
            >
              Rebalance Treasury
            </Button>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<BarChartIcon />}
              onClick={() => navigate('/governance')}
              sx={{ py: 2, borderRadius: 2, fontWeight: 600 }}
            >
              View Analytics
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </div>
  );
};

export default Dashboard;