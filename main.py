from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cloudinary
import cloudinary.uploader
import os
import uuid
import psycopg2

app = FastAPI()

# ✅ CORS fix — allow your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Cloudinary config
cloudinary.config(
    cloud_name="dzwtgztiip",
    api_key="679361233196224",
    api_secret="QREHyDjHoCevBflpUt6B7iEqDKc",
    secure=True
)

# ✅ Supabase/Postgres connection
conn = psycopg2.connect(
    host="db.dzwtgztiipuqnxrpeoyei.supabase.co",
    dbname="postgres",
    user="postgres",
    password="Concrete-0113xyz",
    port=5432
)
cur = conn.cursor()

# ✅ Listing endpoint
@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        # ✅ Upload image to Cloudinary
        result = cloudinary.uploader.upload(image.file)
        image_url = result["secure_url"]

        # ✅ Store in Supabase
        listing_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO listings (id, title, description, location, price_per_day, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (listing_id, title, description, location[:3], price_per_day, image_url))
        conn.commit()

        return {"message": "Listing created successfully", "id": listing_id}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ Get listings
@app.get("/listings")
def get_listings():
    cur.execute("SELECT id, title, description, location, price_per_day, image_url FROM listings ORDER BY created_at DESC")
    rows = cur.fetchall()
    listings = []
    for row in rows:
        listings.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "location": row[3],
            "price_per_day": row[4],
            "image_url": row[5],
        })
    return listings











































   



