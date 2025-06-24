from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import os
import uuid
import io

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase setup
SUPABASE_URL = "https://xxxxx.supabase.co"  # your URL
SUPABASE_KEY = "Concrete-0113xyz"           # your password
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary setup
cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
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
        # Read image into memory
        contents = await image.read()
        result = cloudinary.uploader.upload(io.BytesIO(contents), public_id=str(uuid.uuid4()))
        image_url = result["secure_url"]

        short_location = location.strip().split()[0]

        data = {
            "title": title,
            "description": description,
            "location": short_location,
            "price": price,
            "image_url": image_url
        }

        supabase.table("listings").insert(data).execute()
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










   



