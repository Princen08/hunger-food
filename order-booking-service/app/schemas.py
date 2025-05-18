from datetime import datetime

from pydantic import BaseModel


class OrderBase(BaseModel):
    item_name: str
    quantity: int
    price: float


class OrderCreate(OrderBase):
    """
    Schema for creating a new order.
    The user_id is not included because it will be extracted from the JWT token.
    """

    pass


class OrderResponse(OrderBase):
    """
    Schema for returning order details in responses.
    Includes user_id to associate the order with a specific user.
    """

    id: int
    user_id: str  # Include user_id in the response
    order_date: datetime

    class Config:
        orm_mode = True
