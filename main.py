from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import cloudinary.uploader
import os

app = FastAPI()

# === ✅ CORS FIX ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ✅ Supabase Config ===
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === ✅ Cloudinary Config ===
cloudinary.config(
    cloud_name="dj8id8p3j",
    api_key="154397339799479",
    api_secret="0RPnRY1O_oYMn8WNTIkj1ek-FmQ",
    secure=True
)

# === ✅ POST /listing ===
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
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result.get("secure_url")

        # Get postcode prefix (first part of postcode)
        postcode_prefix = location.strip().split(" ")[0].upper()

        # Store in Supabase
        data = {
            "title": title,
            "description": description,
            "location": postcode_prefix,
            "price_per_day": price_per_day,
            "image_url": image_url
        }
        response = supabase.table("listings").insert(data).execute()

        return {"message": "Listing created successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# === ✅ GET /listings ===
@app.get("/listings")
async def get_listings():
    try:
        response = supabase.table("listings").select("*").execute()
        return response.data
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})









































   



