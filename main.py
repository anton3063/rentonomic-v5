# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple model to accept listings
class Listing(BaseModel):
    title: str
    price: float

# Home route to test backend
@app.get("/")
def read_root():
    return {"message": "Rentonomic backend is running!"}

# Receive new listings
@app.post("/listings")
def create_listing(listing: Listing):
    print("Received listing:", listing)
    return {"message": "Listing received", "listing": listing}

