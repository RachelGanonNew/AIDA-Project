import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

interface LoadingSpinnerProps {
  size?: number;
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 32, text }) => (
  <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" role="status" aria-live="polite" tabIndex={0}>
    <CircularProgress size={size} color="primary" />
    {text && (
      <Typography variant="body2" color="text.secondary" mt={2} aria-label={text}>
        {text}
      </Typography>
    )}
  </Box>
);

export default LoadingSpinner;