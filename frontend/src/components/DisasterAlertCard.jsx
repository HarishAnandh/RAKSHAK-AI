import React from 'react';
import { 
  AlertTriangle, 
  Waves, 
  Wind, 
  Activity, 
  Flame, 
  Mountain, 
  CloudLightning, 
  MapPin, 
  Send, 
  ShieldCheck,
  Radio
} from 'lucide-react';

export default function DisasterAlertCard({ alert, onOpenDispatch }) {
  if (!alert) return null;

  const getDisasterIcon = (type) => {
    switch ((type || '').toLowerCase()) {
      case 'flood': return <Waves size={20} color="#DC2626" />;
      case 'cyclone': return <Wind size={20} color="#DC2626" />;
      case 'earthquake': return <Activity size={20} color="#DC2626" />;
      case 'fire': return <Flame size={20} color="#DC2626" />;
      case 'landslide': return <Mountain size={20} color="#DC2626" />;
      case 'storm': return <CloudLightning size={20} color="#DC2626" />;
      default: return <AlertTriangle size={20} color="#DC2626" />;
    }
  };

  const getRiskColor = (score) => {
    if (score >= 90) return '#991B1B'; // Critical
    if (score >= 70) return '#EA580C'; // High
    if (score >= 40) return '#D97706'; // Medium
    return '#16A34A'; // Low
  };

  return (
    <div className="disaster-alert-card animate-fade-in">
      <div className="alert-card-header">
        <div className="alert-title-wrap">
          <AlertTriangle size={22} className="pulse-dot" />
          <span>🚨 DISASTER ALERT</span>
        </div>
        <div className="alert-live-pulse">
          <Radio size={12} className="pulse-dot" />
          <span>{alert.status || 'ALERT GENERATED'}</span>
        </div>
      </div>

      <div className="alert-card-body">
        <div className="alert-stat-block">
          <div className="stat-label">Disaster Type</div>
          <div className="stat-value">
            {getDisasterIcon(alert.disaster_type)}
            <span>{(alert.disaster_type || 'Unknown').toUpperCase()}</span>
          </div>
        </div>

        <div className="alert-stat-block">
          <div className="stat-label">Affected Region</div>
          <div className="stat-value">
            <MapPin size={18} color="#2563EB" />
            <span>{(alert.region || 'Unknown').toUpperCase()}</span>
          </div>
        </div>

        <div className="risk-meter-container">
          <div className="risk-meter-header">
            <span className="stat-label">Risk Assessment Index</span>
            <span style={{ 
              fontWeight: 800, 
              color: getRiskColor(alert.risk_score), 
              fontSize: '0.9rem' 
            }}>
              {alert.severity} ({alert.risk_score}/100)
            </span>
          </div>
          <div className="risk-meter-bar-track">
            <div 
              className="risk-meter-fill"
              style={{
                width: `${alert.risk_score}%`,
                backgroundColor: getRiskColor(alert.risk_score)
              }}
            />
          </div>
        </div>

        <div className="alert-action-block">
          <div className="action-title">
            <ShieldCheck size={16} />
            <span>Recommended Action</span>
          </div>
          <div className="action-desc">
            {alert.recommended_action}
          </div>
        </div>
      </div>

      <div className="alert-card-footer">
        <div className="demo-disclaimer-tag">
          <span>⚠️ {alert.disclaimer || 'DEMO ALERT - BASED ON REPORT'}</span>
        </div>
        {onOpenDispatch && (
          <button 
            className="btn-dispatch-sim"
            onClick={() => onOpenDispatch(alert)}
          >
            <Send size={13} />
            <span>View Dispatch Channels</span>
          </button>
        )}
      </div>
    </div>
  );
}
