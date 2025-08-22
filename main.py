from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine
from models import Base
from auth import router as auth_router
from profile import router as profile_router

app = FastAPI(title="Workshop4 API", version="0.1.0")

# Create tables on startup if they don't exist
Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
	return {"message": "Hello, World!"}


# Routers
app.include_router(auth_router)
app.include_router(profile_router)
