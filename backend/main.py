import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models.schemas import (
    ChatRequest,
    ChatResponse,
    DisasterAnalysis,
    NotificationTestRequest,
    NotificationTestResponse,
    NotificationResult
)
from agents.rakshak_agent import RakshakAgent
from tools.region_tool import RegionIdentificationTool
from tools.disaster_tool import DisasterAnalysisTool

app = FastAPI(
    title="RAKSHAK AI - Autonomous Disaster Alert Agent API",
    description="Agentic AI backend for Automated Post-Disaster Regional Alert System",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = RakshakAgent()
region_tool = RegionIdentificationTool()
disaster_tool = DisasterAnalysisTool()

@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify backend status and LLM configuration."""
    is_llm = agent.openrouter_client.is_available
    provider = agent.openrouter_client.provider
    return {
        "status": "healthy",
        "agent": "RAKSHAK AI v1.0",
        "mode": f"hybrid ({provider} LLM + Deterministic Agent)" if is_llm else "deterministic_local",
        "openrouter_connected": is_llm,
        "llm_provider": provider,
        "supported_regions_count": len(region_tool.get_supported_regions()),
        "supported_disasters": list(disaster_tool.disaster_config.keys())
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(req: ChatRequest):
    """
    Main endpoint for user interactions with the RAKSHAK agent.
    Performs Observe -> Analyze -> Decide -> Act lifecycle.
    """
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    try:
        response = await agent.process_event(req.message.strip())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing error: {str(e)}")

@app.post("/api/analyze-disaster", response_model=ChatResponse)
async def analyze_disaster(req: ChatRequest):
    """Dedicated endpoint for direct disaster report analysis."""
    return await chat_with_agent(req)

@app.get("/api/demo-events")
async def get_demo_events():
    """Returns curated demo disaster events for quick testing."""
    return {
        "demo_events": [
            {
                "id": "flood_chennai",
                "label": "🌊 Test Flood Alert",
                "message": "Heavy flooding has been reported in Chennai with multiple low-lying areas inundated.",
                "disaster_type": "Flood",
                "region": "Chennai",
                "expected_severity": "HIGH"
            },
            {
                "id": "cyclone_cuddalore",
                "label": "🌀 Test Cyclone Alert",
                "message": "Severe cyclone warning issued near Cuddalore coastal belt with gale winds reaching 120 km/h.",
                "disaster_type": "Cyclone",
                "region": "Cuddalore",
                "expected_severity": "CRITICAL"
            },
            {
                "id": "earthquake_madurai",
                "label": "🌍 Test Earthquake Alert",
                "message": "Earthquake tremors detected in Madurai measuring 4.8 on Richter scale.",
                "disaster_type": "Earthquake",
                "region": "Madurai",
                "expected_severity": "HIGH"
            },
            {
                "id": "fire_coimbatore",
                "label": "🔥 Test Fire Alert",
                "message": "Massive forest fire reported near Coimbatore foothills threatening residential settlements.",
                "disaster_type": "Fire",
                "region": "Coimbatore",
                "expected_severity": "CRITICAL"
            },
            {
                "id": "landslide_kanyakumari",
                "label": "⛰️ Test Landslide Alert",
                "message": "Major landslide blocking arterial roads near Kanyakumari hilly bypass.",
                "disaster_type": "Landslide",
                "region": "Kanyakumari",
                "expected_severity": "HIGH"
            },
            {
                "id": "safety_check",
                "label": "🛡️ Safety Boundary Check",
                "message": "Is Chennai currently flooding right now?",
                "disaster_type": "Safety Query",
                "region": "Chennai",
                "expected_severity": "SAFETY DISCLAIMER"
            }
        ]
    }

@app.post("/api/notifications/test", response_model=NotificationTestResponse)
async def test_notification_dispatch(req: NotificationTestRequest):
    """Simulates direct multi-channel alert broadcast."""
    import uuid
    from datetime import datetime
    
    alert_id = f"ALERT-{uuid.uuid4().hex[:6].upper()}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    dispatched = [
        NotificationResult(
            channel="Cellular SMS Alert System",
            recipient_group=f"Registered Residents of {req.region}",
            status="SUCCESS (SIMULATED)",
            dispatched_at=now_str,
            payload_sample=f"[{req.severity} ALERT] {req.disaster_type} in {req.region}. {req.message[:80]}..."
        ),
        NotificationResult(
            channel="District Early Warning Siren",
            recipient_group=f"Public Audible Grid - {req.region}",
            status="ACTIVATED (SIMULATED)",
            dispatched_at=now_str,
            payload_sample=f"Audio tone sounded + Automated Tamil/English Voice Advisory Broadcast."
        ),
        NotificationResult(
            channel="NDRF & State Disaster Management Webhook",
            recipient_group="Emergency Operations Command (TNSDMA)",
            status="ACKNOWLEDGED (SIMULATED)",
            dispatched_at=now_str,
            payload_sample=f'{{"event": "{req.disaster_type}", "region": "{req.region}", "priority": "{req.severity}"}}'
        )
    ]
    
    return NotificationTestResponse(
        alert_id=alert_id,
        dispatched_channels=dispatched,
        summary=f"Simulated alert dispatched to 3 key disaster warning channels for {req.region}."
    )
