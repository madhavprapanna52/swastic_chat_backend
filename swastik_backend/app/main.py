# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, rooms, messages, academics, quizzes
from app.utils.database import create_tables

app = FastAPI(
    title="Swastik University Chat Platform API",
    description="Backend API for university student social platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
create_tables()

# Include routers
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(messages.router)
app.include_router(academics.router)
app.include_router(quizzes.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Swastik University Chat Platform API",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "User Authentication",
            "Chat Rooms",
            "Real-time Messaging",
            "Academic Resources",
            "Quizzes & Assessments",
            "University Integration"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "swastik-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
