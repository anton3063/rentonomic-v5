from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncpg
import uuid
import cloudinary.uploader
import cloudinary

app = FastAPI()

# ✅ Allow frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rentonomic.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Supabase database connection string (correct, no typos)
DATABASE_URL = "postgresql://postgres:Concrete-0113xyz@db.dzwtgztiipuqnrpeoye.supabase.co:5432/postgres"

# ✅ Cloudinary config
cloudinary.config(
    cloud_name="dzd5v9ggu",  # Double-check this matches your Cloudinary dashboard
    api_key="815282963778522",
    api_secret="JRXqWrZoY1ibmiPyDWW_TpQ4D4c"
)

# ✅ Open connection on app startup
@app.on_event("startup")
async def startup():
    try:
        app.state.db = await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        print("❌ DB Connection Failed:", e)
        raise

# ✅ Close DB connection on shutdown
@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# ✅ POST: Add new listing
@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = Form(...)
):
    try:
        # Upload image to Cloudinary
        uploaded = cloudinary.uploader.upload(image.file)
        image_url = uploaded["secure_url"]

        # Generate unique listing ID
        listing_id = str(uuid.uuid4())

        # Save listing in Supabase (PostgreSQL)
        await app.state.db.execute("""
            INSERT INTO listings (id, title, location, description, price_per_day, image_url)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, listing_id, title, location, description, price_per_day, image_url)

        return JSONResponse(content={"message": "Listing created successfully"}, status_code=201)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ✅ GET: Return all listings
@app.get("/listings")
async def get_listings():
    try:
        rows = await app.state.db.fetch("SELECT * FROM listings ORDER BY id DESC")
        listings = [dict(row) for row in rows]
        return listings
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)















































   



