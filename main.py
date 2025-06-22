from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import cloudinary
import cloudinary.uploader
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloudinary configuration
cloudinary.config(
    cloud_name="dkzvwm3hh",
    api_key="277136188375582",
    api_secret=os.getenv("CLOUDINARY_API_SECRET") or "YOUR_API_SECRET"
)

# In-memory store for listings
listings = []

@app.get("/")
def root():
    return {"message": "Rentonomic backend is running!"}

@app.get("/listings")
def get_listings():
    return {"listings": listings}

@app.post("/listings")
async def create_listing(
    title: str = Form(...),
    price_per_day: int = Form(...),
    description: str = Form(...),
    postcode: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Upload image to Cloudinary
        result = cloudinary.uploader.upload(image.file)
        image_url = result.get("secure_url")

        # Extract postcode prefix
        postcode_prefix = postcode.strip().split(" ")[0]

        # Add 10% service fee
        service_fee = round(price_per_day * 0.10, 2)

        # Build listing
        listing = {
            "id": len(listings) + 1,
            "title": title,
            "price": price_per_day,
            "description": description,
            "location": postcode_prefix,
            "image_url": image_url,
            "service_fee": service_fee
        }

        listings.append(listing)
        return {"message": "Listing created successfully", "listing": listing}

    except Exception as e:
        return {"error": str(e)}


