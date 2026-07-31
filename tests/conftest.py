from copy import deepcopy

import httpx
import pytest

from src.app import activities, app


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities to keep tests isolated and deterministic."""
    original_state = deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(original_state)
