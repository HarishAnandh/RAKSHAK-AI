import React from 'react';
import { 
  CloudSun, 
  CloudRain, 
  Wind, 
  Droplets, 
  Sun, 
  Thermometer, 
  Gauge, 
  AlertTriangle, 
  CheckCircle2, 
  ExternalLink, 
  Radio, 
  Compass,
  Eye,
  CloudLightning,
  Flame,
  Globe
} from 'lucide-react';

export default function LiveWeatherCard({ weather, onTriggerDisasterCheck }) {
  if (!weather) return null;

  const getWeatherIcon = (cond) => {
    const c = (cond || '').toLowerCase();
    if (c.includes('rain') || c.includes('drizzle') || c.includes('shower')) {
      return <CloudRain size={28} color="#0284C7" />;
    }
    if (c.includes('thunder') || c.includes('lightning') || c.includes('storm')) {
      return <CloudLightning size={28} color="#7C3AED" />;
    }
    if (c.includes('clear') || c.includes('sunny')) {
      return <Sun size={28} color="#F59E0B" />;
    }
    if (c.includes('wind') || c.includes('gale') || c.includes('cyclone')) {
      return <Wind size={28} color="#0D9488" />;
    }
    return <CloudSun size={28} color="#0284C7" />;
  };

  const getRiskBadgeColor = (level) => {
    switch (level) {
      case 'CRITICAL': return { bg: '#FEF2F2', text: '#991B1B', border: '#FCA5A5' };
      case 'HIGH': return { bg: '#FFF7ED', text: '#C2410C', border: '#FDBA74' };
      case 'MEDIUM': return { bg: '#FEFCE8', text: '#A16207', border: '#FEF08A' };
      default: return { bg: '#F0FDF4', text: '#15803D', border: '#BBF7D0' };
    }
  };

  const riskBadge = getRiskBadgeColor(weather.meteorological_risk_level);

  return (
    <div className="live-weather-card animate-fade-in">
      <div className="weather-card-header">
        <div className="weather-header-left">
          <div className="weather-live-indicator">
            <Radio size={13} className="pulse-dot" color="#10B981" />
            <span>LIVE WEB SCRAPED TELEMETRY</span>
          </div>
          <div className="weather-location-name">
            {weather.resolved_location || weather.query_location}
          </div>
        </div>

        <div className="weather-header-right">
          <span 
            className="weather-risk-badge"
            style={{ backgroundColor: riskBadge.bg, color: riskBadge.text, borderColor: riskBadge.border }}
          >
            {weather.meteorological_risk_level} MET RISK
          </span>
        </div>
      </div>

      <div className="weather-main-row">
        <div className="weather-temp-hero">
          <div className="weather-icon-wrapper">
            {getWeatherIcon(weather.condition)}
          </div>
          <div>
            <div className="weather-temp-number">
              {Math.round(weather.temperature_c)}°C
              <span className="weather-temp-f">({weather.temperature_f}°F)</span>
            </div>
            <div className="weather-condition-desc">
              {weather.condition}
            </div>
            <div className="weather-feels-like">
              Feels like <strong>{weather.feels_like_c}°C</strong>
            </div>
          </div>
        </div>

        {weather.is_severe && (
          <div className="weather-severe-alert">
            <AlertTriangle size={18} color="#DC2626" />
            <div>
              <div className="weather-severe-title">Severe Weather Hazard Detected</div>
              <div className="weather-severe-text">{weather.severe_warning}</div>
            </div>
          </div>
        )}
      </div>

      <div className="weather-grid-metrics">
        <div className="weather-metric-cell">
          <div className="metric-cell-label">
            <Droplets size={14} color="#0284C7" />
            <span>Humidity</span>
          </div>
          <div className="metric-cell-val">{weather.humidity_percent}%</div>
          <div className="metric-bar-track">
            <div 
              className="metric-bar-fill" 
              style={{ width: `${Math.min(100, weather.humidity_percent)}%`, backgroundColor: '#0284C7' }} 
            />
          </div>
        </div>

        <div className="weather-metric-cell">
          <div className="metric-cell-label">
            <Wind size={14} color="#0D9488" />
            <span>Wind Speed</span>
          </div>
          <div className="metric-cell-val">
            {weather.wind_speed_kmph} <span style={{ fontSize: '0.75rem' }}>km/h ({weather.wind_direction})</span>
          </div>
          <div className="metric-sub-note">Gusts: {weather.wind_gust_kmph} km/h</div>
        </div>

        <div className="weather-metric-cell">
          <div className="metric-cell-label">
            <CloudRain size={14} color="#2563EB" />
            <span>Rainfall</span>
          </div>
          <div className="metric-cell-val">{weather.precipitation_mm} mm</div>
          <div className="metric-sub-note">
            {weather.precipitation_mm > 0 ? 'Precipitation Active' : 'No Rain Recorded'}
          </div>
        </div>

        <div className="weather-metric-cell">
          <div className="metric-cell-label">
            <Gauge size={14} color="#7C3AED" />
            <span>Pressure & UV</span>
          </div>
          <div className="metric-cell-val">{weather.pressure_mb} mb</div>
          <div className="metric-sub-note">UV Index: {weather.uv_index} / 12</div>
        </div>
      </div>

      <div className="weather-card-footer">
        <div className="weather-scraper-source">
          <Globe size={13} color="#64748B" />
          <span>Source: {weather.source_provider} ({weather.scraped_at})</span>
          {weather.source_url && (
            <a 
              href={weather.source_url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="scraper-link-btn"
              title="View Raw Scraped Web Data"
            >
              <ExternalLink size={11} />
            </a>
          )}
        </div>

        {onTriggerDisasterCheck && (
          <button 
            className="weather-sim-btn"
            onClick={() => onTriggerDisasterCheck(weather.area_name || weather.query_location)}
          >
            <span>View Regional Hazard Matrix</span>
          </button>
        )}
      </div>
    </div>
  );
}
