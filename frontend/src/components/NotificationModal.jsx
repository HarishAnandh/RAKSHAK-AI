import React from 'react';
import { X, Send, Bell, CheckCircle, Radio } from 'lucide-react';

export default function NotificationModal({ isOpen, onClose, notificationData }) {
  if (!isOpen) return null;

  const sampleChannels = notificationData?.dispatched_channels || [
    {
      channel_name: "Cellular Emergency SMS Broadcast",
      target: "Registered Residents of Affected Zone",
      status: "READY TO DISPATCH (SIMULATED)",
      payload_sample: "[HIGH ALERT | RAKSHAK] FLOOD in CHENNAI. Move to higher ground immediately."
    },
    {
      channel_name: "Regional Early Warning Siren & PA System",
      target: "Local Municipal Emergency Grid",
      status: "READY TO DISPATCH (SIMULATED)",
      payload_sample: "Siren Frequency: 450Hz Pulse + Tamil/English Automated Voice Alert."
    },
    {
      channel_name: "Tamil Nadu SDMA & NDRF Dispatch Webhook",
      target: "State Emergency Operations Center (EOC)",
      status: "READY TO DISPATCH (SIMULATED)",
      payload_sample: '{"event": "DISASTER_ALERT", "priority": "CRITICAL", "authority": "RAKSHAK-AI"}'
    },
    {
      channel_name: "Civil Defense WhatsApp Alert Channel",
      target: "Community Volunteers & First Responders",
      status: "READY TO DISPATCH (SIMULATED)",
      payload_sample: "🚨 RAKSHAK POST-DISASTER BULLETIN: Rescue coordination teams dispatched."
    }
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Bell size={20} color="#EF4444" />
            <h3 style={{ fontSize: '1.05rem', margin: 0, fontWeight: 800 }}>
              Simulated Multi-Channel Dispatch Hub
            </h3>
          </div>
          <button 
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: '#94A3B8', cursor: 'pointer' }}
          >
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <div style={{ 
            backgroundColor: '#EFF6FF', 
            border: '1px solid #BFDBFE', 
            borderRadius: 8, 
            padding: '0.75rem 1rem', 
            marginBottom: '1rem',
            fontSize: '0.82rem',
            color: '#1E40AF',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Radio size={16} />
            <span>
              <strong>Simulation Mode:</strong> In production, RAKSHAK triggers Twilio SMS, CAP-compliant public sirens, and SDMA APIs.
            </span>
          </div>

          {sampleChannels.map((ch, idx) => (
            <div key={idx} className="channel-card">
              <div className="channel-title">
                <span>{ch.channel_name}</span>
                <span className="channel-status">
                  <CheckCircle size={10} style={{ display: 'inline', marginRight: 4 }} />
                  {ch.status}
                </span>
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748B', marginBottom: '0.25rem' }}>
                Target: <strong>{ch.target}</strong>
              </div>
              <div className="channel-payload">
                {ch.payload_sample}
              </div>
            </div>
          ))}
        </div>

        <div style={{ padding: '1rem 1.25rem', borderTop: '1px solid #E2E8F0', display: 'flex', justifyContent: 'flex-end' }}>
          <button 
            className="btn-send"
            onClick={onClose}
            style={{ padding: '0.5rem 1.25rem' }}
          >
            Close Dispatch Hub
          </button>
        </div>
      </div>
    </div>
  );
}
