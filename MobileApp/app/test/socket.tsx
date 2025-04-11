import React, { useState, useEffect } from "react";
import { useSocket } from "@/contexts/DetectContext";
import { 
  StyleSheet, 
  Text, 
  View, 
  ScrollView, 
  TouchableOpacity, 
  TextInput,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform
} from "react-native";
import { BaseColors } from "@/constants/Colors";
import { Fonts } from "@/shared/SharedStyles";
import { AuthService } from "@/services/auth";

// Sample event types to test
const EVENT_TYPES = [
  { name: 'message', color: '#2196F3' },
  { name: 'detection', color: '#4CAF50' },
  { name: 'alert', color: '#F44336' },
  { name: 'stats', color: '#FF9800' },
  { name: 'posture', color: '#9C27B0' }
];

export default function SocketTestScreen() {
    const { socket, isConnected, connect, disconnect, emit } = useSocket();
    const [logs, setLogs] = useState<Array<{type: string; message: string; timestamp: string}>>([]);
    const [customEvent, setCustomEvent] = useState('custom-event');
    const [customPayload, setCustomPayload] = useState('{"message": "Hello world"}');
    const [clientId, setClientId] = useState('');
    const [token, setToken] = useState('');
    // Add log entry with timestamp
    const addLog = (type: string, message: string) => {
      const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
      setLogs(prevLogs => [
        { type, message, timestamp },
        ...prevLogs.slice(0, 49) // Keep only the last 50 logs
      ]);
    };
    
    // Initialize event listeners
    useEffect(() => {
      const client_id = AuthService.getUser() || '';
      const token = AuthService.getToken();
      
      Promise.all([client_id, token]).then(res => {
        const [client_id, token] = res;
        setClientId(client_id.id);
        setToken(token as string);
      })
      
      if (!socket) return;
      
      const handleEvent = (eventName: string) => (data: any) => {
        addLog(eventName, JSON.stringify(data));
      };
      
      // Set up listeners for each event type
      EVENT_TYPES.forEach(eventType => {
        socket.on(eventType.name, handleEvent(eventType.name));
      });
      
      // Connection events
      socket.on('connect', () => {
        addLog('system', 'Connected to server');
      });
      
      socket.on('disconnect', () => {
        addLog('system', 'Disconnected from server');
      });
      
      socket.on('error', (err: Error) => {
        addLog('error', `Connection error: ${err}`);
      });
      
      return () => {
        // Remove all listeners when component unmounts
        EVENT_TYPES.forEach(eventType => {
          socket.off(eventType.name);
        });
        socket.off('connect');
        socket.off('disconnect');
        socket.off('error');
        socket.off('message');
        socket.off('posture');
      };
    }, [socket]);
    
    // Emit test event
    const emitEvent = (eventName: string, payload?: string) => {
      if (!socket || !isConnected) {
        addLog('error', `Cannot emit event: WebSocket not connected`);
        return;
      }
      
      try {
        const data = payload ? JSON.parse(payload) : "Hello world";
        console.log(JSON.stringify(data));
        socket.emit(data);
        addLog('emit', `Emitted with payload: ${payload || '{}'}`);
      } catch (err: any) {
        addLog('error', `Failed to emit: ${err.message}`);
      }
    };
    
    // Handle reconnection
    const handleReconnect = () => {
      try {
        connect(clientId, token); // Use the context method instead
        addLog('system', 'Attempting to reconnect...');
      } catch (error: any) {
        addLog('error', `Reconnection error: ${error.message}`);
      }
    };

  // Get color for log entry
  const getLogColor = (type: string) => {
    const eventType = EVENT_TYPES.find(et => et.name === type);
    if (eventType) return eventType.color;
    
    switch(type) {
      case 'system': return '#9C27B0';
      case 'emit': return '#009688';
      case 'error': return '#F44336';
      default: return '#757575';
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardAvoidView}
      >
        <ScrollView style={styles.scrollView}>
          {/* Connection Status and Controls */}
          <View style={styles.header}>
            <View style={[styles.statusDot, { backgroundColor: isConnected ? '#4CAF50' : '#F44336' }]} />
            <Text style={styles.statusText}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </Text>
            <View style={styles.buttonContainer}>
              <TouchableOpacity
                style={[styles.button, isConnected ? styles.disconnectButton : styles.connectButton]}
                onPress={() => isConnected ? disconnect() : connect(clientId, token)}
              >
                <Text style={styles.buttonText}>
                  {isConnected ? 'Disconnect' : 'Connect'}
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Detection Controls */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Detection Controls</Text>
            <View style={styles.buttonContainer}>
              <TouchableOpacity
                style={[styles.button, styles.detectButton]}
                onPress={() => {
                  if (socket && isConnected) {
                    const detectMessage = {
                      type: 'detect',
                      client: 'mobile',
                      timestamp: new Date().toISOString()
                    };
                    socket.emit(detectMessage);
                    addLog('emit', 'Started detection');
                  }
                }}
              >
                <Text style={styles.buttonText}>Start Detection</Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.button, styles.stopDetectButton]}
                onPress={() => {
                  if (socket && isConnected) {
                    const stopMessage = {
                      type: 'stopDetect',
                      client: 'mobile',
                      timestamp: new Date().toISOString()
                    };
                    socket.emit(stopMessage);
                    addLog('emit', 'Stopped detection');
                  }
                }}
              >
                <Text style={styles.buttonText}>Stop Detection</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Quick Test Events */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Test Events</Text>
            <View style={styles.eventButtonsContainer}>
              {EVENT_TYPES.map((eventType) => (
                <TouchableOpacity
                  key={eventType.name}
                  style={[styles.eventButton, { backgroundColor: eventType.color }]}
                  onPress={() => emitEvent(eventType.name, `{"test": true, "timestamp": "${Date.now()}"}`)}
                  disabled={!isConnected}
                >
                  <Text style={styles.eventButtonText}>{eventType.name}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Custom Event */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Custom Event</Text>
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Event Name:</Text>
              <TextInput
                style={styles.input}
                value={customEvent}
                onChangeText={setCustomEvent}
                placeholder="Enter event name"
                placeholderTextColor="#9E9E9E"
              />
            </View>
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Payload (JSON):</Text>
              <TextInput
                style={[styles.input, styles.payloadInput]}
                value={customPayload}
                onChangeText={setCustomPayload}
                placeholder='{"key": "value"}'
                placeholderTextColor="#9E9E9E"
                multiline
              />
            </View>
            <TouchableOpacity
              style={[styles.sendButton, !isConnected && styles.disabledButton]}
              onPress={() => emitEvent(customEvent, customPayload)}
              disabled={!isConnected}
            >
              <Text style={styles.sendButtonText}>Send Custom Event</Text>
            </TouchableOpacity>
          </View>

          {/* Event Logs */}
          <View style={styles.section}>
            <View style={styles.logHeaderContainer}>
              <Text style={styles.sectionTitle}>Event Logs</Text>
              <TouchableOpacity
                style={styles.clearButton}
                onPress={() => setLogs([])}
              >
                <Text style={styles.clearButtonText}>Clear</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.logsContainer}>
              {logs.length === 0 ? (
                <Text style={styles.noLogsText}>No events logged yet</Text>
              ) : (
                logs.map((log, index) => (
                  <View key={index} style={styles.logEntry}>
                    <View style={styles.logHeader}>
                      <View 
                        style={[styles.logTypeBadge, { backgroundColor: getLogColor(log.type) }]}
                      >
                        <Text style={styles.logType}>{log.type}</Text>
                      </View>
                      <Text style={styles.logTime}>{log.timestamp}</Text>
                    </View>
                    <Text style={styles.logMessage}>{log.message}</Text>
                  </View>
                ))
              )}
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: BaseColors.dark_pri,
  },
  keyboardAvoidView: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
    padding: 16,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: BaseColors.dark_pri,
    borderRadius: 8,
    marginBottom: 16,
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  statusText: {
    ...Fonts.body,
    color: BaseColors.white,
    flex: 1,
  },
  buttonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  button: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 4,
    marginLeft: 12,
  },
  connectButton: {
    backgroundColor: '#2196F3',
  },
  disconnectButton: {
    backgroundColor: '#F44336',
  },
  buttonText: {
    ...Fonts.bodySmall,
    color: BaseColors.white,
    fontWeight: '500',
  },
  section: {
    backgroundColor: BaseColors.dark_pri,
    borderRadius: 8,
    padding: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    ...Fonts.h3,
    color: BaseColors.white,
    marginBottom: 12,
  },
  eventButtonsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  eventButton: {
    width: '48%',
    padding: 12,
    borderRadius: 4,
    marginBottom: 8,
    alignItems: 'center',
  },
  eventButtonText: {
    ...Fonts.bodySmall,
    color: BaseColors.white,
    fontWeight: '500',
  },
  inputContainer: {
    marginBottom: 12,
  },
  inputLabel: {
    ...Fonts.bodySmall,
    color: BaseColors.white,
    marginBottom: 4,
  },
  input: {
    backgroundColor: BaseColors.dark_pri,
    color: BaseColors.white,
    padding: 8,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: '#444444',
  },
  payloadInput: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  sendButton: {
    backgroundColor: '#009688',
    padding: 12,
    borderRadius: 4,
    alignItems: 'center',
    marginTop: 8,
  },
  disabledButton: {
    opacity: 0.5,
  },
  sendButtonText: {
    ...Fonts.body,
    color: BaseColors.white,
    fontWeight: '500',
  },
  logHeaderContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  clearButton: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    backgroundColor: '#616161',
    borderRadius: 4,
  },
  clearButtonText: {
    ...Fonts.small,
    color: BaseColors.white,
  },
  logsContainer: {
    maxHeight: 300,
  },
  noLogsText: {
    ...Fonts.body,
    color: '#9E9E9E',
    fontStyle: 'italic',
    textAlign: 'center',
    paddingVertical: 16,
  },
  logEntry: {
    backgroundColor: BaseColors.dark_pri,
    borderRadius: 4,
    padding: 8,
    marginBottom: 8,
  },
  logHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  logTypeBadge: {
    paddingVertical: 2,
    paddingHorizontal: 6,
    borderRadius: 4,
  },
  logType: {
    ...Fonts.small,
    color: BaseColors.white,
    fontWeight: '500',
  },
  logTime: {
    ...Fonts.small,
    color: '#BDBDBD',
  },
  logMessage: {
    ...Fonts.bodySmall,
    color: BaseColors.white,
  },
  detectButton: {
    backgroundColor: '#4CAF50',
  },
  stopDetectButton: {
    backgroundColor: '#F44336',
  },
});