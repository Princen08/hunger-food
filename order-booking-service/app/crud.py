from app.database import supabase
from app.schemas import OrderCreate
from app.utils.logger import logger  # Import your logger


def create_order(order: OrderCreate, user_id: str):
    """
    Create a new order in the Supabase database.
    """
    try:
        response = (
            supabase.table("orders")
            .insert(
                {
                    "user_id": user_id,
                    "item_name": order.item_name,
                    "quantity": order.quantity,
                    "price": order.price,
                    "status": "Pending",
                }
            )
            .execute()
        )

        if not response.data:  # Check if data is empty
            logger.error("Failed to create order")
            return None
        logger.info(f"Order created successfully: {response.data}")
        return response.data[0] if response.data else None
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return None


def get_orders():
    """
    Retrieve all orders from the Supabase database.
    """
    try:
        response = supabase.table("orders").select("*").execute()
        if not response.data:  # Check if data is empty
            logger.warning("No orders found")
            return None
        logger.info(f"Fetched {len(response.data)} orders")
        return response.data
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        return None


def get_order(order_id: int):
    """
    Retrieve a specific order by ID from the Supabase database.
    """
    try:
        response = supabase.table("orders").select("*").eq("id", order_id).execute()
        if not response.data:  # Check if data is empty
            logger.warning(f"Order with id {order_id} not found")
            return None
        logger.info(f"Fetched order with id {order_id}: {response.data[0]}")
        return response.data[0]
    except Exception as e:
        logger.error(f"Error fetching order with id {order_id}: {e}")
        return None


def delete_order(order_id: int):
    """
    Delete an order by ID from the Supabase database.
    """
    try:
        response = supabase.table("orders").delete().eq("id", order_id).execute()
        if not response.data:  # Check if data is empty
            logger.warning(f"Order with id {order_id} not found")
            return None
        logger.info(f"Order with id {order_id} deleted successfully")
        return response.data
    except Exception as e:
        logger.error(f"Error deleting order with id {order_id}: {e}")
        return None
