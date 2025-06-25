from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
from supabase import create_client
import os

app = FastAPI()

# CORS: allow all origins for now (test phase)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables (make sure these are set on Render or your environment)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

if not all([SUPABASE_URL, SUPABASE_KEY, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    raise RuntimeError("One or more environment variables are missing. Please check your .env or Render settings.")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
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
        # Read image bytes from uploaded file
        contents = await image.read()

        # Upload image to Cloudinary and get URL
        upload_result = cloudinary.uploader.upload(contents, resource_type="image")
        image_url = upload_result.get("secure_url")
        if not image_url:
            raise HTTPException(status_code=500, detail="Failed to upload image to Cloudinary")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload error: {e}")

    # Prepare data for Supabase insertion
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

    return {"message": "Listing created successfully", "listing": response.data}

@app.get("/listings")
async def get_listings():
    response = supabase.table("listings").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail=f"Database error: {response.error.message}")
    return {"listings": response.data}
























   



