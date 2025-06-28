from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import cloudinary.uploader
import os

app = FastAPI()

# Allow frontend domain (CORS fix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase setup
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary setup
cloudinary.config(
    cloud_name="dkrvmd2of",
    api_key="879964474696449",
    api_secret="nzDyslQw1-mUIbFSyGq-j_94U4Y"
)

@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result.get("secure_url")

        # Save to Supabase
        data = {
            "title": title,
            "description": description,
            "location": location[:3].upper(),
            "price_per_day": price_per_day,
            "image_url": image_url
        }
        supabase.table("listings").insert(data).execute()

        return {"message": "Listing created successfully!"}

    except Exception as e:
        return {"error": str(e)}








































   



