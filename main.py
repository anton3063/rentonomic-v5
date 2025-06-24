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

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Supabase config from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure Cloudinary with your credentials
cloudinary.config(
    cloud_name="dkzwvm3hh",
    api_key="277136188375582",
    api_secret=os.getenv("CLOUDINARY_API_SECRET")  # Make sure to set this env var on Render
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
        image_url = upload_result["secure_url"]

        short_location = location.strip().split()[0]

        listing_data = {
            "title": title,
            "description": description,
            "location": short_location,
            "price": price,
            "image_url": image_url
        }
        supabase.table("listings").insert(listing_data).execute()

        return {"message": "Listing created successfully"}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/listings")
def get_listings():
    try:
        response = supabase.table("listings").select("*").execute()
        return response.data
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
















   



