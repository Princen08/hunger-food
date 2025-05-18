from fastapi import FastAPI
from app.database import supabase
from app.routers import orders
from app.utils.logger import logger  # Import your logger

app = FastAPI()

# Include the orders router
app.include_router(orders.router)


@app.get("/", tags=["Health Check"])
async def health():
    return {"message": "Welcome to the Order Booking Service!"}
