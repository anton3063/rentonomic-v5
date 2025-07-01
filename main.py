from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import psycopg2
import cloudinary.uploader

app = FastAPI()

# ✅ CORS settings to allow frontend access
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

# ✅ PostgreSQL connection via Railway
conn = psycopg2.connect(
    "postgresql://postgres:UoiETFVckuSWSjGMLjjJnXNLgsUfwFKd@switchback.proxy.rlwy.net:27985/railway"
)
cur = conn.cursor()

# ✅ Cloudinary config
cloudinary.config(
    cloud_name="dvkqsvtjo",
    api_key="129442524553611",
    api_secret="r9SnBLZTo8rQkPh4iNNsGCRJrRQ"
)

# ✅ Create the listings table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    title TEXT,
    location TEXT,
    description TEXT,
    price_per_day NUMERIC,
    image_url TEXT
);
""")
conn.commit()

# ✅ Submit a new listing
@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Upload image to Cloudinary
        result = cloudinary.uploader.upload(image.file)
        image_url = result.get("secure_url")

        # Insert listing into PostgreSQL
        cur.execute("""
            INSERT INTO listings (title, location, description, price_per_day, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, location, description, price_per_day, image_url))
        conn.commit()

        return {"message": "Listing created successfully", "image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Fetch all listings
@app.get("/listings")
def get_listings():
    try:
        cur.execute("SELECT * FROM listings")
        rows = cur.fetchall()
        listings = [
            {
                "id": row[0],
                "title": row[1],
                "location": row[2],
                "description": row[3],
                "price_per_day": float(row[4]),
                "image_url": row[5]
            } for row in rows
        ]
        return listings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


























































   



