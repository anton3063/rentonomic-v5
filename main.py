from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import os

# Replace with your actual Supabase connection details
DB_USER = "postgres"
DB_PASSWORD = "your_password_here"
DB_HOST = "your_host_here.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can restrict to your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database model
class Listing(Base):
    __tablename__ = "listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic model for request/response
class ListingCreate(BaseModel):
    name: str
    description: str
    location: str

class ListingRead(ListingCreate):
    id: uuid.UUID
    created_at: datetime

Base.metadata.create_all(bind=engine)

@app.post("/listings", response_model=ListingRead)
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
    return new_listing

@app.get("/listings", response_model=List[ListingRead])
def get_listings():
    db = SessionLocal()
    listings = db.query(Listing).order_by(Listing.created_at.desc()).all()
    db.close()
    return listings



