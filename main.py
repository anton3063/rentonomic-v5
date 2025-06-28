from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS: Allow Netlify + custom domain
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://rentonomic.netlify.app",
    "https://rentonomic.com"  # ✅ ALLOW your custom domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase config
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary config
cloudinary.config(
    cloud_name="dkzvwm3hh",
    api_key="695636737188945",
    api_secret="5GZxMoG0hR_aAo38eN7XKxb4jxM",
    secure=True
)

@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = Form(...)
):
    try:
        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(image.file, folder="rentonomic")
        image_url = upload_result["secure_url"]

        # Shorten postcode to general area
        location_prefix = location.split()[0] if location else ""

        # Save to Supabase
        data = {
            "title": title,
            "description": description,
            "location": location_prefix,
            "price_per_day": price_per_day,
            "image_url": image_url
        }
        response = supabase.table("listings").insert(data).execute()

        return {"message": "Listing created", "id": response.data[0]["id"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/listings")
async def get_listings():
    try:
        response = supabase.table("listings").select("*").execute()
        return response.data
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



































   



