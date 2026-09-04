import React, { useState } from 'react';
import { 
  Eye, 
  Search, 
  MapPin, 
  Scale, 
  Zap, 
  CheckCircle2, 
  AlertCircle, 
  Info,
  Clock,
  Cpu,
  Terminal,
  Code2,
  Layers,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

export default function AgentActivityPanel({ traces, toolExecutions, isProcessing }) {
  const [activeTab, setActiveTab] = useState('trace'); // 'trace' or 'tools'
  const [expandedTools, setExpandedTools] = useState({});

  const toggleToolExpand = (idx) => {
    setExpandedTools(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  const getStageIcon = (stage) => {
    switch (stage) {
      case 'OBSERVE': return <Eye size={15} color="#4F46E5" />;
      case 'ANALYZE': return <Search size={15} color="#0284C7" />;
      case 'LOCATE': return <MapPin size={15} color="#D97706" />;
      case 'DECIDE': return <Scale size={15} color="#DB2777" />;
      case 'ACT': return <Zap size={15} color="#059669" />;
      default: return <Cpu size={15} color="#64748B" />;
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'COMPLETED':
      case 'SUCCESS': return <CheckCircle2 size={14} color="#10B981" />;
      case 'WARNING':
      case 'FALLBACK_ENGAGED': return <AlertCircle size={14} color="#F59E0B" />;
      default: return <Info size={14} color="#3B82F6" />;
    }
  };

  return (
    <aside className="sidebar-activity-panel">
      <div className="activity-panel-header">
        <div className="activity-panel-title">
          <Cpu size={18} color="#38BDF8" />
          <span>RAKSHAK AGENT ACTIVITY</span>
        </div>
        <span className="activity-badge">
          {isProcessing ? 'ACTIVE EXECUTION' : `${traces.length} STEPS`}
        </span>
      </div>

      <div className="activity-tabs-bar">
        <button 
          className={`activity-tab-btn ${activeTab === 'trace' ? 'active' : ''}`}
          onClick={() => setActiveTab('trace')}
        >
          <Layers size={13} />
          <span>Decision Trace ({traces.length})</span>
        </button>
        <button 
          className={`activity-tab-btn ${activeTab === 'tools' ? 'active' : ''}`}
          onClick={() => setActiveTab('tools')}
        >
          <Code2 size={13} />
          <span>Tool Outputs ({toolExecutions?.length || 0})</span>
        </button>
      </div>

      <div className="activity-panel-content">
        {isProcessing && (
          <div className="activity-stage-card stage-ANALYZE animate-fade-in" style={{ backgroundColor: '#EFF6FF' }}>
            <div className="stage-card-header">
              <span className="stage-tag ANALYZE">PROCESSING</span>
              <span className="stage-timestamp pulse-dot">IN PROGRESS</span>
            </div>
            <div className="stage-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <div className="pulse-dot" style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: '#2563EB' }} />
              Agent reasoning in progress...
            </div>
            <div className="stage-detail">
              Evaluating input against disaster matrices & regional geofences.
            </div>
          </div>
        )}

        {activeTab === 'trace' && (
          <>
            {traces && traces.length > 0 ? (
              traces.map((step, idx) => (
                <div 
                  key={idx} 
                  className={`activity-stage-card stage-${step.stage} animate-fade-in`}
                >
                  <div className="stage-card-header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                      {getStageIcon(step.stage)}
                      <span className={`stage-tag ${step.stage}`}>{step.stage}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                      {getStatusIcon(step.status)}
                      <span className="stage-timestamp">{step.timestamp}</span>
                    </div>
                  </div>

                  <div className="stage-title">{step.title}</div>
                  <div className="stage-detail">{step.detail}</div>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', color: '#94A3B8', marginTop: '3rem', fontSize: '0.85rem' }}>
                <Cpu size={32} style={{ margin: '0 auto 0.75rem auto', opacity: 0.4 }} />
                <p>Agent standing by.</p>
                <p style={{ fontSize: '0.78rem', marginTop: '0.25rem' }}>
                  Send a disaster event to observe the autonomous decision lifecycle.
                </p>
              </div>
            )}
          </>
        )}

        {activeTab === 'tools' && (
          <>
            {toolExecutions && toolExecutions.length > 0 ? (
              toolExecutions.map((tool, idx) => {
                const isExpanded = !!expandedTools[idx];
                return (
                  <div key={idx} className="tool-log-card animate-fade-in">
                    <div className="tool-log-header" onClick={() => toggleToolExpand(idx)}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                        <span className="tool-name">{tool.tool_name}</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        <span className="tool-latency">{tool.execution_time_ms}ms</span>
                        <span className={`tool-status-tag ${tool.status}`}>{tool.status}</span>
                      </div>
                    </div>

                    <div className="tool-desc-text">{tool.description}</div>

                    {isExpanded && (
                      <div className="tool-expanded-json">
                        <div className="json-block-title">Tool Input:</div>
                        <pre className="json-code-view">{JSON.stringify(tool.inputs, null, 2)}</pre>
                        
                        <div className="json-block-title" style={{ marginTop: '0.5rem' }}>Tool Output:</div>
                        <pre className="json-code-view">{JSON.stringify(tool.output, null, 2)}</pre>
                      </div>
                    )}
                  </div>
                );
              })
            ) : (
              <div style={{ textAlign: 'center', color: '#94A3B8', marginTop: '3rem', fontSize: '0.85rem' }}>
                <Code2 size={32} style={{ margin: '0 auto 0.75rem auto', opacity: 0.4 }} />
                <p>No tool telemetry logged yet.</p>
                <p style={{ fontSize: '0.78rem', marginTop: '0.25rem' }}>
                  Run a query to inspect internal tool inputs and outputs.
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </aside>
  );
}
