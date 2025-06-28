from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import cloudinary.uploader
import os
import requests

app = FastAPI()

# === CORS CONFIGURATION ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],  # Make sure this matches your live frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CLOUDINARY CONFIG ===
cloudinary.config(
    cloud_name="dkzwvm3hh",
    api_key="476458759548133",
    api_secret="5S2-mfl6Y1HqRQU4KzSgbGeU8N8",
    secure=True
)

# === SUPABASE CONFIG ===
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"

# === ROUTES ===

@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        # === Upload image to Cloudinary ===
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result["secure_url"]

        # === Extract postcode prefix (e.g., YO8 from YO8 6RE) ===
        general_location = location.split(" ")[0].upper()

        # === Send data to Supabase ===
        data = {
            "title": title,
            "description": description,
            "location": general_location,
            "price_per_day": price_per_day,
            "image_url": image_url
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/listings",
            json=data,
            headers={
                "apikey": SUPABASE_API_KEY,
                "Authorization": f"Bearer {SUPABASE_API_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
        )

        if response.status_code != 201:
            return {"error": "Failed to store listing in database", "details": response.text}

        return {"success": True, "listing": response.json()}

    except Exception as e:
        return {"error": str(e)}





































   



