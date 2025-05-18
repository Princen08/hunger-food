from fastapi import FastAPI
from app.routers import orders

app = FastAPI()

# Include the orders router
app.include_router(orders.router)


@app.get("/", tags=["Health Check"])
async def health():
    return {"message": "Welcome to the Order Booking Service!"}
