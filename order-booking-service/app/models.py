from enum import Enum as PyEnum  # Import Python's Enum for defining the status

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.sql import func  # Import func for default timestamp

from app.base import Base  # Import the Base class for SQLAlchemy models


class OrderStatusEnum(str, PyEnum):  # Use Python's Enum for defining the statuses
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

    def __str__(self):
        return self.value


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        String, nullable=False
    )  # Store user_id as a string (MongoDB ObjectId)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order_date = Column(DateTime(timezone=True), default=func.now())
    status = Column(
        Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False
    )  # Use SQLAlchemy's Enum
