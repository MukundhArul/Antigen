from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Global settings for the Antigen Framework.
    
    Design Choice: Using Pydantic BaseSettings for type-safe, environment-variable-driven configuration.
    This guarantees that the system starts with exactly the expected data types for critical limits.
    
    Zero-Day Handling: Strict typing prevents configuration poisoning. The max_steps token kill-switch
    is centralized here. If a runaway loop is triggered, the engine refers back to this invariant.
    """
    
    # Environment Controls
    environment: str = "development"
    debug: bool = True
    
    # Storage
    database_url: str = "sqlite+aiosqlite:///./antigen.db"
    
    # Safety & Infinite Loop Guardrails (The Token Kill-Switch)
    max_steps: int = 15
    token_cap: int = 100000
    
    # Sandbox provisioning
    sandbox_mode: str = "local_subprocess"
    
    class Config:
        env_file = ".env"

# Singleton instance
settings = Settings()
