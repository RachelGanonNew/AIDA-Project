import React, { useState } from 'react';
import { Box, Typography, Paper, Grid, Button } from '@mui/material';
import toast from 'react-hot-toast';
import { getCrossChainAssets, getHathorContractStatus, estimateHathorGas } from '../services/apiService';

const HathorShowcase: React.FC = () => {
  const [daoAddress, setDaoAddress] = useState<string>('0xDAO000000000000000000000000000000000001');
  const [contractAddress, setContractAddress] = useState<string>('0x1234567890123456789012345678901234567890');
  const [hathorStatus, setHathorStatus] = useState<any>(null);
  const [gasEstimate, setGasEstimate] = useState<any>(null);
  const [crossChain, setCrossChain] = useState<any>(null);

  const handleFetchContractStatus = async () => {
    try {
      const data = await getHathorContractStatus(contractAddress);
      setHathorStatus(data);
      toast.success('Fetched Nano Contract status');
    } catch (e) {
      toast.error('Failed to fetch contract status');
    }
  };

  const handleEstimateGas = async () => {
    try {
      const payload = {
        action_type: 'proposal_execution',
        dao_address: daoAddress,
        proposal_id: 'demo-prop-001',
        parameters: { complexity: 1.0 },
      };
      const data = await estimateHathorGas(payload);
      setGasEstimate(data);
      toast.success('Estimated gas');
    } catch (e) {
      toast.error('Failed to estimate gas');
    }
  };

  const handleFetchCrossChain = async () => {
    try {
      const data = await getCrossChainAssets(daoAddress);
      setCrossChain(data);
      toast.success('Fetched cross-chain assets');
    } catch (e) {
      toast.error('Failed to fetch cross-chain assets');
    }
  };

  return (
    <div className="layout-main-inner">
      <Box className="dashboard-header">
        <Typography variant="h4" fontWeight={700}>Hathor Showcase</Typography>
        <Typography color="text.secondary" mt={1}>Live demo of Hathor Nano Contracts and EVM Bridge integrations</Typography>
      </Box>

      <Paper elevation={2} sx={{ p: 3, border: '1px solid #e0e0e0', borderRadius: 2, mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, boxShadow: 'none' }}>
              <Typography variant="subtitle1" fontWeight={600}>Nano Contract Status</Typography>
              <Box display="flex" gap={1} mt={1}>
                <input style={{ flex: 1 }} value={contractAddress} onChange={(e)=>setContractAddress(e.target.value)} placeholder="Contract Address" />
                <Button variant="contained" onClick={handleFetchContractStatus}>Fetch</Button>
              </Box>
              {hathorStatus && (
                <Box mt={2}>
                  <Typography variant="body2">Status: {hathorStatus.status}</Typography>
                  {typeof hathorStatus.success_rate === 'number' && (
                    <Typography variant="body2">Success Rate: {(hathorStatus.success_rate*100).toFixed(1)}%</Typography>
                  )}
                  {typeof hathorStatus.total_transactions === 'number' && (
                    <Typography variant="body2">Total Tx: {hathorStatus.total_transactions}</Typography>
                  )}
                </Box>
              )}
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, boxShadow: 'none' }}>
              <Typography variant="subtitle1" fontWeight={600}>Estimate Gas</Typography>
              <Box display="flex" gap={1} mt={1}>
                <input style={{ flex: 1 }} value={daoAddress} onChange={(e)=>setDaoAddress(e.target.value)} placeholder="DAO Address" />
                <Button variant="contained" onClick={handleEstimateGas}>Estimate</Button>
              </Box>
              {gasEstimate && (
                <Box mt={2}>
                  <Typography variant="body2">Estimated Gas: {gasEstimate.estimated_gas}</Typography>
                </Box>
              )}
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper elevation={1} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, boxShadow: 'none' }}>
              <Typography variant="subtitle1" fontWeight={600}>Cross-Chain Assets via Hathor EVM Bridge</Typography>
              <Box display="flex" gap={1} mt={1}>
                <input style={{ flex: 1 }} value={daoAddress} onChange={(e)=>setDaoAddress(e.target.value)} placeholder="DAO Address" />
                <Button variant="contained" onClick={handleFetchCrossChain}>Fetch</Button>
              </Box>
              {crossChain && (
                <Box mt={2}>
                  <Typography variant="body2">Total Value: ${crossChain.total_cross_chain_value?.toLocaleString?.() ?? crossChain.total_cross_chain_value}</Typography>
                  <Typography variant="body2">Risk Level: {crossChain.risk_assessment?.risk_level}</Typography>
                  <Box mt={1}>
                    <Typography variant="body2" fontWeight={600}>Recommendations:</Typography>
                    {(crossChain.recommendations||[]).slice(0,3).map((r: string, i: number)=>(
                      <Typography key={i} variant="body2">• {r}</Typography>
                    ))}
                  </Box>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>
      </Paper>
    </div>
  );
};

export default HathorShowcase;
