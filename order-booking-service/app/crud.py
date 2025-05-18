from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Order
from app.schemas import OrderCreate


async def create_order(db: AsyncSession, order: OrderCreate, user_id: str):
    db_order = Order(
        user_id=user_id,  # Associate the order with the user_id
        item_name=order.item_name,
        quantity=order.quantity,
        price=order.price,
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()


async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def delete_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order:
        await db.delete(order)
        await db.commit()
    return order
