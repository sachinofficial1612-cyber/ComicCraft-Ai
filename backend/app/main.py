from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .database import init_db
from .routes import health_router, projects_router, panels_router, export_router
from .utils.logger import get_logger

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ComicCraft Database...")
    init_db()
    yield

# Always ensure DB tables are created
init_db()

app = FastAPI(
    title="ComicCraft AI API",
    description="AI Comic Story Creator Backend API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred. Please try again later.", "error": str(exc)}
    )

# Include API Routers
app.include_router(health_router)
app.include_router(projects_router)
app.include_router(panels_router)
app.include_router(export_router)

@app.get("/")
def root():
    return {
        "app": "ComicCraft AI",
        "description": "Turn your story idea into a complete illustrated comic.",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
