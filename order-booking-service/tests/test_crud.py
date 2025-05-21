from unittest.mock import MagicMock
import pytest

from app.crud import create_order, get_orders, get_order, delete_order
from app.schemas import OrderCreate

# Tests for create_order
def test_create_order_success(db_mock):
    # Mock the successful response from Supabase
    mock_response = MagicMock()
    mock_response.data = [{
        "id": 1,
        "user_id": "test_user_id",
        "item_name": "Test Item",
        "quantity": 1,
        "price": 10.0,
        "status": "Pending"
    }]
    db_mock.table.return_value.insert.return_value.execute.return_value = mock_response

    order_data = OrderCreate(item_name="Test Item", quantity=1, price=10.0)
    user_id = "test_user_id"
    
    new_order = create_order(order_data, user_id)

    assert new_order is not None
    assert new_order["item_name"] == "Test Item"
    assert new_order["user_id"] == user_id
    db_mock.table.assert_called_with("orders")
    db_mock.table().insert.assert_called_once()

def test_create_order_failure_no_data(db_mock):
    # Mock a response where no data is returned (simulating a creation failure)
    mock_response = MagicMock()
    mock_response.data = None
    db_mock.table.return_value.insert.return_value.execute.return_value = mock_response

    order_data = OrderCreate(item_name="Test Item", quantity=1, price=10.0)
    user_id = "test_user_id"
    
    new_order = create_order(order_data, user_id)

    assert new_order is None
    db_mock.table.assert_called_with("orders")
    db_mock.table().insert.assert_called_once()

def test_create_order_exception(db_mock):
    # Mock an exception during Supabase call
    db_mock.table.return_value.insert.return_value.execute.side_effect = Exception("DB Error")

    order_data = OrderCreate(item_name="Test Item", quantity=1, price=10.0)
    user_id = "test_user_id"
    
    new_order = create_order(order_data, user_id)

    assert new_order is None
    db_mock.table.assert_called_with("orders")
    db_mock.table().insert.assert_called_once()

# Tests for get_orders
def test_get_orders_success(db_mock):
    mock_response = MagicMock()
    mock_response.data = [
        {"id": 1, "user_id": "test_user_id", "item_name": "Item 1", "quantity": 1, "price": 10.0, "status": "Pending"},
        {"id": 2, "user_id": "test_user_id", "item_name": "Item 2", "quantity": 2, "price": 20.0, "status": "Completed"}
    ]
    # get_orders in crud.py does not filter by user_id, it selects all
    db_mock.table.return_value.select.return_value.execute.return_value = mock_response
    
    orders = get_orders() # No user_id argument
    
    assert orders is not None
    assert len(orders) == 2
    assert orders[0]["item_name"] == "Item 1"
    db_mock.table.assert_called_with("orders")
    db_mock.table().select.assert_called_with("*")
    db_mock.table().select().execute.assert_called_once() # Ensure execute is called

def test_get_orders_no_orders_exist(db_mock):
    mock_response = MagicMock()
    mock_response.data = []
    db_mock.table.return_value.select.return_value.execute.return_value = mock_response
    
    orders = get_orders() # No user_id argument
    
    assert orders is None # crud.py get_orders returns None when response.data is empty
    db_mock.table.assert_called_with("orders")
    db_mock.table().select.assert_called_with("*")
    db_mock.table().select().execute.assert_called_once()

def test_get_orders_exception(db_mock):
    db_mock.table.return_value.select.return_value.execute.side_effect = Exception("DB Error")
    
    orders = get_orders() # No user_id argument
    
    assert orders is None 
    db_mock.table.assert_called_with("orders")
    db_mock.table().select.assert_called_with("*")
    db_mock.table().select().execute.assert_called_once()

# Tests for get_order
def test_get_order_success(db_mock):
    mock_response = MagicMock()
    mock_response.data = [{"id": 1, "user_id": "test_user_id", "item_name": "Test Item", "quantity": 1, "price": 10.0, "status": "Pending"}]
    # get_order in crud.py filters by order_id only
    db_mock.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
    
    order = get_order(1) # Only order_id argument
    
    assert order is not None
    assert order["item_name"] == "Test Item"
    db_mock.table.assert_called_with("orders")
    db_mock.table().select.assert_called_with("*")
    db_mock.table().select().eq.assert_called_with("id", 1)
    db_mock.table().select().eq().execute.assert_called_once()


def test_get_order_not_found(db_mock):
    mock_response = MagicMock()
    mock_response.data = []
    db_mock.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
    
    order = get_order(999) # Non-existent order_id, only order_id argument
    
    assert order is None
    db_mock.table.assert_called_with("orders")
    db_mock.table().select.assert_called_with("*")
    db_mock.table().select().eq.assert_called_with("id", 999)
    db_mock.table().select().eq().execute.assert_called_once()

def test_get_order_exception(db_mock):
    db_mock.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("DB Error")
    
    order = get_order(1) # Only order_id argument
    
    assert order is None
    db_mock.table.assert_called_with("orders")
    db_mock.table().select.assert_called_with("*")
    db_mock.table().select().eq.assert_called_with("id", 1)
    db_mock.table().select().eq().execute.assert_called_once()

# Tests for delete_order
def test_delete_order_success(db_mock):
    # delete_order in crud.py filters by order_id only
    # However, the current test implementation for delete_order in test_crud.py
    # implies that delete_order itself first fetches the order (select) and then deletes it.
    # The actual crud.delete_order function only issues a delete operation.
    # The tests here are more like integration tests for a "delete if exists" workflow.
    # For now, I will adjust the call signature and mock for the direct delete.
    # A more accurate test would involve mocking only the delete().eq().execute() chain.
    
    mock_delete_response = MagicMock()
    mock_delete_response.data = [{"id": 1}] 
    db_mock.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_delete_response
    
    deleted_order_response = delete_order(1) # Only order_id argument
    
    assert deleted_order_response is not None
    assert deleted_order_response[0]["id"] == 1 
    db_mock.table.assert_called_with("orders")
    db_mock.table().delete.assert_called_once()
    db_mock.table().delete().eq.assert_called_with("id", 1)
    db_mock.table().delete().eq().execute.assert_called_once()


def test_delete_order_not_found(db_mock):
    # crud.delete_order returns None if data is empty after delete
    mock_delete_response = MagicMock()
    mock_delete_response.data = [] # Simulate no data returned after delete (order not found)
    db_mock.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_delete_response
    
    deleted_order_response = delete_order(999) # Only order_id argument
    
    assert deleted_order_response is None # crud.delete_order returns None if data is empty
    db_mock.table.assert_called_with("orders")
    db_mock.table().delete.assert_called_once()
    db_mock.table().delete().eq.assert_called_with("id", 999)
    db_mock.table().delete().eq().execute.assert_called_once()


def test_delete_order_exception_on_select(db_mock):
    # This test name is now misleading as crud.delete_order doesn't do a select.
    # Renaming to test_delete_order_exception
    # Test an exception during the delete operation itself.
    db_mock.table.return_value.delete.return_value.eq.return_value.execute.side_effect = Exception("DB Error on Delete")
    
    deleted_order_response = delete_order(1) # Only order_id argument
    
    assert deleted_order_response is None
    db_mock.table.assert_called_with("orders")
    db_mock.table().delete.assert_called_once()
    db_mock.table().delete().eq.assert_called_with("id", 1)
    db_mock.table().delete().eq().execute.assert_called_once()


def test_delete_order_exception_on_delete(db_mock):
    # This test is similar to the one above now.
    # Kept for consistency but effectively tests the same as test_delete_order_exception
    db_mock.table.return_value.delete.return_value.eq.return_value.execute.side_effect = Exception("DB Error on Delete")
    
    deleted_order_response = delete_order(1) # Only order_id argument
    
    assert deleted_order_response is None
    db_mock.table.assert_called_with("orders")
    db_mock.table().delete.assert_called_once()
    db_mock.table().delete().eq.assert_called_with("id", 1)
    db_mock.table().delete().eq().execute.assert_called_once()

# Ensure db_mock is reset for each test by pytest's fixture scoping
# (db_mock is function-scoped in conftest.py)
# No explicit reset needed here.
# Example:
# If db_mock.table().insert was called in test_create_order_success,
# for test_create_order_failure_no_data, db_mock.table().insert.call_count will be 0
# before the insert call within test_create_order_failure_no_data itself.
# This is because db_mock is a fresh MagicMock for each test function.
