from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, movies, reviews, admin

# Create tables if not exists (redundant if init_db run, but safe)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=[
        "http://localhost:4321",
        "http://localhost:8000",
        "http://127.0.0.1:4321",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MONO-LOG.fun API!"}
