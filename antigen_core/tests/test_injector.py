import pytest
import asyncio
from src.core.injector import fault_injector, FaultConfig

# A dummy target function wrapped by the injector for testing
@fault_injector.intercept("dummy_func")
async def dummy_func(data: dict) -> dict:
    return data

@pytest.mark.asyncio
async def test_no_fault():
    """Verify that the decorator passes through transparently when no faults are active."""
    fault_injector.clear_faults()
    result = await dummy_func({"key": "value"})
    assert result == {"key": "value"}

@pytest.mark.asyncio
async def test_http_error_fault():
    """Verify that configuring an http_error reliably raises an Exception natively."""
    fault_injector.clear_faults()
    fault_injector.configure_fault(
        "dummy_func", 
        FaultConfig(fault_type="http_error", probability=1.0, fault_params={"status_code": 500})
    )
    
    with pytest.raises(Exception, match="HTTPError: 500"):
        await dummy_func({"key": "value"})

@pytest.mark.asyncio
async def test_json_corruption_fault():
    """Verify that JSON dictionary structures are properly poisoned post-execution."""
    fault_injector.clear_faults()
    fault_injector.configure_fault(
        "dummy_func", 
        FaultConfig(fault_type="json_corruption", probability=1.0)
    )
    
    result = await dummy_func({"key": "value"})
    assert "_corrupted_by_antigen" in result
    # It should have nullified the first key
    assert result["key"] is None
