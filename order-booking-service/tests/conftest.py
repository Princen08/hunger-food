import pytest
import pytest_asyncio
from unittest.mock import MagicMock, patch
from httpx import AsyncClient

# 1. Patch supabase.create_client FIRST
# This ensures that when app.database imports create_client, it gets the mock,
# and thus app.database.supabase becomes this mock_supabase_instance.
mock_supabase_instance = MagicMock()
patch_create_client = patch('supabase.create_client', return_value=mock_supabase_instance)
patch_create_client.start()

# 2. Patch other utilities (auth, logger)
# Patch authenticate_user
patch_authenticate_user = patch('app.utils.auth.authenticate_user', return_value='test_user_id')
patch_authenticate_user.start()

# Patch logger instances to prevent actual logging or external calls
patch_utils_logger = patch('app.utils.logger.logger', MagicMock())
patch_crud_logger = patch('app.crud.logger', MagicMock())
patch_routers_orders_logger = patch('app.routers.orders.logger', MagicMock())

patch_utils_logger.start()
patch_crud_logger.start()
patch_routers_orders_logger.start()

# 3. NOW import the FastAPI app
from app.main import app  # app.database will be initialized here using the mocked create_client

@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="function")
def db_mock():
    # This fixture should provide the SAME mock_supabase_instance that app.database.supabase is using.
    mock_supabase_instance.reset_mock() # Reset call history etc. for each test
    return mock_supabase_instance

# Optional: stop patches at the end of the session for cleanliness
# (ensure this is correctly defined if not already)
def pytest_sessionfinish(session, exitstatus):
    patch_create_client.stop()
    patch_authenticate_user.stop()
    patch_utils_logger.stop()
    patch_crud_logger.stop()
    patch_routers_orders_logger.stop()
