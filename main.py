from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Rentonomic backend is running!"}

@app.get("/listings")
def get_listings():
    return {
        "listings": [
            {"id": 1, "title": "Electric Drill", "price_per_day": 5},
            {"id": 2, "title": "Projector", "price_per_day": 10},
            {"id": 3, "title": "Camping Tent", "price_per_day": 7}
        ]
    }
