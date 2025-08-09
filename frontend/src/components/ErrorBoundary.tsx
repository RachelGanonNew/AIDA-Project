
import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // You can log error info to an error reporting service here
    // console.error('ErrorBoundary caught an error', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="100vh" bgcolor="background.default" color="text.primary">
          <Typography variant="h5" fontWeight={700} mb={2}>Something went wrong.</Typography>
          <Typography variant="body1" mb={2}>An unexpected error occurred. Please refresh the page or try again later.</Typography>
    <Box component={Paper} elevation={2} className="errorboundary-box">
            <Typography variant="body2" fontFamily="monospace">
              {this.state.error?.message}
            </Typography>
          </Box>
        </Box>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;