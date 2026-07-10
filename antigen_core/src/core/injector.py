import asyncio
import random
from typing import Callable, Any, Dict
from functools import wraps
from pydantic import BaseModel

class FaultConfig(BaseModel):
    probability: float = 1.0
    fault_type: str  # e.g., 'latency', 'http_error', 'json_corruption'
    fault_params: Dict[str, Any] = {}

class AsynchronousToolFaultInjector:
    """
    Aspect-oriented fault injection engine (The Attacker's primary weapon).
    
    Design Choice: Uses function decorators (`@fault_injector.intercept`) to wrap 
    target agent tools transparently. This isolates the fault logic from the business logic.
    Instead of rewriting mock tools, we dynamically hijack them at runtime.
    
    Zero-Day Handling: The injector uses native `asyncio.sleep` and raises standard 
    Exceptions. If a target agent lacks `try/except` blocks, the system will accurately
    simulate a catastrophic thread crash, which the Defender Loop will later catch 
    and repair.
    """
    
    def __init__(self):
        self._active_faults: Dict[str, FaultConfig] = {}
        
    def configure_fault(self, tool_name: str, config: FaultConfig):
        """Set an active fault context for a specific tool."""
        self._active_faults[tool_name] = config
        
    def clear_faults(self):
        """Reset the arena context."""
        self._active_faults.clear()

    async def _apply_pre_fault(self, config: FaultConfig):
        """Applies faults that block or fail execution before the tool runs."""
        if random.random() > config.probability:
            return

        if config.fault_type == "latency":
            delay = config.fault_params.get("delay_ms", 1000) / 1000.0
            await asyncio.sleep(delay)
            
        elif config.fault_type == "http_error":
            status_code = config.fault_params.get("status_code", 503)
            # Simulating an unhandled network exception
            raise Exception(f"HTTPError: {status_code} Service Unavailable or Rate Limited")

    def intercept(self, tool_name: str):
        """
        Decorator to wrap async target tools. 
        Hooks into the pre and post execution lifecycles.
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                config = self._active_faults.get(tool_name)
                
                # Apply Pre-Execution faults
                if config and config.fault_type in ["latency", "http_error"]:
                    await self._apply_pre_fault(config)
                
                # Execute original tool logic
                result = await func(*args, **kwargs)
                
                # Apply Post-Execution faults (Data mutation)
                if config and config.fault_type == "json_corruption" and random.random() <= config.probability:
                    if isinstance(result, str):
                        # Naive JSON corruption: remove closing brackets
                        return result.rstrip("}") 
                    elif isinstance(result, dict):
                        # Poison the dictionary structure
                        result["_corrupted_by_antigen"] = True
                        if len(result.keys()) > 0:
                            first_key = list(result.keys())[0]
                            result[first_key] = None # Nullify expected data
                        
                return result
            return wrapper
        return decorator

# Global arena injector
fault_injector = AsynchronousToolFaultInjector()
