import os
import logging
from fastapi import FastAPI, HTTPException

# Setup logging for debug
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Required environment variables
REQUIRED_ENV_VARS = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "CLOUDINARY_CLOUD_NAME",
    "CLOUDINARY_API_KEY",
    "CLOUDINARY_API_SECRET",
]

# Check and log environment variables presence
for var in REQUIRED_ENV_VARS:
    val = os.getenv(var)
    if val is None or val.strip() == "":
        logger.error(f"Missing environment variable: {var}")
        raise RuntimeError(f"Missing required environment variable: {var}")
    else:
        # Log only the first 5 characters for safety
        logger.debug(f"{var} is set to: '{val[:5]}...'")

@app.get("/")
async def root():
    return {"message": "Rentonomic backend is running!"}

# Add your API routes here...
# Example:
# @app.get("/listings")
# async def get_listings():
#     # Your code to fetch listings from Supabase
#     pass

# @app.post("/listing")
# async def add_listing():
#     # Your code to add a listing, including handling images with Cloudinary
#     pass























   



