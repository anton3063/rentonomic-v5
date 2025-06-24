from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import datetime
import cloudinary
import cloudinary.uploader
import os

# === DATABASE CONNECTION (SUPABASE POSTGRES) ===
DATABASE_URL = "postgresql://postgres:Concrete-0113xyz@db.dzwtgztiipuqnxrpeoye.supabase.co:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# === CLOUDINARY SETUP ===
cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",       # 🔁 Replace with your Cloudinary cloud name
    api_key="YOUR_API_KEY",             # 🔁 Replace with your Cloudinary API key
    api_secret="YOUR_API_SECRET"        # 🔁 Replace with your Cloudinary API secret
)

# === DATABASE MODEL ===
class Listing(Base):
    __tablename__ = "listings"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    location = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# === FASTAPI SETUP ===
app = FastAPI()

class ListingCreate(BaseModel):
    name: str
    description: str | None = None
    location: datetime.datetime | None = None

@app.post("/listings")
def create_listing(listing: ListingCreate):
    db = SessionLocal()
    new_listing = Listing(
        name=listing.name,
        description=listing.description,
        location=listing.location
    )
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    db.close()
    return {"message": "Listing created", "id": new_listing.id}

@app.get("/listings")
def get_listings():
    db = SessionLocal()
    listings = db.query(Listing).all()
    db.close()
    return listings

# === (Optional) CLOUDINARY IMAGE UPLOAD ROUTE ===
@app.post("/upload-image/")
def upload_image(file: UploadFile = File(...)):
    result = cloudinary.uploader.upload(file.file)
    return {"secure_url": result["secure_url"]}



   



