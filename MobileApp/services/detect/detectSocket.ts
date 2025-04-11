import config from "@/constants/config";

let socket: WebSocket | null = null;
let eventHandlers: Map<string, Set<Function>> = new Map();

export const initSocket = (client_id: string, token: string): WebSocket => {
  if (!socket || socket.readyState === WebSocket.CLOSED) {
    try {
      const socketClient = `${config.SOCKET_URL}?client_id=${client_id}&token=${token}`;
      socket = new WebSocket(socketClient);

      socket.onopen = () => {
        console.log("WebSocket connected");
        triggerEvent("connect");
      };

      socket.onclose = () => {
        console.log("WebSocket disconnected");
        triggerEvent("disconnect");
      };

      socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        triggerEvent("error", error);
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const eventType = data.type;
          triggerEvent(eventType, data.data);
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
          triggerEvent("message", event.data);
        }
      };
    } catch (error) {
      console.error("Failed to create WebSocket:", error);
      throw error;
    }
  }
  return socket;
};

export const getSocket = (): WebSocket | null => socket;

export const disconnectSocket = (): void => {
  if (socket) {
    socket.close();
    socket = null;
  }
};

// Event system to mimic Socket.IO behavior
export const on = (event: string, callback: Function): void => {
  if (!eventHandlers.has(event)) {
    eventHandlers.set(event, new Set());
  }
  eventHandlers.get(event)?.add(callback);
};

export const off = (event: string, callback?: Function): void => {
  if (!eventHandlers.has(event)) return;

  if (callback) {
    eventHandlers.get(event)?.delete(callback);
  } else {
    eventHandlers.delete(event);
  }
};

export const emit = (data?: any): void => {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    console.error("Cannot emit event: WebSocket not connected");
    return;
  }

  const message = JSON.stringify(data);

  socket.send(message);
};

// Helper to trigger events on our handlers
const triggerEvent = (event: string, data?: any): void => {
  if (!eventHandlers.has(event)) return;

  eventHandlers.get(event)?.forEach((callback) => {
    try {
      callback(data);
    } catch (error) {
      console.error(`Error in ${event} handler:`, error);
    }
  });
};
