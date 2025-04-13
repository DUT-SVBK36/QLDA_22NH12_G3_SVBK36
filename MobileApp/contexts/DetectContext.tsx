import React, { createContext, useContext, useEffect, useState, ReactNode, useRef } from 'react';
import { initSocket, disconnectSocket, on, off, emit } from '@/services/detect/detectSocket';
import setupEventListeners from '@/services/detect/detectEvent';
import { AuthService } from '@/services/auth';

interface WebSocketWrapper {
  on: (event: string, callback: Function) => void;
  off: (event: string, callback?: Function) => void;
  emit: (data?: any) => void;
  connect: (client_id: string, token: string) => void;
  disconnect: () => void;
}

interface SocketContextType {
  socket: WebSocketWrapper | null;
  isConnected: boolean;
  connect: (client_id: string, token: string) => void;
  disconnect: () => void;
  emit: (data?: any) => void;
}

const SocketContext = createContext<SocketContextType | null>(null);

interface SocketProviderProps {
  children: ReactNode;
}

export const SocketProvider: React.FC<SocketProviderProps> = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [socket, setSocket] = useState<WebSocketWrapper | null>(null);

  const connect = (client_id: string, token: string) => {
    try {
      initSocket(client_id, token);
      // Socket connection status is handled by event listeners
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
    }
  };

  const disconnect = () => {
    disconnectSocket();
  };

  useEffect(() => {
    // Create the socket wrapper with our custom API
    const socketWrapper: WebSocketWrapper = {
      on,
      off,
      emit,
      connect,
      disconnect,
    };
    
    setSocket(socketWrapper);
    
    // Set up event handlers
    setupEventListeners();

    // Set up connection status handlers
    const handleConnect = () => setIsConnected(true);
    const handleDisconnect = () => setIsConnected(false);
    
    on('connect', handleConnect);
    on('disconnect', handleDisconnect);
    
    // Initial connection attempt
    
    return () => {
      off('connect', handleConnect);
      off('disconnect', handleDisconnect);
      disconnect();
    };
  }, []);

  return (
    <SocketContext.Provider 
      value={{ 
        socket, 
        isConnected, 
        connect,
        disconnect,
        emit,
      }}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocket = (): SocketContextType => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider');
  }
  return context;
};