from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import cloudinary.uploader
import os
from dotenv import load_dotenv

# Load .env if available (optional)
load_dotenv()

app = FastAPI()

# ✅ CORS: Allow frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Supabase config
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Cloudinary config
cloudinary.config(
    cloud_name="dmrbagjxz",
    api_key="874448255545393",
    api_secret="xN7Mz4_MQZ1tQifU2oNQWkdzUsA",
    secure=True,
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
        # ✅ Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result.get("secure_url")

        # ✅ Trim location to first part of postcode
        general_location = location.strip().split(" ")[0].upper()

        # ✅ Insert into Supabase
        data = {
            "title": title,
            "description": description,
            "location": general_location,
            "price_per_day": price_per_day,
            "image_url": image_url
        }

        response = supabase.table("listings").insert(data).execute()

        if response.status_code == 201 or response.status_code == 200:
            return {"message": "Listing created successfully"}
        else:
            return JSONResponse(status_code=500, content={"error": "Failed to insert listing into database"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})










































   



