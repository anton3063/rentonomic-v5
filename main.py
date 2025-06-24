from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import cloudinary
import cloudinary.uploader

app = FastAPI()

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === SUPABASE CONFIG ===
SUPABASE_URL = "https://dzwtgztiiupqnxrpeoye.supabase.co"
SUPABASE_API_KEY = "Concrete-0113xyz"  # Your real Supabase service role key

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

# === CLOUDINARY CONFIG (optional – safe to leave as-is if unused) ===
cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

# === POST TO SUPABASE LISTINGS ===
def add_listing(listing: dict):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/listings",
        headers=headers,
        json=listing
    )
    return response.json()

@app.post("/listings")
async def create_listing(request: Request):
    data = await request.json()
    result = add_listing(data)
    return {"status": "success", "result": result}

@app.get("/")
def home():
    return {"message": "Rentonomic backend is running"}





   



