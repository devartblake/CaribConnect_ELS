from contextlib import asynccontextmanager

from sqlmodel import Session
from app.core.db import close_mongo_connection, init_db, init_mongo
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize MongoDB on startup
    await init_mongo()
    # Create superuser for SQLAlchemy-based DB if needed
    with Session(engine) as session:
        init_db(session)
    yield
    # Close MongoDB connection on shutdown
    await close_mongo_connection()
    
app.include_router(api_router, prefix=settings.API_V1_STR)
app.router.lifespan = lifespan