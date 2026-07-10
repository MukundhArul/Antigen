import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from src.core.database import Base

"""
Design Choice: Relational Database for State Tracing.
Using SQLite for local rapid prototyping but with standard SQLAlchemy ORM maps.
This allows us to seamlessly migrate to PostgreSQL later. The relationship between 
ChaosRun and AgentTrajectoryStep creates a directed acyclic graph (DAG) of the agent's memory.

Zero-Day Handling: Strict enums for `StageEnum` ensure that runaway processes can be safely 
pushed to a "FAILED" state, acting as a global kill-switch lock for the run ID.
"""

class StageEnum(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    RESOLVED = "RESOLVED"
    FAILED = "FAILED"

class ChaosRun(Base):
    """
    Tracks the overarching session of an Attacker vs. Defender interaction.
    """
    __tablename__ = "chaos_runs"

    id = Column(Integer, primary_key=True, index=True)
    target_agent_id = Column(String, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(Enum(StageEnum), default=StageEnum.PENDING)
    
    # Telemetry specific to the Antigen evaluation metrics
    robustness_score = Column(Float, nullable=True)
    latency_deg_coeff = Column(Float, nullable=True)
    loop_convergence_velocity = Column(Float, nullable=True)
    
    steps = relationship("AgentTrajectoryStep", back_populates="run", cascade="all, delete-orphan")

class AgentTrajectoryStep(Base):
    """
    Logs each step inside a run trajectory. 
    Crucial for Defender Loop to trace back failure origins.
    """
    __tablename__ = "agent_trajectory_steps"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("chaos_runs.id"))
    step_number = Column(Integer)
    action_type = Column(String)  # E.g., 'Tool Call', 'LLM Output'
    action_input = Column(Text)   # JSON stringified tool kwargs
    action_output = Column(Text)  # Result or Exception string
    
    # Fault injection tracking (What did the Attacker inject here?)
    fault_injected = Column(String, nullable=True) 
    timestamp = Column(DateTime, default=datetime.utcnow)

    run = relationship("ChaosRun", back_populates="steps")
