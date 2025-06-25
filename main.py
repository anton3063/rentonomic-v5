import os
import io
import uuid
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader

app = FastAPI()

# CORS setup - allow all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Validate required env variables
if not (SUPABASE_URL and SUPABASE_KEY and CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET):
    raise RuntimeError("One or more environment variables are missing")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure Cloudinary client
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)

@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price: float = Form(...),
    image: UploadFile = Form(...)
):
    try:
        contents = await image.read()
        upload_result = cloudinary.uploader.upload(io.BytesIO(contents), public_id=str(uuid.uuid4()))
        image_url = upload_result.get("secure_url")

        # Extract first part of postcode for GDPR compliance (e.g. "YO8" from "YO8 6RE")
        short_location = location.strip().split()[0] if location else ""

        listing_data = {
            "name": title,
            "description": description,
            "location": short_location,
            "price": price,
            "image_url": image_url
        }

        response = supabase.table("listings").insert(listing_data).execute()

        if response.status_code != 201:
            return JSONResponse(content={"error": "Failed to create listing"}, status_code=500)

        return {"message": "Listing created successfully"}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/listings")
def get_listings():
    try:
        response = supabase.table("listings").select("*").execute()
        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to fetch listings"}, status_code=500)
        return response.data
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)





















   



