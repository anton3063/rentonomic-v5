from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncpg
import uuid
import cloudinary
import cloudinary.uploader

app = FastAPI()

# ✅ CORS fix – includes all frontend origins
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

# ✅ Supabase connection string
DATABASE_URL = "postgresql://postgres:Concrete-0113xyz@dzwtgztiipuqnrpeoye.pooler.supabase.co:5432/postgres"

# ✅ Cloudinary config
cloudinary.config(
    cloud_name="dzd5v9ggu",
    api_key="815282963778522",
    api_secret="JRXqWrZoY1ibmiPyDWW_TpQ4D4c"
)

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# ✅ POST: Add a listing
@app.post("/listing")
async def create_listing(
    title: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    price_per_day: float = Form(...),
    image: UploadFile = Form(...)
):
    uploaded = cloudinary.uploader.upload(image.file)
    image_url = uploaded["secure_url"]
    listing_id = str(uuid.uuid4())

    await app.state.db.execute("""
        INSERT INTO listings (id, title, location, description, price_per_day, image_url)
        VALUES ($1, $2, $3, $4, $5, $6)
    """, listing_id, title, location, description, price_per_day, image_url)

    return {"message": "Listing created successfully"}

# ✅ GET: Retrieve all listings
@app.get("/listings")
async def get_listings():
    rows = await app.state.db.fetch("SELECT * FROM listings ORDER BY id DESC")
    return [dict(row) for row in rows]





















































   



