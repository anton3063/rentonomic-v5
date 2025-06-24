from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cloudinary
import cloudinary.uploader

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloudinary config
cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

# Simple in-memory storage (temporary)
listings_db = []

class Listing(BaseModel):
    title: str
    description: str
    image_url: str
    location: str

@app.get("/")
def home():
    return {"message": "Rentonomic backend is live."}

@app.get("/listings")
def get_listings():
    return listings_db

@app.post("/listings")
async def create_listing(listing: Listing):
    listings_db.append(listing.dict())
    return {"message": "Listing received!", "listing": listing}






   



