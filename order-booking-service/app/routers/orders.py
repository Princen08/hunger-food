from fastapi import APIRouter, Depends, HTTPException

from app.crud import create_order, delete_order, get_order, get_orders
from app.schemas import OrderCreate, OrderResponse
from app.utils.auth import authenticate_user
from app.utils.logger import logger  # Import your logger

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse)
async def create_new_order(
    order: OrderCreate,
    user_id: str = Depends(authenticate_user),
):
    """
    Create a new order in the Supabase database.
    """
    new_order = create_order(order, user_id)
    if not new_order:
        logger.error("Failed to create order")
        raise HTTPException(status_code=500, detail="Failed to create order")
    logger.info(f"Order created successfully: {new_order}")
    return new_order


@router.get("/", response_model=list[OrderResponse])
async def read_orders():
    """
    Retrieve all orders from the Supabase database.
    """
    orders = get_orders()
    if not orders:
        logger.warning("No orders found")
        raise HTTPException(status_code=404, detail="No orders found")
    logger.info(f"Fetched {len(orders)} orders")
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int):
    """
    Retrieve a specific order by ID from the Supabase database.
    """
    order = get_order(order_id)
    if not order:
        logger.warning(f"Order with id {order_id} not found")
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found"
        )
    else:
        logger.info(f"Fetched order with id {order_id}: {order}")
        return order


@router.delete("/{order_id}")
async def delete_order_by_id(order_id: int):
    """
    Delete an order by ID from the Supabase database.
    """
    deleted_order = delete_order(order_id)
    if not deleted_order:
        logger.warning(f"Order with id {order_id} not found")
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found"
        )
    logger.info(f"Order with id {order_id} deleted successfully")
    return {"detail": f"Order with id {order_id} deleted successfully"}
