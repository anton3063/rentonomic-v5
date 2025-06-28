from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import os
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# === CORS CONFIGURATION ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rentonomic.com",
        "https://www.rentonomic.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === SUPABASE SETUP ===
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === CLOUDINARY SETUP ===
cloudinary.config(
    cloud_name="dkwzvm3hh",
    api_key="577527256799347",
    api_secret="jzODb-QQRdmZHOA3A2N-WMbJqJo",
    secure=True
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
        # Upload image to Cloudinary
        result = cloudinary.uploader.upload(image.file, folder="rentonomic", public_id=str(uuid4()))
        image_url = result.get("secure_url")

        # Insert listing into Supabase
        data = {
            "title": title,
            "description": description,
            "location": location[:3].upper(),  # Truncate for GDPR
            "price_per_day": price_per_day,
            "image_url": image_url
        }
        response = supabase.table("listings").insert(data).execute()
        return {"message": "Listing created successfully", "data": response.data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/listings")
def get_listings():
    try:
        response = supabase.table("listings").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}






































   



