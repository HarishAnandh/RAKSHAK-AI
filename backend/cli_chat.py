import asyncio
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Safe stream reconfigure
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from agents.rakshak_agent import RakshakAgent

BANNER = """
======================================================================
  [RAKSHAK AI] Autonomous Regional Disaster Alert Agent (Terminal CLI)
======================================================================
  Type any disaster report (e.g. 'Heavy flooding reported in Chennai')
  or type any region name (e.g. 'Salem', 'Erode', 'Cuddalore', 'Punjab')
  Type 'exit' or 'quit' to close.
======================================================================
"""

async def main():
    print(BANNER)
    agent = RakshakAgent()
    provider = agent.openrouter_client.provider if agent.openrouter_client.is_available else "Deterministic Local"
    print(f"[*] Agent Core Online | Provider: {provider} | Supported: {len(agent.region_tool.get_all_regions())} Districts\n")

    while True:
        try:
            user_input = input("\n[Operator Dispatch] > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\n[RAKSHAK] Session terminated. Standing by.")
                break

            print("\n[RAKSHAK] Ingesting event & executing decision lifecycle...\n")
            response = await agent.process_event(user_input)

            # 1. Print Decision Trace
            print("--- AGENT DECISION TRACE ---")
            for step in response.structured_trace:
                status_mark = "[DONE]" if step.status == "COMPLETED" else ("[WARN]" if step.status == "WARNING" else "[INFO]")
                print(f"  {status_mark} [{step.stage}] {step.title}: {step.detail} ({step.timestamp})")

            # 2. Print Analysis & Result
            print("\n--- RAKSHAK AGENT OUTPUT ---")
            print(response.reply_text)

            # 3. Print Alert Payload if alert was generated
            if response.alert:
                print("\n[EMERGENCY DISASTER ALERT ISSUED]")
                print(f"   Alert ID:       {response.alert.alert_id}")
                print(f"   Disaster Type:  {response.alert.disaster_type.upper()}")
                print(f"   Region / Zone:  {response.alert.region.upper()}")
                print(f"   Severity Level: {response.alert.severity}")
                print(f"   Risk Score:     {response.alert.risk_score}/100")
                print(f"   Action:         {response.alert.recommended_action}")
                print(f"   Disclaimer:     {response.alert.disclaimer}")

            # 4. Print Notification Preview if available
            if response.notification_preview:
                print("\n[SIMULATED NOTIFICATION CHANNELS PREPARED]")
                for ch in response.notification_preview.get("dispatched_channels", []):
                    print(f"   * {ch['channel_name']} -> {ch['target']} [{ch['status']}]")

            # 5. Print Hazard Profile if available
            if response.regional_hazard_profile:
                p = response.regional_hazard_profile
                print(f"\n[REGIONAL HAZARD PROFILE: {p.region_name.upper()}]")
                print(f"   Zone:           {p.zone}")
                print(f"   Terrain:        {p.terrain_type}")
                print(f"   Vulnerability:  {p.composite_vulnerability_score}/100")
                print(f"   Primary Threat: {p.primary_threat}")
                print("   Probabilities Breakdown:")
                for h in p.hazards:
                    bar_len = h.probability_percent // 10
                    bar = "=" * bar_len + "-" * (10 - bar_len)
                    print(f"     - {h.disaster_type:<12} {h.probability_percent:>3}% [{bar}] ({h.risk_level}) -> {h.historical_notes}")

            print("\n" + "=" * 70)

        except (KeyboardInterrupt, EOFError):
            print("\n\n[RAKSHAK] Session ended.")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(main())
