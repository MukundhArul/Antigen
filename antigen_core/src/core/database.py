from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config.global_settings import settings

"""
Design Choice: Asynchronous SQLAlchemy Core.
Using an async engine (aiosqlite) ensures that database I/O operations from telemetry 
logging do not block the primary event loop. This is critical because the Attacker/Defender 
agents are running heavy parallel routines, and synchronous I/O would artificial bottleneck 
latency metrics.

Zero-Day Handling: Connection pooling is managed natively by SQLAlchemy. If the DB goes down 
or is locked, the async generator pattern safely cleans up resources instead of leaving hanging threads.
"""

# Engine configuration optimized for concurrency
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db_session():
    """Dependency to yield an async database session for FastAPI endpoints or worker nodes."""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Initialize the database schema dynamically based on declared models."""
    async with engine.begin() as conn:
        # Import models here to avoid circular imports during Base metadata creation
        from src.core.models import ChaosRun, AgentTrajectoryStep
        await conn.run_sync(Base.metadata.create_all)
