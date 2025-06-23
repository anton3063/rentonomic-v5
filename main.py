from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

# === DATABASE CONFIG ===
DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD_HERE@db.dzwtgztiipuqnxrpeoye.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# === MODEL ===
class Listing(Base):
    __tablename__ = "listings"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

# Create tables if not exists
Base.metadata.create_all(bind=engine)

# === API SETUP ===
app = FastAPI()

class ListingCreate(BaseModel):
    name: str
    description: str = None

@app.post("/listings")
def create_listing(listing: ListingCreate):
    db = SessionLocal()
    new_listing = Listing(name=listing.name, description=listing.description)
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


   



