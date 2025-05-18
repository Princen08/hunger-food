from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import create_order, delete_order, get_order, get_orders
from app.database import get_db
from app.schemas import OrderCreate, OrderResponse
from app.utils.auth import authenticate_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse)
async def create_new_order(
    order: OrderCreate,
    user_id: str = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    return await create_order(db, order, user_id)


@router.get("/", response_model=list[OrderResponse])
async def read_orders(db: Session = Depends(get_db)):
    return await get_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int, db: Session = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found"
        )
    return order


@router.delete("/{order_id}")
async def delete_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = await delete_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found"
        )
    return {"detail": f"Order with id {order_id} deleted successfully"}
