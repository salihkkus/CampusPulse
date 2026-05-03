from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.rooms_routes import router as rooms_router
from routes.ai_routes import router as ai_router
from routes.financial_routes import router as financial_router
from routes.frontend_routes import router as frontend_router
from routes.charts_routes import router as charts_router
from routes.reports_routes import router as reports_router

app = FastAPI(
    title="CampusPulse API",
    description="Energy Waste Detection System API",
    version="1.0.0"
)

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for production (or set to your specific Render frontend URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CampusPulse API is running"}

# Include routers
app.include_router(rooms_router)
app.include_router(ai_router)
app.include_router(financial_router)
app.include_router(frontend_router)
app.include_router(charts_router)
app.include_router(reports_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
