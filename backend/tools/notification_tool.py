from datetime import datetime
from typing import Dict, Any, List
import uuid

class NotificationTool:
    """Tool for simulating regional multi-channel post-disaster alert dispatch."""

    def __init__(self):
        self.channels = [
            {"id": "DEMO_SMS", "name": "Cellular Emergency SMS Broadcast", "target": "Registered Residents"},
            {"id": "BROADCAST_SIREN", "name": "Regional Early Warning Siren & PA", "target": "Local Municipality"},
            {"id": "EOC_WEBHOOK", "name": "Tamil Nadu SDMA & NDRF Dispatch API", "target": "Emergency Responders"},
            {"id": "WHATSAPP_BROADCAST", "name": "Civil Defense WhatsApp Channel", "target": "Community Volunteers"}
        ]

    def prepare_and_dispatch(self, region: str, disaster_type: str, severity: str, message: str, risk_score: int) -> Dict[str, Any]:
        """Simulates dispatching emergency alerts across channels."""
        dispatch_id = f"DISPATCH-{uuid.uuid4().hex[:8].upper()}"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dispatched = []
        for ch in self.channels:
            dispatched.append({
                "channel_id": ch["id"],
                "channel_name": ch["name"],
                "target": f"{ch['target']} ({region})",
                "status": "READY TO DISPATCH (SIMULATED)",
                "dispatched_at": now_str,
                "payload_sample": f"[{severity} ALERT | RAKSHAK] {disaster_type.upper()} in {region}. {message[:120]}..."
            })

        return {
            "dispatch_id": dispatch_id,
            "status": "QUEUED_AND_DISPATCHED",
            "region": region,
            "channels_count": len(dispatched),
            "dispatched_channels": dispatched,
            "preview_summary": f"Notification prepared for {region} across {len(dispatched)} public channels."
        }
