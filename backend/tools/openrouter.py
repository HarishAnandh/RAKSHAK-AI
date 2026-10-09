import os
import json
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Ensure .env is always loaded
load_dotenv()

class OpenRouterClient:
    """Client for LLM Inference (Auto-detects Hugging Face & OpenRouter) with transparent diagnostics."""

    def __init__(self):
        load_dotenv()
        # Check Hugging Face tokens and OpenRouter tokens
        self.hf_token = os.getenv("HUGGINGFACE_API_KEY", "").strip() or os.getenv("HF_TOKEN", "").strip()
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.last_error: Optional[str] = None

        # If OPENROUTER_API_KEY starts with hf_, treat it as a Hugging Face token
        if self.openrouter_key.startswith("hf_"):
            self.hf_token = self.openrouter_key
            self.openrouter_key = ""

        if self.hf_token:
            self.provider = "Hugging Face"
            self.api_key = self.hf_token
            self.model = os.getenv("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct")
            self.base_url = "https://router.huggingface.co/hf-inference/v1/chat/completions"
        elif self.openrouter_key:
            self.provider = "OpenRouter"
            self.api_key = self.openrouter_key
            self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
            self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        else:
            self.provider = "None"
            self.api_key = ""
            self.model = ""
            self.base_url = ""

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def analyze_with_llm(self, user_message: str) -> Optional[Dict[str, Any]]:
        """
        Sends the message to LLM for structured disaster extraction.
        Returns parsed JSON dict or None with transparent error logging.
        """
        if not self.is_available:
            self.last_error = "No API key configured in .env"
            return None

        prompt = f"""You are RAKSHAK AI, an autonomous disaster response agent.
Analyze the following user report:
"{user_message}"

Extract the following JSON format strictly:
{{
  "is_realtime_verification_query": boolean,
  "disaster_type": string ("Flood", "Cyclone", "Earthquake", "Fire", "Landslide", "Tsunami", "Storm", or "Unknown"),
  "location": string (Detected city, district, or "Unknown"),
  "severity": string ("LOW", "MEDIUM", "HIGH", "CRITICAL"),
  "risk_score": integer (0 to 100),
  "risk_level": string ("LOW", "MEDIUM", "HIGH", "CRITICAL"),
  "alert_required": boolean,
  "recommended_action": string,
  "summary_message": string
}}
Return ONLY raw valid JSON."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if self.provider == "OpenRouter":
            headers["HTTP-Referer"] = "https://rakshak.ai"
            headers["X-Title"] = "RAKSHAK AI Disaster Alert Agent"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a precise disaster alert extraction engine. Output strictly raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 450
        }

        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                response = await client.post(self.base_url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    # Clean possible markdown code fences
                    if content.startswith("```"):
                        content = content.strip("`")
                        if content.startswith("json"):
                            content = content[4:].strip()
                    parsed = json.loads(content)
                    self.last_error = None
                    return parsed
                else:
                    self.last_error = f"HTTP {response.status_code} ({response.text[:100]})"
                    return None
        except Exception as e:
            self.last_error = f"Network/Parser Error: {str(e)}"
            return None
