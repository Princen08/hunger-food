import pytest

# client fixture is automatically available from conftest.py


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Order Booking Service!"}
