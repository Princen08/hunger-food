from fastapi import FastAPI

from app.base import Base
from app.database import engine
from app.models import Order  # noqa: F401
from app.routers import orders

app = FastAPI()

# Include the orders router
app.include_router(orders.router)


@app.on_event("startup")
async def create_tables():
    print("Creating tables...")
    async with engine.begin() as conn:
        # Use run_sync to execute Base.metadata.create_all
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")


@app.get("/", tags=["Health Check"])
async def health():
    return {"message": "Welcome to the Order Booking Service!"}
