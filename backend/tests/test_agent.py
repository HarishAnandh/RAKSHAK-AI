import asyncio
from agents.rakshak_agent import RakshakAgent
from tools.disaster_tool import DisasterAnalysisTool
from tools.region_tool import RegionIdentificationTool

def test_region_identification():
    region_tool = RegionIdentificationTool()
    name, meta, conf = region_tool.identify_region("Heavy flood in Chennai today")
    assert name == "Chennai"
    assert meta["district"] == "Chennai"
    assert conf > 0.8

    name, meta, conf = region_tool.identify_region("Severe storm in Madurai")
    assert name == "Madurai"

    name, meta, conf = region_tool.identify_region("Cyclone near Cuddalore coast")
    assert name == "Cuddalore"

    name, meta, conf = region_tool.identify_region("Something happened in London")
    assert name is None
    assert conf == 0.0

def test_disaster_detection():
    disaster_tool = DisasterAnalysisTool()
    dtype, conf = disaster_tool.detect_disaster("Heavy flooding has been reported")
    assert dtype == "Flood"
    assert conf > 0.8

    dtype, conf = disaster_tool.detect_disaster("Massive forest fire spreading")
    assert dtype == "Fire"

    dtype, conf = disaster_tool.detect_disaster("Earthquake tremors felt")
    assert dtype == "Earthquake"

    dtype, conf = disaster_tool.detect_disaster("Sunny weather and nice breeze")
    assert dtype == "Unknown"

def test_risk_calculation():
    disaster_tool = DisasterAnalysisTool()
    res = disaster_tool.calculate_risk("Flood", "Heavy flooding reported")
    assert res["risk_score"] >= 70
    assert res["severity"] in ["HIGH", "CRITICAL"]
    assert res["alert_required"] is True

    res_mild = disaster_tool.calculate_risk("Flood", "minor light flooding receding")
    assert res_mild["risk_score"] < 70

def test_agent_flood_chennai():
    agent = RakshakAgent()
    res = asyncio.run(agent.process_event("Heavy flooding has been reported in Chennai"))
    assert res.analysis.disaster_type == "Flood"
    assert res.analysis.location == "Chennai"
    assert res.analysis.risk_score >= 70
    assert res.analysis.alert_required is True
    assert res.alert is not None
    assert res.alert.status == "ALERT GENERATED"
    assert len(res.decision_trace) >= 5
    assert len(res.structured_trace) >= 5

def test_agent_safety_rule():
    agent = RakshakAgent()
    res = asyncio.run(agent.process_event("Is Chennai currently flooding?"))
    assert res.analysis.is_safety_warning is True
    assert "I cannot verify real-time conditions" in res.reply_text
    assert res.alert is None

def test_agent_unknown_region():
    agent = RakshakAgent()
    res = asyncio.run(agent.process_event("Severe earthquake detected in Tokyo"))
    assert res.analysis.location == "Region could not be confidently identified"
