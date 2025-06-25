from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase config
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary config (unsigned upload — no secret!)
cloudinary.config(
    cloud_name="dkzvwm3hh",
    api_key="277136188375582"
)

@app.post("/listing")
async def create_listing(
    name: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...),
):
    try:
        upload_result = cloudinary.uploader.upload(
            image.file,
            resource_type="image",
            upload_preset="rentonomic_unsigned"
        )
        image_url = upload_result.get("secure_url")
        if not image_url:
            raise HTTPException(status_code=500, detail="Failed to upload image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload error: {e}")

    data = {
        "name": name,
        "description": description,
        "location": location,
        "price_per_day": price_per_day,
        "image_url": image_url,
    }
    response = supabase.table("listings").insert(data).execute()

    if response.error:
        raise HTTPException(status_code=500, detail=f"Database error: {response.error.message}")

    return {"message": "Listing created", "listing": response.data}

@app.get("/listings")
async def get_listings():
    response = supabase.table("listings").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail=f"Database error: {response.error.message}")
    return response.data



























   



