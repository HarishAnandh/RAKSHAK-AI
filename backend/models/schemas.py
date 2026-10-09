from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message or disaster report")

class HazardProbabilityItem(BaseModel):
    disaster_type: str
    probability_percent: int
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    historical_notes: str
    icon: str

class RegionalHazardProfile(BaseModel):
    region_name: str
    zone: str
    terrain_type: str
    coastal: bool
    composite_vulnerability_score: int
    primary_threat: str
    hazards: List[HazardProbabilityItem]
    emergency_contacts: List[str]

class ToolExecutionLog(BaseModel):
    tool_name: str
    stage: str
    status: str
    inputs: Dict[str, Any]
    output: Dict[str, Any]
    execution_time_ms: float
    description: str

class DisasterAnalysis(BaseModel):
    disaster_type: str = Field(..., description="Identified disaster type (Flood, Cyclone, Earthquake, Fire, Landslide, Tsunami, Storm, Unknown)")
    location: str = Field(..., description="Detected location name or 'Unknown'")
    affected_region: str = Field(..., description="Affected administrative or regional area")
    severity: str = Field(..., description="Assessed severity level: LOW, MEDIUM, HIGH, CRITICAL")
    risk_score: int = Field(..., description="Numerical risk score from 0 to 100")
    risk_level: str = Field(..., description="Risk level category matching score: LOW, MEDIUM, HIGH, CRITICAL")
    alert_required: bool = Field(..., description="Whether an alert is required")
    recommended_action: str = Field(..., description="Operational emergency guidelines")
    confidence: float = Field(default=0.9, description="Confidence score of the identification")
    is_realtime_query: bool = Field(default=False, description="Whether query asks for unverified live real-time conditions")
    is_safety_warning: bool = Field(default=False, description="Flag for real-time safety disclaimer")

class AlertPayload(BaseModel):
    alert_id: str
    region: str
    disaster_type: str
    severity: str
    risk_score: int
    status: str
    message: str
    recommended_action: str
    timestamp: str
    disclaimer: str
    cap_xml: Optional[str] = None

class DecisionTraceStep(BaseModel):
    stage: str  # OBSERVE, ANALYZE, LOCATE, DECIDE, ACT
    title: str
    detail: str
    status: str  # COMPLETED, WARNING, INFO
    timestamp: str
    tool_name: Optional[str] = None
    tool_output_summary: Optional[str] = None

class LiveWeatherReport(BaseModel):
    status: str
    query_location: str
    resolved_location: str
    area_name: str
    region: str
    country: str
    temperature_c: float
    temperature_f: float
    feels_like_c: float
    condition: str
    humidity_percent: int
    wind_speed_kmph: float
    wind_direction: str
    wind_gust_kmph: float
    precipitation_mm: float
    cloud_cover_percent: int
    uv_index: int
    pressure_mb: int
    is_severe: bool = False
    severe_warning: Optional[str] = None
    meteorological_risk_level: str = "LOW"
    source_provider: str
    source_url: str
    scraped_at: str

class ChatResponse(BaseModel):
    agent: str = "RAKSHAK AI"
    status: str = "processed"
    user_message: str
    analysis: DisasterAnalysis
    alert: Optional[AlertPayload] = None
    notification_preview: Optional[Dict[str, Any]] = None
    regional_hazard_profile: Optional[RegionalHazardProfile] = None
    live_weather: Optional[LiveWeatherReport] = None
    live_seismic_feed: Optional[Dict[str, Any]] = None
    dynamic_gis: Optional[Dict[str, Any]] = None
    decision_trace: List[str]
    structured_trace: List[DecisionTraceStep]
    tool_executions: List[ToolExecutionLog] = []
    reply_text: str

class NotificationTestRequest(BaseModel):
    region: str
    disaster_type: str
    severity: str
    message: str
    channels: Optional[List[str]] = ["DEMO_SMS", "BROADCAST_SIREN", "EOC_WEBHOOK"]

class NotificationResult(BaseModel):
    channel: str
    recipient_group: str
    status: str
    dispatched_at: str
    payload_sample: str

class NotificationTestResponse(BaseModel):
    alert_id: str
    dispatched_channels: List[NotificationResult]
    summary: str
