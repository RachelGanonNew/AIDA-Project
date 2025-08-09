import React, { useState, useEffect } from 'react';
import { Box, Button, Chip, Typography, Alert, CircularProgress } from '@mui/material';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

interface WalletConnectProps {
  onConnect?: (address: string) => void;
  onDisconnect?: () => void;
  className?: string;
}

const WalletConnect: React.FC<WalletConnectProps> = ({ 
  onConnect, 
  onDisconnect, 
  className = '' 
}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [address, setAddress] = useState<string>('');
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    // Check if wallet is already connected
    const savedAddress = localStorage.getItem('hathor_wallet_address');
    if (savedAddress) {
      setAddress(savedAddress);
      setIsConnected(true);
      onConnect?.(savedAddress);
    }
  }, [onConnect]);

  const connectWallet = async () => {
    setIsConnecting(true);
    setError('');

    try {
      // Check if Hathor wallet is available
      if (typeof window !== 'undefined' && (window as any).hathor) {
        const hathor = (window as any).hathor;
        // Request account access
        const accounts = await hathor.request({ method: 'eth_requestAccounts' });
        if (accounts && accounts.length > 0) {
          const walletAddress = accounts[0];
          setAddress(walletAddress);
          setIsConnected(true);
          localStorage.setItem('hathor_wallet_address', walletAddress);
          onConnect?.(walletAddress);
        }
      } else {
        // Mock connection for demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
        const mockAddress = '0x' + Math.random().toString(16).substr(2, 40);
        setAddress(mockAddress);
        setIsConnected(true);
        localStorage.setItem('hathor_wallet_address', mockAddress);
        onConnect?.(mockAddress);
      }
    } catch (err) {
      console.error('Error connecting wallet:', err);
      setError('Failed to connect wallet. Please try again.');
    } finally {
      setIsConnecting(false);
    }
  };

  const disconnectWallet = () => {
    setAddress('');
    setIsConnected(false);
    localStorage.removeItem('hathor_wallet_address');
    onDisconnect?.();
  };

  const getShortAddress = (addr: string) => {
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
  };

  if (isConnected) {
    return (
      <Box display="flex" alignItems="center" gap={2} className={className}>
        <Chip
          icon={<AccountBalanceWalletIcon color="success" />}
          label={getShortAddress(address)}
          color="success"
          variant="outlined"
        />
        <Button onClick={disconnectWallet} size="small" color="inherit" variant="text">
          Disconnect
        </Button>
      </Box>
    );
  }

  return (
    <Box className={className}>
      <Button
        onClick={connectWallet}
        disabled={isConnecting}
        startIcon={isConnecting ? <CircularProgress size={18} /> : <AccountBalanceWalletIcon />}
        variant="contained"
        color="primary"
  className="walletconnect-btn"
      >
        {isConnecting ? 'Connecting...' : 'Connect Wallet'}
      </Button>
      {error && (
  <Alert severity="error" icon={<ErrorOutlineIcon />} className="walletconnect-alert">
          {error}
        </Alert>
      )}
      {!isConnecting && (
        <Typography variant="caption" color="text.secondary" mt={2}>
          Connect your Hathor wallet to interact with AIDA
        </Typography>
      )}
    </Box>
  );
};

export default WalletConnect;