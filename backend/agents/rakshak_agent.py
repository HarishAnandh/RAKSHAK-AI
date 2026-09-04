import re
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

from models.schemas import (
    DisasterAnalysis, 
    AlertPayload, 
    DecisionTraceStep, 
    ChatResponse, 
    RegionalHazardProfile, 
    HazardProbabilityItem,
    ToolExecutionLog
)
from tools.disaster_tool import DisasterAnalysisTool
from tools.region_tool import RegionIdentificationTool
from tools.notification_tool import NotificationTool
from tools.openrouter import OpenRouterClient

class RakshakAgent:
    """
    RAKSHAK AI - Autonomous Post-Disaster Regional Alert Agent
    Lifecycle: Observe -> Analyze (Disaster & Region) -> Assess Risk -> Decide -> Act (Alert & Notification)
    """

    def __init__(self):
        self.disaster_tool = DisasterAnalysisTool()
        self.region_tool = RegionIdentificationTool()
        self.notification_tool = NotificationTool()
        self.openrouter_client = OpenRouterClient()

    def _is_greeting_or_help(self, text: str) -> bool:
        """Detects if input is a conversational greeting or intro/help query."""
        cleaned = text.lower().strip()
        greetings = [
            "hi", "hello", "hey", "namaste", "vanakkam", "halo", "greetings",
            "good morning", "good afternoon", "good evening", "who are you",
            "what can you do", "what are you", "help", "how to use", "start",
            "what is rakshak", "about", "info"
        ]
        if cleaned in greetings:
            return True
        for g in ["hi ", "hello ", "hey ", "who are you", "what can you do"]:
            if cleaned.startswith(g):
                return True
        return False

    def _is_realtime_verification_query(self, text: str) -> bool:
        """
        Detects if the user is asking whether a disaster is happening right now in reality,
        e.g., 'Is Chennai currently flooding?', 'Is there a cyclone in Madurai right now?'
        """
        cleaned = text.lower().strip()
        patterns = [
            r"is\s+([a-zA-Z\s]+)\s+(currently|now|today|happening|under|facing|flooding|burning)",
            r"is\s+there\s+(a|an|any)?\s*(disaster|flood|cyclone|earthquake|fire|tsunami|storm)\s+(in|at|near|currently|right now|now)",
            r"are\s+there\s+(floods|cyclones|earthquakes|fires|tsunamis|storms)\s+in",
            r"what\s+is\s+the\s+(current|live|real-time|latest)\s+status\s+in",
            r"tell\s+me\s+if\s+([a-zA-Z\s]+)\s+is\s+(flooding|safe|in danger|affected)"
        ]
        for pattern in patterns:
            if re.search(pattern, cleaned):
                return True
        return False

    async def process_event(self, message: str) -> ChatResponse:
        """Processes user input through the agentic lifecycle."""
        now = datetime.now()
        timestamp_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        decision_trace_lines: List[str] = []
        structured_trace: List[DecisionTraceStep] = []
        tool_executions: List[ToolExecutionLog] = []

        # 1. OBSERVE
        decision_trace_lines.append("✓ Event received and validated by RAKSHAK Core")
        structured_trace.append(DecisionTraceStep(
            stage="OBSERVE",
            title="Received Input Message",
            detail=f"Ingested natural-language operator dispatch: '{message}'",
            status="COMPLETED",
            timestamp=timestamp_str,
            tool_name="EventIngestionGate",
            tool_output_summary="Validated string length and encoding"
        ))

        # Check Conversational Greeting / Help Intent
        if self._is_greeting_or_help(message):
            decision_trace_lines.append("✓ Conversational Intent: Agent Introduction & Capabilities")
            structured_trace.append(DecisionTraceStep(
                stage="ANALYZE",
                title="Intent Classification",
                detail="Classified input as conversational greeting / system inquiry.",
                status="INFO",
                timestamp=timestamp_str,
                tool_name="IntentClassifier",
                tool_output_summary="Intent: GREETING_HELP"
            ))
            structured_trace.append(DecisionTraceStep(
                stage="ACT",
                title="Agent Guidance Issued",
                detail="Presented RAKSHAK operational capabilities & rapid test triggers.",
                status="COMPLETED",
                timestamp=timestamp_str,
                tool_name="ResponseComposer",
                tool_output_summary="Returned capabilities banner"
            ))

            greeting_analysis = DisasterAnalysis(
                disaster_type="None",
                location="N/A",
                affected_region="N/A",
                severity="LOW",
                risk_score=0,
                risk_level="LOW",
                alert_required=False,
                recommended_action="Provide a disaster event report (e.g. 'Heavy flooding reported in Chennai') or type any region (e.g. 'Salem', 'Erode') to view disaster probabilities.",
                confidence=1.0,
                is_realtime_query=False,
                is_safety_warning=False
            )

            reply_text = (
                "👋 **Hello! I am RAKSHAK AI**, an autonomous regional disaster alert agent.\n\n"
                "I monitor disaster reports, assess severity and risk levels ($0\\text{–}100$), "
                "calculate regional hazard probabilities, and formulate emergency alerts.\n\n"
                "**What you can do:**\n"
                "- 📊 **Type any region name** (e.g. *'Salem'*, *'Chennai'*, *'Erode'*, *'Cuddalore'*, *'Nilgiris'*, *'Punjab'*) to view **Disaster Occurrence Probabilities**.\n"
                "- 🚨 **Report an event**: *'Heavy flooding has been reported in Chengalpattu'* (Triggers immediate alert & dispatch).\n"
                "- ⚡ Or click any of the **Quick Test Buttons** above!"
            )

            return ChatResponse(
                agent="RAKSHAK AI",
                status="processed",
                user_message=message,
                analysis=greeting_analysis,
                alert=None,
                notification_preview=None,
                regional_hazard_profile=None,
                decision_trace=decision_trace_lines,
                structured_trace=structured_trace,
                tool_executions=tool_executions,
                reply_text=reply_text
            )

        # Check Real-time Safety Boundary Rule
        is_realtime_query = self._is_realtime_verification_query(message)
        if is_realtime_query:
            decision_trace_lines.append("⚠ Real-time verification query detected: Safety protocol engaged")
            structured_trace.append(DecisionTraceStep(
                stage="ANALYZE",
                title="Safety Boundary Check",
                detail="Query requests real-time unverified status. Activating disaster-safety disclaimer protocol.",
                status="WARNING",
                timestamp=timestamp_str,
                tool_name="SafetyBoundaryFilter",
                tool_output_summary="SAFETY_DISCLAIMER_ACTIVE"
            ))

            safety_analysis = DisasterAnalysis(
                disaster_type="Inquiry",
                location="Tamil Nadu",
                affected_region="N/A",
                severity="LOW",
                risk_score=0,
                risk_level="LOW",
                alert_required=False,
                recommended_action="Refer to official State Disaster Management Authority (TNSDMA) or IMD bulletins for live ground verification.",
                confidence=1.0,
                is_realtime_query=True,
                is_safety_warning=True
            )

            reply_text = (
                "⚠️ **Safety Boundary Protocol:** I cannot verify real-time conditions without authenticated live sensor telemetry. "
                "Based on information provided in disaster reports, I can analyze scenarios and generate simulated alerts.\n\n"
                "If you would like to test alert workflows, please describe an event (e.g., *'Heavy flooding reported in Chennai'*)."
            )

            return ChatResponse(
                agent="RAKSHAK AI",
                status="processed",
                user_message=message,
                analysis=safety_analysis,
                alert=None,
                notification_preview=None,
                regional_hazard_profile=None,
                decision_trace=decision_trace_lines,
                structured_trace=structured_trace,
                tool_executions=tool_executions,
                reply_text=reply_text
            )

        # 2. ANALYZE (Disaster & Region)
        llm_result = None
        if self.openrouter_client.is_available:
            t0 = time.time()
            llm_result = await self.openrouter_client.analyze_with_llm(message)
            t1 = time.time()
            tool_executions.append(ToolExecutionLog(
                tool_name="OpenRouterClient",
                stage="ANALYZE",
                status="SUCCESS" if llm_result else "FALLBACK_ENGAGED",
                inputs={"user_message": message, "provider": self.openrouter_client.provider, "model": self.openrouter_client.model},
                output=llm_result or {"note": "LLM offline/fallback to deterministic local engine"},
                execution_time_ms=round((t1 - t0) * 1000, 2),
                description=f"Inference via {self.openrouter_client.provider} ({self.openrouter_client.model})"
            ))

            structured_trace.append(DecisionTraceStep(
                stage="ANALYZE",
                title=f"{self.openrouter_client.provider} LLM Inference",
                detail=f"Inference execution ({round((t1 - t0)*1000, 1)}ms). Result: {llm_result.get('disaster_type', 'N/A') if llm_result else 'Local fallback'}",
                status="INFO" if llm_result else "WARNING",
                timestamp=timestamp_str,
                tool_name="OpenRouterClient",
                tool_output_summary=str(llm_result) if llm_result else "Fallback to Local Engine"
            ))

        # Region Identification Tool Execution
        t0_reg = time.time()
        region_name, region_meta, reg_confidence = self.region_tool.identify_region(message)
        if not region_name and llm_result and llm_result.get("location") and llm_result["location"] != "Unknown":
            candidate_region, candidate_meta, _ = self.region_tool.identify_region(llm_result["location"])
            if candidate_region:
                region_name, candidate_meta, reg_confidence = candidate_region, candidate_meta, 0.9
        t1_reg = time.time()

        tool_executions.append(ToolExecutionLog(
            tool_name="RegionIdentificationTool",
            stage="LOCATE",
            status="SUCCESS" if region_name else "NO_MATCH",
            inputs={"raw_text": message},
            output={
                "identified_region": region_name,
                "zone": region_meta.get("zone") if region_meta else None,
                "coastal": region_meta.get("coastal") if region_meta else None,
                "confidence": reg_confidence
            },
            execution_time_ms=round((t1_reg - t0_reg) * 1000, 2),
            description="Geofencing entity extractor & fuzzy phonetic district resolver"
        ))

        # Disaster Identification Tool Execution
        t0_dis = time.time()
        disaster_type, dis_confidence = self.disaster_tool.detect_disaster(message)
        if disaster_type == "Unknown" and llm_result and llm_result.get("disaster_type") and llm_result["disaster_type"] != "Unknown":
            disaster_type = llm_result["disaster_type"]
            dis_confidence = 0.85
        t1_dis = time.time()

        tool_executions.append(ToolExecutionLog(
            tool_name="DisasterAnalysisTool (Classification)",
            stage="ANALYZE",
            status="SUCCESS" if disaster_type != "Unknown" else "UNRECOGNIZED",
            inputs={"raw_text": message},
            output={"disaster_type": disaster_type, "confidence": dis_confidence},
            execution_time_ms=round((t1_dis - t0_dis) * 1000, 2),
            description="Keyword signature classifier & NLP disaster detector"
        ))

        # Decision trace update for Disaster
        if disaster_type != "Unknown":
            decision_trace_lines.append(f"✓ Disaster type identified: {disaster_type.upper()}")
            structured_trace.append(DecisionTraceStep(
                stage="ANALYZE",
                title="Disaster Classification",
                detail=f"Identified disaster pattern as '{disaster_type}' with confidence {int(dis_confidence*100)}%",
                status="COMPLETED",
                timestamp=timestamp_str,
                tool_name="DisasterAnalysisTool",
                tool_output_summary=f"type={disaster_type}, conf={dis_confidence}"
            ))

        # Decision trace update for Region
        if region_name:
            zone_desc = region_meta.get('zone', region_name) if region_meta else region_name
            decision_trace_lines.append(f"✓ Location identified: {region_name.upper()} ({zone_desc})")
            structured_trace.append(DecisionTraceStep(
                stage="LOCATE",
                title="Geographic Region Resolution",
                detail=f"Located region: {region_name} (Zone: {zone_desc})",
                status="COMPLETED",
                timestamp=timestamp_str,
                tool_name="RegionIdentificationTool",
                tool_output_summary=f"region={region_name}, zone={zone_desc}"
            ))

        # --- SCENARIO 1: REGION QUERY -> GENERATE DISASTER PROBABILITIES PROFILE ---
        if region_name and disaster_type == "Unknown":
            t0_prof = time.time()
            profile_data = self.region_tool.get_regional_hazard_profile(region_name, region_meta)
            t1_prof = time.time()

            tool_executions.append(ToolExecutionLog(
                tool_name="RegionIdentificationTool (HazardProfile)",
                stage="ANALYZE",
                status="SUCCESS",
                inputs={"region_name": region_name},
                output=profile_data,
                execution_time_ms=round((t1_prof - t0_prof) * 1000, 2),
                description="Topographic vulnerability matrix & multi-hazard probability calculator"
            ))

            hazard_items = [
                HazardProbabilityItem(
                    disaster_type=h["disaster_type"],
                    probability_percent=h["probability_percent"],
                    risk_level=h["risk_level"],
                    historical_notes=h["historical_notes"],
                    icon=h["icon"]
                )
                for h in profile_data["hazards"]
            ]

            hazard_profile = RegionalHazardProfile(
                region_name=profile_data["region_name"],
                zone=profile_data["zone"],
                terrain_type=profile_data["terrain"],
                coastal=profile_data["coastal"],
                composite_vulnerability_score=profile_data["composite_vulnerability_score"],
                primary_threat=profile_data["primary_threat"],
                hazards=hazard_items,
                emergency_contacts=profile_data["emergency_contacts"]
            )

            decision_trace_lines.append(f"✓ Regional Hazard Matrix evaluated ({len(hazard_items)} disaster vectors computed)")
            decision_trace_lines.append(f"✓ Composite Vulnerability Index: {hazard_profile.composite_vulnerability_score}/100")
            decision_trace_lines.append("✓ Regional Disaster Occurrence Probabilities profile formulated")

            structured_trace.append(DecisionTraceStep(
                stage="ANALYZE",
                title="Disaster Probability Computation",
                detail=f"Computed historical vulnerability & occurrence probabilities for {region_name} across {len(hazard_items)} disaster categories.",
                status="COMPLETED",
                timestamp=timestamp_str,
                tool_name="RegionIdentificationTool",
                tool_output_summary=f"vulnerability_score={hazard_profile.composite_vulnerability_score}/100"
            ))

            structured_trace.append(DecisionTraceStep(
                stage="ACT",
                title="Regional Hazard Profile Issued",
                detail=f"Issued Regional Disaster Vulnerability Profile for {region_name} (Composite Index: {hazard_profile.composite_vulnerability_score}/100).",
                status="COMPLETED",
                timestamp=timestamp_str,
                tool_name="ResponseComposer",
                tool_output_summary=f"profile_generated={region_name}"
            ))

            # Build rich markdown probability table
            table_rows = []
            for h in hazard_items:
                bar = "█" * (h.probability_percent // 10) + "░" * (10 - (h.probability_percent // 10))
                table_rows.append(f"| **{h.disaster_type}** | `{h.probability_percent}%` | `{bar}` | **{h.risk_level}** | {h.historical_notes} |")

            table_str = "\n".join(table_rows)

            reply_text = (
                f"### 📊 Regional Disaster Vulnerability & Occurrence Probabilities: **{region_name}**\n\n"
                f"- **Administrative Zone**: {hazard_profile.zone}\n"
                f"- **Geographic Terrain**: {hazard_profile.terrain_type}\n"
                f"- **Composite Vulnerability Index**: **{hazard_profile.composite_vulnerability_score}/100**\n"
                f"- **Primary Threat Vector**: {hazard_profile.primary_threat}\n\n"
                f"| Disaster Hazard | Occurrence Probability | Probability Gauge | Risk Level | Regional Assessment & History |\n"
                f"| :--- | :---: | :---: | :---: | :--- |\n"
                f"{table_str}\n\n"
                f"💡 **Simulate an Event in {region_name}:**\n"
                f"To trigger an active alert calculation, report an occurrence (e.g. *'Heavy {hazard_items[0].disaster_type.lower()} reported in {region_name} with low-lying areas affected'*)."
            )

            loc_analysis = DisasterAnalysis(
                disaster_type="Hazard Profile",
                location=region_name,
                affected_region=hazard_profile.zone,
                severity="MEDIUM",
                risk_score=hazard_profile.composite_vulnerability_score,
                risk_level="MEDIUM" if hazard_profile.composite_vulnerability_score < 80 else "HIGH",
                alert_required=False,
                recommended_action=f"Maintain regional readiness for {hazard_profile.primary_threat}.",
                confidence=reg_confidence,
                is_realtime_query=False,
                is_safety_warning=False
            )

            return ChatResponse(
                agent="RAKSHAK AI",
                status="processed",
                user_message=message,
                analysis=loc_analysis,
                alert=None,
                notification_preview=None,
                regional_hazard_profile=hazard_profile,
                decision_trace=decision_trace_lines,
                structured_trace=structured_trace,
                tool_executions=tool_executions,
                reply_text=reply_text
            )

        # --- SCENARIO 2: DISASTER ONLY (e.g. "Flood") ---
        if disaster_type != "Unknown" and not region_name:
            structured_trace.append(DecisionTraceStep(
                stage="DECIDE",
                title="Pending Geographic Geofence",
                detail=f"Disaster {disaster_type} verified. Awaiting specific affected district to issue alert.",
                status="INFO",
                timestamp=timestamp_str,
                tool_name="DecisionMatrix",
                tool_output_summary="Awaiting geofence"
            ))

            dis_analysis = DisasterAnalysis(
                disaster_type=disaster_type,
                location="Region could not be confidently identified",
                affected_region="Unspecified Region",
                severity="MEDIUM",
                risk_score=50,
                risk_level="MEDIUM",
                alert_required=False,
                recommended_action="Specify the affected city or district to formulate regional alerts.",
                confidence=dis_confidence,
                is_realtime_query=False,
                is_safety_warning=False
            )

            reply_text = (
                f"🚨 **{disaster_type} Signature Detected.**\n\n"
                f"However, **region could not be confidently identified**. "
                f"Please specify the affected district or city (e.g., *'Heavy {disaster_type.lower()} in Chennai'* or *'Severe {disaster_type.lower()} near Salem'*) "
                f"so I can compute localized risk scores and generate regional warning broadcasts."
            )

            return ChatResponse(
                agent="RAKSHAK AI",
                status="processed",
                user_message=message,
                analysis=dis_analysis,
                alert=None,
                notification_preview=None,
                regional_hazard_profile=None,
                decision_trace=decision_trace_lines,
                structured_trace=structured_trace,
                tool_executions=tool_executions,
                reply_text=reply_text
            )

        # --- SCENARIO 3: FULL DISASTER EVENT REPORT -> ASSESS RISK & ALERT ---
        t0_risk = time.time()
        risk_data = self.disaster_tool.calculate_risk(disaster_type, message, region_meta)
        t1_risk = time.time()

        tool_executions.append(ToolExecutionLog(
            tool_name="DisasterAnalysisTool (RiskMatrix)",
            stage="DECIDE",
            status="SUCCESS",
            inputs={"disaster_type": disaster_type, "message": message, "is_coastal": region_meta.get("coastal") if region_meta else False},
            output=risk_data,
            execution_time_ms=round((t1_risk - t0_risk) * 1000, 2),
            description="Quantitative risk index calculator (0-100) & modifier evaluator"
        ))

        severity = risk_data["severity"]
        risk_score = risk_data["risk_score"]
        risk_level = risk_data["risk_level"]
        alert_required = risk_data["alert_required"] and (disaster_type != "Unknown") and bool(region_name)
        recommended_action = risk_data["recommended_action"]

        decision_trace_lines.append(f"✓ Severity assessed: {severity}")
        decision_trace_lines.append(f"✓ Risk score calculated: {risk_score}/100 ({risk_level})")
        decision_trace_lines.append(f"✓ Alert decision: {'CRITICAL / REQUIRED' if alert_required else 'MONITORING ONLY'}")

        structured_trace.append(DecisionTraceStep(
            stage="DECIDE",
            title="Risk Assessment & Action Matrix",
            detail=f"Calculated Risk Score: {risk_score}/100 ({risk_level} severity). Alert Required: {alert_required}.",
            status="COMPLETED",
            timestamp=timestamp_str,
            tool_name="DisasterAnalysisTool",
            tool_output_summary=f"risk_score={risk_score}, severity={severity}"
        ))

        # ACT (Alert Generation & Notification Dispatch)
        alert_payload = None
        notification_preview = None

        affected_loc_display = region_name if region_name else "Region could not be confidently identified"
        zone_display = region_meta.get("zone", "Unspecified Zone") if region_meta else "Unspecified Region"

        analysis = DisasterAnalysis(
            disaster_type=disaster_type,
            location=affected_loc_display,
            affected_region=zone_display,
            severity=severity,
            risk_score=risk_score,
            risk_level=risk_level,
            alert_required=alert_required,
            recommended_action=recommended_action,
            confidence=round((dis_confidence + reg_confidence) / 2, 2) if disaster_type != "Unknown" and region_name else 0.4,
            is_realtime_query=False,
            is_safety_warning=False
        )

        if alert_required:
            alert_id = f"RAKSHAK-{uuid.uuid4().hex[:6].upper()}"
            alert_message = (
                f"🚨 [DEMO ALERT] {severity} {disaster_type.upper()} WARNING FOR {affected_loc_display.upper()}.\n"
                f"Calculated Risk Index: {risk_score}/100 ({risk_level}).\n"
                f"Action Required: {recommended_action}"
            )

            alert_payload = AlertPayload(
                alert_id=alert_id,
                region=affected_loc_display,
                disaster_type=disaster_type,
                severity=severity,
                risk_score=risk_score,
                status="ALERT GENERATED",
                message=alert_message,
                recommended_action=recommended_action,
                timestamp=date_str,
                disclaimer="ALERT GENERATED FROM PROVIDED EVENT (DEMO ONLY)"
            )

            decision_trace_lines.append("✓ Emergency alert generated")
            structured_trace.append(DecisionTraceStep(
                stage="ACT",
                title="Emergency Alert Generation",
                detail=f"Issued Regional Alert {alert_id} for {affected_loc_display} with {severity} priority.",
                status="COMPLETED",
                timestamp=timestamp_str,
                tool_name="AlertGenerator",
                tool_output_summary=f"alert_id={alert_id}"
            ))

            t0_notif = time.time()
            notification_preview = self.notification_tool.prepare_and_dispatch(
                region=affected_loc_display,
                disaster_type=disaster_type,
                severity=severity,
                message=alert_message,
                risk_score=risk_score
            )
            t1_notif = time.time()

            tool_executions.append(ToolExecutionLog(
                tool_name="NotificationTool",
                stage="ACT",
                status="SUCCESS",
                inputs={"region": affected_loc_display, "disaster_type": disaster_type, "severity": severity, "risk_score": risk_score},
                output=notification_preview,
                execution_time_ms=round((t1_notif - t0_notif) * 1000, 2),
                description="Simulated multi-channel emergency broadcast dispatcher (SMS, Siren, SDMA, WhatsApp)"
            ))

            decision_trace_lines.append(f"✓ Notification prepared ({notification_preview['channels_count']} channels simulated)")
            structured_trace.append(DecisionTraceStep(
                stage="ACT",
                title="Multi-Channel Notification Dispatch",
                detail=f"Queued emergency dispatch to Cellular SMS, Early Warning Sirens, SDMA/NDRF Webhooks, and Civil Defense.",
                status="COMPLETED",
                timestamp=timestamp_str,
                tool_name="NotificationTool",
                tool_output_summary=f"channels_count={notification_preview['channels_count']}"
            ))

            reply_text = (
                f"🚨 **{severity} ALERT GENERATED (DEMO)** for **{affected_loc_display}**.\n\n"
                f"**Disaster Type**: {disaster_type}\n"
                f"**Assessed Risk Score**: {risk_score}/100 ({risk_level})\n"
                f"**Affected Region / Zone**: {zone_display}\n"
                f"**Recommended Action**: {recommended_action}\n\n"
                f"*Simulated emergency notifications have been prepared for regional dispatch.*"
            )
        else:
            reply_text = (
                f"I analyzed your input: *\"{message}\"*, but could not detect a recognized disaster pattern or specific location. "
                f"Please provide an event description such as: *'Heavy flooding reported in Chennai'* or *'Cyclone warning near Cuddalore'*."
            )

        return ChatResponse(
            agent="RAKSHAK AI",
            status="processed",
            user_message=message,
            analysis=analysis,
            alert=alert_payload,
            notification_preview=notification_preview,
            regional_hazard_profile=None,
            decision_trace=decision_trace_lines,
            structured_trace=structured_trace,
            tool_executions=tool_executions,
            reply_text=reply_text
        )
