from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import cloudinary.uploader
import os

app = FastAPI()

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rentonomic.com",
        "https://www.rentonomic.com",
        "https://rentonomic.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://dzwtgztiipuqnrpeoye.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "rentonomic"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "726146152152631"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "3ixdoYJKW8KRqx8HRD0s5CQHxj8")
)

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result["secure_url"]

        data = {
            "title": title,
            "description": description,
            "location": location,
            "price_per_day": price_per_day,
            "image_url": image_url
        }

        response = supabase.table("listings").insert(data).execute()

        return {"message": "Listing created successfully", "data": response.data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/listings")
def get_listings():
    try:
        response = supabase.table("listings").select("*").execute()
        return response.data
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})






















































   



