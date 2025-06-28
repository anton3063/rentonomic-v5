from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import os

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary configuration
cloudinary.config(
    cloud_name="dkzvwm3hh",
    api_key="544521827699365",
    api_secret="Qyi2BG2oF-ffnh7QTrYVfMg-bDU"
)

@app.get("/")
def read_root():
    return {"message": "Rentonomic backend is live!"}

@app.get("/listings")
def get_listings():
    try:
        response = supabase.table("listings").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            image.file,
            folder="rentonomic"
        )
        image_url = upload_result.get("secure_url")

        # Shorten location to prefix (e.g., YO8 6RE → YO8)
        short_location = location.split()[0].strip().upper()

        # Insert listing into Supabase
        data = {
            "title": title,
            "description": description,
            "location": short_location,
            "price_per_day": price_per_day,
            "image_url": image_url
        }
        supabase.table("listings").insert(data).execute()

        return {"message": "Listing created successfully!"}
    except Exception as e:
        return {"error": str(e)}


































   



