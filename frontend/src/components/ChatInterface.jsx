import React, { useState, useRef, useEffect } from 'react';
import { Send, Shield, AlertTriangle, Sparkles, CheckCircle2, User, Bot, HelpCircle } from 'lucide-react';
import DisasterAlertCard from './DisasterAlertCard';
import RegionalHazardCard from './RegionalHazardCard';

export default function ChatInterface({ 
  messages, 
  onSendMessage, 
  isProcessing, 
  onOpenDispatch 
}) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || isProcessing) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  return (
    <div className="chat-section">
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div 
            key={index} 
            className={`message-row ${msg.sender === 'user' ? 'user-row' : 'agent-row'} animate-fade-in`}
          >
            <div className={`message-bubble ${msg.sender === 'user' ? 'user-bubble' : 'agent-bubble'}`}>
              {msg.sender === 'agent' && (
                <div className="agent-bubble-header">
                  <div className="agent-badge-group">
                    <span className="agent-name">
                      <Shield size={16} color="#DC2626" />
                      RAKSHAK AI
                    </span>
                    <span className="agent-mode-tag">Autonomous Agent</span>
                  </div>
                  <span className="message-timestamp">{msg.timestamp}</span>
                </div>
              )}

              {msg.sender === 'user' && (
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.3rem', opacity: 0.8, fontSize: '0.75rem' }}>
                  <span style={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 4 }}>
                    <User size={13} />
                    FIELD OPERATOR / USER
                  </span>
                  <span className="message-timestamp" style={{ color: '#94A3B8' }}>{msg.timestamp}</span>
                </div>
              )}

              <div className="message-text">
                {msg.text}
              </div>

              {/* Safety Warning Callout if unverified real-time query */}
              {msg.analysis?.is_safety_warning && (
                <div className="safety-callout-box">
                  <AlertTriangle className="safety-callout-icon" size={20} />
                  <div>
                    <div className="safety-callout-title">
                      Real-Time Safety Boundary Protocol Engaged
                    </div>
                    <div className="safety-callout-desc">
                      RAKSHAK AI does not connect to unverified live feeds for instant physical verification without official telemetry. Simulated emergency alerts can be generated from explicit scenario reports.
                    </div>
                  </div>
                </div>
              )}

              {/* Regional Hazard & Disaster Probability Breakdown Card */}
              {msg.regional_hazard_profile && (
                <RegionalHazardCard 
                  profile={msg.regional_hazard_profile}
                  onSimulateEvent={onSendMessage}
                />
              )}

              {/* Disaster Alert Card */}
              {msg.alert && (
                <DisasterAlertCard 
                  alert={msg.alert} 
                  onOpenDispatch={onOpenDispatch}
                />
              )}
            </div>
          </div>
        ))}

        {isProcessing && (
          <div className="message-row agent-row animate-fade-in">
            <div className="message-bubble agent-bubble" style={{ maxWidth: 360 }}>
              <div className="agent-bubble-header">
                <span className="agent-name">
                  <Bot size={16} color="#2563EB" />
                  RAKSHAK Reasoning Core
                </span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#475569', fontSize: '0.85rem' }}>
                <div className="pulse-dot" style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#2563EB' }} />
                <span>Observing event & executing analysis tools...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-container" onSubmit={handleSubmit}>
        <div className="chat-input-box">
          <input
            type="text"
            className="chat-text-input"
            placeholder="Type a region (e.g. 'Salem', 'Chennai') or report an event ('Heavy flooding in Chennai')..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isProcessing}
          />
        </div>
        <button 
          type="submit" 
          className="btn-send"
          disabled={!inputText.trim() || isProcessing}
        >
          <Send size={16} />
          <span>Analyze & Decide</span>
        </button>
      </form>
    </div>
  );
}
