from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

# ✅ FastAPI app
app = FastAPI()

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rentonomic.com",
        "https://www.rentonomic.com",
        "https://rentonomic.netlify.app"  # optional
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Supabase config
SUPABASE_URL = "https://dzwtgztiipuqnxrpeoyei.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6d3RnenRpaXB1cW54cnBlb3llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2NzAxNDUsImV4cCI6MjA2NjI0NjE0NX0.9pTagxo-EKolvBAYY3lxVVvRC89DsbSGUY6Gy67Y7MQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Listing model
class Listing(BaseModel):
    title: str
    description: str
    location: str
    price_per_day: float
    image_url: str

# ✅ Root test
@app.get("/")
def read_root():
    return {"message": "Rentonomic backend is live!"}

# ✅ Add new listing
@app.post("/listing")
def create_listing(listing: Listing):
    data = {
        "title": listing.title,
        "description": listing.description,
        "location": listing.location,
        "price_per_day": listing.price_per_day,
        "image_url": listing.image_url,
    }
    response = supabase.table("listings").insert(data).execute()
    return {"message": "Listing created successfully", "data": response.data}

# ✅ Get all listings
@app.get("/listings")
def get_listings():
    response = supabase.table("listings").select("*").execute()
    return response.data

































   



