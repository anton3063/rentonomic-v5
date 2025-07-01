from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cloudinary
import cloudinary.uploader
import psycopg2
import os

app = FastAPI()

# ✅ CORS config
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

# ✅ Cloudinary setup
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "rentonomic"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "726146152152631"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "3ixdoYJKW8KRqx8HRD0s5CQHxj8")
)

# ✅ PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

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
        # Upload image to Cloudinary
        uploaded = cloudinary.uploader.upload(image.file)
        image_url = uploaded["secure_url"]

        # Save listing to PostgreSQL
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO listings (title, description, location, price_per_day, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, location, price_per_day, image_url))

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Listing created successfully", "image_url": image_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/listings")
def get_listings():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, title, description, location, price_per_day, image_url FROM listings ORDER BY id DESC")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "location": row[3],
                "price_per_day": row[4],
                "image_url": row[5]
            })

        return results
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})























































   



