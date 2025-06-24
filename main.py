from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
import cloudinary.uploader
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

LISTINGS_FILE = "listings.json"

# Listing model
class Listing(BaseModel):
    title: str
    description: str
    location: str
    image_url: str
    price_per_day: float

# Load listings from file
def load_listings():
    if os.path.exists(LISTINGS_FILE):
        with open(LISTINGS_FILE, "r") as f:
            return json.load(f)
    return []

# Save listings to file
def save_listings(data):
    with open(LISTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/listings", response_model=List[Listing])
def get_listings():
    return load_listings()

@app.post("/listings")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result.get("secure_url")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    new_listing = {
        "title": title,
        "description": description,
        "location": location,
        "image_url": image_url,
        "price_per_day": price_per_day
    }

    listings = load_listings()
    listings.append(new_listing)
    save_listings(listings)

    return {"message": "Listing created successfully", "listing": new_listing}







   



