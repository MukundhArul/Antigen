import os
import subprocess
import asyncio
from typing import Dict, Any, Tuple

class AutomatedRepairEngine:
    """
    The Defender Loop: Monitors for crashes and attempts to self-heal the codebase.
    
    Design Choice: Uses raw subprocesses to interact with `git` and `pytest`. 
    This allows the repair engine to truly fork the state of the repository, guaranteeing 
    that patches are isolated to the specific ChaosRun branch before being merged.
    
    Zero-Day Handling: If the target agent hits a fatal error (like an unhandled exception 
    from the fault injector), this engine catches the stack trace and synthesizes a fix natively,
    bypassing the need for manual engineering intervention.
    """
    
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.max_retries = 3

    async def _run_shell_cmd(self, cmd: str) -> Tuple[int, str, str]:
        """Utility to run shell commands asynchronously."""
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.workspace_path
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

    async def fork_environment(self, run_id: int) -> bool:
        """Forks the codebase into a dedicated patch branch."""
        branch_name = f"fix/run_{run_id}"
        # Ensure we are on main/master first (simplification for prototype)
        # In a real environment, you'd want to stash/clean first
        code, out, err = await self._run_shell_cmd(f"git checkout -b {branch_name}")
        if code != 0 and "already exists" not in err:
            print(f"Failed to fork environment: {err}")
            return False
        return True

    async def _draft_patch_via_llm(self, stack_trace: str, file_path: str) -> str:
        """
        STUB: In production, this calls the LLM with the stack trace and the source file,
        prompting it to write a unified diff or complete file replacement.
        """
        print(f"Drafting patch for {file_path} based on trace:\n{stack_trace[:100]}...")
        # Simulated patch generation: just returning a safe stub for demonstration
        patched_code = "# Patched by Antigen Defender Loop\n"
        patched_code += "def safe_function(*args, **kwargs):\n    try:\n        pass\n    except Exception:\n        return None\n"
        return patched_code

    async def apply_patch(self, file_path: str, patched_code: str) -> bool:
        """Writes the patch to the local filesystem (sandbox simulation)."""
        target_path = os.path.join(self.workspace_path, file_path)
        try:
            with open(target_path, "w") as f:
                f.write(patched_code)
            return True
        except Exception as e:
            print(f"Patch write failed: {e}")
            return False

    async def verify_patch(self) -> bool:
        """Runs the test suite inside the sandboxed branch to verify the fix."""
        # We run pytest locally in the workspace
        code, out, err = await self._run_shell_cmd("pytest tests/")
        # Return True if tests pass (exit code 0)
        return code == 0

    async def merge_patch(self, run_id: int) -> bool:
        """Merges the successful fix back into the main branch."""
        branch_name = f"fix/run_{run_id}"
        # Checkout main, merge branch, delete branch
        # (Assuming 'main' is the default branch for this prototype)
        cmds = [
            "git checkout main",
            f"git merge {branch_name} --no-edit",
            f"git branch -d {branch_name}"
        ]
        
        for cmd in cmds:
            code, out, err = await self._run_shell_cmd(cmd)
            if code != 0:
                print(f"Merge failed on cmd '{cmd}': {err}")
                return False
        return True

    async def execute_repair_loop(self, run_id: int, stack_trace: str, target_file: str) -> bool:
        """
        Orchestrates the full self-healing workflow.
        Returns True if RESOLVED, False if FAILED after max retries.
        """
        print(f"Starting Defender Loop for Run {run_id}")
        
        if not await self.fork_environment(run_id):
            return False

        for attempt in range(1, self.max_retries + 1):
            print(f"Repair attempt {attempt}/{self.max_retries}")
            
            # 1. Draft the patch
            patched_code = await self._draft_patch_via_llm(stack_trace, target_file)
            
            # 2. Apply it
            if not await self.apply_patch(target_file, patched_code):
                continue
                
            # 3. Verify it
            if await self.verify_patch():
                print(f"Patch verified successfully on attempt {attempt}.")
                # 4. Merge if successful
                return await self.merge_patch(run_id)
            else:
                print(f"Patch failed verification on attempt {attempt}.")
                # In production, we feed the pytest error back into `_draft_patch_via_llm`

        print("Defender Loop exhausted all retries. Marking as FAILED.")
        # Cleanup if failed
        await self._run_shell_cmd("git checkout main")
        return False

# Global repair instance requires workspace path at initialization
# Example: repair_engine = AutomatedRepairEngine(workspace_path="/app/antigen_core")
