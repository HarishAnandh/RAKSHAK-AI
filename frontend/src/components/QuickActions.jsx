import React from 'react';
import { Zap, ShieldAlert } from 'lucide-react';

export default function QuickActions({ onSelectScenario, disabled }) {
  const scenarios = [
    {
      label: "🌊 Test Flood Alert",
      text: "Heavy flooding has been reported in Chennai with low-lying areas inundated.",
      type: "flood"
    },
    {
      label: "🌀 Test Cyclone Alert",
      text: "Severe cyclone warning issued near Cuddalore coastal belt with gale winds.",
      type: "cyclone"
    },
    {
      label: "🌍 Test Earthquake Alert",
      text: "Earthquake tremors detected in Madurai measuring 4.8 on Richter scale.",
      type: "earthquake"
    },
    {
      label: "🔥 Test Fire Alert",
      text: "Massive forest fire reported near Coimbatore foothills threatening settlements.",
      type: "fire"
    },
    {
      label: "🛡️ Safety Boundary Check",
      text: "Is Chennai currently flooding right now?",
      type: "safety",
      isSafety: true
    }
  ];

  return (
    <div className="chat-quick-actions-bar">
      <div className="quick-action-label">
        <Zap size={13} color="#D97706" />
        <span>Quick Tests:</span>
      </div>
      {scenarios.map((sc, i) => (
        <button
          key={i}
          className={`quick-btn ${sc.isSafety ? 'safety-btn' : ''}`}
          onClick={() => onSelectScenario(sc.text)}
          disabled={disabled}
        >
          {sc.label}
        </button>
      ))}
    </div>
  );
}
