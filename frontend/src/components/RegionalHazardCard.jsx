import React from 'react';
import { 
  MapPin, 
  ShieldAlert, 
  Waves, 
  Wind, 
  Activity, 
  Flame, 
  Mountain, 
  CloudLightning, 
  AlertTriangle,
  PhoneCall,
  Zap
} from 'lucide-react';

export default function RegionalHazardCard({ profile, onSimulateEvent }) {
  if (!profile) return null;

  const getDisasterIcon = (type) => {
    switch ((type || '').toLowerCase()) {
      case 'flood': return <Waves size={16} color="#0284C7" />;
      case 'cyclone': return <Wind size={16} color="#0D9488" />;
      case 'earthquake': return <Activity size={16} color="#D97706" />;
      case 'fire': return <Flame size={16} color="#EA580C" />;
      case 'landslide': return <Mountain size={16} color="#854D0E" />;
      case 'storm': return <CloudLightning size={16} color="#4F46E5" />;
      default: return <AlertTriangle size={16} color="#DC2626" />;
    }
  };

  const getBarColor = (pct) => {
    if (pct >= 85) return '#DC2626'; // Red
    if (pct >= 70) return '#EA580C'; // Orange
    if (pct >= 40) return '#D97706'; // Amber
    return '#10B981'; // Emerald
  };

  const getBadgeStyle = (level) => {
    switch (level) {
      case 'CRITICAL': return { bg: '#FEF2F2', text: '#991B1B', border: '#FCA5A5' };
      case 'HIGH': return { bg: '#FFF7ED', text: '#C2410C', border: '#FDBA74' };
      case 'MEDIUM': return { bg: '#FEFCE8', text: '#A16207', border: '#FEF08A' };
      default: return { bg: '#F0FDF4', text: '#15803D', border: '#BBF7D0' };
    }
  };

  return (
    <div className="regional-hazard-card animate-fade-in">
      <div className="hazard-card-header">
        <div className="hazard-title-group">
          <div className="hazard-region-badge">
            <MapPin size={16} />
            <span>{profile.region_name.toUpperCase()}</span>
          </div>
          <span className="hazard-zone-tag">{profile.zone}</span>
        </div>
        <div className="vulnerability-score-badge">
          <span className="vuln-label">Vulnerability Index</span>
          <span className="vuln-score">{profile.composite_vulnerability_score}/100</span>
        </div>
      </div>

      <div className="hazard-card-body">
        <div className="threat-summary-bar">
          <ShieldAlert size={16} color="#EA580C" />
          <span><strong>Primary Threat Profile:</strong> {profile.primary_threat}</span>
        </div>

        <div className="hazard-probability-list">
          <div className="hazard-list-title">
            <span>Historical Hazard Occurrence Probabilities</span>
            <span style={{ fontSize: '0.75rem', color: '#64748B' }}>Calculated from Regional Topography & Met Data</span>
          </div>

          {profile.hazards.map((item, idx) => {
            const badge = getBadgeStyle(item.risk_level);
            return (
              <div key={idx} className="hazard-item-row">
                <div className="hazard-item-info">
                  <div className="hazard-name-group">
                    {getDisasterIcon(item.disaster_type)}
                    <span className="hazard-name">{item.disaster_type}</span>
                  </div>
                  <div className="hazard-level-group">
                    <span 
                      className="hazard-risk-badge" 
                      style={{ backgroundColor: badge.bg, color: badge.text, borderColor: badge.border }}
                    >
                      {item.risk_level}
                    </span>
                    <span className="hazard-percent" style={{ color: getBarColor(item.probability_percent) }}>
                      {item.probability_percent}%
                    </span>
                  </div>
                </div>

                <div className="hazard-progress-track">
                  <div 
                    className="hazard-progress-fill"
                    style={{
                      width: `${item.probability_percent}%`,
                      backgroundColor: getBarColor(item.probability_percent)
                    }}
                  />
                </div>

                <div className="hazard-notes">
                  {item.historical_notes}
                </div>
              </div>
            );
          })}
        </div>

        {onSimulateEvent && profile.hazards.length > 0 && (
          <div className="simulate-hazard-bar">
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#1E293B', display: 'flex', alignItems: 'center', gap: 4 }}>
              <Zap size={14} color="#D97706" />
              Simulate in {profile.region_name}:
            </span>
            <button 
              className="quick-btn"
              style={{ fontSize: '0.78rem', padding: '0.3rem 0.65rem' }}
              onClick={() => onSimulateEvent(`Heavy ${profile.hazards[0].disaster_type.toLowerCase()} reported in ${profile.region_name} with low-lying areas affected`)}
            >
              Simulate {profile.hazards[0].disaster_type} Alert
            </button>
            {profile.hazards[1] && (
              <button 
                className="quick-btn"
                style={{ fontSize: '0.78rem', padding: '0.3rem 0.65rem' }}
                onClick={() => onSimulateEvent(`Severe ${profile.hazards[1].disaster_type.toLowerCase()} warning issued near ${profile.region_name}`)}
              >
                Simulate {profile.hazards[1].disaster_type} Alert
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
