# 🛡️ RAKSHAK AI — Autonomous Post-Disaster Regional Alert System

**RAKSHAK AI** is an Agentic AI-powered emergency operations system that autonomously observes natural-language disaster reports, classifies the disaster type, pinpoints the affected geographic region, calculates a quantitative risk index (0–100), makes autonomous alert decisions, and dispatches simulated multi-channel regional warning broadcasts.

---
## API KEYS
HF_TOKEN=hf_xxxxxxxxxxxxxxxxx
HF_MODEL=Qwen/Qwen2.5-72B-Instruct
PORT=8001
## 📌 Problem Statement

During sudden catastrophic events (floods, cyclones, earthquakes, wildfires), emergency response delays are often caused by the time taken to parse chaotic field reports, assess regional severity, determine alert thresholds, and compose multi-channel public warnings. Manual processes create critical communication bottlenecks when minutes save lives.

---

## 💡 Solution

**RAKSHAK AI** acts as an autonomous regional disaster alert agent that implements a closed-loop reasoning pipeline:

$$\text{Observe} \longrightarrow \text{Analyze} \longrightarrow \text{Decide} \longrightarrow \text{Act}$$

- **Zero Hallucination Geofencing**: Confidently matches locations against recognized regional boundaries (initial focus on Tamil Nadu districts and coastal zones) or safely flags unverified areas.
- **Quantitative Risk Assessment Matrix**: Combines disaster baselines with contextual severity modifiers (e.g., flood level, cyclone wind speeds, coastal proximity) to compute a score from $0\text{ to }100$.
- **Real-Time Safety Boundary Protocol**: Prevents false emergency claims by distinguishing between simulated event reports and unverified live condition inquiries.
- **Hybrid AI Engine**: Seamlessly leverages OpenRouter LLMs when an API key is present, with an immediate, deterministic rule-based local agent fallback when offline.

---

## 🤖 What Makes RAKSHAK "Agentic"?

Unlike a generic conversational chatbot that merely generates passive text replies, **RAKSHAK AI**:
1. **Maintains Goal-Oriented Agency**: Receives unstructured reports and pursues the objective of formulating a verified regional emergency alert.
2. **Executes Specialized Multi-Tool Calls**:
   - `DisasterAnalysisTool`: Classifies disaster signatures and computes risk coefficients.
   - `RegionIdentificationTool`: Resolves geographic aliases and determines administrative zones without hallucinating.
   - `NotificationTool`: Formulates and stages multi-channel broadcasts (Cellular SMS, Emergency Sirens, SDMA Webhooks, Civil Defense).
   - `OpenRouterClient`: Optional LLM reasoning layer with graceful fallback.
3. **Generates Transparent Decision Traces**: Emits auditable step-by-step reasoning logs (`OBSERVE`, `ANALYZE`, `LOCATE`, `DECIDE`, `ACT`) displayed in real-time on the Emergency Operations Center dashboard.

---

## 🏗️ System Architecture

```text
               ┌──────────────────────────────────────────────────┐
               │              FIELD OPERATOR / USER               │
               └────────────────────────┬─────────────────────────┘
                                        │ (Disaster Event Report)
                                        ▼
               ┌──────────────────────────────────────────────────┐
               │             RAKSHAK AGENT CORE                   │
               │   (Observe → Analyze → Locate → Decide → Act)   │
               └─────┬──────────────┬──────────────┬──────────────┘
                     │              │              │
     ┌───────────────┴──┐   ┌───────┴────────┐   ┌─┴────────────────┐
     │  Disaster Tool   │   │  Region Tool   │   │ OpenRouter Client│
     │  (Risk Scoring)  │   │ (Tamil Nadu)   │   │  (LLM Fallback)  │
     └───────┬──────────┘   └───────┬────────┘   └─┬────────────────┘
             │                      │              │
             └──────────────┬───────┴──────────────┘
                            ▼
               ┌───────────────────────────────────┐
               │      DECISION MATRIX & ALERT      │
               │     Risk Score (0–100) / Priority │
               └────────────────────┬──────────────┘
                                    ▼
               ┌───────────────────────────────────┐
               │         NOTIFICATION TOOL         │
               │  SMS / Sirens / SDMA / WhatsApp   │
               └────────────────────┬──────────────┘
                                    ▼
               ┌───────────────────────────────────┐
               │      EOC DASHBOARD & TRACE        │
               └───────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React + Vite (Fast HMR & build)
- **Styling**: Vanilla CSS (Tailored Emergency Operations Center aesthetic, dark navy header, glassmorphism, pulse indicators)
- **Icons**: `lucide-react`
- **Architecture**: Modular components (`Header`, `ChatInterface`, `DisasterAlertCard`, `AgentActivityPanel`, `QuickActions`, `NotificationModal`)

### Backend
- **Framework**: FastAPI (High-performance asynchronous Python API)
- **Validation**: Pydantic v2
- **Networking**: HTTPX
- **Configuration**: `python-dotenv`
- **Testing**: `pytest`

### AI & Reasoning
- **OpenRouter API**: Pluggable LLM integration (`OPENROUTER_API_KEY`)
- **Deterministic Agent**: Built-in deterministic NLP & rule-based engine ensuring **100% functionality without API keys or internet dependencies**.

---

## 📋 Agent Workflow Lifecycle

| Stage | Activity | Description |
| :--- | :--- | :--- |
| **OBSERVE** | Input Validation | Receives and validates raw field reports or operator dispatches. |
| **ANALYZE** | Disaster Analysis | Detects disaster type (`Flood`, `Cyclone`, `Earthquake`, `Fire`, `Landslide`, `Tsunami`, `Storm`). |
| **LOCATE** | Region Identification | Resolves geographic entities (e.g. `Chennai`, `Madurai`, `Coimbatore`, `Cuddalore`, `Nagapattinam`, `Kanyakumari`). |
| **DECIDE** | Risk Assessment | Evaluates severity modifiers and coastal proximity to compute risk score ($0\text{–}100$) and threshold. |
| **ACT** | Alert & Dispatch | Generates regional alert payload and queues multi-channel notification broadcasts. |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health status, active reasoning mode, supported regions & disaster models. |
| `POST` | `/api/chat` | Main conversational endpoint running full agent lifecycle. |
| `POST` | `/api/analyze-disaster` | Direct payload analysis endpoint. |
| `GET` | `/api/demo-events` | Curated sample events for quick test simulations. |
| `POST` | `/api/notifications/test`| Triggers simulated multi-channel broadcast test. |

---

## 🚀 How to Run

### 1. Start the Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Optional but recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Set your OpenRouter API key in .env or run directly in deterministic mode
cp .env.example .env

# Run FastAPI server
uvicorn main:app --reload --port 8000
```

The backend will be live at `http://localhost:8000` (Swagger UI at `http://localhost:8000/docs`).

### 2. Run Backend Unit Tests

```bash
cd backend
python -m pytest tests/
```

### 3. Start the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

The application UI will be available at `http://localhost:5173`.

---

## 🧪 Demo Scenarios & Test Cases

Try entering these natural-language inputs or click the **Quick Action Buttons** in the top bar:

1. **Flood Scenario**:
   - *Input*: `"Heavy flooding has been reported in Chennai with low-lying areas inundated."`
   - *Result*: Detects `Flood` in `Chennai`, assesses `HIGH` risk ($85/100$), generates `ALERT GENERATED`, creates full 5-stage trace, and stages 4 notification channels.

2. **Cyclone Scenario**:
   - *Input*: `"Severe cyclone warning issued near Cuddalore coastal belt with gale winds."`
   - *Result*: Detects `Cyclone` in `Cuddalore` with coastal proximity boost $\rightarrow$ `CRITICAL` risk ($95/100$), issues immediate evacuation guidance.

3. **Earthquake Scenario**:
   - *Input*: `"Earthquake tremors detected in Madurai measuring 4.8 on Richter scale."`
   - *Result*: Detects `Earthquake` in `Madurai` $\rightarrow$ `HIGH` risk ($70/100$).

4. **Wildfire Scenario**:
   - *Input*: `"Massive forest fire reported near Coimbatore foothills threatening settlements."`
   - *Result*: Detects `Fire` in `Coimbatore` $\rightarrow$ `CRITICAL` risk ($90/100$).

5. **Real-Time Safety Boundary Rule**:
   - *Input*: `"Is Chennai currently flooding right now?"`
   - *Result*: Engages safety protocol: *"I cannot verify real-time conditions. Based on the information provided, I can generate a simulated alert."*

6. **Unidentified Region Handling**:
   - *Input*: `"Severe flood reported in Atlantis."`
   - *Result*: Returns *"Region could not be confidently identified"* with zero hallucination.

---

## 🔮 Future Improvements

1. **CAP (Common Alerting Protocol) XML Format**: Integration of OASIS CAP v1.2 standard for direct integration with NDMA alert feeds.
2. **Live Telemetry & IoT Sensor Ingestion**: Connecting rain gauges, river level sensors, and seismic telemetry.
3. **GeoJSON Interactive Map Layer**: Leaflet / Mapbox interactive GIS map with regional risk heatmap overlays.
4. **Automated Live SMS & Voice Dispatch**: Twilio / AWS SNS / Gov SMS gateway integrations for real-world deployments.
