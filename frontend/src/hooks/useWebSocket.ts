import { useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';

interface WebSocketMessage {
  type: string;
  dao_address: string;
  data: any;
  timestamp: number;
}

export const useWebSocket = (daoAddress?: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!daoAddress) return;

    const wsUrl = `ws://localhost:8000/ws/${daoAddress}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      setIsConnected(true);
      toast.success('Real-time updates connected');
    };

    ws.current.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        setLastMessage(message);
        
        // Handle different message types
        if (message.type === 'health_update') {
          toast.success('DAO health updated');
        } else if (message.type === 'proposal_update') {
          toast.info('Proposal status changed');
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      toast.error('Real-time updates disconnected');
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      toast.error('Connection error');
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [daoAddress]);

  const sendMessage = (message: string) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(message);
    }
  };

  return {
    isConnected,
    lastMessage,
    sendMessage
  };
};