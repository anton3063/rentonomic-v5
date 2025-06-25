from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import os

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase setup
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary setup
cloudinary.config(
    cloud_name="dhgzj1bkj",
    api_key="367543761227265",
    api_secret="nTP_9yqMxl_X7IbGvhT4zmbU7Dg",
    secure=True
)

class Listing(BaseModel):
    title: str
    location: str
    description: str
    price_per_day: float
    image_url: str

@app.post("/listings")
async def create_listing(listing: Listing):
    data = {
        "title": listing.title,
        "location": listing.location,
        "description": listing.description,
        "price_per_day": listing.price_per_day,
        "image_url": listing.image_url
    }
    response = supabase.table("listings").insert(data).execute()
    return {"message": "Listing created", "data": response.data}

@app.get("/listings")
async def get_listings():
    response = supabase.table("listings").select("*").execute()
    return response.data






























   



