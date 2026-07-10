# Project Antigen: Omni-Loop Critical Runtime

![Antigen Logo/Banner Placeholder](https://via.placeholder.com/800x200.png?text=Project+Antigen)

Project Antigen is a production-grade, multi-agent chaos engineering and autonomous self-healing framework for AI-native web applications. 

Traditional static code analysis is insufficient for autonomous agents that hallucinate, drift, or execute unpredictable trajectories. Antigen solves this by executing a closed-loop digital arena where an **Attacker Loop** injects environmental/contextual faults (the "antigen"), and a **Defender Loop** dynamically diagnoses failures, provisions sandboxes, drafts patches, and tests source repairs to establish zero-day immunity.

## 🚀 Key Features

*   **Asynchronous Tool Fault Injection:** Aspect-oriented Python decorators natively intercept tool calls to simulate latencies, HTTP drops (e.g., 503/429 errors), and JSON corruption, testing the agent's fallback handling.
*   **Adversarial Context Mutation Engine:** 
    *   **Semantic Warping:** Mutates crisp user queries into verbose, contradictory jargon matrices to stress-test logical reasoning.
    *   **Indirect Prompt Injection:** Smuggles system overrides into secondary data payloads (like DB reads or search results) to verify input sanitization.
*   **Behavioral Contract Evaluator:** Validates execution trajectories against strict mathematical invariants (`PydanticSchemaInvariant`, `SafetyLeakageInvariant`) and calculates critical metrics like Robustness Score (RS) and Latency Degradation Coefficient (LDC).
*   **Autonomous Self-Healing Engine (The Defender):** Monitors the agent for thread crashes. Upon failure, it uses Git to fork the repo, spins up a subprocess sandbox, drafts a Python patch based on the stack trace, and verifies it via `pytest` before merging the fix.
*   **Token Kill-Switch:** Centralized guardrails prevent runaway agent loops under fault conditions.

## 📁 Architecture Overview

The system is built on Python 3.11+ using `FastAPI` for the control plane and `SQLAlchemy` (Async) for SQLite telemetry storage.

```text
antigen_core/
├── config/
│   └── global_settings.py          # Environment, token caps, and sandbox variables
├── src/
│   ├── api/
│   │   ├── main.py                 # FastAPI system controls and run triggers
│   │   └── dependencies.py         # Shared state injections and async DB handling
│   ├── core/
│   │   ├── database.py             # SQLAlchemy async configuration
│   │   ├── models.py               # ORM mappings for Runs and Agent Trajectories
│   │   ├── injector.py             # Aspect-oriented tool fault interceptors
│   │   ├── mutator.py              # Semantic Warping and Prompt Injection engine
│   │   ├── evaluator.py            # Invariant validation checking and score math
│   │   └── repair.py               # Self-Healing controller and sandbox loop
│   └── agents/
│       ├── target_agent.py         # Mock target agent runtime loop under evaluation
│       └── tools.py                # Reference mock tools (DB query, web search) wrapped with injectors
└── tests/                          # Pytest integration scripts
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd antigen_core
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Running the Framework

### Start the Control Plane API
Launch the FastAPI server to interact with the orchestration engine:
```bash
uvicorn src.api.main:app --reload
```
Navigate to `http://127.0.0.1:8000/docs` to view the Swagger UI and trigger a `ChaosRun`.

### Run the Test Suite
To verify the Attacker mechanics and Defender sandbox logic natively:
```bash
pytest tests/
```

## 📊 Core Metrics

Antigen evaluates agents using strict mathematical metrics rather than relying on "LLM-as-a-judge":
*   **Robustness Score (RS):** The severity-weighted success ratio of behavioral contracts.
*   **Latency Degradation Coefficient (LDC):** Ratio of completion token inflation relative to injected millisecond environmental delays.
*   **Loop Convergence Velocity (LCV):** The efficiency curve of trajectory path recovery.

## 🤝 Contributing
Contributions are welcome. Please ensure that any new tools added to the target agent are wrapped with the `@fault_injector.intercept` decorator and that all invariants implement the `BaseInvariant` schema.

---
*Project Antigen: Evolving immunity through managed chaos.*
