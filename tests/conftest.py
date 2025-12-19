import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(autouse=True)
def clear_redis_data():
    from services.redis_service import redis_client
    redis_client._data.clear()
    yield
    redis_client._data.clear()


@pytest.fixture
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
