from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Temporary in-memory database
listings = []

# Listing model
class Listing(BaseModel):
    title: str
    description: str
    location: str
    image_url: str
    price_per_day: float

@app.post("/listings")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    # Upload image to Cloudinary
    result = cloudinary.uploader.upload(image.file)
    image_url = result.get("secure_url")

    # Build listing
    new_listing = {
        "title": title,
        "description": description,
        "location": location,
        "price_per_day": price_per_day,
        "image_url": image_url
    }
    listings.append(new_listing)
    return {"message": "Listing created successfully!", "listing": new_listing}

@app.get("/listings", response_model=List[Listing])
def get_listings():
    return listings







   



