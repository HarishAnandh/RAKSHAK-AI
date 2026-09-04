import React, { useState, useEffect } from 'react';
import { ShieldAlert, Radio, Bell, RefreshCw, Sparkles, Cpu } from 'lucide-react';

export default function Header({ backendHealth, onOpenNotificationModal, isProcessing }) {
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const isOnline = backendHealth?.status === 'healthy';

  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-shield">
          <ShieldAlert size={26} color="#FFFFFF" />
        </div>
        <div className="brand-title-group">
          <h1>
            RAKSHAK AI
            <span className="brand-badge">Agentic EOC</span>
          </h1>
          <div className="brand-subtitle">
            Autonomous Post-Disaster Regional Alert System
          </div>
        </div>
      </div>

      <div className="header-status-group">
        <div className="status-pill">
          <span className={`status-indicator ${isProcessing ? 'processing' : (isOnline ? 'online' : 'offline')} ${isOnline ? 'pulse-dot' : ''}`}></span>
          <span>
            {isProcessing ? 'AGENT REASONING...' : (isOnline ? 'AGENT ONLINE' : 'AGENT OFFLINE')}
          </span>
        </div>

        {backendHealth && (
          <div className="status-pill" title={backendHealth.mode}>
            {backendHealth.openrouter_connected ? (
              <>
                <Sparkles size={14} color="#38BDF8" />
                <span style={{ color: '#38BDF8' }}>
                  {backendHealth.llm_provider || 'Cloud'} LLM
                </span>
              </>
            ) : (
              <>
                <Cpu size={14} color="#CBD5E1" />
                <span>Deterministic Mode</span>
              </>
            )}
          </div>
        )}

        <div className="system-clock">
          <Radio size={14} color="#38BDF8" />
          <span>{currentTime} IST</span>
        </div>

        <button 
          className="btn-header-tool"
          onClick={onOpenNotificationModal}
          title="View Simulated Multi-Channel Notification Status"
        >
          <Bell size={15} />
          <span>Dispatch Hub</span>
        </button>
      </div>
    </header>
  );
}
