from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cloudinary
import cloudinary.uploader
from supabase import create_client

# Supabase config
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary config (SIGNED UPLOAD)
cloudinary.config(
    cloud_name="dkzvwm3hh",
    api_key="333963673922839",
    api_secret="IxbphXAT7lvFuKt4R8VDEJrM8AA",
    secure=True
)

# FastAPI app
app = FastAPI()

# CORS middleware to allow requests from rentonomic.com
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

# Listing model
class Listing(BaseModel):
    title: str
    description: str
    location: str
    price_per_day: float
    image_url: str

# POST /listing endpoint
@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = Form(...)
):
    try:
        # Upload image to Cloudinary (signed upload)
        result = cloudinary.uploader.upload(
            image.file,
            folder="rentonomic"
        )
        image_url = result.get("secure_url")

        # Save listing in Supabase
        listing_data = {
            "title": title,
            "description": description,
            "location": location,
            "price_per_day": price_per_day,
            "image_url": image_url,
        }
        supabase_client.table("listings").insert(listing_data).execute()

        return {"message": "Listing created successfully"}

    except Exception as e:
        return {"error": str(e)}


































   



