from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from src.core.database import init_db, AsyncSessionLocal
from src.core.models import ChaosRun, StageEnum
from src.api.dependencies import get_db

from src.agents.target_agent import MockTargetAgent
from src.core.mutator import mutator_engine
from src.core.injector import fault_injector, FaultConfig

app = FastAPI(
    title="Antigen Framework API",
    description="Control plane for orchestrating Attacker/Defender LLM simulations.",
    version="1.0.0"
)

@app.on_event("startup")
async def on_startup():
    """Initialize database tables on application boot."""
    await init_db()
    print("Database initialized successfully.")

class RunRequest(BaseModel):
    user_query: str
    target_agent_id: str = "agent_alpha"
    mutation_severity: float = 0.5
    inject_latency: bool = False
    inject_http_error: bool = False

async def _orchestrate_chaos_run(run_id: int, request: RunRequest):
    """
    Background worker that executes the Arena workflow:
    Mutate -> Attack -> Target Execute -> Defend (if crash)
    """
    # 1. Setup Attacker Context
    if request.inject_latency:
        fault_injector.configure_fault("fetch_user_profile", FaultConfig(fault_type="latency", fault_params={"delay_ms": 1500}))
    if request.inject_http_error:
        # This will natively crash the mock agent, triggering the Defender branch
        fault_injector.configure_fault("fetch_user_profile", FaultConfig(fault_type="http_error", fault_params={"status_code": 500}))
        
    warped_query = mutator_engine.semantic_warp(request.user_query, severity=request.mutation_severity)
    
    # 2. Spin up target agent
    agent = MockTargetAgent(agent_id=request.target_agent_id)
    
    try:
        # Target Agent execution
        result = await agent.run_trajectory(warped_query)
        
        # If it survives the faults and mutations, mark resolved
        async with AsyncSessionLocal() as session:
            run_obj = await session.get(ChaosRun, run_id)
            if run_obj:
                run_obj.status = StageEnum.RESOLVED
                await session.commit()
                
    except Exception as e:
        # 3. Defender Loop Catch
        print(f"Run {run_id} CRASHED: {e}")
        # In a full deployment, we trigger the AutomatedRepairEngine here:
        # repair_success = await repair_engine.execute_repair_loop(...)
        
        async with AsyncSessionLocal() as session:
            run_obj = await session.get(ChaosRun, run_id)
            if run_obj:
                run_obj.status = StageEnum.FAILED  # Or RESOLVED if repair succeeded
                await session.commit()
    finally:
        # Clean the arena for the next run
        fault_injector.clear_faults()


@app.post("/runs/", status_code=202)
async def start_chaos_run(request: RunRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """
    Triggers a new asynchronous ChaosRun in the arena.
    Returns immediately while the Attacker vs Defender deathmatch runs in the background.
    """
    # Create database entry
    new_run = ChaosRun(
        target_agent_id=request.target_agent_id,
        status=StageEnum.PENDING
    )
    db.add(new_run)
    await db.commit()
    await db.refresh(new_run)
    
    # Update status to running
    new_run.status = StageEnum.RUNNING
    await db.commit()
    
    # Fire off background worker
    background_tasks.add_task(_orchestrate_chaos_run, new_run.id, request)
    
    return {"message": "Arena initialized. Run started.", "run_id": new_run.id}

@app.get("/runs/{run_id}")
async def get_run_status(run_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the current status and metrics of a specific ChaosRun.
    """
    query = select(ChaosRun).where(ChaosRun.id == run_id)
    result = await db.execute(query)
    run_obj = result.scalar_one_or_none()
    
    if not run_obj:
        raise HTTPException(status_code=404, detail="Run not found in telemetry database.")
        
    return {
        "run_id": run_obj.id,
        "status": run_obj.status.value,
        "robustness_score": run_obj.robustness_score,
        "target_agent": run_obj.target_agent_id
    }
