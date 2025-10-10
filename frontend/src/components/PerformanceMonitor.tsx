import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { useWebSocket } from '../hooks/useWebSocket';

const PerformanceMonitor: React.FC = () => {
  const { isConnected } = useWebSocket('0x1234567890123456789012345678901234567890');

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: 'primary.main', color: 'white' }}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        <Typography variant="h6" fontWeight={600} color="white">
          System Performance
        </Typography>
        <Box display="flex" alignItems="center" gap={1}>
          <Box
            sx={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              bgcolor: isConnected ? 'success.main' : 'error.main'
            }}
          />
          <Typography variant="body2" color="white">
            {isConnected ? 'Real-time Connected' : 'Disconnected'}
          </Typography>
        </Box>
      </Box>
      <Typography variant="body2" color="white">
        WebSocket Status: {isConnected ? '✅ Active' : '❌ Inactive'}
      </Typography>
    </Paper>
  );
};

export default PerformanceMonitor;