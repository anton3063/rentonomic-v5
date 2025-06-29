from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cloudinary.uploader
import psycopg2
import uuid

app = FastAPI()

# === CORS SETTINGS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],  # Must exactly match frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CLOUDINARY CONFIG ===
cloudinary.config(
    cloud_name="dxvhlqldx",
    api_key="382784757258584",
    api_secret="FAbfUoHqfKqUNu6EZulMRZ6uU0I"
)

# === DATABASE CONNECTION (Supabase) ===
conn = psycopg2.connect(
    "postgresql://postgres:Concrete-0113xyz@db.dzwgtziiupqnxrpeoyei.supabase.co:5432/postgres"
)
cur = conn.cursor()

# === ENDPOINT ===
@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: str = Form(...),
    image: UploadFile = Form(...)
):
    try:
        # Upload image to Cloudinary
        result = cloudinary.uploader.upload(image.file, public_id=str(uuid.uuid4()))
        image_url = result["secure_url"]

        # Insert into Supabase (PostgreSQL)
        cur.execute(
            "INSERT INTO listings (title, description, location, price_per_day, image_url) VALUES (%s, %s, %s, %s, %s)",
            (title, description, location, price_per_day, image_url)
        )
        conn.commit()

        return {"message": "Listing created successfully"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)












































   



