from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import uuid
import io

app = FastAPI()

# CORS setup for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase credentials
SUPABASE_URL = "https://dzwtgztiiupqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary config with your real credentials
cloudinary.config(
    cloud_name="dkzwvm3hh",
    api_key="277136188375582",
    api_secret="w3P038_rap8tlmjNS7su1oaz-0w"
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
        result = cloudinary.uploader.upload(io.BytesIO(contents), public_id=str(uuid.uuid4()))
        image_url = result["secure_url"]

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














   



