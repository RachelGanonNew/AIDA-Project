import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { WalletIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

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
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className={`flex items-center space-x-3 ${className}`}
      >
        <div className="flex items-center space-x-2 bg-green-900/20 border border-green-500/30 rounded-lg px-3 py-2">
          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
          <span className="text-sm text-green-400 font-medium">
            {getShortAddress(address)}
          </span>
        </div>
        <button
          onClick={disconnectWallet}
          className="text-sm text-gray-400 hover:text-white transition-colors"
        >
          Disconnect
        </button>
      </motion.div>
    );
  }

  return (
    <div className={className}>
      <button
        onClick={connectWallet}
        disabled={isConnecting}
        className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white px-4 py-2 rounded-lg transition-colors"
      >
        <WalletIcon className="h-5 w-5" />
        <span>{isConnecting ? 'Connecting...' : 'Connect Wallet'}</span>
      </button>
      
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center space-x-2 mt-2 text-red-400 text-sm"
        >
          <ExclamationTriangleIcon className="h-4 w-4" />
          <span>{error}</span>
        </motion.div>
      )}
      
      {!isConnecting && (
        <p className="text-xs text-gray-500 mt-2">
          Connect your Hathor wallet to interact with AIDA
        </p>
      )}
    </div>
  );
};

export default WalletConnect; 