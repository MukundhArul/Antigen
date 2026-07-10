import pytest
import os
import tempfile
from src.core.repair import AutomatedRepairEngine

@pytest.mark.asyncio
async def test_sandbox_apply_patch():
    """
    Validates that the AutomatedRepairEngine can successfully synthesize
    and write code patches to the sandboxed filesystem.
    We use a temporary directory to avoid polluting the actual repo during tests.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        repair_engine = AutomatedRepairEngine(workspace_path=temp_dir)
        
        # Setup: Create a dummy vulnerable file in the temp sandbox
        test_file = "vulnerable_target.py"
        with open(os.path.join(temp_dir, test_file), "w") as f:
            f.write("def vulnerable():\n    pass")
            
        # Execute: Ask engine to apply a synthesized patch
        patched_code = "def vulnerable():\n    try:\n        pass\n    except Exception:\n        return None\n"
        success = await repair_engine.apply_patch(test_file, patched_code)
        
        # Verify
        assert success is True
        with open(os.path.join(temp_dir, test_file), "r") as f:
            content = f.read()
            assert "try:" in content
            assert "except Exception:" in content
