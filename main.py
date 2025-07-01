from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
import cloudinary
import cloudinary.uploader
import uuid
import os

app = FastAPI()

# CORS
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

# Cloudinary
cloudinary.config(
    cloud_name="dzwtgztiipuqnrpeoye",
    api_key="214334361169765",
    api_secret="U9sbyvZ4MJeqbkTuML4MkG8do08"
)

# Database
DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://postgres:Concrete-0113xyz@containers-us-west-110.railway.app:XXXXX/postgres"  # Replace XXXXX with your port

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "Backend is running"}

@app.get("/listings")
def get_listings():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT title, description, location, price_per_day, image_url FROM listings ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        listings = [
            {"title": r[0], "description": r[1], "location": r[2], "price": float(r[3]), "image_url": r[4]}
            for r in rows
        ]
        return listings
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Upload image to Cloudinary
        result = cloudinary.uploader.upload(image.file, public_id=str(uuid.uuid4()))
        image_url = result.get("secure_url")

        # Insert listing
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO listings (title, description, location, price_per_day, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, location, price_per_day, image_url))
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Listing created successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

























































   



