import React, { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid';
import { Box, Typography, Paper, Chip, CircularProgress } from '@mui/material';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import BarChartIcon from '@mui/icons-material/BarChart';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
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
      <Box display="flex" alignItems="center" justifyContent="center" minHeight={300}>
        <CircularProgress />
      </Box>
    );
  }

  return (
  <div className="layout-main-inner treasury-root">

      <Box>
        <Typography variant="h4" fontWeight={700}>Treasury Analysis</Typography>
        <Typography color="text.secondary" mt={1}>
          AI-powered treasury health analysis and optimization recommendations
        </Typography>
      </Box>

      {treasuryData && (
        <>

          <Paper elevation={2} sx={{ px: { xs: 2, sm: 3 }, pt: { xs: 2, sm: 3 }, pb: { xs: 4, sm: 6 }, mb: { xs: 2, sm: 3, md: 4 }, borderRadius: 2, boxShadow: 1 }}>
            <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <AccountBalanceIcon color="primary" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Total Value</Typography>
                  <Typography variant="h6">${treasuryData.total_value_usd?.toLocaleString()}</Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <BarChartIcon color="success" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Diversification</Typography>
                  <Typography variant="h6">{(treasuryData.asset_diversification_score * 100).toFixed(0)}%</Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <WarningAmberIcon color="warning" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Risk Score</Typography>
                  <Typography variant="h6">{(treasuryData.risk_score * 100).toFixed(0)}%</Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={1} sx={{ p: 2, height: '100%', display: 'flex', alignItems: 'center' }}>
                <TrendingUpIcon color="secondary" />
                <Box ml={2}>
                  <Typography variant="body2" color="text.secondary">Liquidity</Typography>
                  <Typography variant="h6">{(treasuryData.liquidity_score * 100).toFixed(0)}%</Typography>
                </Box>
              </Paper>
            </Grid>
            </Grid>
          </Paper>


          <Paper elevation={2} className="treasury-section" sx={{ mt: { xs: 6, sm: 8 }, px: { xs: 2, sm: 4 }, py: { xs: 2, sm: 3 }, borderRadius: 2 }}>
            <Typography variant="h6" fontWeight={600} mb={2}>Asset Allocation</Typography>
            <Box height={256}>
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
            </Box>
          </Paper>


          <Grid container spacing={2} mt={3}>
            <Grid item xs={12} md={6}>
              <Paper elevation={1} className="treasury-risk-card" sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2 }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <WarningAmberIcon color="warning" className="treasury-risk-icon" />
                  <Typography variant="subtitle1" fontWeight={600}>Risk Factors</Typography>
                </Box>
                <Box>
                  {treasuryData.risk_factors?.map((risk: string, index: number) => (
                    <Box key={index} display="flex" alignItems="center" mb={1}>
                      <Box className="treasury-risk-dot" />
                      <Typography variant="body2" color="text.secondary">{risk}</Typography>
                    </Box>
                  ))}
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper elevation={1} className="treasury-recommend-card" sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2 }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <CheckCircleIcon color="success" className="treasury-recommend-icon" />
                  <Typography variant="subtitle1" fontWeight={600}>AI Recommendations</Typography>
                </Box>
                <Box>
                  {treasuryData.recommendations?.map((rec: string, index: number) => (
                    <Box key={index} display="flex" alignItems="center" mb={1}>
                      <CheckCircleIcon color="success" fontSize="small" className="treasury-recommend-dot" />
                      <Typography variant="body2" color="text.secondary">{rec}</Typography>
                    </Box>
                  ))}
                </Box>
              </Paper>
            </Grid>
          </Grid>


          {treasuryData.rebalancing_suggestions && (
            <Paper elevation={2} className="treasury-section" sx={{ mt: { xs: 3, sm: 4 }, px: { xs: 2, sm: 4 }, py: { xs: 2, sm: 3 }, borderRadius: 2 }}>
              <Typography variant="h6" fontWeight={600} mb={2}>Rebalancing Suggestions</Typography>
              <Grid container spacing={2}>
                {treasuryData.rebalancing_suggestions.map((suggestion: any, index: number) => (
                  <Grid item xs={12} key={index}>
                    <Paper elevation={1} className="treasury-rebalance-card" sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2 }}>
                      <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
                        <Typography variant="subtitle2" fontWeight={600}>{suggestion.action}</Typography>
                        <Chip label={suggestion.priority} color={suggestion.priority === 'high' ? 'error' : suggestion.priority === 'medium' ? 'warning' : 'primary'} />
                      </Box>
                      <Typography variant="body2" color="text.secondary" mb={1}>{suggestion.description}</Typography>
                      <Typography variant="caption" color="text.secondary">Impact: {suggestion.estimated_impact}</Typography>
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          )}
        </>
      )}
  </div>
  );
};

export default TreasuryAnalysis;