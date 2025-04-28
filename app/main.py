from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import users, debts, score

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credit System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(debts.router)
app.include_router(score.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Credit System API"}