from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uuid
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend origin
origins = ["https://rentonomic.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase config
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary config
CLOUDINARY_UPLOAD_URL = "https://api.cloudinary.com/v1_1/dhyl0yxej/image/upload"
CLOUDINARY_API_KEY = "122738243499659"
CLOUDINARY_API_SECRET = "PBHAFuFRmNFVK7IQlznRuZpBiDw"

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
        files = {"file": (image.filename, await image.read())}
        data = {
            "api_key": CLOUDINARY_API_KEY,
            "timestamp": str(uuid.uuid4()),
            "folder": "rentonomic"
        }
        response = requests.post(CLOUDINARY_UPLOAD_URL, data=data, files=files, auth=(CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET))

        if response.status_code != 200:
            return {"error": "Image upload failed"}

        image_url = response.json().get("secure_url")

        # Insert listing into Supabase
        short_location = location.split()[0].upper()  # e.g., "YO8"
        data = {
            "title": title,
            "description": description,
            "location": short_location,
            "price_per_day": price_per_day,
            "image_url": image_url
        }

        result = supabase.table("listings").insert(data).execute()

        return {"message": "Listing created successfully", "data": result.data}

    except Exception as e:
        return {"error": str(e)}







































   



