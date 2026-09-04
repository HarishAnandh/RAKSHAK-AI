import re
from typing import Dict, Any, Tuple, List, Optional

DISASTER_CONFIG: Dict[str, Dict[str, Any]] = {
    "Flood": {
        "keywords": ["flood", "flooding", "waterlogging", "submerged", "inundated", "waterlogged", "deluge", "overflowing", "flash flood"],
        "base_risk": 65,
        "default_action": "Move to higher ground, avoid wading in floodwaters, disconnect electrical appliances, and monitor local disaster alerts."
    },
    "Cyclone": {
        "keywords": ["cyclone", "hurricane", "typhoon", "cyclonic storm", "depression in bay of bengal", "gale"],
        "base_risk": 75,
        "default_action": "Stay indoors away from windows, secure loose rooftop items, keep emergency kit ready, and follow evacuation advisories."
    },
    "Earthquake": {
        "keywords": ["earthquake", "tremor", "quake", "aftershock", "seismic", "richter scale", "ground shaking"],
        "base_risk": 70,
        "default_action": "Drop, Cover, and Hold on. Move away from glass and unreinforced masonry. If outdoors, move to an open area away from buildings."
    },
    "Fire": {
        "keywords": ["fire", "forest fire", "wildfire", "blaze", "inferno", "flames", "smoke explosion", "burn"],
        "base_risk": 65,
        "default_action": "Evacuate immediately via designated emergency exits. Call Fire Emergency (101). Do not use elevators."
    },
    "Landslide": {
        "keywords": ["landslide", "mudslide", "rockfall", "slope collapse", "debris flow", "hill collapse"],
        "base_risk": 70,
        "default_action": "Evacuate hillside and slope zones immediately. Avoid river valleys and low-lying pathways susceptible to mudflow."
    },
    "Tsunami": {
        "keywords": ["tsunami", "tidal wave", "harbor wave", "ocean surge", "sea water ingress"],
        "base_risk": 85,
        "default_action": "Immediately evacuate coastal zones. Move at least 2 km inland or to heights above 30 meters immediately."
    },
    "Storm": {
        "keywords": ["storm", "thunderstorm", "heavy rain", "downpour", "lightning", "squall", "cloudburst", "gusty winds", "hailstorm"],
        "base_risk": 55,
        "default_action": "Seek sturdy indoor shelter, avoid sheltering under isolated trees, unplug non-essential electronics, and avoid water bodies."
    }
}

SEVERITY_MODIFIERS = {
    # Critical (+20 to +30)
    "catastrophic": 30, "devastating": 25, "emergency": 20, "red alert": 25, "severe": 20,
    "massive": 20, "critical": 20, "life-threatening": 25, "evacuation ordered": 25,
    
    # High (+10 to +15)
    "heavy": 15, "major": 15, "flash": 15, "warning": 12, "high": 12, "submerged": 15,
    "destroyed": 15, "spreading": 14, "deadly": 15, "orange alert": 15,
    
    # Medium (0 to +8)
    "moderate": 5, "yellow alert": 5, "rising": 8, "continuous": 7, "gusts": 6,
    
    # Low / Mild (-15 to -25)
    "minor": -20, "light": -20, "mild": -18, "isolated": -15, "small": -15, "controlled": -20,
    "low risk": -25, "receding": -20
}

class DisasterAnalysisTool:
    """Tool for deterministic or assisted disaster categorization and risk scoring."""

    def __init__(self):
        self.disaster_config = DISASTER_CONFIG
        self.severity_modifiers = SEVERITY_MODIFIERS

    def detect_disaster(self, text: str) -> Tuple[Optional[str], float]:
        """Detects disaster type from input text."""
        cleaned = text.lower()
        matched_type = None
        highest_score = 0

        for dtype, config in self.disaster_config.items():
            for kw in config["keywords"]:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, cleaned):
                    # Longer matching keyword gets higher weight
                    score = len(kw)
                    if score > highest_score:
                        highest_score = score
                        matched_type = dtype

        if matched_type:
            return matched_type, 0.95
        return "Unknown", 0.0

    def calculate_risk(self, disaster_type: str, text: str, location_meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Calculates risk score (0-100), risk level, severity, and action.
        LOW: 0–39
        MEDIUM: 40–69
        HIGH: 70–89
        CRITICAL: 90–100
        """
        cleaned = text.lower()
        
        if disaster_type == "Unknown":
            return {
                "severity": "LOW",
                "risk_score": 15,
                "risk_level": "LOW",
                "alert_required": False,
                "recommended_action": "Monitor news channels and maintain general vigilance."
            }

        base = self.disaster_config[disaster_type]["base_risk"]
        modifier_sum = 0
        matched_modifiers = []

        for mod_word, weight in self.severity_modifiers.items():
            pattern = r'\b' + re.escape(mod_word) + r'\b'
            if re.search(pattern, cleaned):
                modifier_sum += weight
                matched_modifiers.append(mod_word)

        # Contextual boosts (e.g. Coastal region + Tsunami / Cyclone)
        if location_meta and location_meta.get("coastal") and disaster_type in ["Cyclone", "Tsunami", "Storm"]:
            modifier_sum += 8

        # Cap modifier effect
        final_score = base + modifier_sum
        final_score = max(5, min(100, final_score))

        # Risk level determination
        if final_score >= 90:
            risk_level = "CRITICAL"
            severity = "CRITICAL"
        elif final_score >= 70:
            risk_level = "HIGH"
            severity = "HIGH"
        elif final_score >= 40:
            risk_level = "MEDIUM"
            severity = "MEDIUM"
        else:
            risk_level = "LOW"
            severity = "LOW"

        # Alert required if MEDIUM, HIGH, or CRITICAL (score >= 40)
        alert_required = final_score >= 40
        action = self.disaster_config[disaster_type]["default_action"]

        if severity == "CRITICAL":
            action = "IMMEDIATE EMERGENCY EVACUATION: " + action
        elif severity == "HIGH":
            action = "HIGH ALERT: " + action

        return {
            "severity": severity,
            "risk_score": final_score,
            "risk_level": risk_level,
            "alert_required": alert_required,
            "recommended_action": action,
            "modifiers_detected": matched_modifiers
        }
