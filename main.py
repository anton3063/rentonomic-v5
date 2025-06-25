from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import requests
import os
from supabase import create_client, Client

# === SUPABASE CONFIG ===
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === CLOUDINARY CONFIG ===
CLOUD_NAME = "dkzvwm3hh"
API_KEY = "538411894574491"
API_SECRET = "BLjMCFrVlCVQZWUZ...your_full_secret_here..."

app = FastAPI()

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === LISTING MODEL (for reference only) ===
class Listing(BaseModel):
    item_name: str
    description: str
    location: str
    price_per_day: float
    image_url: str

# === ROUTES ===

@app.post("/listings")
async def create_listing(
    item_name: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    file: UploadFile = File(...)
):
    # Upload image to Cloudinary
    upload_url = f"https://api.cloudinary.com/v1_1/{CLOUD_NAME}/image/upload"
    upload_preset = "rentonomic_unsigned"

    contents = await file.read()
    response = requests.post(
        upload_url,
        files={"file": contents},
        data={"upload_preset": upload_preset}
    )

    if response.status_code != 200:
        return {"error": f"Image upload error: {response.json().get('error', {}).get('message', 'Unknown error')}"}

    image_url = response.json()["secure_url"]

    # Save to Supabase
    listing_data = {
        "id": str(uuid.uuid4()),
        "item_name": item_name,
        "description": description,
        "location": location,
        "price_per_day": price_per_day,
        "image_url": image_url
    }

    supabase.table("listings").insert(listing_data).execute()
    return {"message": "Listing created successfully", "data": listing_data}


@app.get("/listings")
def get_listings():
    response = supabase.table("listings").select("*").execute()
    return response.data






























   



