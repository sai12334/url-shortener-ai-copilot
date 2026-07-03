"""
FastAPI application entrypoint.

Wires together: CORS, DB table creation on startup, and the two routers
(urls, copilot). Kept minimal — no business logic lives here.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.database import Base, engine
from app.routers import copilot, urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="AI-Assisted Software Engineering Copilot",
    description=(
        "Prototype demonstrating an engineer-led, AI-assisted development "
        "workflow, with a fully implemented URL shortener as the mandatory "
        "demo use case."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


# Copilot routes are namespaced under /copilot; URL shortener routes are
# registered last since they include a catch-all GET /{short_code}.
app.include_router(copilot.router)
app.include_router(urls.router)
