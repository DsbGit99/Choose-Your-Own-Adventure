from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="An API to generate stories for *Choose Your Own Adventure*.",
    version="0.1.0",
    docs_url="/docs",  # FastAPI comes with automatic documenation viewable from web browser
    redoc_url="/redoc",
)

# Cross Origin Resource Sharing (CORS) is a security layer
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # What clients are allowed?
    allow_credentials=True,  # i.e. SSL, TLS
    allow_methods=["*"],  # i.e. HTTP CRUD operations like GET, POST PUT, etc.
    allow_headers=["*"],  # additional information included with requests
)

if __name__ == "__main__":
    import uvicorn

    # NOTE: The "reload" parameter here enables auto-reloading during development,
    # which automatically restarts the server when code changes are detected.

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
