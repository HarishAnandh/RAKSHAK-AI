import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import AgentActivityPanel from './components/AgentActivityPanel';
import QuickActions from './components/QuickActions';
import NotificationModal from './components/NotificationModal';
import { checkHealth, sendChatMessage } from './services/api';
import './App.css';

export default function App() {
  const [backendHealth, setBackendHealth] = useState(null);
  const [messages, setMessages] = useState([
    {
      sender: 'agent',
      text: "Hello. I'm RAKSHAK AI, an autonomous disaster alert agent. Tell me about a disaster event and I will analyze the affected region and generate an appropriate alert.",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      analysis: null,
      alert: null
    }
  ]);
  const [activeTraces, setActiveTraces] = useState([
    {
      stage: 'OBSERVE',
      title: 'Agent Standby',
      detail: 'RAKSHAK core online. Waiting for incoming disaster event telemetry.',
      status: 'INFO',
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [toolExecutions, setToolExecutions] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedNotificationData, setSelectedNotificationData] = useState(null);

  useEffect(() => {
    // Health check on startup
    const ping = async () => {
      const data = await checkHealth();
      setBackendHealth(data);
    };
    ping();
    const interval = setInterval(ping, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const userTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = {
      sender: 'user',
      text: text,
      timestamp: userTime
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsProcessing(true);

    try {
      const response = await sendChatMessage(text);
      
      const agentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      const agentMsg = {
        sender: 'agent',
        text: response.reply_text,
        timestamp: agentTime,
        analysis: response.analysis,
        alert: response.alert,
        notification_preview: response.notification_preview,
        regional_hazard_profile: response.regional_hazard_profile
      };

      setMessages((prev) => [...prev, agentMsg]);

      // Update right sidebar with structured agent decision trace & tool telemetry
      if (response.structured_trace && response.structured_trace.length > 0) {
        setActiveTraces(response.structured_trace);
      }

      if (response.tool_executions && response.tool_executions.length > 0) {
        setToolExecutions(response.tool_executions);
      }

      if (response.notification_preview) {
        setSelectedNotificationData(response.notification_preview);
      }
    } catch (err) {
      const errorMsg = {
        sender: 'agent',
        text: `⚠️ **Processing Notice:** ${err.message || 'Unable to reach RAKSHAK backend. Please ensure the backend server is running on port 8000.'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        analysis: null,
        alert: null
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleOpenDispatch = (alert) => {
    setIsModalOpen(true);
  };

  return (
    <div className="app-container">
      <Header 
        backendHealth={backendHealth} 
        onOpenNotificationModal={() => setIsModalOpen(true)}
        isProcessing={isProcessing}
      />

      <QuickActions 
        onSelectScenario={handleSendMessage}
        disabled={isProcessing}
      />

      <div className="main-layout">
        <ChatInterface 
          messages={messages}
          onSendMessage={handleSendMessage}
          isProcessing={isProcessing}
          onOpenDispatch={handleOpenDispatch}
        />

        <AgentActivityPanel 
          traces={activeTraces}
          toolExecutions={toolExecutions}
          isProcessing={isProcessing}
        />
      </div>

      <NotificationModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        notificationData={selectedNotificationData}
      />
    </div>
  );
}
