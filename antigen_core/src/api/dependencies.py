from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an async database session per request.
    
    Design Choice: Using an async generator pattern ensures that database connections 
    are properly yielded to the request context and definitively closed (returned to the pool) 
    in the `finally` block of the async context manager, even if the HTTP request errors out.
    """
    async with AsyncSessionLocal() as session:
        yield session
