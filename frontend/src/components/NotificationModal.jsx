import React, { useState } from 'react';
import { X, Send, Bell, CheckCircle, Radio, Copy, Code2, Globe, Check, AlertCircle } from 'lucide-react';

export default function NotificationModal({ isOpen, onClose, notificationData }) {
  if (!isOpen) return null;

  const [activeTab, setActiveTab] = useState('channels'); // 'channels' or 'cap' or 'webhook'
  const [copied, setCopied] = useState(false);
  const [webhookUrl, setWebhookUrl] = useState('');
  const [webhookStatus, setWebhookStatus] = useState(null);
  const [isSending, setIsSending] = useState(false);

  const sampleChannels = notificationData?.dispatched_channels || [
    {
      channel_name: "OASIS CAP v1.2 Standard Alert XML",
      target: "National & State Disaster Management Feeds",
      status: "CAP XML COMPILED",
      payload_sample: "<?xml version='1.0' encoding='UTF-8'?><alert xmlns='urn:oasis:names:tc:emergency:cap:1.2'>..."
    },
    {
      channel_name: "Tamil Nadu SDMA & NDRF Dispatch Webhook",
      target: "Emergency Operations Command (TNSDMA)",
      status: "READY FOR LIVE DISPATCH",
      payload_sample: '{"event": "DISASTER_ALERT", "priority": "CRITICAL", "authority": "RAKSHAK-AI"}'
    },
    {
      channel_name: "Cellular Emergency SMS Broadcast Grid",
      target: "Registered Residents of Affected Zone",
      status: "QUEUED FOR BROADCAST",
      payload_sample: "[HIGH ALERT | RAKSHAK] FLOOD in CHENNAI. Evacuate low-lying areas."
    },
    {
      channel_name: "Regional Early Warning Siren & PA System",
      target: "Public Audible Grid Network",
      status: "ACTIVE GRID SIGNAL PREPARED",
      payload_sample: "Siren Frequency: 450Hz Continuous + Tamil/English Automated Advisory."
    }
  ];

  const capXmlContent = notificationData?.cap_xml || `<?xml version="1.0" encoding="UTF-8"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
  <identifier>RAKSHAK-LIVE-CAP</identifier>
  <sender>rakshak-ai@emergency-ops.gov.in</sender>
  <sent>${new Date().toISOString()}</sent>
  <status>Actual</status>
  <msgType>Alert</msgType>
  <scope>Public</scope>
  <info>
    <category>Safety</category>
    <event>Disaster Emergency Hazard</event>
    <urgency>Immediate</urgency>
    <severity>High</severity>
    <certainty>Observed</certainty>
    <headline>REGIONAL DISASTER WARNING</headline>
    <description>Emergency broadcast compiled in compliance with ITU-T X.1303 / OASIS CAP standard.</description>
    <area>
      <areaDesc>Tamil Nadu, India</areaDesc>
    </area>
  </info>
</alert>`;

  const handleCopyCap = () => {
    navigator.clipboard.writeText(capXmlContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleTestWebhook = async () => {
    if (!webhookUrl.trim()) return;
    setIsSending(true);
    setWebhookStatus(null);
    try {
      const res = await fetch(webhookUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          alert_id: "RAKSHAK-LIVE-TEST",
          timestamp: new Date().toISOString(),
          message: "🚨 [RAKSHAK AI DISPATCH] Live EOC Webhook Test Successful.",
          authority: "RAKSHAK Autonomous EOC Agent"
        })
      });
      if (res.ok) {
        setWebhookStatus({ success: true, text: `Delivered! HTTP ${res.status} OK` });
      } else {
        setWebhookStatus({ success: false, text: `Server returned HTTP ${res.status}` });
      }
    } catch (err) {
      setWebhookStatus({ success: false, text: `Connection Failed: ${err.message}` });
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: 640 }}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Bell size={20} color="#EF4444" />
            <h3 style={{ fontSize: '1.05rem', margin: 0, fontWeight: 800 }}>
              Regional Emergency Dispatch & CAP Protocol Hub
            </h3>
          </div>
          <button 
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: '#94A3B8', cursor: 'pointer' }}
          >
            <X size={20} />
          </button>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem', padding: '0.75rem 1.25rem 0', borderBottom: '1px solid #E2E8F0', background: '#F8FAFC' }}>
          <button 
            className={`activity-tab-btn ${activeTab === 'channels' ? 'active' : ''}`}
            onClick={() => setActiveTab('channels')}
            style={{ borderBottom: activeTab === 'channels' ? '2px solid #2563EB' : 'none' }}
          >
            <Radio size={13} />
            <span>Dispatch Channels ({sampleChannels.length})</span>
          </button>
          <button 
            className={`activity-tab-btn ${activeTab === 'cap' ? 'active' : ''}`}
            onClick={() => setActiveTab('cap')}
            style={{ borderBottom: activeTab === 'cap' ? '2px solid #2563EB' : 'none' }}
          >
            <Code2 size={13} />
            <span>OASIS CAP v1.2 XML Feed</span>
          </button>
          <button 
            className={`activity-tab-btn ${activeTab === 'webhook' ? 'active' : ''}`}
            onClick={() => setActiveTab('webhook')}
            style={{ borderBottom: activeTab === 'webhook' ? '2px solid #2563EB' : 'none' }}
          >
            <Globe size={13} />
            <span>Live Webhook Test</span>
          </button>
        </div>

        <div className="modal-body" style={{ maxHeight: '60vh', overflowY: 'auto' }}>
          {activeTab === 'channels' && (
            <>
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
                <CheckCircle size={16} color="#10B981" />
                <span>
                  <strong>Multi-Channel Staging:</strong> Structured for OASIS CAP standards, cellular broadcast towers, and EOC live webhooks.
                </span>
              </div>

              {sampleChannels.map((ch, idx) => (
                <div key={idx} className="channel-card" style={{ background: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: 8, padding: '0.75rem', marginBottom: '0.6rem' }}>
                  <div className="channel-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontWeight: 700, fontSize: '0.88rem' }}>
                    <span>{ch.channel_name}</span>
                    <span className="channel-status" style={{ fontSize: '0.72rem', background: '#ECFDF5', color: '#047857', padding: '0.15rem 0.45rem', borderRadius: 4 }}>
                      <CheckCircle size={10} style={{ display: 'inline', marginRight: 4 }} />
                      {ch.status}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748B', margin: '0.2rem 0' }}>
                    Target: <strong>{ch.target}</strong>
                  </div>
                  <div className="channel-payload" style={{ fontFamily: 'monospace', fontSize: '0.75rem', background: '#FFFFFF', border: '1px solid #CBD5E1', padding: '0.4rem', borderRadius: 4, color: '#334155' }}>
                    {ch.payload_sample}
                  </div>
                </div>
              ))}
            </>
          )}

          {activeTab === 'cap' && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#475569' }}>
                  Standard OASIS Common Alerting Protocol (CAP v1.2 / ITU-T X.1303)
                </span>
                <button 
                  onClick={handleCopyCap}
                  style={{ display: 'flex', alignItems: 'center', gap: 4, background: '#EFF6FF', border: '1px solid #BFDBFE', color: '#1D4ED8', borderRadius: 6, padding: '0.3rem 0.6rem', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 700 }}
                >
                  {copied ? <Check size={13} color="#10B981" /> : <Copy size={13} />}
                  {copied ? 'Copied XML!' : 'Copy CAP XML'}
                </button>
              </div>
              <pre style={{ background: '#0F172A', color: '#38BDF8', padding: '1rem', borderRadius: 8, fontSize: '0.75rem', overflowX: 'auto', maxHeight: 300 }}>
                {capXmlContent}
              </pre>
            </div>
          )}

          {activeTab === 'webhook' && (
            <div>
              <p style={{ fontSize: '0.82rem', color: '#475569', marginBottom: '0.75rem' }}>
                Test real-time HTTP POST dispatch to your custom EOC API, Discord, or Slack Webhook:
              </p>
              <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem' }}>
                <input 
                  type="url"
                  placeholder="https://discord.com/api/webhooks/... or https://your-eoc.gov/webhook"
                  value={webhookUrl}
                  onChange={(e) => setWebhookUrl(e.target.value)}
                  style={{ flex: 1, padding: '0.6rem 0.8rem', border: '1px solid #CBD5E1', borderRadius: 6, fontSize: '0.85rem' }}
                />
                <button 
                  onClick={handleTestWebhook}
                  disabled={!webhookUrl.trim() || isSending}
                  className="btn-send"
                  style={{ padding: '0.6rem 1rem', fontSize: '0.82rem' }}
                >
                  <Send size={13} />
                  {isSending ? 'Sending...' : 'Dispatch Live'}
                </button>
              </div>

              {webhookStatus && (
                <div style={{ 
                  padding: '0.65rem 0.85rem', 
                  borderRadius: 6, 
                  fontSize: '0.8rem', 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.4rem',
                  background: webhookStatus.success ? '#ECFDF5' : '#FEF2F2',
                  color: webhookStatus.success ? '#065F46' : '#991B1B',
                  border: `1px solid ${webhookStatus.success ? '#A7F3D0' : '#FECACA'}`
                }}>
                  {webhookStatus.success ? <CheckCircle size={15} /> : <AlertCircle size={15} />}
                  <span>{webhookStatus.text}</span>
                </div>
              )}
            </div>
          )}
        </div>

        <div style={{ padding: '0.75rem 1.25rem', borderTop: '1px solid #E2E8F0', display: 'flex', justifyContent: 'flex-end', background: '#F8FAFC' }}>
          <button 
            className="btn-send"
            onClick={onClose}
            style={{ padding: '0.45rem 1.15rem', fontSize: '0.85rem' }}
          >
            Close Protocol Hub
          </button>
        </div>
      </div>
    </div>
  );
}
