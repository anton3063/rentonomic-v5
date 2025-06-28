from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

# Load environment variables (optional if you prefer hardcoding instead)
load_dotenv()

# === Supabase Config ===
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Cloudinary Config ===
cloudinary.config(
    cloud_name="dkszvwm3hh",
    api_key="482233231939864",
    api_secret="lTqxgoF_UM-LvpoWuV7FszVGM64"
)

# === FastAPI Setup ===
app = FastAPI()

# === CORS Setup (IMPORTANT: Allow rentonomic.com) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],  # PROPER frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Endpoint to Receive Listing ===
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

        # Trim location to just the prefix (e.g., YO8)
        location_prefix = location.strip().split(" ")[0]

        # Save listing to Supabase
        response = supabase.table("listings").insert({
            "title": title,
            "description": description,
            "location": location_prefix,
            "price_per_day": price_per_day,
            "image_url": image_url
        }).execute()

        if response.error:
            return JSONResponse(content={"error": str(response.error)}, status_code=500)

        return {"message": "Listing created successfully"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# === Test Route ===
@app.get("/")
def read_root():
    return {"message": "Rentonomic backend is running"}




































   



