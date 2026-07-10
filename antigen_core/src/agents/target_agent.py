import json
import asyncio
from typing import Dict, Any, List
from src.agents.tools import fetch_user_profile, search_knowledge_base
from src.core.mutator import mutator_engine

class MockTargetAgent:
    """
    Simulates the runtime loop of an LLM-based autonomous agent.
    
    Design Choice: We avoid a real LLM call here to ensure tests are deterministic 
    and fast. Instead, we simulate the LLM's "reasoning" step, showing how it would 
    call tools and parse responses.
    
    Zero-Day Handling (Vulnerable Baseline): This mock agent intentionally lacks 
    `try/except` blocks around its tool calls. When the Attacker injects a fault 
    (e.g., HTTP 500) into `fetch_user_profile`, this agent will crash. The Defender Loop 
    (repair.py) is responsible for catching that crash, forking the repo, and dynamically 
    rewriting this file to include safe error handling.
    """
    
    def __init__(self, agent_id: str = "agent_alpha"):
        self.agent_id = agent_id
        self.memory: List[Dict[str, Any]] = []
        
    async def run_trajectory(self, user_query: str) -> str:
        """
        Executes a multi-step trajectory based on the user's query.
        """
        print(f"[{self.agent_id}] Received query: {user_query}")
        
        # Step 1: Tool Call - Fetch User Profile
        # VULNERABILITY: If fault_injector triggers here, the thread dies natively.
        profile_data = await fetch_user_profile("user_123")
        
        # VULNERABILITY: The agent reads profile data but doesn't sanitize it.
        # If mutator_engine injected a payload via an upstream mock database hook,
        # the agent might blindly append it to memory, risking prompt leakage.
        self.memory.append({"role": "system", "content": f"Fetched profile: {profile_data}"})
        
        # Step 2: Tool Call - Search KB
        kb_results = await search_knowledge_base(user_query)
        self.memory.append({"role": "system", "content": f"KB Result: {kb_results}"})
        
        # Step 3: Synthesis (Mock LLM Generation)
        # We simulate the agent formatting its final output as JSON.
        final_output = {
            "status": "success",
            "agent_id": self.agent_id,
            "processed_query": user_query[:20] + "...",
            "profile_role": profile_data.get("role", "unknown"),
            "action_taken": "Analyzed profile and KB."
        }
        
        return json.dumps(final_output)

# Expose a simple execution function for the FastAPI layer
async def execute_mock_run():
    agent = MockTargetAgent()
    # Apply semantic warping to the input query before the agent sees it
    warped_query = mutator_engine.semantic_warp("Check my user status.", severity=0.5)
    result = await agent.run_trajectory(warped_query)
    return result
