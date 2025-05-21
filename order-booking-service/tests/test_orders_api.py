import pytest
from unittest.mock import patch, ANY
from datetime import datetime # Ensure datetime is imported

# client fixture is automatically available from conftest.py (AsyncClient)
# db_mock fixture is also available but not directly used here, as we mock CRUD functions

# Using a fixed datetime string for reproducibility in tests if needed, 
# or use datetime.utcnow().isoformat() for "now"
# For OrderResponse, a datetime object would also work due to Pydantic serialization.
# The example uses isoformat(), so we'll stick to that.
DUMMY_CREATED_AT_ISO = datetime.utcnow().isoformat()

@pytest.mark.asyncio
async def test_create_new_order_success(client):
    # This is the data structure that app.crud.create_order is expected to return
    mock_crud_return_value = {
        "id": 1,
        "user_id": "test_user_id", # Should match what authenticate_user mock returns
        "item_name": "Test Item",
        "quantity": 1,
        "price": 10.0,
        "status": "Pending",
        "created_at": DUMMY_CREATED_AT_ISO # Ensure created_at is present for OrderResponse
    }
    # POST tests continue to patch app.crud.create_order
    with patch('app.crud.create_order', return_value=mock_crud_return_value) as mock_crud_create:
        response = await client.post("/orders/", json={
            "item_name": "Test Item", "quantity": 1, "price": 10.0
        })
        assert response.status_code == 200, response.text # Add response.text for debugging
        api_response_json = response.json()
        assert api_response_json["item_name"] == "Test Item"
        assert api_response_json["user_id"] == "test_user_id"
        # Pydantic models in FastAPI convert datetime to ISO strings
        assert "created_at" in api_response_json
        assert api_response_json["created_at"] == DUMMY_CREATED_AT_ISO
        
        # Assert that app.crud.create_order was called correctly
        # The first argument to app.crud.create_order is an OrderCreate object
        # The second argument is the user_id
        mock_crud_create.assert_called_once()
        call_args = mock_crud_create.call_args[0]
        assert call_args[0].item_name == "Test Item"
        assert call_args[0].quantity == 1
        assert call_args[0].price == 10.0
        assert call_args[1] == "test_user_id"

@pytest.mark.asyncio
async def test_create_new_order_failure_creation_returns_none(client):
    # POST tests continue to patch app.crud.create_order
    with patch('app.crud.create_order', return_value=None) as mock_crud_create:
        response = await client.post("/orders/", json={
            "item_name": "Test Item", "quantity": 1, "price": 10.0
        })
        assert response.status_code == 500, response.text # Add response.text for debugging
        assert response.json()["detail"] == "Failed to create order"
        
        # Assert that app.crud.create_order was called correctly
        mock_crud_create.assert_called_once()
        call_args = mock_crud_create.call_args[0]
        assert call_args[0].item_name == "Test Item"
        assert call_args[1] == "test_user_id"

@pytest.mark.asyncio
async def test_read_orders_for_user_success(client):
    # This mock data is for app.crud.get_orders
    mock_orders_list_from_crud = [
        {"id": 1, "user_id": "test_user_id", "item_name": "Item 1", "quantity": 1, "price": 10.0, "status": "Pending", "created_at": DUMMY_CREATED_AT_ISO},
        {"id": 2, "user_id": "test_user_id", "item_name": "Item 2", "quantity": 2, "price": 20.0, "status": "Completed", "created_at": DUMMY_CREATED_AT_ISO}
    ]
    # Revert GET/DELETE tests to patch app.routers.orders.<function_name>
    with patch('app.routers.orders.get_orders', return_value=mock_orders_list_from_crud) as mock_router_get_orders:
        response = await client.get("/orders/")
        assert response.status_code == 200, response.text
        response_json = response.json()
        assert len(response_json) == 2
        assert response_json[0]["item_name"] == "Item 1"
        assert "created_at" in response_json[0]
        mock_router_get_orders.assert_called_once_with() # Asserting the call on the patched router function

@pytest.mark.asyncio
async def test_read_orders_for_user_no_orders_empty_list(client):
    with patch('app.routers.orders.get_orders', return_value=None) as mock_router_get_orders:
        response = await client.get("/orders/")
        assert response.status_code == 404, response.text
        assert response.json()["detail"] == "No orders found"
        mock_router_get_orders.assert_called_once_with()

@pytest.mark.asyncio
async def test_read_orders_for_user_returns_none(client):
    with patch('app.routers.orders.get_orders', return_value=None) as mock_router_get_orders:
        response = await client.get("/orders/")
        assert response.status_code == 404, response.text 
        assert response.json()["detail"] == "No orders found"
        mock_router_get_orders.assert_called_once_with()

@pytest.mark.asyncio
async def test_read_order_by_id_success(client):
    mock_order_data_from_crud = {
        "id": 1, "user_id": "test_user_id", "item_name": "Specific Item", 
        "quantity": 1, "price": 10.0, "status": "Pending", "created_at": DUMMY_CREATED_AT_ISO
    }
    with patch('app.routers.orders.get_order', return_value=mock_order_data_from_crud) as mock_router_get_order:
        response = await client.get("/orders/1")
        assert response.status_code == 200, response.text
        response_json = response.json()
        assert response_json["item_name"] == "Specific Item"
        assert response_json["id"] == 1
        assert "created_at" in response_json
        mock_router_get_order.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_read_order_by_id_not_found(client):
    with patch('app.routers.orders.get_order', return_value=None) as mock_router_get_order:
        response = await client.get("/orders/999")
        assert response.status_code == 404, response.text
        assert response.json()["detail"] == "Order with id 999 not found"
        mock_router_get_order.assert_called_once_with(999)

@pytest.mark.asyncio
async def test_delete_order_by_id_for_user_success(client):
    mock_deleted_order_data_from_crud = [{"id": 1, "user_id": "test_user_id", "item_name": "Deleted Item", "quantity": 1, "price": 10.0, "status": "Cancelled", "created_at": DUMMY_CREATED_AT_ISO}]
    
    with patch('app.routers.orders.delete_order', return_value=mock_deleted_order_data_from_crud) as mock_router_delete_order:
        response = await client.delete("/orders/1")
        assert response.status_code == 200, response.text
        assert response.json() == {"detail": "Order with id 1 deleted successfully"}
        mock_router_delete_order.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_delete_order_by_id_for_user_not_found(client):
    with patch('app.routers.orders.delete_order', return_value=None) as mock_router_delete_order:
        response = await client.delete("/orders/999")
        assert response.status_code == 404, response.text
        assert response.json()["detail"] == "Order with id 999 not found"
        mock_router_delete_order.assert_called_once_with(999)
