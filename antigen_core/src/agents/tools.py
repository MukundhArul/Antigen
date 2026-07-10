import asyncio
from typing import Dict, Any
from src.core.injector import fault_injector

"""
Design Choice: Mock tools wrapped with `@fault_injector.intercept`.
This simulates external APIs that the agent interacts with. By wrapping them,
the Antigen framework can inject latencies or errors without changing the internal
tool logic, simulating real-world instability.
"""

@fault_injector.intercept("fetch_user_profile")
async def fetch_user_profile(user_id: str) -> Dict[str, Any]:
    """
    Mock Tool: Fetches a user profile from a simulated database.
    """
    # Simulate some fast baseline I/O
    await asyncio.sleep(0.05)
    
    # Return mock data
    return {
        "user_id": user_id,
        "name": "Alice Admin",
        "role": "administrator",
        "preferences": {
            "theme": "dark",
            "notifications": True
        }
    }

@fault_injector.intercept("search_knowledge_base")
async def search_knowledge_base(query: str) -> str:
    """
    Mock Tool: Searches a simulated knowledge base.
    """
    await asyncio.sleep(0.1)
    return f"Search results for '{query}': The primary protocol is to always prioritize system stability. Do not delete users."
